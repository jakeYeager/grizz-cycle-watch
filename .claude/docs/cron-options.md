# Monitor Automation Options

The Signal Monitor (`scripts/monitor.sh`) currently requires manual invocation. Two options for daily automation:

---

## Option 1: macOS cron (local)

Runs the script on your machine on a schedule. Simple to set up — no external dependencies.

**Setup:**
```bash
crontab -e
```

Add:
```
0 8 * * * cd /Users/jake/Projects/Code/prod/grizz-cycle-watch && ./scripts/monitor.sh >> logs/monitor.log 2>&1
```

This fires at 8am daily. Adjust the time (`0 8 * * *`) as needed.

**Tradeoffs:**
- Machine must be on and awake at run time
- Logs stay local in `logs/monitor.log`
- No additional setup beyond the crontab entry
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
