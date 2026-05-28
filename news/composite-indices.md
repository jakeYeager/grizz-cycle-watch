---
title: "Composite Indices"
date: "2026-05-26"
description: "Delay-Tactics Composite (DTC) and Narrative-Divergence Index (NDI) — structured rubric definitions, zone logic, current readings, escalation hooks, and convergence-window analysis. Cross-section synthesis tools introduced 2026-05-26."
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

**Current reading (2026-05-26): YELLOW.**

- **A**: ~44 days to July 9 buffer wall; ~101 days to hard exhaustion at sustained draw rate. Birol six-week clock (April 16 → ~May 28) observably expiring this week per IEA May OMR — 246 mb global inventory draw across March–April at the fastest rate on record; OECD on-land stocks down 146 mb. The clock is replaced, not extended, by the buffer-arithmetic-to-July-9 read.
- **B**: ~$550–800M estimated cumulative — revised down from the May 23 entry's $600–800M/month framing because the May 26 monitor confirmed China-Iran crude offtake fell ~20% YoY to ~1.1 mb/d (Shandong port enforcement, teapot refinery shutdowns). Below the $1B threshold; axis not breached. **Precision note (2026-05-28):** the $550–800M figure is rate-and-volume extrapolation, not confirmed on-chain aggregate — Chainalysis has confirmed the PGSA crypto-toll mechanism is operational but published no cumulative revenue total; TRM Labs' $8–10B/year Iran crypto figure is not PGSA-disaggregated. The "20% YoY decline" framing applies to the post-April-13 blockade-loading rate; March–early-April flow ran at 1.5 mb/d+ (above the 2025 1.38 mb/d baseline) and is still arriving in China on a 2–4 month transit lag through June–July. Separately, the EOPL shadow-channel generates a parallel Iran revenue stream (~$50–100M/day at current volumes × $86–89/bbl Iranian discount) that is structurally orthogonal to Axis B (Axis B = transit tolls; shadow-channel = export revenue) and is not captured in this metric.
- **C**: 5 days since Khamenei HEU directive (May 21). Below 14-day threshold; axis not breached.

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

## Convergence window

The DTC and NDI converge in time during the Q2 2026 earnings cycle (late July), which overlaps with the July 9 IEA buffer wall (DTC axis A) and the next plausible Mag-7 guidance event (NDI CRITICAL trigger). Alignment force on both indices within the same ~14-day period — marked for forward-looking Synthesis Reviewer attention.

**EOPL transit-lag clock added 2026-05-28.** A third supply clock is now identified inside the same window: Iranian crude loaded January–early April 2026 under the pre-full-blockade rate (1.5 mb/d+ at Shandong/Dalian per Kpler) is in transit to Chinese refineries on a 2–4 month lag and arriving through June–July. This is the concealed supply cushion supporting current Chinese refinery throughput; it drains directly into the July 9 IEA window. The convergence is now three-clock: (1) IEA emergency-release window expiry (DTC axis A binding); (2) EOPL shadow-pipeline drain (Chinese refinery supply tightens as pre-blockade-loaded cargoes work off); (3) Q2 earnings cycle (NDI CRITICAL trigger window). All three constrain the same ~late-July period; the second clock is structurally distinct from the first (one is global buffer arithmetic; the other is China-specific feedstock supply). Forward-looking flag — does not advance the current YELLOW reading.
