# Escalation Decision Tree

Single source of truth for escalation logic. Eager-loaded by all three monitoring agents.

---

## Level 1 → Log only

Default for all signals. A single indicator moving, even materially, stays at log level unless a threshold below is met.

---

## Level 2 → Position update (edit `news/watch-list.md`)

Trigger when **any** of:
- Scenario probability shift of ≥15 percentage points (e.g., Scenario C moves from 20% to 35%)
- A framework phase visibly advances (e.g., first documented Kindleberger Stage 4 signal)
- 3+ log entries within 7 days pointing in the same direction within a single section

---

## Level 3 → Addendum to existing analysis

Trigger when:
- A political or operational development materially updates the geometry of an existing analysis (e.g., new actor enters the three-body problem)
- New quantitative data changes probabilities or timelines in a current working document
- An active situation report (`status: working-document`) has a confirmed resolution or escalation

**Format:** New file with `addendum-to: "Original Title (YYYY-MM-DD)"` in frontmatter. Do not edit the original file.

---

## Level 4 → Full analysis report

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

---

## Addendum vs. Full Report

- Event directly extends an existing analysis and the original framing still holds → **Addendum**
- Event requires a new framing, introduces a new variable, or the original analysis is now superseded → **Full Report**

---

## Routing by report type

| Report type | Target directory |
|---|---|
| Single-topic analysis or addendum | Relevant section directory (`theory/`, `market-behavior/`, `global-debt/`, `armed-conflict/`) |
| Cross-section convergence report (Level 4 convergence trigger) | `news-convergence/` |
