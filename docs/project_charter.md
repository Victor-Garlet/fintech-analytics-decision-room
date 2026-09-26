# Case brief

## The setting

Wise's public [Q1 FY27 update](https://owners.wise.com/news-releases/news-release-details/wise-q1-fy27-trading-update) reported a lower cross-border take rate and more instant transfers. Those company-level facts supply a realistic question for this case; they are **not** inputs to the fictional transaction dataset and do not establish what happened inside Wise.

I modelled an independent European payments fintech with generated customers, quotes, transfers, fees, provider costs and settlements. The case is complete as a local analytical build. Every transaction-level finding and recommendation is synthetic.

## The question

> How can a payments fintech lower prices and improve transfer speed while keeping a reliable view of unit economics, pricing controls and settlement risk?

The working decision is narrower than “raise take rate”: identify which part of a decline reflects an approved customer investment, which part is an avoidable fault, and where a routing change is worth testing.

## Who would use the answer

In this fictional operating model, Finance Analytics needs a reconciled fee and settlement view. Payments Operations needs exception ownership. Pricing and Product need to protect intended price changes. Provider Management needs to weigh speed against cost and customer friction.

## Questions I tested

| Question | Evidence needed | Decision it informs |
| --- | --- | --- |
| Is the take-rate movement intentional, mix-driven or unexpected? | A volume-weighted bridge from list price to collected fee, with approved investment and leakage separated. | Preserve intended price reductions and fix the unexpected shortfall. |
| Why can Finance and Operations report different monthly totals? | Completion and settlement timestamps, with a month-by-month bridge. | Use purpose-specific measures connected by an explicit contract. |
| Where are settlement exceptions concentrated? | Record-level settlement states, route, provider, reason and ageing. | Assign a targeted control owner. |
| Does a faster provider route justify its cost? | Speed, provider cost, support and contribution at a comparable grain. | Design a controlled experiment before changing routing. |

These were starting hypotheses, not predetermined conclusions. The [decision log](decision_log.md) records the choices made as the case developed.

## What I built

1. A deterministic [10,000-transfer synthetic snapshot](../data/prototype) with the complete [scenario configuration](../config/scenarios.yml).
2. A [data dictionary](data_dictionary.md) and [metric contract](metric_contract.md) defining grains, event clocks, formulas and tolerances.
3. A local DuckDB warehouse with [dbt staging, intermediate and mart models](../dbt_fintech/models).
4. Tests for keys, relationships, pricing equations, settlement coverage, timing, reconciliation and decision-mart grain.
5. A [diagnostic analysis](../reports/diagnostic_analysis.md), [executive decision memo](../reports/executive_memo.md) and [routing experiment design](../reports/experiment_design.md).
6. A [static case presentation](../site) that shows the decision visually; the linked reports and code carry the underlying evidence.

## Evidence boundary

| Type | What it can support |
| --- | --- |
| Public fact | Company context with a dated, official source in the [source register](source_register.md). |
| Project assumption | A disclosed rule needed to make the simulation coherent, listed in [assumptions](assumptions.md). |
| Synthetic result | A finding reproducible from this repository's generated records and SQL. |

I have not worked for Wise on this case and have no access to its customer, provider or internal operating data. The provider names and economic terms are fictional. A result from this simulation must never be described as a finding about Wise.

## Scope and limits

The case focuses on fee economics, transfer speed, reconciliation and a bounded routing decision. It does not model production fraud, live FX exposure, full profitability, all revenue lines or randomised provider outcomes. Contribution margin is a proxy, and the route comparison is observational.

The work is complete when a reader can reproduce the snapshot and analytical build, trace each reported number to a definition and model, see the relevant checks, understand the recommendation without SQL, and identify what evidence would change it.
