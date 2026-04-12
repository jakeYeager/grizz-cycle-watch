# data/

Reference price data for agent monitoring passes.

## prices.csv

Updated by `scripts/fetch_prices.py`. Append-only — new rows added on each run, existing dates skipped.

| Column | Series | Source | Watch List Threshold |
|---|---|---|---|
| `brent_usd` | Brent crude spot (USD/bbl) | FRED: DCOILBRENTEU | WARN >$95 / ALERT >$130 |
| `gold_usd` | Gold price, London PM fix (USD/troy oz) | FRED: GOLDPMGBD228NLBM | — (use in correlation with brent) |
| `treasury_10yr` | 10-Year Treasury yield (%) | FRED: DGS10 | WARN >4.75% / ALERT >5.0% |
| `vix` | CBOE VIX volatility index | FRED: VIXCLS | WARN >25 / ALERT >40 |
| `hy_spread` | ICE BofA US HY OA spread (%) | FRED: BAMLH0A0HYM2 | WARN >5.0% / ALERT >7.0% |

**Note on `hy_spread`:** The high-yield credit spread is the cleanest signal for distinguishing structural deleveraging from policy-messaging whiplash. Credit spreads do not react to tariff announcements the way equity and commodity prices do. Rising HY spread alongside gold/oil correlation strengthens a Stage 4 Kindleberger / Minsky Phase 3 call; divergence (gold/oil moving without spread widening) suggests noise.

## Setup

```bash
# Register for a free FRED API key:
# https://fred.stlouisfed.org/docs/api/api_key.html

export FRED_API_KEY=your_key_here

# Initial full history pull (from 2020-01-01):
uv run scripts/fetch_prices.py --full

# Daily update (last 30 days, skips existing dates):
uv run scripts/fetch_prices.py
```

`uv` handles the `requests` dependency automatically — no install step needed.

## Adding to cron

```
0 7 * * 1-5 cd /path/to/grizz-cycle-watch && FRED_API_KEY=your_key uv run scripts/fetch_prices.py >> logs/prices.log 2>&1
```

Runs weekdays at 7am, before the monitor pass at 8am.
