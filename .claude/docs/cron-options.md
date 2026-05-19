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
0 7 * * 1-5 cd /Users/jake/Projects/Code/prod/grizz-cycle-watch && FRED_API_KEY=your_key uv run scripts/fetch_prices.py >> logs/prices.log 2>&1

# Fetch slow-cadence macro data (CPI, housing, unemployment, bank credit standards)
# Weekly is enough — these series release monthly/quarterly, not daily
45 6 * * 1 cd /Users/jake/Projects/Code/prod/grizz-cycle-watch && FRED_API_KEY=your_key uv run scripts/fetch_aggregates.py >> logs/aggregates.log 2>&1

# Run signal monitor (reads prices.csv and aggregates.csv before web searches)
0 8 * * 1-5 cd /Users/jake/Projects/Code/prod/grizz-cycle-watch && ./scripts/monitor.sh >> logs/monitor.log 2>&1
```

Price fetch runs at 7am Mon–Fri and the macro-aggregate fetch runs weekly at 6:45am Monday; monitor runs at 8am. The monitor reads `data/prices.csv` and `data/aggregates.csv` for ground-truth levels before any web searches, so the sequence matters — both fetches precede the monitor.

**One-time setup:**
```bash
# Seed full history before first automated run
export FRED_API_KEY=your_key_here
uv run scripts/fetch_prices.py --full
uv run scripts/fetch_aggregates.py --full
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

## Version control in automated runs

The scripts currently make no git commits — agent edits land as uncommitted working tree changes and require manual `git add / commit`.

### Local cron

Add `git add` and `git commit` at the end of each script, scoped to the files that agent is expected to touch. Changes become local commits that accumulate until you push. Low risk — you see everything before it leaves the machine.

### Remote schedule skill

The agent must commit **and push** or the changes evaporate when the run ends. The question is where it pushes:

| Pattern | How it works | Best for |
|---|---|---|
| Push to `main` directly | Lowest friction; changes are immediately canonical | Housekeeping (structural fixes only) |
| Push to `agent/` branch | Changes queue for periodic human merge | Signal log entries |
| Commit to branch + open PR | Full review gate before merging | Analysis reports, convergence reports |

### Suggested strategy by agent

| Agent | Commit strategy | Rationale |
|---|---|---|
| Housekeeping | Push to `main` | Structural fixes (frontmatter, link repairs) are low-risk and don't need review |
| Signal Monitor | Push to `agent/signal-log` branch | Log entries are research artifacts; weekly merge gives a light review pass |
| Report Writer | Open PR to `main` | Analysis files are substantive — warrant human sign-off before becoming canonical |

*Not yet wired up. Revisit when ready to push repo to remote and configure schedule skill.*

---

*Noted: 2026-04-11. Updated: 2026-04-12.*
