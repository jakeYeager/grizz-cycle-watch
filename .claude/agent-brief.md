# Grizz Cycle Watch — Agent Brief

Compact orientation for Monitor and Synthesis agents. Read this first, then the files listed under Context.

---

## Project Purpose

Research wiki tracking how regulation/deregulation cycles propagate through news events and market behavior. Four analytical frameworks produce a watch list of late-stage indicators. Signals are logged; accumulated signals trigger escalation to analysis reports.

---

## Current Cycle Position

**Read `news/watch-list.md` for current cycle position — the framework phase table and scenario probability table there are the single authoritative source and always reflect the most recent Synthesis Reviewer pass.** Do not assume cycle position from this brief; it does not get updated on Reviewer cadence.

Quick orientation: all four frameworks are in late-stage positions. Regulatory sits at the Phase 4/5 boundary with the first Phase 5 candidate signal *operational* (not just candidate). Kindleberger is Stage 4 confirmed on both trigger conditions, with the gate cascade now transmitting through multiple distinct channels (asset-class aggregate, marquee-fund non-standard absorption, individual-fund actually-gated). Minsky is Phase 3 deepening — the next discrete phase advance requires SIFI collateral-call propagation, not yet observed. Armed Conflict remains active across Scenarios B/C/D with direct kinetic enforcement on both sides. Specifics, dated revisions, and named indicator status live in the watch list.

---

## Price Reference Data

`data/prices.csv` contains daily observations for five key series updated by `scripts/fetch_prices.py`. Read the last 14 rows for current levels before running web searches — use these as ground truth rather than searching for prices separately.

| Column | What it measures | Watch list threshold |
|---|---|---|
| `brent_usd` | Brent crude spot (USD/bbl) | WARN >$95 / ALERT >$130 |
| `gold_usd` | Gold price (USD/troy oz) | Use in correlation with brent |
| `treasury_10yr` | 10-Year Treasury yield (%) | WARN >4.75% / ALERT >5.0% |
| `vix` | CBOE VIX | WARN >25 / ALERT >40 |
| `hy_spread` | ICE BofA US HY credit spread (%) | WARN >5.0% / ALERT >7.0% |

**`hy_spread` is the signal quality test for gold/oil correlation moves:** if both gold and oil fall but HY spread does not widen, the move is likely policy-messaging whiplash rather than structural deleveraging. Rising HY spread alongside the correlation confirms Stage 4 / Minsky Phase 3.

---

## Macro Aggregate Data

`data/aggregates.csv` contains slower-cadence structural macro series — monthly, weekly, and quarterly official statistics — updated by `scripts/fetch_aggregates.py`. It is the companion to `prices.csv`: where prices are fast and sentiment-driven, these series move on a release schedule. Read the most recent populated value of each column for current macro levels before running web searches. The file is a ragged grid — each series populates only on its own release dates — so "last N rows" does not apply; scan upward per column for the latest non-empty value.

| Column | What it measures | Threshold (flag basis) |
|---|---|---|
| `home_sales` | Existing home sales, units SAAR | WARN < −10% YoY |
| `case_shiller` | Case-Shiller US National home price index | NOTE < 0% YoY (prices falling) |
| `months_supply` | Months' supply of new houses | WARN > 9 |
| `mortgage_30yr` | 30-Year fixed mortgage rate (%) | WARN > 7.5% |
| `cpi` | CPI-U all items | WARN > 3% / ALERT > 4% YoY |
| `cpi_core` | CPI-U core (ex food & energy) | WARN > 3% / ALERT > 4% YoY |
| `unemployment` | Unemployment rate (%) | WARN > 4.5% / ALERT > 5.0% |
| `sloos_tightening` | SLOOS net % banks tightening C&I loans | WARN > 20% / ALERT > 40% |
| `mortgage_delinquency` | Single-family mortgage delinquency rate (%) | WARN > 3% / ALERT > 5% |

`sloos_tightening` is the quantified form of the Kindleberger Stage 4 "simultaneous credit tightening" trigger condition. `cpi`, `cpi_core`, `case_shiller`, and `home_sales` are index or count series whose meaningful read is the year-over-year change, not the raw level — the CSV stores the raw value and the fetch script reports YoY.

**Staleness check:** these series release on a monthly/quarterly schedule, so `aggregates.csv` does not need daily refreshing — but it can fall behind a release. If the latest populated value of a column predates a release known to have landed since the last fetch (e.g. a new CPI print), note it in the run summary and recommend the user run `uv run scripts/fetch_aggregates.py`.

---

## Composite Indices

Two composite indices were introduced 2026-05-26 to consolidate scattered watch-list signals into recomputable readings. **Read `news/composite-indices.md` for rubric definitions, sub-index detail, current zone readings, escalation hooks, and the convergence-window analysis.** The watch list (`news/watch-list.md`) references these composites by name and zone state but does not duplicate the rubric.

| Index | Tracks | Sections bridged |
|---|---|---|
| **DTC — Delay-Tactics Composite** | Runway remaining for parties stalling Hormuz resolution: external buffer-days (axis A), Iran toll-revenue cumulative since PGSA inception (axis B), days since last substantive diplomatic move (axis C) | Armed Conflict + Global Debt + Regulatory |
| **NDI — Narrative-Divergence Index** | Load the AI / neo-space-race "this time is different" narrative is carrying vs. broad-market and physical-economy reality: cap-weighted/equal-weight S&P spread (N1), AI/space capex-to-revenue (N2), sell-side power-cost flag (N3), smart-money exit principal count (N4), argument-rebuttal frequency (N5) | Market Behavior |

Both have explicit escalation hooks (zone flips → Level 2; CRITICAL trigger → Level 4). Recomputed on Synthesis Reviewer cadence rather than daily.

---

## Active Clocks

Named upcoming binaries that bind framework reads. Each warrants pre-position search activity in the 24–48 hours leading up to the date.

| Date | Clock | What it binds |
|---|---|---|
| 2026-05-29 | BCRED Q2 tender expiry | Highest-information Market Behavior data point — gate vs. no-gate; a gate without the Q1 $400M employee-capital one-off mechanism would be a stronger Stage 4 cascade signal than Vista's May 27 single-LP gate |
| 2026-06-03 | DTC axis C breach date (day 14 since Khamenei HEU directive) | If MOU remains unsigned, DTC flips YELLOW→ORANGE per the escalation hook in `news/watch-list.md` |
| 2026-06-03/04 | Armed Conflict 7d ageing-out window | May 26–27 counter-directional entries roll out of the 7-day window; one additional escalation entry would flip the section directionally clean |
| 2026-06-16/17 | Warsh first FOMC meeting | Discrete Phase 5 binary — a rate cut against the 3.8% April CPI print would be a hard Phase 5 confirmation (political capture overriding the price-stability mandate) |
| Late June 2026 | MSACSR May 2026 print | Sustained-crossing confirmation of the >9.0 housing-supply threshold first breached 2026-04 at 9.4 |
| 2026-07-09 | IEA emergency-release window expiry | DTC axis A binding; hard physical exhaustion projected ~Sept 5 at sustained 4.1 mb/d draw rate per IEA May OMR |
| Late July 2026 | DTC × NDI × EOPL three-clock convergence | IEA buffer wall + EOPL shadow-pipeline drain (Jan–Apr 2026 Iranian loads arriving on a 2–4 mo transit lag) + Q2 earnings cycle (NDI CRITICAL trigger window) all constrain the same ~14-day period |

Pre-position search activity should escalate as each binary approaches.

---

## Required Context Files

Read these before acting. They contain the indicators, current positions, log format, and escalation rules.

| File | Purpose |
|---|---|
| `news/watch-list.md` | Watch list — specific indicators per section |
| `news/signal-log.md` | Recent signal entries — do not duplicate |
| `.claude/rules/signal-monitoring.md` | Log format and escalation decision tree |

## Deep Context Files

Read when a signal touches that section.

| File | Section |
|---|---|
| `theory/regulatory-cycle-phases.md` | Regulatory Cycle |
| `market-behavior/kindleberger-mania-model.md` | Market Behavior |
| `market-behavior/legal-fraud-psychology.md` | Market Behavior |
| `global-debt/debt-crisis-catalysts.md` | Global Debt |
| `armed-conflict/market-conflict-cycles.md` | Armed Conflict (framework) |
| `armed-conflict/three-blockade-problem.md` | Armed Conflict (current active situation; three simultaneous closure mechanisms) |
| `armed-conflict/three-body-problem.md` | Armed Conflict (Israel-Iran-US geometry) |
| `armed-conflict/ordnance-cost-asymmetry.md` | Armed Conflict (cost curve / defense economics) |
| `armed-conflict/empty-pipeline.md` | Armed Conflict (supply shock reference; superseded by three-blockade-problem) |
| `news-convergence/2026-04-13-retail-capital-channel.md` | Cross-section convergence (DOL rule, Apollo gate, retail capital channel) |
| `news-convergence/2026-04-14-kindleberger-confirmed-india-scenario-d.md` | Cross-section convergence (Stage 4 confirmed, China resolved, India Scenario D) |
| `news-convergence/2026-04-21-pressure-clock-reconfiguration.md` | Cross-section convergence (pressure clock window closes without rupture; political expiry → buffer-statement clock reframing; first time-domain forcing-function reconfiguration) |
| `news-convergence/2026-05-18-stage4-confirmation-warsh-operational.md` | Cross-section convergence (Tier 1 data axis Stage 4 confirmation; Warsh Phase 5 candidate signal operational via DOJ-probe-as-lever precedent; Spirit Airlines first US corporate failure attributed to fuel shock) |

---

## Search Query Patterns

Use these as starting points. Vary phrasing — the goal is to surface signals that match watch list indicators, not general news.

### Regulatory Cycle
- `CFPB enforcement 2026` / `CFPB reinstatement`
- `Dodd-Frank reversal 2026` / `Dodd-Frank challenge`
- `DOL 401k safe harbor rule 2026` / `ERISA alternative investments fiduciary`
- `Anderson v Intel Corp Supreme Court` / `401k fiduciary prudence ruling`
- `SEC enforcement action 2026` / `OCC regulatory`
- `financial fraud disclosure 2026` / `regulatory capture financial 2026`
- `Warsh FOMC June 2026` / `Kevin Warsh first meeting` / `Fed rate decision Warsh`
- `Powell Fed Board 2026` / `Powell-Warsh tension` / `DOJ Powell probe Fed`

### Market Behavior
- `hedge fund short interest 2026` / `Goldman prime brokerage flows`
- `institutional equity positioning April 2026` / `hedge fund drawdown 2026`
- `margin calls 2026` / `forced selling equities`
- `private equity NAV markdown` / `redemption gate 2026`
- `private credit default rate Fitch Moody 2026`
- `Dimon JPMorgan private credit 2026` / `Apollo Carlyle Ares gate 2026`
- `BCRED Q2 tender 2026` / `Blackstone Private Credit tender offer`
- `Vista Credit BDC gate 2026` / `Vista Credit limited redemptions`
- `non-traded BDC net outflow 2026` / `Stanger BDC redemptions`
- `crypto sell-off risk-off 2026`
- `Mag-7 capex Q2 2026` / `hyperscaler capex revenue ratio` / `data center power constraint Mag-7`
- `Buffett indicator 2026` / `market cap to GDP 2026` / `Burry Berkshire Einhorn Grantham`

### Global Debt
- `10-year Treasury yield 2026` / `Treasury yield 5 percent`
- `Japan JGB yield 2026` / `BOJ rate hike normalization`
- `BIS credit-to-GDP warning` / `BIS quarterly review 2026`
- `shadow banking stress 2026` / `money market fund`
- `repo market disruption 2026`
- `derivatives counterparty failure` / `systemic risk bank 2026`
- `G7 sovereign debt rating` / `sovereign credit downgrade 2026`
- `India GDP energy shock 2026` / `India current account deficit Hormuz`
- `MSACSR housing months supply 2026` / `Census new residential sales 2026`
- `Case-Shiller April May 2026` / `MBA mortgage delinquency Q1 Q2 2026`

### Armed Conflict
- `Strait of Hormuz tanker 2026` / `AIS Hormuz transits`
- `US Iran ceasefire talks 2026` / `Iran nuclear talks second round`
- `US Iran 14-point MOU` / `Iran US framework agreement 2026`
- `Khamenei HEU directive` / `Iran enriched uranium stockpile 2026`
- `IRGC drone Hormuz 2026` / `IRGC naval incident`
- `Bandar Abbas strike 2026` / `US Iran direct strike 2026`
- `China Hormuz transit 2026` / `PLA fleet Hormuz`
- `PGSA Persian Gulf Strait Authority` / `Iran toll regime Hormuz 2026`
- `EOPL Eastern Outer Port Limit` / `STS ship-to-ship Malaysia Iran 2026` / `dark fleet Iran China 2026`
- `Hengli teapot refinery sanctions 2026` / `Shandong refinery Iranian crude`
- `Iranian crude Malaysian blend laundering` / `FinCEN Iran crypto advisory`
- `Tether CBI freeze Iran 2026` / `OFAC Iran shadow fleet`
- `India Hormuz bilateral deal` / `India Iran oil transit 2026`
- `India LPG shortage 2026` / `India energy crisis fuel`
- `Houthi Bab al-Mandab 2026`
- `Brent crude Iran war 2026`
- `EU aviation fuel shortage 2026` / `European jet fuel` / `ACI Europe paraffin`
- `IEA emergency release window` / `IEA Monthly Oil Market Report 2026`
- `fertilizer prices 2026` / `urea ammonia shortage` / `sulfur shortage 2026`
- `Ireland fuel shortage 2026` / `Australia fuel shortage 2026`

---

## Immediate Escalation Triggers

Any of these warrant a Level 4 full report regardless of other signals:

- Brent crude sustained above **$130/bbl** for 48+ hours
- 10-year Treasury yield breaches **5.0%**
- Derivatives counterparty failure or margin call at a systemically important institution
- Any confirmed nuclear or radiological event
- G7 sovereign credit rating downgrade by a major agency
- Strait of Hormuz physical infrastructure struck, mined, or formally closed under international law
- 3+ watch list indicators from different sections moving toward the same scenario within 7 days

---

## Known Confounding Factors

**Trump administration messaging volatility (persistent through 2026-05):** Frequent tariff, ceasefire-status, and deal-narrative reversals generate aggressive position unwinding that mimics structural fire-sale signatures. When logging asset moves, note whether the timing aligns with a specific policy statement or deal headline. Moves that reverse within 24–48 hours of a messaging shift are whiplash, not structural. Cross-reference new signals against prior entries to assess whether the pattern is sustained or episodic.

**Worked example (2026-05-23 → 2026-05-28):** Trump "largely negotiated" (May 23) → Brent rallies from $116 to $97 in 9 sessions, crossing the $105 de-escalation threshold on May 27 → Trump "not rushing into a deal" + Shamkhani publicly calls the MOU "fantasy" (May 27) → US strikes near Bandar Abbas Airport + IRGC retaliatory strike on US air base (May 28) → Brent reverts to $97.51, holding. The full sequence — narrative pump → threshold cross → kinetic reset — closed inside 5 calendar days. The May 27 Brent de-escalation print is the kind of signal that looks structural at the moment of logging but is whiplash in retrospect; the 2026-05-28 Synthesis Reviewer pass explicitly downweighted it. When a narrative-driven price move arrives, log it but flag the deal-headline correlation and check whether the move holds 48+ hours past the next reversal opportunity.

---

## Relevance Standard

Be conservative. A signal clears the bar if it clearly moves a specific named indicator in the watch list. General market commentary, opinion pieces, and background explainers do not qualify unless they contain primary data (price levels, government statements, official agency actions) that directly advances a watch list indicator.

Cross-cutting signals — events that move indicators across multiple sections simultaneously — are the highest priority.
