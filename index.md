---
title: Overview
---

Research wiki tracking how regulation and deregulation cycles propagate through news events and market behavior. Four analytical frameworks produce a standing watch list of late-stage indicators; accumulated signals trigger escalation to analysis reports.

## Scope

The project is organized into four topic areas, each with a primary theoretical framework:

- **Theory** — regulatory cycle models and post-crisis reform patterns
- **Market Behavior** — mania/bubble psychology, fraud cycles, behavioral finance
- **Global Debt** — leverage crises, sovereign debt dynamics, Minsky debt cycles
- **Armed Conflict** — market-conflict nexus, geopolitical risk transmission, active situation reports

## Workflow

1. **Daily price fetch** — `uv run scripts/fetch_prices.py` pulls FRED + Yahoo Finance data into `data/prices.csv`
2. **Signal monitor** — `./scripts/monitor.sh` reads the watch list and price data, searches for matching news, and appends entries to `news/signal-log.md`
3. **Synthesis review** — accumulated log entries are evaluated against the current cycle position in `news/watch-list.md`; signals that cross escalation thresholds trigger analysis reports in the relevant topic directory
4. **Triage** — new research dropped into `_inbox/` is formatted and routed to the appropriate topic directory per `.claude/rules/inbox-triage.md`

See `README.md` for setup and daily run commands.
