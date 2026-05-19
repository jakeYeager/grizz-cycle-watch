# data/

Reference data for agent monitoring passes — fast daily prices and slower-cadence macro aggregates.

## prices.csv

Updated by `scripts/fetch_prices.py`. Append-only — new rows added on each run, existing dates skipped.

| Column | Series | Source | Watch List Threshold |
|---|---|---|---|
| `brent_usd` | Brent crude spot (USD/bbl) | FRED: DCOILBRENTEU | WARN >$95 / ALERT >$130 |
| `gold_usd` | Gold futures front month (USD/troy oz) | Yahoo Finance: GC=F | — (use in correlation with brent) |
| `treasury_10yr` | 10-Year Treasury yield (%) | FRED: DGS10 | WARN >4.75% / ALERT >5.0% |
| `vix` | CBOE VIX volatility index | FRED: VIXCLS | WARN >25 / ALERT >40 |
| `hy_spread` | ICE BofA US HY OA spread (%) | FRED: BAMLH0A0HYM2 | WARN >5.0% / ALERT >7.0% |

**Note on `gold_usd`:** Sourced from GC=F (COMEX gold futures front month) via Yahoo Finance. LBMA fixing series are not available through the FRED API due to licensing restrictions. GC=F is a futures price rather than a spot fix but tracks spot closely for daily monitoring purposes.

**Note on `hy_spread`:** The high-yield credit spread is the cleanest signal for distinguishing structural deleveraging from policy-messaging whiplash. Credit spreads do not react to tariff announcements the way equity and commodity prices do. Rising HY spread alongside gold/oil correlation strengthens a Stage 4 Kindleberger / Minsky Phase 3 call; divergence (gold/oil moving without spread widening) suggests noise.

## aggregates.csv

Updated by `scripts/fetch_aggregates.py`. The slow-cadence companion to `prices.csv` — structural macro series that release on a monthly, weekly, or quarterly schedule. A ragged grid: each series populates only on its own release dates, so most rows are sparse.

| Column | Series | Source | Cadence | Threshold (flag basis) |
|---|---|---|---|---|
| `home_sales` | Existing home sales (units, SAAR) | FRED: EXHOSLUSM495S | monthly | WARN < −10% YoY |
| `case_shiller` | Case-Shiller US National home price index | FRED: CSUSHPISA | monthly (~2-mo lag) | NOTE < 0% YoY |
| `months_supply` | Months' supply of new houses | FRED: MSACSR | monthly | WARN > 9 |
| `mortgage_30yr` | 30-Year fixed mortgage rate (%) | FRED: MORTGAGE30US | weekly | WARN > 7.5% |
| `cpi` | CPI-U all items | FRED: CPIAUCSL | monthly | WARN > 3% / ALERT > 4% YoY |
| `cpi_core` | CPI-U core (ex food & energy) | FRED: CPILFESL | monthly | WARN > 3% / ALERT > 4% YoY |
| `unemployment` | Unemployment rate (%) | FRED: UNRATE | monthly | WARN > 4.5% / ALERT > 5.0% |
| `sloos_tightening` | SLOOS net % banks tightening C&I loans | FRED: DRTSCILM | quarterly | WARN > 20% / ALERT > 40% |
| `mortgage_delinquency` | Single-family mortgage delinquency rate (%) | FRED: DRSFRMACBS | quarterly | WARN > 3% / ALERT > 5% |

**Note on YoY series:** `cpi`, `cpi_core`, `case_shiller`, and `home_sales` are index or count series — the CSV stores the raw FRED value, and `fetch_aggregates.py` reports the year-over-year change, which is what their threshold flags fire on. A routine run uses a 400-day lookback so the YoY comparison always has a prior-year observation.

**Note on `sloos_tightening`:** the net percentage of banks tightening commercial & industrial lending standards is the quantified form of the Kindleberger Stage 4 "simultaneous credit tightening" trigger condition.

**Note on `EXHOSLUSM495S`:** this FRED series carries a thin history (~13 monthly observations). It delivers a current value and a usable YoY; deep home-sales history would need a different series ID.

## Setup

```bash
# Register for a free FRED API key:
# https://fred.stlouisfed.org/docs/api/api_key.html

export FRED_API_KEY=your_key_here

# Initial full history pull:
uv run scripts/fetch_prices.py --full       # prices, from 2020-01-01
uv run scripts/fetch_aggregates.py --full   # aggregates, from 2015-01-01

# Routine update (skips existing dates):
uv run scripts/fetch_prices.py              # prices — run daily (last 30 days)
uv run scripts/fetch_aggregates.py          # aggregates — run weekly (last 400 days)
```

`uv` handles the `requests` dependency automatically — no install step needed.

## Adding to cron

```
0 7 * * 1-5 cd /path/to/grizz-cycle-watch && FRED_API_KEY=your_key uv run scripts/fetch_prices.py >> logs/prices.log 2>&1
45 6 * * 1 cd /path/to/grizz-cycle-watch && FRED_API_KEY=your_key uv run scripts/fetch_aggregates.py >> logs/aggregates.log 2>&1
```

Prices fetch weekdays at 7am; aggregates fetch weekly on Monday at 6:45am — both before the monitor pass at 8am. See `.claude/docs/cron-options.md` for the full setup.
