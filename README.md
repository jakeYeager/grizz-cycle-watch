# grizz-cycle-watch

Research wiki tracking how regulation/deregulation cycles propagate through news events and market behavior.

## Setup

```bash
# Copy and fill in your FRED API key (free at fred.stlouisfed.org/docs/api/api_key.html)
cp .env.example .env   # or just: echo "FRED_API_KEY=your_key" > .env

# Seed full data history
uv run scripts/fetch_prices.py --full       # prices (2020–present)
uv run scripts/fetch_aggregates.py --full   # macro aggregates (2015–present)
```

`data/prices.csv` and `data/aggregates.csv` are gitignored — they live locally and grow with each run.

## Daily sequence

Run in order. The monitor reads `data/prices.csv` and `data/aggregates.csv` before searching, so the fetches must come first.

```bash
# 1. Update price data (Brent, Treasury 10yr, VIX, HY spread)
uv run scripts/fetch_prices.py

# 2. Run the signal monitor (searches news, appends to news/signal-log.md)
./scripts/monitor.sh
```

`data/aggregates.csv` (CPI, housing, unemployment, bank credit standards) refreshes on a separate **weekly** cadence — its FRED series release monthly or quarterly, so a daily fetch isn't needed:

```bash
uv run scripts/fetch_aggregates.py   # run weekly — refreshes slow-cadence macro series
```

To extend the lookback window or target a single section:

```bash
uv run scripts/fetch_prices.py --days 14   # wider window (useful for Brent, which lags ~7 days)
./scripts/monitor.sh --since 72h
./scripts/monitor.sh --section "Armed Conflict"
```

To evaluate a specific article:

```bash
./scripts/evaluate.sh https://example.com/article          # print evaluation only
./scripts/evaluate.sh https://example.com/article --write  # append to log if relevant
```

## Maintenance

Run weekly or after large structural changes:

```bash
./scripts/housekeeping.sh           # run checks + agent
./scripts/housekeeping.sh --dry-run # print findings only, no agent
```

Checks: internal link validation, `_quarto.yml` consistency, frontmatter completeness, signal log size (archives at 100 entries), stale working-documents.

## Automation

See `.claude/docs/cron-options.md` for macOS cron and Claude Code schedule skill options.

## Build

```bash
quarto render   # outputs to _site/
quarto preview  # local dev server
```
