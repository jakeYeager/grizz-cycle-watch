#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "yfinance"]
# ///
"""
fetch_prices.py — Pull key price series from FRED + Yahoo Finance into data/prices.csv.

Series:
  brent_usd       Brent crude spot price (USD/bbl)         FRED: DCOILBRENTEU
  gold_usd        Gold futures front month (USD/troy oz)   Yahoo Finance: GC=F
  treasury_10yr   10-Year Treasury yield (%)               FRED: DGS10
  vix             CBOE VIX volatility index                FRED: VIXCLS
  hy_spread       ICE BofA US HY OA spread (%)             FRED: BAMLH0A0HYM2

Note on gold_usd: sourced from GC=F (COMEX gold futures front month) via
Yahoo Finance because LBMA fixing series are not available via the FRED API
(LBMA licensing restricts redistribution). GC=F is a futures price, not a
spot fix, but tracks spot closely for daily monitoring purposes.

The HY spread (hy_spread) is the cleanest Minsky Phase 3 indicator —
it does not react to tariff tweets the way equity and commodity prices do,
making it useful for distinguishing structural deleveraging from
policy-messaging whiplash.

Usage:
  uv run scripts/fetch_prices.py              # last 30 days (default)
  uv run scripts/fetch_prices.py --days 90
  uv run scripts/fetch_prices.py --full       # from 2020-01-01

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
import yfinance as yf


# ---------------------------------------------------------------------------
# Series configuration
# ---------------------------------------------------------------------------

SERIES = {
    "brent_usd":     ("DCOILBRENTEU",  "Brent crude spot (USD/bbl)"),
    "treasury_10yr": ("DGS10",         "10-Year Treasury yield (%)"),
    "vix":           ("VIXCLS",        "CBOE VIX"),
    "hy_spread":     ("BAMLH0A0HYM2",  "ICE BofA US HY spread (%)"),
}

GOLD_LABEL = "Gold futures GC=F (USD/troy oz)"

# Threshold levels printed as flags on latest values.
# Each entry: (value, direction, label)
#   direction "above" — flag fires when v >= value  (escalation signals)
#   direction "below" — flag fires when v <  value  (resolution signals)
THRESHOLDS = {
    "brent_usd": [
        (130.0, "above", "ALERT — Level 4 escalation trigger"),
        (95.0,  "above", "WARN  — Stagflation pressure on G7 debt service"),
        (90.0,  "below", "NOTE  — Scenario A resolution signal"),
    ],
    "treasury_10yr": [
        (5.0,  "above", "ALERT — Level 4 escalation trigger"),
        (4.75, "above", "WARN  — G7 sovereign debt service stress"),
        (4.0,  "below", "NOTE  — Scenario A resolution signal"),
    ],
    "hy_spread": [
        (7.0,  "above", "ALERT — Distress-level credit spread"),
        (5.0,  "above", "WARN  — Elevated; watch for Minsky Phase 3 deepening"),
    ],
    "vix": [
        (40.0, "above", "ALERT — Crisis-level volatility"),
        (25.0, "above", "WARN  — Elevated uncertainty"),
    ],
}

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
CSV_PATH  = Path(__file__).parent.parent / "data" / "prices.csv"
FIELDNAMES = ["date", "brent_usd", "gold_usd", "treasury_10yr", "vix", "hy_spread"]


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


def fetch_gold(start: str, end: str) -> dict:
    """Fetch GC=F (COMEX gold futures front month) daily closes via yfinance."""
    df = yf.Ticker("GC=F").history(start=start, end=end)
    if df.empty:
        return {}
    return {
        idx.date().isoformat(): f"{row['Close']:.2f}"
        for idx, row in df.iterrows()
    }


def threshold_flag(col: str, value: str) -> str:
    levels = THRESHOLDS.get(col)
    if not levels:
        return ""
    try:
        v = float(value)
    except ValueError:
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
    parser.add_argument("--days", type=int, default=30,
                        help="Number of days to look back (default: 30)")
    parser.add_argument("--full", action="store_true",
                        help="Pull full history from 2020-01-01")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("FRED_API_KEY")
    if not api_key:
        print("Error: FRED_API_KEY not set.", file=sys.stderr)
        print("Register free at https://fred.stlouisfed.org/docs/api/api_key.html",
              file=sys.stderr)
        sys.exit(1)

    end_date   = date.today()
    start_date = date(2020, 1, 1) if args.full else end_date - timedelta(days=args.days)

    print(f"▶ fetch_prices.py — {start_date} → {end_date}")
    print(f"  Series: {', '.join(SERIES)}, gold_usd\n")

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
            if e.response is not None and e.response.status_code == 400:
                print("series not found on FRED — check ID or source")
            else:
                print(f"HTTP error: {e}")
        except Exception as e:
            print(f"FAILED: {e}")

    # Fetch gold via yfinance
    print(f"  {'GC=F':<25} {GOLD_LABEL}...", end=" ", flush=True)
    try:
        gold_obs = fetch_gold(start_date.isoformat(), end_date.isoformat())
        for d, v in gold_obs.items():
            all_data.setdefault(d, {})["gold_usd"] = v
        print(f"{len(gold_obs)} observations")
    except Exception as e:
        print(f"FAILED: {e}")

    if not all_data:
        print("\nNo data fetched. Check API key and network connection.")
        sys.exit(1)

    # Merge into CSV: append new dates, update existing rows with any newly
    # available columns (e.g. after a series swap or manual gold merge).
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
        else:
            # Fill in any columns that were previously missing (empty string)
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

    # Print latest values with threshold flags — each series uses its own
    # most recent date because some series (e.g. Brent) lag others by days.
    if all_data:
        print("\nLatest values:")
        display = {col: (label, sid) for col, (sid, label) in SERIES.items()}
        display["gold_usd"] = (GOLD_LABEL, "GC=F")
        for col in FIELDNAMES[1:]:  # preserve column order, skip "date"
            label, _ = display[col]
            dated = [(d, v[col]) for d, v in all_data.items() if col in v]
            if dated:
                latest_d, val = max(dated)
                flag     = threshold_flag(col, val)
                flag_str = f"  ← {flag}" if flag else ""
                print(f"  {label:<40} {val}  ({latest_d}){flag_str}")
            else:
                print(f"  {label:<40} n/a")


if __name__ == "__main__":
    main()
