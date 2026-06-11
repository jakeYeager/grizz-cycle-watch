---
title: "Bezzle Index — BDC Basket Data Pull (Q4 2024 – Q1 2026)"
date: "2026-06-10"
description: "First empirical pull for the experimental Bezzle Index. Trailing-6-quarter PIK-income share (B1) and non-accrual / NAV divergence (B2) across the six-name BDC basket, sourced from primary SEC 10-Q/10-K filings. Establishes the baseline and tests whether B1/B2 carry signal independent of the gate-cascade and HY-OAS indicators."
status: "working-document"
categories: [news, markets, behavioral-finance]
---

# Bezzle Index — BDC Basket Data Pull (Q4 2024 – Q1 2026)

*Experimental. First measured reading replacing the provisional YELLOW in `composite-indices.md`. All figures from primary EDGAR filings (Tier 1); per-name source filings and derivation notes held in the source-agent records. Q1 2026 (filed Apr–May 2026) is the latest filed quarter as of 2026-06-10; Q2 2026 10-Qs not yet filed.*

## B1 — PIK income as % of total investment income

| Name | Q1'26 | Q4'25 | Q3'25 | Q2'25 | Q1'25 | Q4'24 | Trend |
|---|---|---|---|---|---|---|---|
| ARCC | 15.2% | 14.8% | 15.5% | 17.7% | 16.0% | 16.5% | Flat-to-down |
| OBDC | 6.9% | 7.0% | 6.2% | 6.1% | 7.6% | 10.6% | Falling |
| BCRED | 6.0% | 7.2% | 6.4% | 5.7% | 5.3% | 5.8% | Rising (only name) |
| FSK | 12.5% | 15.8% | 14.5% | 13.3% | 16.0% | 23.6% | Falling |
| BXSL | 6.6% | 8.4% | 8.2% | 6.4% | 6.0% | 5.1% | Up then back (control) |
| MFIC | 4.7% | 5.1% | 5.7% | 9.0% | 5.2% | 4.6% | Choppy, low |
| **Basket mean** | **8.7%** | **9.7%** | **9.4%** | **9.7%** | **9.4%** | **11.0%** | **Flat-to-declining** |

**B1 verdict: no signal in this window.** Basket-mean PIK share is flat-to-declining (11.0% → 8.7%). Only BCRED shows a sustained step-up, and it eased in Q1'26. PIK is *elevated in level* for ARCC and FSK (~12–16%) but not *rising* — and rising-PIK was the entire leading-indicator thesis (the liar-loan analog). The RED condition "PIK > 1.5× and rising 3+ quarters" is met by no name. **B1 is redundant against what's already known.**

## B2 — Non-accruals and NAV (the divergence test)

Non-accrual % (cost basis unless noted FV); NAV/share at quarter-end. Q1'25 → Q1'26 move shown.

| Name | Non-accrual Q1'25 → Q1'26 | NAV Q1'25 → Q1'26 | Read |
|---|---|---|---|
| ARCC | 1.5% → 2.1% cost (0.9% → 1.2% FV) | $19.82 → $19.59 (−1.2%) | Mild rise, NAV softening — moving together |
| OBDC | 1.6% → 2.0% cost (peak 3.2% Q3'25) | $15.14 → $14.41 (−4.8%) | Rising, NAV down — together (firm cites spread widening) |
| BCRED | 0.3% → 2.4% cost (0.1% → 1.4% FV) | $25.25 → $24.19 (−4.2%) | **4× Q1'26 spike**, marked in NAV — together; JV non-accruals excluded run 4.8% cost |
| FSK | 2.1% → 4.2% FV (cost n/d) | $23.37 → $18.83 (−19.4%) | Doubled; open deterioration, marked not masked — highest in basket |
| BXSL | 0.3% → 4.7% cost (3.1% FV Q1'26) | $27.39 → $26.26 (−4.1%) | **Control broke**: non-accruals spike 4.7% while NAV holds −4% — mild divergence |
| MFIC | 1.7% → 5.3% cost (0.9% → 3.5% FV) | $14.93 → $13.82 (−7.4%) | **Classic amend-and-pretend**: non-accruals quadruple, NAV barely moves |

**B2 verdict: strong, unanimous, and partly leading.**

1. **Every one of the six names' non-accruals rose** over the trailing four quarters — most sharply, several with a distinct **Q1 2026 inflection** (BCRED and BXSL both jumped 4×+ in that single quarter; MFIC and FSK on steeper climbs).
2. **The amend-and-pretend divergence (non-accruals running ahead of NAV markdown) is real in 2 of 6** — MFIC clearly, BXSL mildly. BCRED is *not* masking (it marked the spike into NAV), but it parks higher non-accruals in unconsolidated JVs (Emerald/Verdelite at 4.8% cost) that the consolidated line excludes — a structural concealment vector the index should track explicitly.
3. **It leads the project's existing signal.** The Q1 2026 filings (Apr–May 2026) showed basket-wide credit deterioration *before* the BCRED Q2 2026 redemption gate that the signal log captured on 2026-06-09 — and **HY OAS is flat at 2.75%**, i.e. the project's realized-stress credit gauge shows nothing here. B2 is earlier and broader than both the single-fund gate and the spread.

## Index implication

- **Reading: YELLOW holds — but now on firm B2 footing, not provisional.** RED (current rubric) is gated on rising PIK, which did not happen, so the rubric mechanically holds YELLOW; but the rubric is mis-weighted (see below).
- **Kill-criterion test: PASSED on B2, FAILED on B1.** The index survives because B2 surfaces a unanimous, partly-leading, HY-OAS-invisible signal. B1 should be demoted.

## Recommended rubric revision (for spec update)

1. **Demote B1 (PIK share)** from load-bearing leading leg to a *level-context* sub-indicator. It is informative as a level (ARCC/FSK structurally high) but did not lead.
2. **Promote B2 to the index engine**, split into two distinct signals:
   - **B2a — non-accrual acceleration** (basket-breadth: how many names' non-accruals are rising QoQ, and the magnitude of the largest single-quarter jump). The Q1'26 inflection is the prototype.
   - **B2b — NAV divergence** (non-accrual rise outrunning NAV markdown — the true amend-and-pretend concealment signal; MFIC/BXSL are the current carriers).
3. **Add a B2c — JV non-accrual concealment flag**: non-accruals parked in unconsolidated JVs above the consolidated-portfolio rate (BCRED Emerald/Verdelite). This is concealment-by-structure, exactly the bezzle mechanism.
4. **Re-gate RED** on B2a (breadth) + B2b (divergence) rather than on PIK.
