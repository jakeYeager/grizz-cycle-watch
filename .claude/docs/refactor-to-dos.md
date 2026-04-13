# Refactor To-Dos

Open architectural questions deferred from active sessions. Review before the next refactor pass.

---

## Search Query Patterns — periodic refresh or extraction

**Problem:** The search query patterns in `.claude/agent-brief.md` encode current actors and flashpoints. As situations resolve or new actors emerge, stale queries produce noise or miss new signals. Queries and cycle position are also coupled in the same file, so updating one risks drifting the other.

**Option A — Extract to `news/search-queries.md` (living document)**

Move query patterns out of `agent-brief.md` into a dedicated living document that the Signal Monitor eager-loads alongside `agent-brief.md`. When a Level 2 position update is made to `watch-list.md`, also review and update `search-queries.md`. Keeps query evolution visible in git history alongside the position changes that motivated it. Fits the existing file-based architecture with no structural changes.

**Option B — Query coverage check in the monitor script**

After each monitor run, the agent outputs a "query coverage note" flagging any watch-list indicators it couldn't find a matching query for. Human reviews and updates manually on inspection. Lower automation overhead; relies on human follow-through.

Option A is the simpler default. Option B is an enhancement that could layer on top of A.

---

## `news-convergence/` naming convention

**Resolved (2026-04-13):** Convention is `YYYY-MM-DD-short-slug.md`. Slug describes the distinctive argument; "convergence" is implicit from the directory. Existing files renamed accordingly:
- `april-2026-convergence.md` → `2026-04-11-phase-transition.md`
- `april-2026-framework-convergence.md` → `2026-04-13-retail-capital-channel.md`

**Open:** The `inbox-triage.md` routing table and open questions section should be updated to document this convention explicitly for dated reports in `news-convergence/`. Consider whether the same `YYYY-MM-DD-slug` convention should apply to `news/` dated reports (see `inbox-triage.md` §10).

---

## Document status taxonomy — document in `inbox-triage.md`

**Resolved (2026-04-13):** Three-value status taxonomy adopted:

| Status | Meaning | Housekeeping behavior |
|---|---|---|
| `working-document` | Incomplete draft — not ready for reference | Flag if >30 days without update |
| `active` | Complete, tied to an ongoing situation — addenda expected | Do not flag for staleness |
| *(no status)* | Stable framework/reference document | Ignore |

Housekeeping agent spec updated to reflect this. **Open:** Add the taxonomy table to `inbox-triage.md` frontmatter schema section (§2) so it's visible during triage.
