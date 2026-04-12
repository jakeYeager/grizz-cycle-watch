# Signal Monitoring Rule

Governs how signals are captured, evaluated, and escalated into analysis reports.

---

## 1. The Three-Layer Model

| Layer | File | Purpose | Trigger |
|---|---|---|---|
| **Signal log** | `news/signal-log.md` | Append-only event capture | Any watch list indicator moves |
| **Position update** | `news/watch-list.md` | Current cycle state table | Accumulated signals shift a phase or scenario probability |
| **Analysis file** | Section directory | Full report or addendum | Escalation thresholds met — see `escalation-tree.md` |

---

## 2. Agents

The three agents that handle the monitoring pipeline are defined in `.claude/agents/`. Each eager-loads `.claude/rules/escalation-tree.md` before acting.

| Agent | Spec | Role |
|---|---|---|
| Signal Monitor | `.claude/agents/signal-monitor.md` | Searches for news, writes log entries |
| Synthesis Reviewer | `.claude/agents/synthesis-reviewer.md` | Evaluates accumulated signals, recommends escalation level |
| Report Writer | `.claude/agents/report-writer.md` | Drafts analysis files and addenda |

Escalation thresholds and routing logic live in `.claude/rules/escalation-tree.md`.

---

## 3. Invocation

### Running the Monitor

```bash
./scripts/monitor.sh                             # standard pass, last 24–48hrs
./scripts/monitor.sh --since 72h                 # extend lookback
./scripts/monitor.sh --section "Armed Conflict"  # single section
```

### Evaluating a one-off article

```bash
./scripts/evaluate.sh https://example.com/article          # print evaluation only
./scripts/evaluate.sh https://example.com/article --write  # append to log if relevant
```

Without `--write`, output goes to stdout for review before committing. With `--write`, the agent appends directly to `news/signal-log.md`.

### Updating agent behavior

Agent context is file-based and version-controlled. Changes take effect on the next invocation.

| To change | Edit |
|---|---|
| What the agent searches for | Search query patterns in `.claude/agent-brief.md` |
| Relevance threshold | Relevance Standard in `.claude/agent-brief.md` |
| Cycle position | Position table in `news/watch-list.md` and `.claude/agent-brief.md` |
| Watch list indicators | `news/watch-list.md` + search queries in `.claude/agent-brief.md` |
| Escalation thresholds | `.claude/rules/escalation-tree.md` |
| Agent roles or context | `.claude/agents/` spec files |

---

## 4. Open Questions

- **Automated vs. manual cadence:** Signal Monitor can run on a schedule or be invoked manually. Daily automated search is the target state; until then, invoke when user flags a relevant event.
- **Source quality standards:** Defined in `.claude/rules/standards/source-quality.md`.
- **Log archiving and structural maintenance:** Handled by the Housekeeping Agent (`scripts/housekeeping.sh`). Run weekly or after large structural changes.
