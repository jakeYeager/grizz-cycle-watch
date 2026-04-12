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

## 2. Log Entry Format

Add new entries at the top of `news/signal-log.md`, under a `## YYYY-MM-DD` date heading. Create the heading if it doesn't exist.

```markdown
### [Short title]

**Indicators:** [watch list indicator(s) moved — exact language from news/watch-list.md]

**Sections:** [Regulatory Cycle / Market Behavior / Global Debt / Armed Conflict]

**Scenario impact:** [probability shift, phase implication, or "confirms existing"]

**Source:** [outlet or source, date]

**Note:** [1–3 sentences — what this changes in the framework, not just what happened]
```

**Rules:**
- Do not edit past entries. Corrections go in a new entry referencing the original.
- Keep the Note field analytical, not descriptive — explain what the signal changes, not what it is.
- If a signal touches multiple sections, list all of them. Cross-cutting events are the most important to capture.
- If no watch list indicator is clearly moved, the event does not warrant a log entry.

---

## 3. Agents

The three agents that handle the monitoring pipeline are defined in `.claude/agents/`. Each eager-loads `.claude/rules/escalation-tree.md` before acting.

| Agent | Spec | Role |
|---|---|---|
| Signal Monitor | `.claude/agents/signal-monitor.md` | Searches for news, writes log entries |
| Synthesis Reviewer | `.claude/agents/synthesis-reviewer.md` | Evaluates accumulated signals, recommends escalation level |
| Report Writer | `.claude/agents/report-writer.md` | Drafts analysis files and addenda |

Escalation thresholds and routing logic live in `.claude/rules/escalation-tree.md`.

---

## 4. Invocation

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

## 5. Open Questions

- **Automated vs. manual cadence:** Signal Monitor can run on a schedule or be invoked manually. Daily automated search is the target state; until then, invoke when user flags a relevant event.
- **Source quality standards:** Currently no formal source tier list. Prioritize primary sources (government statements, central bank releases, shipping AIS data, official exchange data) over commentary.
- **Log archiving:** Once `news/signal-log.md` exceeds ~100 entries, consider splitting into dated archive files (e.g., `news/signal-log-2026-q2.md`) and starting a fresh current log.
