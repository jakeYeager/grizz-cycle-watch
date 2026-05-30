#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""
fetch_aggregates.py — Pull slow-cadence macro series from FRED into data/aggregates.csv.

This is the structural-macro companion to fetch_prices.py. Where prices.csv holds
fast, sentiment-driven daily market prices, aggregates.csv holds the slower
official-statistic series the watch list leans on — monthly, weekly, and
quarterly data that move on a release schedule, not on a tariff tweet.

Series (all FRED — no Yahoo Finance leg, so no yfinance dependency):
  home_sales            Existing home sales (units, SAAR)        FRED: EXHOSLUSM495S  monthly
  case_shiller          Case-Shiller US National HPI (index)     FRED: CSUSHPISA      monthly (~2-mo lag)
  months_supply         Months' supply of new houses             FRED: MSACSR         monthly
  mortgage_30yr         30-Year fixed mortgage rate (%)           FRED: MORTGAGE30US   weekly
  cpi                   CPI-U all items (index)                   FRED: CPIAUCSL       monthly
  cpi_core              CPI-U core, ex food & energy (index)      FRED: CPILFESL       monthly
  unemployment          Unemployment rate (%)                     FRED: UNRATE         monthly
  sloos_tightening      SLOOS net % banks tightening C&I loans    FRED: DRTSCILM       quarterly
  mortgage_delinquency  Single-family mortgage delinquency (%)    FRED: DRSFRMACBS     quarterly
  cc_delinquency        Credit-card delinquency, all comm. banks  FRED: DRCCLACBS      quarterly
  cc_chargeoff          Credit-card charge-off, all comm. banks   FRED: CORCCACBS      quarterly
  loans_ndfi            Loans to nondepository financial insts.   FRED: LNFACBM027SBOG monthly
  total_loans           Loans & leases in bank credit (denom.)    FRED: LOANS          monthly

Bank->nonbank-financial channel note: loans_ndfi is the H.8 "Loans to Nondepository
Financial Institutions, All Commercial Banks" series (monthly SA, $bn) — the bank->private-
credit direct-lending exposure indicator added to the Global Debt watch list (2026-05-29).
IMPORTANT scope nuance: NDFI is BROADER than private credit — it captures banks' lending to
all nondepository financials (PE/private-credit funds, mortgage REITs, broker-dealers,
consumer lenders, BDCs). The FSB's ~$220B "bank credit lines to private credit funds" is a
SUBSET of this ~$2.0T aggregate; this series is the trackable upper-bound proxy for the
channel, not the PC-specific figure. The meaningful read is the YoY growth rate (the watch
list's ~21%/yr Level-2 hook), so it is in YOY_COLUMNS — recent prints run hotter (~26% YoY
April 2026, ~52-58% late 2025) than the long-run pace.

Normalization denominator: total_loans is the H.8 "Loans and Leases in Bank Credit, All
Commercial Banks" series (FRED LOANS, monthly SA, $bn) — the monthly twin of weekly TOTLL,
chosen because it shares loans_ndfi's month-start dates, so the normalized share
(loans_ndfi / total_loans) is a clean same-row division with no nearest-date matching. It is
a pure reference denominator: not in YOY_COLUMNS and carries no threshold (total bank loans
always grows; the signal is the RATIO, not the level). As of Apr 2026 the share is ~14.4%,
up from ~4.3% in 2015 — the normalized form of the watch-list bank->private-credit indicator
that survives the nominal-growth caveat on loans_ndfi.

Consumer-credit note: cc_delinquency and cc_chargeoff are the system/commercial-bank
read on the consumer revolving-credit indicator added to the Global Debt watch list
(2026-05-29). They are the FRED-automatable half of that indicator. The headline NY Fed
CCP balance-weighted 90+ DPD *stock* rate (~13.12%, approaching the 13.7% 2010 peak) is
NOT on the FRED API — it is a quarterly Household Debt & Credit Report (Consumer Credit
Panel/Equifax) PDF/Excel release and remains a manual pull. The bifurcation between the
two is the signal: a re-acceleration in these bank-level series toward their thresholds
would mark below-prime stress turning systemic.

Cadence note: this file is a ragged grid by design — most rows are sparse and
each series populates only on its own release dates. The merge logic handles
that the same way prices.csv handles series that lag each other.

YoY note: CPI, core CPI, Case-Shiller, and home sales are index/count series
whose meaningful read is the year-over-year change, not the raw level. The CSV
stores the raw FRED value (a faithful data store); year-over-year is computed
at display time and is what the threshold flags fire on for those series.

Usage:
  uv run scripts/fetch_aggregates.py              # last 400 days (default — covers YoY)
  uv run scripts/fetch_aggregates.py --days 90
  uv run scripts/fetch_aggregates.py --full       # from 2015-01-01 (use for first backfill)

Requires:
  FRED_API_KEY environment variable
  Register free at: https://fred.stlouisfed.org/docs/api/api_key.html

  uv handles all dependencies automatically via inline metadata.
"""

import argparse
import csv
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import requests


# ---------------------------------------------------------------------------
# Series configuration
# ---------------------------------------------------------------------------

SERIES = {
    "home_sales":           ("EXHOSLUSM495S", "Existing home sales (units, SAAR)"),
    "case_shiller":         ("CSUSHPISA",     "Case-Shiller US National HPI (index)"),
    "months_supply":        ("MSACSR",        "Months' supply of new houses"),
    "mortgage_30yr":        ("MORTGAGE30US",  "30-Year fixed mortgage rate (%)"),
    "cpi":                  ("CPIAUCSL",      "CPI-U all items (index)"),
    "cpi_core":             ("CPILFESL",      "CPI-U core, ex food & energy (index)"),
    "unemployment":         ("UNRATE",        "Unemployment rate (%)"),
    "sloos_tightening":     ("DRTSCILM",      "SLOOS net % banks tightening C&I"),
    "mortgage_delinquency": ("DRSFRMACBS",    "Single-family mortgage delinquency (%)"),
    "cc_delinquency":       ("DRCCLACBS",     "Credit-card delinquency, all comm. banks (%)"),
    "cc_chargeoff":         ("CORCCACBS",     "Credit-card charge-off, all comm. banks (%)"),
    "loans_ndfi":           ("LNFACBM027SBOG", "Loans to nondepository financial insts., all comm. banks ($B)"),
    "total_loans":          ("LOANS",          "Loans & leases in bank credit, all comm. banks ($B) — NDFI-share denom."),
}

# Index/count series — displayed and threshold-checked as year-over-year % change.
# Everything else is read as a level. loans_ndfi is a $-level series but its
# meaningful read is the YoY growth rate (the watch list's ~21%/yr channel-expansion hook).
YOY_COLUMNS = {"home_sales", "case_shiller", "cpi", "cpi_core", "loans_ndfi"}

# Threshold levels printed as flags on latest values.
# Each entry: (value, direction, label)
#   direction "above" — flag fires when v >= value
#   direction "below" — flag fires when v <  value
# For YOY_COLUMNS the flag is checked against the YoY % change, not the raw value.
THRESHOLDS = {
    # checked against YoY % change
    "cpi": [
        (4.0, "above", "ALERT — inflation accelerating past the 2026 high"),
        (3.0, "above", "WARN  — above the Fed 2% target band"),
    ],
    "cpi_core": [
        (4.0, "above", "ALERT — core inflation entrenched"),
        (3.0, "above", "WARN  — sticky core above target"),
    ],
    "case_shiller": [
        (0.0, "below", "NOTE  — national home prices falling YoY"),
    ],
    "home_sales": [
        (-10.0, "below", "WARN  — home sales contracting sharply YoY"),
    ],
    # checked against the level
    "mortgage_30yr": [
        (7.5, "above", "WARN  — mortgage rate at affordability-stress level"),
    ],
    "months_supply": [
        (9.0, "above", "WARN  — new-home inventory glut"),
    ],
    "unemployment": [
        (5.0, "above", "ALERT — recessionary labor-market deterioration"),
        (4.5, "above", "WARN  — labor market loosening"),
    ],
    "sloos_tightening": [
        (40.0, "above", "ALERT — crisis-level credit tightening (Kindleberger Stage 4)"),
        (20.0, "above", "WARN  — meaningful net credit tightening"),
    ],
    "mortgage_delinquency": [
        (5.0, "above", "ALERT — distress-level mortgage delinquency"),
        (3.0, "above", "WARN  — rising mortgage delinquency"),
    ],
    # Currently 2.92% and falling from the 3.2% 2024 cycle peak (pre-pandemic ~2.5%,
    # 2010 crisis peak ~6.8%). A re-acceleration past the prior peak is the tell that
    # below-prime card stress is turning systemic.
    "cc_delinquency": [
        (5.0, "above", "ALERT — distress-level card delinquency (systemic)"),
        (3.5, "above", "WARN  — card delinquency re-accelerating past 2024 peak"),
    ],
    # Currently ~3.8%; 2024 cycle peak 4.6%, pre-pandemic baseline ~3.7%.
    "cc_chargeoff": [
        (6.0, "above", "ALERT — crisis-level card charge-offs"),
        (4.5, "above", "WARN  — card charge-offs back above 2024 cycle peak"),
    ],
    # Checked against YoY % growth (loans_ndfi is in YOY_COLUMNS). The watch-list hook
    # is the ~21%/yr structural pace; recent prints run ~26% (Apr 2026), ~52-58% (late 2025).
    "loans_ndfi": [
        (35.0, "above", "ALERT — NDFI lending growth accelerating sharply (bank→nonbank-financial channel)"),
        (20.0, "above", "WARN  — NDFI lending sustaining >~21%/yr pace — bank→private-credit channel expanding"),
    ],
}

FRED_BASE  = "https://api.stlouisfed.org/fred/series/observations"
CSV_PATH   = Path(__file__).parent.parent / "data" / "aggregates.csv"
FIELDNAMES = ["date"] + list(SERIES)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_dotenv(path: Path = Path(__file__).parent.parent / ".env") -> None:
    """Load KEY=VALUE pairs from .env into os.environ. Silent if file missing."""
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
    except FileNotFoundError:
        pass


def fetch_series(api_key: str, series_id: str, start: str, end: str) -> dict:
    r = requests.get(
        FRED_BASE,
        params={
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "observation_start": start,
            "observation_end": end,
        },
        timeout=15,
    )
    r.raise_for_status()
    return {
        obs["date"]: obs["value"]
        for obs in r.json().get("observations", [])
        if obs["value"] != "."  # FRED uses "." for missing values
    }


def yoy_change(history: dict, col: str, latest_date: str):
    """Year-over-year % change for col at latest_date, computed from merged history.

    Returns (yoy_pct, prior_date) or (None, None) when no comparable observation
    roughly one year back exists (e.g. CSV not yet backfilled past 12 months).
    """
    series = {d: history[d][col] for d in history if history[d].get(col)}
    if latest_date not in series:
        return None, None
    try:
        target = date.fromisoformat(latest_date).replace(
            year=date.fromisoformat(latest_date).year - 1
        )
    except ValueError:
        return None, None

    # Closest observation to one year before latest_date.
    best = None
    best_gap = None
    for d_str in series:
        try:
            gap = abs((date.fromisoformat(d_str) - target).days)
        except ValueError:
            continue
        if best_gap is None or gap < best_gap:
            best, best_gap = d_str, gap
    if best is None or best_gap > 45:  # no observation within ~6 weeks of the mark
        return None, None

    try:
        cur, prev = float(series[latest_date]), float(series[best])
    except ValueError:
        return None, None
    if prev == 0:
        return None, None
    return (cur - prev) / prev * 100.0, best


def threshold_flag(col: str, value) -> str:
    levels = THRESHOLDS.get(col)
    if not levels:
        return ""
    try:
        v = float(value)
    except (ValueError, TypeError):
        return ""
    for threshold, direction, label in levels:
        if direction == "above" and v >= threshold:
            return label
        if direction == "below" and v < threshold:
            return label
    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=400,
                        help="Number of days to look back (default: 400 — enough for a YoY read)")
    parser.add_argument("--full", action="store_true",
                        help="Pull full history from 2015-01-01 (use for the first backfill)")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("FRED_API_KEY")
    if not api_key:
        print("Error: FRED_API_KEY not set.", file=sys.stderr)
        print("Register free at https://fred.stlouisfed.org/docs/api/api_key.html",
              file=sys.stderr)
        sys.exit(1)

    end_date   = date.today()
    start_date = date(2015, 1, 1) if args.full else end_date - timedelta(days=args.days)

    print(f"▶ fetch_aggregates.py — {start_date} → {end_date}")
    print(f"  Series: {', '.join(SERIES)}\n")

    # Fetch FRED series
    all_data: dict[str, dict] = {}
    for col, (sid, label) in SERIES.items():
        print(f"  {sid:<25} {label}...", end=" ", flush=True)
        try:
            obs = fetch_series(api_key, sid, start_date.isoformat(), end_date.isoformat())
            for d, v in obs.items():
                all_data.setdefault(d, {})[col] = v
            print(f"{len(obs)} observations")
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else None
            if code == 400:
                print("series not found on FRED — check ID or source")
            elif code == 500:
                print("FRED server error (500) — skipped, try again later")
            else:
                print(f"HTTP error: {e}")
        except Exception as e:
            print(f"FAILED: {e}")

    if not all_data:
        print("\nNo data fetched. Check API key and network connection.")
        sys.exit(1)

    # Merge into CSV: append new dates, fill in any previously-missing columns.
    CSV_PATH.parent.mkdir(exist_ok=True)
    existing_rows: dict[str, dict] = {}
    if CSV_PATH.exists():
        with open(CSV_PATH, newline="") as f:
            for row in csv.DictReader(f):
                existing_rows[row["date"]] = row

    new_count = updated_count = 0
    for d, values in all_data.items():
        if d not in existing_rows:
            existing_rows[d] = {"date": d}
            new_count += 1
        for col, val in values.items():
            if not existing_rows[d].get(col):
                existing_rows[d][col] = val
                updated_count += 1

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for d in sorted(existing_rows):
            writer.writerow(existing_rows[d])

    print(f"\n  {new_count} new rows, {updated_count} cells updated → {CSV_PATH.relative_to(Path.cwd())}")

    # Print latest values with threshold flags. Each series uses its own most
    # recent date — these series release on different schedules. YoY columns
    # are computed off the full merged history, not just the fetched window.
    print("\nLatest values:")
    for col in FIELDNAMES[1:]:
        _, label = SERIES[col]
        dated = [(d, v[col]) for d, v in existing_rows.items() if v.get(col)]
        if not dated:
            print(f"  {label:<46} n/a")
            continue
        latest_d, val = max(dated)
        if col in YOY_COLUMNS:
            yoy, _ = yoy_change(existing_rows, col, latest_d)
            if yoy is not None:
                disp = f"{val}  ({yoy:+.1f}% YoY)"
                flag = threshold_flag(col, yoy)
            else:
                disp = f"{val}  (YoY n/a — backfill with --full)"
                flag = ""
        else:
            disp = str(val)
            flag = threshold_flag(col, val)
        flag_str = f"  ← {flag}" if flag else ""
        print(f"  {label:<46} {disp}  ({latest_d}){flag_str}")


if __name__ == "__main__":
    main()
