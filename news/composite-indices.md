---
title: "Composite Indices"
date: "2026-05-26"
description: "Delay-Tactics Composite (DTC), Narrative-Divergence Index (NDI), and the experimental Bezzle Index (BZI) — structured rubric definitions, zone logic, current readings, escalation hooks, and convergence-window analysis. Cross-section synthesis tools introduced 2026-05-26; BZI added 2026-06-10 on trial."
status: "living-document"
categories: [news]
---

# Composite Indices

*Introduced 2026-05-26 to consolidate scattered watch-list signals into composite readings. Recomputed on Synthesis Reviewer cadence rather than daily.*

## Delay-Tactics Composite (DTC)

A three-axis indicator measuring how much runway the parties stalling Hormuz resolution still have. Bridges Armed Conflict + Global Debt + Regulatory.

**Components:**

| Axis | Reads | Source priority |
|---|---|---|
| **A. External buffer-days remaining** | Days to next binding fuel-buffer wall (currently July 9, 2026 IEA emergency release window); hard physical exhaustion projected ~Sept 5 at sustained 4.1 mb/d draw rate per IEA May OMR | IEA Monthly Oil Market Report, EIA weekly petroleum status, ACI Europe, EU Commission energy dashboard |
| **B. Iran toll-revenue cumulative since PGSA inception (USD)** | Cumulative PGSA toll revenue since regime go-live (~April 22, 2026); rolling 30-day inflow rate maintained as sub-watch | OFAC, FinCEN, TRM Labs, Chainalysis on-chain forensics |
| **C. Days since last substantive diplomatic movement** | Days since last Tier 1 confirmed substantive move on the 14-point MOU framework (signing, partial signing, named-actor public concession or walk-back) | State Dept, IAEA, MFA Oman/UK/France, Iranian state media |

**Zone logic:**

| Zone | Condition |
|---|---|
| GREEN | A > 90 days AND B < $1B AND C < 14 days |
| YELLOW | Any one axis breached |
| ORANGE | Any two axes breached |
| RED | All three breached — *smokescreen collapse moment* |

**Current reading (2026-06-05): ORANGE.** Flipped from YELLOW (held since 2026-05-26) on the axis-C breach below. Two axes are now breached — **A (external buffer-days, breached since before the May 26 reading) + C (diplomatic-movement clock, breached 2026-06-04)** — while B remains clean. The flip is a breach-*count* move: axis A alone carried the YELLOW reading; axis C joining it is what reaches ORANGE (axis C breaching against an otherwise-clean composite would only have produced YELLOW). Per the escalation hook below, the YELLOW→ORANGE flip fired a Level 2 position update (see `news/watch-list.md`, 2026-06-05). NDI unchanged (RED-not-CRITICAL).

- **A**: ~34 days to July 9 buffer wall as of 2026-06-05 (was ~44 days at the May 26 reading); ~91 days to hard exhaustion at sustained draw rate. Birol six-week clock (April 16 → ~May 28) expired per IEA May OMR — 246 mb global inventory draw across March–April at the fastest rate on record; OECD on-land stocks down 146 mb. The clock is replaced, not extended, by the buffer-arithmetic-to-July-9 read. **This is the long-standing breach (A > 90 days is the GREEN condition; 34 days is well under it) that carried the YELLOW reading alone from 2026-05-26; axis C has now joined it.**
- **B**: ~$550–800M estimated cumulative — revised down from the May 23 entry's $600–800M/month framing because the May 26 monitor confirmed China-Iran crude offtake fell ~20% YoY to ~1.1 mb/d (Shandong port enforcement, teapot refinery shutdowns). Below the $1B threshold; axis not breached. **Precision note (2026-05-28):** the $550–800M figure is rate-and-volume extrapolation, not confirmed on-chain aggregate — Chainalysis has confirmed the PGSA crypto-toll mechanism is operational but published no cumulative revenue total; TRM Labs' $8–10B/year Iran crypto figure is not PGSA-disaggregated. The "20% YoY decline" framing applies to the post-April-13 blockade-loading rate; March–early-April flow ran at 1.5 mb/d+ (above the 2025 1.38 mb/d baseline) and is still arriving in China on a 2–4 month transit lag through June–July. Separately, the EOPL shadow-channel generates a parallel Iran revenue stream (~$50–100M/day at current volumes × $86–89/bbl Iranian discount) that is structurally orthogonal to Axis B (Axis B = transit tolls; shadow-channel = export revenue) and is not captured in this metric.
- **C**: **Breached 2026-06-04.** 14 days since the May 21 Khamenei HEU directive (May 21 = day 0; the 14-day threshold lands June 4), with no Tier 1-confirmed substantive diplomatic move in the interval. The June 1 formal Iranian talks-withdrawal, the June 3 Qeshm Island kinetic exchange, and Hezbollah's June 4 rejection of the Israel–Lebanon ceasefire are each the inverse of substantive movement; the 14-point MOU remains unsigned and no text exchange was confirmed. Trump's "deal in a week" framing is deal-narrative messaging, not a primary diplomatic act, and does not reset the clock (whiplash rule, per the agent-brief). Axis C crossing the threshold is the second breached axis and the trigger for the YELLOW→ORANGE flip above.

**Escalation hooks:**

- Flip to ORANGE → Level 2 position update (cross-section confirmation of stalemate exhaustion)
- Flip to RED → Level 4 convergence candidate (forced re-alignment imminent)
- Asymmetric reading note (2026-05-26): China's commercial enforcement of US secondary sanctions is *reducing* Iran's toll runway (axis B) while *accelerating* European buffer drawdown (axis A) — the two clocks are non-linearly coupled rather than independent.

## Narrative-Divergence Index (NDI)

A late-Kindleberger-Stage-4 diagnostic. Measures how much load the AI / neo-space-race "this time is different" narrative is carrying versus broad-market and physical-economy reality. Sits under Market Behavior.

**Components:**

| Sub-index | Reads | Source |
|---|---|---|
| **N1. Cap-weighted / equal-weight S&P 500 spread** | 30-day rolling spread between cap-weighted SPX return and SPX equal-weight return (positive = narrative concentration) | FRED, SPGI, `data/aggregates.csv` |
| **N2. AI/space capex-to-revenue ratio** | Trailing 4Q capex divided by trailing 4Q revenue for Mag-7 + AI/space pure-plays (PLTR, ANET, RKLB, ANDR, comparable cohort) | 10-Q/10-K filings |
| **N3. Sell-side power-cost flag** | Binary trigger: first major Tier 1/2 sell-side note explicitly flagging data center power constraint as a Mag-7 earnings risk | Goldman / J.P. Morgan / Morgan Stanley / BofA tech research desks |
| **N4. Smart-money exit principal count** | Number of separately identifiable named principals on documented Stage 4 exit (baseline 4: Burry, Berkshire, Einhorn, Grantham as of 2026-04-21) | 13F filings, deregistration notices, GP letters |
| **N5. Argument-rebuttal frequency** | Tier 2-3 outlets publishing "this time is different" argument alongside its rebuttal in the same outlet, rolling 60d. Quantified trigger: ≥3 distinct outlets within window | Bloomberg, Fortune, WSJ, FT, CNBC, Barron's, Axios |
| **N6. Fed-model equity risk premium compression** | Forward S&P 500 12-mo earnings yield minus 10-yr UST yield (basis: Axios / Bloomberg "Fed-model" methodology, distinct from Damodaran DCF-implied ERP which uses long-run growth assumptions and currently sits at long-run average ~4.2%). Quantitative N5-companion: when the Fed-model reading compresses sharply, the divergence vs. DCF-implied ERP is itself an N1-adjacent narrative-vs-fundamentals signal | FRED earnings yield + DGS10; Axios / Bloomberg compilations; Damodaran NYU Stern for DCF cross-check |

**Zone logic:**

| Zone | Condition |
|---|---|
| GREEN | N1 spread within ±1 std dev of 5y mean; N2 within historical industry range; N4 ≤ 2; N6 > 1.0 pp |
| YELLOW | N1 > +1 std dev; N2 elevated (>1.5× historical); N4 = 3; N6 0.5–1.0 pp |
| RED | N1 > +2 std dev; N2 > 2× historical; N4 ≥ 4; N5 ≥3 distinct outlets within rolling 60d; N6 < 0.5 pp |
| CRITICAL | First Mag-7 guidance miss attributed to input costs or power *OR* N1 spread blows out while EW rolls over *OR* N6 < 0.0 pp (Fed-model ERP turns negative — equity yields below UST) — *Stage 5 onset signature* |

**Current reading (2026-05-26): RED on structural sub-indices; not yet CRITICAL.**

- **N1**: at or near record (Buffett Indicator 226–232% per the April 21 watch-list update); explicit 30-day cap-weight vs. equal-weight spread number flagged for the next `aggregates.csv` refresh.
- **N2**: hyperscaler capex committing >$50B/yr each (Meta, MSFT, GOOG) against revenue not growing at that rate → >2× historical → red.
- **N3**: no Tier 1/2 sell-side note flagging hyperscaler power-cost risk identified in the Q1 2026 earnings cycle. Green-but-uncertain (no trigger fired).
- **N4**: 4 named principals (Burry, Berkshire, Einhorn, Grantham) → red threshold met.
- **N5**: confirmed and sustained as of 2026-05-28 — Bloomberg "TINA effectively over" / "Stagflation Era Flashbacks" cluster (April 7–9) + Fortune "dizzying new high" argument-rebuttal piece (April 19) + Axios "The disappearing premium to own stocks" (May 25) = 3 distinct Tier 2 outlets within rolling 60d window. Quantified threshold met; pattern is multi-outlet, multi-month, not a one-off Fortune piece.
- **N6**: **0.17 pp as of 2026-05-25** (Axios / Tier 2 — S&P 500 forward earnings yield 4.73% minus 10-yr UST 4.56%). RED threshold met (<0.5 pp). Second-tightest Fed-model ERP reading since the late-1990s dot-com peak (historical context: Dec 1999 trough was negative; Dec 2007 pre-GFC was ~3.4%; post-GFC peak was 8.17%). Damodaran's DCF-implied ERP cross-check at 4.23% (Jan 1, 2026, Tier 1) is at long-run average — divergence between the two methodologies is itself an N1-adjacent signal: forward-growth assumptions are doing the load-bearing work for valuations.

**Escalation hooks:**

- N3 binary fires (first sell-side power-cost flag) → Level 2 (narrative cracking)
- N6 sustained < 0.5 pp for 30d AND a Tier 1/2 sell-side note explicitly flagging the compression as a risk → Level 2 (narrative cracking, quantified)
- Mag-7 guidance miss attributed to input costs or power → Level 4 (Stage 5 onset)
- N1 spread sustained > +2 std dev with EW rolling over → Level 4 (Stage 5 onset)
- N6 < 0.0 pp (Fed-model ERP turns negative — equity yields below UST) → Level 4 (Stage 5 onset signature)

## Bezzle Index (BZI)

*Introduced 2026-06-10 (experimental). Rebuilt 2026-06-10 around B2 after the first BDC-basket pull — see `news/bezzle-index-basket-data.md`.* A concealment-pressure gauge. Galbraith's *bezzle* is the inventory of undiscovered fraud that **grows in the boom and is revealed in the bust** — invisible by construction, so it is proxied by the red flags that *lead* the reveal. Every other watch-list metric (gates, charge-offs, HY OAS, defaults) measures **realized** stress; the BZI is the orthogonal axis — **concealed** stress, the gap between reported and economic health. Bridges Global Debt + Regulatory + Market Behavior and feeds the otherwise-binary Regulatory **Phase 5 "major fraud disclosure"** trigger with a graduated, leading read. The cycle's concealment vector is private credit — the same Minsky Phase 3 anchor the project already tracks — so the BZI measures what gates do not: how much deterioration is held off the books rather than surfaced.

**Empirical pivot (2026-06-10).** The original spec made **PIK-income share (B1)** the load-bearing leg, on the liar-loan-analog thesis. The first basket pull (trailing 6 quarters, ARCC/OBDC/BCRED/FSK/BXSL/MFIC, all primary EDGAR) **falsified that for this cycle**: basket-mean PIK share was flat-to-declining (11.0% → 8.7%), elevated in *level* for ARCC/FSK but not *rising* — no lead. The signal lived entirely in the **non-accrual/NAV complex**: all six names' non-accruals rose, with a sharp Q1 2026 inflection, amend-and-pretend divergence at MFIC/BXSL, and non-accruals parked in unconsolidated JVs at BCRED — none of it visible in flat HY OAS (2.75%), and *ahead* of the Q2 2026 BCRED gate. So the index is rebuilt: **B1 demoted to level-context (no longer gates escalation); the B2 non-accrual complex, split three ways, becomes the engine.**

**Components:**

| Sub-index | Reads | Role | Lead/lag | Source |
|---|---|---|---|---|
| **B2a. Non-accrual acceleration / breadth** | Across the fixed BDC basket: count of names with QoQ-rising non-accruals + magnitude of the largest single-quarter jump. Breadth is the deterioration signal that precedes spreads | **Engine** | Leading | 10-Q portfolio summaries |
| **B2b. NAV divergence** | Non-accrual rise *outrunning* NAV markdown (the amend-and-pretend tell of Level-3 manager-discretion valuation) — the true concealment signal | **Engine** | Leading | 10-Q schedules of investments |
| **B2c. JV non-accrual concealment** | Non-accruals in unconsolidated JVs running above the consolidated-portfolio rate (concealment-by-structure — e.g. BCRED's Emerald/Verdelite) | **Engine (modifier)** | Leading | 10-Q JV schedules |
| **B3. Restatement wave** | Count of 8-K Item 4.02 ("non-reliance on previously issued financial statements"), rolling 90d vs. trailing-3yr baseline | Confirmation | Leading | EDGAR full-text search (free JSON API) |
| **B4. Auditor flight** | 8-K Item 4.01 auditor resignations/dismissals (weighted to resignations + financial issuers) + first-time going-concern opinions, rolling 90d vs. baseline | Confirmation | Leading | EDGAR |
| **B5. Activist short cluster** | Distinct credible activist-short reports (Hindenburg / Muddy Waters / Viceroy class) on US-listed financials/credit names, rolling 90d. Tier 2, adversarial — narrative-discounted, requires a second confirming signal | Confirmation | Coincident | Agent web-research |
| **B6. Enforcement realization** | SEC AAER + DOJ securities-fraud action counts, rolling 12mo vs. baseline — the bezzle being *revealed* | Confirmation | Lagging | SEC AAER list, DOJ press |
| **B1. PIK-income share** *(demoted)* | PIK interest as % of total investment income, trailing quarter, basket. **Level-context only — does NOT gate escalation** (did not lead in the Q4'24–Q1'26 window). Informative on earnings composition; a renewed *rising* trend would restore it to engine status | Context | Leading | BDC 10-Qs (EDGAR) |

**Zone logic.** Gated on the B2 engine. The distinction the index claims is *concealment* (divergence/structure), not mere *deterioration* (breadth) — honest marking of rising non-accruals (FSK, BCRED-consolidated) is the opposite of bezzle. So breadth alone is YELLOW; concealment is what earns RED.

| Zone | Condition | Meaning |
|---|---|---|
| GREEN | ≤1 basket name with rising non-accruals; no NAV divergence; no JV-concealment gap; B3/B4/B6 at baseline; B5 ≤ 1 | Bezzle stable |
| YELLOW | Non-accrual breadth — rising at ≥3 of 6 names **OR** any single ≥3× QoQ non-accrual jump | Deterioration accumulating, ahead of spreads |
| RED | Breadth ≥4 of 6 **AND** material NAV divergence at ≥2 names (B2b). B2c JV-concealment at a tracked fund is an aggravating modifier that raises within-zone severity but does not alone trip RED | Deterioration being concealed — Phase 5 disclosure probability elevated |
| CRITICAL | A confirmed restatement, gate-with-markdown, or enforcement action at a *tracked* private-credit fund or deregulated institution that retroactively validates the B2 buildup | Bezzle reveal = Phase 5 onset |

**Current reading (2026-06-10): YELLOW, RED-adjacent (first measured pull).** Breadth condition is *fully* met and then some — non-accruals rose at **6 of 6** names, with two ≥4× single-quarter jumps (BCRED 0.3%→2.4% cost, BXSL 0.3%→4.7% cost, both Q1 2026). The RED gate is held off by the divergence leg: **material B2b divergence is clear at one name (MFIC — non-accruals quadruple to 5.3% cost while NAV slips just −7%), mild at a second (BXSL), and absent at the rest**, which are marking deterioration honestly into NAV. **B2c is present** (BCRED parks 4.8%-cost non-accruals in Emerald/Verdelite JVs, above its 2.4% consolidated rate) — logged as an aggravating modifier, not a RED trigger on its own. Confirmation legs B3/B4/B6 are at baseline. Net: a measured YELLOW leaning toward RED, materially firmer than the prior provisional YELLOW. **Decision point: the Q2 2026 10-Qs (~Aug filing).** If the Q1'26 non-accrual inflection broadens or B2b divergence reaches a clear second name, that tips RED.

**Escalation hooks:**

- GREEN→YELLOW → Level 1 (log; deterioration accumulating ahead of spreads)
- YELLOW→RED → Level 2 position update (concealment confirmed; pre-position the Phase 5 binary)
- RED→CRITICAL → Level 4 — *this is the escalation-tree Phase 5 fraud-disclosure trigger firing*, reached by a graduated path instead of a surprise; routes per the Phase 5 line and the convergence-report routing table
- Inversion note: a sudden B6/restatement spike from a low base *while the B2 engine is already RED* is the highest-information print in the index — the reveal moment, the bezzle converting to disclosure.

**Trial caveats (still on probation):**

1. *RED gate must stay on concealment, not deterioration.* Breadth of rising non-accruals could simply be the credit cycle turning; what makes it *bezzle* is the divergence (B2b) and the JV parking (B2c). If RED ever fires on breadth alone, the index has collapsed back into a coincident credit-stress gauge that HY OAS / charge-offs already cover.
2. *Measuring something actively hidden, quarterly.* The bezzle is concealment by design, so the index is adversarial against its own data source; BDC filings are quarterly (no fast-move capture); a fixed public-BDC basket structurally misses private actors (often the worst). A slow, directional, strategic read — not a tripwire.

**Data path:** none of this is on FRED. B2a/B2b/B2c need quarterly agent extraction from 10-Q portfolio schedules (the basket pull); B3/B4/B6 are automatable via EDGAR full-text search + the SEC AAER page (a new fetch script, comparable to `fetch_aggregates.py`); B5 is agent web-research. Cadence is quarterly, on Synthesis-Reviewer rhythm. **Revised kill criterion:** the B1-redundancy finding is already banked. The index now lives or dies on B2 — if the next two quarterly pulls show the non-accrual breadth/divergence either (a) never confirmed by any disclosure-side leg (B3/B4/B6) before resolving, or (b) tracking HY OAS / the gate-cascade with no lead, then B2 is a lagging duplicate and the index retires.

## Convergence window

The DTC and NDI converge in time during the Q2 2026 earnings cycle (late July), which overlaps with the July 9 IEA buffer wall (DTC axis A) and the next plausible Mag-7 guidance event (NDI CRITICAL trigger). Alignment force on both indices within the same ~14-day period — marked for forward-looking Synthesis Reviewer attention.

**EOPL transit-lag clock added 2026-05-28.** A third supply clock is now identified inside the same window: Iranian crude loaded January–early April 2026 under the pre-full-blockade rate (1.5 mb/d+ at Shandong/Dalian per Kpler) is in transit to Chinese refineries on a 2–4 month lag and arriving through June–July. This is the concealed supply cushion supporting current Chinese refinery throughput; it drains directly into the July 9 IEA window. The convergence is now three-clock: (1) IEA emergency-release window expiry (DTC axis A binding); (2) EOPL shadow-pipeline drain (Chinese refinery supply tightens as pre-blockade-loaded cargoes work off); (3) Q2 earnings cycle (NDI CRITICAL trigger window). All three constrain the same ~late-July period; the second clock is structurally distinct from the first (one is global buffer arithmetic; the other is China-specific feedstock supply). Forward-looking flag — does not advance the current YELLOW reading.
