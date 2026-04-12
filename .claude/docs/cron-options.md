# Monitor Automation Options

The Signal Monitor (`scripts/monitor.sh`) currently requires manual invocation. Two options for daily automation:

---

## Option 1: macOS cron (local)

Runs the script on your machine on a schedule. Simple to set up — no external dependencies.

**Setup:**
```bash
mkdir -p /Users/jake/Projects/Code/prod/grizz-cycle-watch/logs
crontab -e
```

Add the two-step daily sequence — price fetch first, then monitor pass:
```
# Fetch FRED price data (Brent, gold, Treasury yield, VIX, HY spread)
0 7 * * 1-5 cd /Users/jake/Projects/Code/prod/grizz-cycle-watch && FRED_API_KEY=your_key python3 scripts/fetch_prices.py >> logs/prices.log 2>&1

# Run signal monitor (reads prices.csv before web searches)
0 8 * * 1-5 cd /Users/jake/Projects/Code/prod/grizz-cycle-watch && ./scripts/monitor.sh >> logs/monitor.log 2>&1
```

Price fetch runs at 7am Mon–Fri; monitor runs at 8am. The monitor reads `data/prices.csv` for ground-truth price levels before any web searches, so the sequence matters.

**One-time setup:**
```bash
# Seed full price history before first automated run
export FRED_API_KEY=your_key_here
python3 scripts/fetch_prices.py --full
```

**Tradeoffs:**
- Machine must be on and awake at run time
- Logs stay local in `logs/prices.log` and `logs/monitor.log`
- `FRED_API_KEY` must be set in the crontab entry (cron doesn't inherit shell env)
- Best for: current state (local-only repo)

---

## Option 2: Claude Code schedule skill (remote)

Claude Code's built-in scheduling system runs agents on a cron schedule in the cloud. No machine required.

**Prerequisite:** The repo must be pushed to a remote (GitHub/GitLab) so the scheduled agent can pull current context — watch list, log, topic files.

**Setup:** Use the `/schedule` skill in Claude Code to configure a daily trigger with a prompt that pulls from the repo and runs the monitoring pass.

**Tradeoffs:**
- Fires regardless of whether your machine is on
- Agent pushes log entries back via git — requires write access to the remote
- More robust for always-on monitoring
- Requires the repo to be public or the agent to have auth
- Best for: after the repo is pushed to a remote

---

## Recommended path

1. Now: set up macOS cron (Option 1) for immediate daily runs
2. Later: when this branch is merged and pushed to GitHub, migrate to the schedule skill (Option 2) for cloud-based automation

---

*Noted: 2026-04-11. Revisit when ready to push repo to remote.*
