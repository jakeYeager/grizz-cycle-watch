# Signal Monitoring Rule

Governs how signals are captured, evaluated, and escalated into analysis reports.

---

## 1. The Three-Layer Model

| Layer | File | Purpose | Trigger |
|---|---|---|---|
| **Signal log** | `news/signal-log.md` | Append-only event capture | Any watch list indicator moves |
| **Position update** | `news/watch-list.md` | Current cycle state table | Accumulated signals shift a phase or scenario probability |
| **Analysis file** | Section directory | Full report or addendum | Escalation thresholds met (see Section 4) |

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

## 3. Agent Architecture

Three agents handle the monitoring pipeline. Each reads topic context before acting.

### Agent 1 — Signal Monitor

**Role:** Searches for news matching watch list indicators and writes log entries.

**Context to read before searching:**
- `news/watch-list.md` — current watch list and cycle position
- `news/signal-log.md` — recent entries (avoid duplicating events already logged)

**Search strategy:**
- For each section in the watch list, run searches targeting the specific indicators listed
- Prioritize cross-cutting signals (events that move indicators in multiple sections)
- Ignore general market commentary unless it directly references a watch list indicator

**Output:** One or more log entries appended to `news/signal-log.md`. Never writes analysis files directly.

**Cadence:** Daily, or immediately when a user flags a relevant event.

---

### Agent 2 — Synthesis Reviewer

**Role:** Reads recent log entries against full topic context and recommends an escalation level.

**Context to read before synthesizing:**
- All section files (theory/, market-behavior/, global-debt/, armed-conflict/)
- `news/watch-list.md` — current cycle position
- `news/signal-log.md` — all entries since last position update

**Output:** One of four recommendations:
1. **No action** — signals confirm existing position, no change warranted
2. **Position update** — update the cycle position table in `news/watch-list.md`
3. **Addendum** — draft a companion file to an existing analysis
4. **Full report** — draft a new analysis file (see escalation thresholds below)

**The synthesis question:** Are the accumulated signals evidence of a phase transition, or confirmation of the current phase? Confirmation → log. Transition → escalate.

---

### Agent 3 — Report Writer

**Role:** Drafts full analysis files or addenda when triggered by the Synthesis Reviewer.

**Context to read before writing:**
- The specific analysis file being extended (if addendum)
- Relevant section files for cross-references
- `news/signal-log.md` entries that triggered the escalation
- `.claude/rules/inbox-triage.md` — formatting standards, frontmatter schema, APA citations

**Output:**
- **Addendum:** new file in the relevant section directory, frontmatter `addendum-to:` field set, registered in `_quarto.yml`
- **Full report:** new file in the most appropriate section directory, full frontmatter, registered in `_quarto.yml`
- **Convergence report:** when Level 4 is triggered by cross-section convergence (multiple frameworks simultaneously), route to `news-convergence/` instead of a topic directory

---

## 4. Escalation Decision Tree

### Level 1 → Log only
Default for all signals. A single indicator moving, even materially, stays at log level unless escalation thresholds below are met.

### Level 2 → Position update (edit `news/watch-list.md`)

Trigger when **any** of:
- Scenario probability shift of ≥15 percentage points (e.g., Scenario C moves from 20% to 35%)
- A framework phase visibly advances (e.g., first documented Kindleberger Stage 4 signal)
- 3+ log entries within 7 days pointing in the same direction within a single section

### Level 3 → Addendum to existing analysis

Trigger when:
- A political or operational development materially updates the geometry of an existing analysis (e.g., new actor enters the three-body problem)
- New quantitative data changes probabilities or timelines in a current working document
- An active situation report (status: working-document) has a confirmed resolution or escalation

**Format:** New file with `addendum-to: "Original Title (YYYY-MM-DD)"` in frontmatter. Do not edit the original file.

### Level 4 → Full analysis report

**Immediate triggers (any single event):**
- Brent crude sustained above $130/bbl for 48+ hours
- 10-year Treasury yield breaches 5.0%
- Derivatives counterparty failure or margin call at a systemically important financial institution
- G7 sovereign credit rating downgrade by a major agency
- Confirmed forced deleveraging event (ETF flash crash, money market fund gate, repo disruption)
- Any confirmed nuclear/radiological event or direct strike on nuclear infrastructure
- Strait of Hormuz physical infrastructure struck, mined, or declared formally closed by Iran under international law

**Convergence triggers (within a 7-day window):**
- 3+ watch list indicators from different sections all moving toward the same scenario
- Cross-section convergence: armed conflict signal + debt signal + regulatory signal simultaneously (suggests systemic interaction, not isolated event)

**Phase shift triggers:**
- Regulatory: first confirmed Phase 5 signal — major fraud disclosure, political reversal of 2025 deregulation, or enforcement crisis at a deregulated institution
- Kindleberger: documented smart money exit + simultaneous credit tightening (Stage 4 onset)
- Minsky: forced deleveraging at scale — not just a price drop but collateral calls propagating across institutions

### Addendum vs. Full Report call
- Event directly extends an existing analysis and the original framing still holds → **Addendum**
- Event requires a new framing, introduces a new variable, or the original analysis is now superseded → **Full Report**

---

## 5. Invocation

### Running the Monitor

```bash
./scripts/monitor.sh                          # standard pass, last 24–48hrs
./scripts/monitor.sh --since 72h              # extend lookback
./scripts/monitor.sh --section "Armed Conflict"  # single section
```

### Evaluating a one-off article

```bash
./scripts/evaluate.sh https://example.com/article        # print evaluation only
./scripts/evaluate.sh https://example.com/article --write  # append to log if relevant
```

Without `--write`, output goes to stdout for review before committing. With `--write`, the agent appends directly to `news/signal-log.md`.

### "Training" the agent

Agent context is not a model fine-tune — it is file-based and version-controlled. The agent reads these files at invocation time:

| File | What it controls |
|---|---|
| `.claude/agent-brief.md` | Cycle position, search query patterns, escalation triggers, relevance standard |
| `news/watch-list.md` | Current watch list — the primary signal specification |
| `news/signal-log.md` | Recent entries — prevents duplicate logging |
| Topic analysis files | Deep framework context for evaluating relevance |

**To adjust what the agent searches for:** edit the search query patterns in `.claude/agent-brief.md`.
**To tighten or loosen relevance:** edit the Relevance Standard section in `.claude/agent-brief.md`.
**To update cycle position:** edit the position table in both `news/watch-list.md` and `.claude/agent-brief.md`.
**To add a new watch list indicator:** add it to `news/watch-list.md` and add corresponding search queries to `.claude/agent-brief.md`.

---

## 6. Open Questions

- **Automated vs. manual cadence:** Signal Monitor can run on a schedule or be invoked manually. Daily automated search is the target state; until then, invoke when user flags a relevant event.
- **Source quality standards:** Currently no formal source tier list. Prioritize primary sources (government statements, central bank releases, shipping AIS data, official exchange data) over commentary.
- **Log archiving:** Once `news/signal-log.md` exceeds ~100 entries, consider splitting into dated archive files (e.g., `news/log-2026-q2.md`) and starting a fresh current log.
