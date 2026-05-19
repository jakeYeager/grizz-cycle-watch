# Grizz Cycle Watch — Agent Brief

Compact orientation for Monitor and Synthesis agents. Read this first, then the files listed under Context.

---

## Project Purpose

Research wiki tracking how regulation/deregulation cycles propagate through news events and market behavior. Four analytical frameworks produce a watch list of late-stage indicators. Signals are logged; accumulated signals trigger escalation to analysis reports.

---

## Current Cycle Position

As of 2026-04-14:

| Framework | Phase | Status |
|---|---|---|
| Regulatory Cycle (20–30yr) | Phase 4 / 5 boundary | DOL 401(k) safe harbor rule triggered; retail capital channel into private credit opened; judicial resistance active (CFPB courts, Anderson v. Intel Corp.) |
| Kindleberger Mania | **Stage 4 confirmed** | Both escalation-tree trigger conditions met: Goldman prime brokerage equity exit (7.6:1 short-to-long) + five-platform simultaneous private credit gates |
| Minsky Debt | **Phase 3 deepening** | $20.8bn Q1 withdrawal requests across five platforms; Fitch 5.8% default rate confirms zombie refinancing failures |
| Hormuz / Armed Conflict | Active — Scenarios B/C/D | Scenario B 43%, C 32%, D 15%; China escalation column fully met; India as near-term Scenario D actor; April 21 ceasefire expiry is next hard binary |

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

### Market Behavior
- `hedge fund short interest 2026` / `Goldman prime brokerage flows`
- `institutional equity positioning April 2026` / `hedge fund drawdown 2026`
- `margin calls 2026` / `forced selling equities`
- `private equity NAV markdown` / `redemption gate 2026`
- `private credit default rate Fitch Moody 2026`
- `Dimon JPMorgan private credit 2026` / `Apollo Carlyle Ares gate 2026`
- `crypto sell-off risk-off 2026`

### Global Debt
- `10-year Treasury yield 2026` / `Treasury yield 5 percent`
- `Japan JGB yield 2026` / `BOJ rate hike normalization`
- `BIS credit-to-GDP warning` / `BIS quarterly review 2026`
- `shadow banking stress 2026` / `money market fund`
- `repo market disruption 2026`
- `derivatives counterparty failure` / `systemic risk bank 2026`
- `G7 sovereign debt rating` / `sovereign credit downgrade 2026`
- `India GDP energy shock 2026` / `India current account deficit Hormuz`

### Armed Conflict
- `Strait of Hormuz tanker 2026` / `AIS Hormuz transits`
- `US Iran ceasefire talks 2026` / `Iran nuclear talks second round`
- `US Iran ceasefire April 21` / `Iran ceasefire expiry`
- `IRGC drone Hormuz 2026` / `IRGC naval incident`
- `China Hormuz transit 2026` / `PLA fleet Hormuz`
- `India Hormuz bilateral deal` / `India Iran oil transit 2026`
- `India LPG shortage 2026` / `India energy crisis fuel`
- `Houthi Bab al-Mandab 2026`
- `Brent crude Iran war 2026`
- `EU aviation fuel shortage 2026` / `European jet fuel`
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

**Trump administration messaging volatility (active as of 2026-04-11):** Frequent tariff announcements, reversals, and trade war escalation/de-escalation cycles are generating aggressive position unwinding that mimics structural fire-sale signatures. When logging gold/oil correlation moves or broad asset sell-offs, note whether the timing aligns with a specific policy statement or trade headline. Moves that reverse within 24–48 hours of a messaging shift are likely whiplash, not structural. As log history accumulates, cross-reference new correlation signals against prior entries to assess whether the pattern is sustained or episodic.

---

## Relevance Standard

Be conservative. A signal clears the bar if it clearly moves a specific named indicator in the watch list. General market commentary, opinion pieces, and background explainers do not qualify unless they contain primary data (price levels, government statements, official agency actions) that directly advances a watch list indicator.

Cross-cutting signals — events that move indicators across multiple sections simultaneously — are the highest priority.
