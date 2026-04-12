#!/usr/bin/env python3
"""
fetch_prices.py — Pull key price series from FRED into data/prices.csv.

Series:
  brent_usd       Brent crude spot price (USD/bbl)         DCOILBRENTEU
  gold_usd        Gold price, London AM fix (USD/troy oz)  GOLDAMGBD228NLBM
  treasury_10yr   10-Year Treasury yield (%)               DGS10
  vix             CBOE VIX volatility index                VIXCLS
  hy_spread       ICE BofA US HY OA spread (%)             BAMLH0A0HYM2

The HY spread (hy_spread) is the cleanest Minsky Phase 3 indicator —
it does not react to tariff tweets the way equity and commodity prices do,
making it useful for distinguishing structural deleveraging from
policy-messaging whiplash.

Usage:
  python3 scripts/fetch_prices.py              # last 30 days (default)
  python3 scripts/fetch_prices.py --days 90
  python3 scripts/fetch_prices.py --full       # from 2020-01-01

Requires:
  FRED_API_KEY environment variable
  Register free at: https://fred.stlouisfed.org/docs/api/api_key.html

  pip install requests
"""

import argparse
import csv
import os
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Series configuration
# ---------------------------------------------------------------------------

SERIES = {
    "brent_usd":     ("DCOILBRENTEU",       "Brent crude spot (USD/bbl)"),
    "gold_usd":      ("GOLDAMGBD228NLBM",   "Gold price (USD/troy oz)"),
    "treasury_10yr": ("DGS10",             "10-Year Treasury yield (%)"),
    "vix":           ("VIXCLS",            "CBOE VIX"),
    "hy_spread":     ("BAMLH0A0HYM2",      "ICE BofA US HY spread (%)"),
}

# Watch list threshold levels — printed as flags on latest values
THRESHOLDS = {
    "brent_usd": [
        (130.0, "ALERT — Level 4 escalation trigger"),
        (95.0,  "WARN  — Stagflation pressure on G7 debt service"),
        (90.0,  "NOTE  — Below $90 = Scenario A resolution signal"),
    ],
    "treasury_10yr": [
        (5.0,  "ALERT — Level 4 escalation trigger"),
        (4.75, "WARN  — G7 sovereign debt service stress"),
        (4.0,  "NOTE  — Below 4.0% = Scenario A resolution signal"),
    ],
    "hy_spread": [
        (7.0,  "ALERT — Distress-level credit spread"),
        (5.0,  "WARN  — Elevated; watch for Minsky Phase 3 deepening"),
    ],
    "vix": [
        (40.0, "ALERT — Crisis-level volatility"),
        (25.0, "WARN  — Elevated uncertainty"),
    ],
}

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
CSV_PATH  = Path(__file__).parent.parent / "data" / "prices.csv"
FIELDNAMES = ["date"] + list(SERIES.keys())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def load_existing_dates(path: Path) -> set:
    if not path.exists():
        return set()
    with open(path, newline="") as f:
        return {row["date"] for row in csv.DictReader(f)}


def threshold_flag(col: str, value: str) -> str:
    levels = THRESHOLDS.get(col)
    if not levels:
        return ""
    try:
        v = float(value)
    except ValueError:
        return ""
    for threshold, label in levels:
        if v >= threshold:
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

    api_key = os.environ.get("FRED_API_KEY")
    if not api_key:
        print("Error: FRED_API_KEY not set.", file=sys.stderr)
        print("Register free at https://fred.stlouisfed.org/docs/api/api_key.html",
              file=sys.stderr)
        sys.exit(1)

    end_date   = date.today()
    start_date = date(2020, 1, 1) if args.full else end_date - timedelta(days=args.days)

    print(f"▶ fetch_prices.py — {start_date} → {end_date}")
    print(f"  Series: {', '.join(SERIES)}\n")

    # Fetch all series
    all_data: dict[str, dict] = {}
    for col, (sid, label) in SERIES.items():
        print(f"  {sid:<25} {label}...", end=" ", flush=True)
        try:
            obs = fetch_series(api_key, sid, start_date.isoformat(), end_date.isoformat())
            for d, v in obs.items():
                all_data.setdefault(d, {})[col] = v
            print(f"{len(obs)} observations")
        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"FAILED: {e}")

    if not all_data:
        print("\nNo data fetched. Check API key and network connection.")
        sys.exit(1)

    # Append only new dates to CSV
    existing = load_existing_dates(CSV_PATH)
    new_rows  = {d: v for d, v in all_data.items() if d not in existing}

    CSV_PATH.parent.mkdir(exist_ok=True)
    write_header = not CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        for d in sorted(new_rows):
            row = {"date": d}
            row.update(new_rows[d])
            writer.writerow(row)

    print(f"\n  {len(new_rows)} new rows written → {CSV_PATH.relative_to(Path.cwd())}")

    # Print latest values with threshold flags
    if all_data:
        latest_date = max(all_data)
        latest      = all_data[latest_date]
        print(f"\nLatest values ({latest_date}):")
        for col, (sid, label) in SERIES.items():
            val  = latest.get(col, "n/a")
            flag = threshold_flag(col, val) if val != "n/a" else ""
            flag_str = f"  ← {flag}" if flag else ""
            print(f"  {label:<40} {val}{flag_str}")


if __name__ == "__main__":
    main()
