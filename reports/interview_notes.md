# Interview explanation guide

## Two-minute version

I built a synthetic European fintech decision case around a realistic trade-off: lower customer prices and faster transfers can both weaken unit economics if the business cannot distinguish intentional investment from leakage or expensive routing.

I generated deterministic transaction data, modelled it in DuckDB and dbt, defined the metrics before analysis, and added tests for keys, fee equations, settlement coverage and mart reconciliation.

The main finding was that a 2.18 bps take-rate decline was not one problem. Approved price investment explained 0.57 bps, while a concentrated pricing configuration issue explained 1.67 bps and $3,960.94 of simulated leakage. I also found a route-level reconciliation hotspot and a speed-cost trade-off where the fastest provider cost 12.76 bps more.

My recommendation was to fix the observed control failures first, then test a limited routing change with customer and operational guardrails. The project ends with an executive memo, an experiment design and a reproducible analytical layer.

## Five-minute version

Start with the business question and why a single KPI is insufficient. Explain the evidence boundary: Wise provides public context, while every transaction and finding is synthetic.

Then cover the analytical sequence:

1. Defined grains, event timestamps and metric contracts.
2. Built staging and unit-economics models.
3. Reconciled the Operations completion cohort to the Finance settlement period.
4. Decomposed take-rate movement with a weighted shift-share method.
5. Isolated leakage by corridor and segment.
6. Compared speed, cost, support and contribution by route.
7. Converted high-confidence findings into controls and the lower-confidence opportunity into an experiment.

Use three numbers to anchor the story:

- 2.18 bps collected take-rate decline.
- 1.67 bps from unexpected leakage.
- 39.7% exception rate in one corridor-provider pair.

Close with the judgement call: I did not recommend a blanket reroute even though it appeared cheaper, because the comparison was observational and the faster route also had a lower support-contact rate.

## Fifteen-minute deep dive

### Problem framing

- Decision owner: pricing, operations and finance leadership.
- Decision: what to fix immediately and what to test.
- Risk: treating every margin movement as the same economic event.

### Data model

- Transfer grain for customer experience and unit economics.
- Settlement grain for the Finance event clock.
- Expected, collected and leaked fee fields kept separate.
- Provider cost and support cost joined at transfer grain.

### Controls

- Deterministic generation and committed prototype snapshot.
- Source, staging, intermediate and mart layers.
- Tests for uniqueness, relationships, accepted values and equations.
- Singular tests for the reporting bridge and take-rate decomposition.

### Analysis

- Operations-to-Finance bridge closes to a $0.01 tolerance.
- Symmetric shift-share decomposition separates portfolio mix from within-cell list yield.
- Approved investment and leakage are direct fee adjustments, not inferred residuals.
- Route comparison covers speed, provider cost, support and contribution.

### Recommendation

- Fix the C07 pricing configuration.
- Repair the C13/P04 settlement control.
- Test a 25% C01 routing treatment with pre-agreed guardrails.

### Limitations

- Synthetic data cannot support claims about Wise.
- Contribution margin is incomplete by design.
- Provider assignment is observational.
- Scenario output is not causal impact.

## Likely follow-up questions

**Why DuckDB?**

It keeps the public project easy to run locally while preserving SQL and modelling practices that transfer to a cloud warehouse.

**Why dbt instead of doing everything in Python?**

The core work is relational transformation, metric definition and reconciliation. dbt makes lineage, tests and business logic reviewable. Python is used where it adds value: deterministic generation and visual output.

**Why not recommend the cheapest provider?**

The fastest route also had fewer support contacts, and provider assignment was not random. A controlled test is the defensible way to estimate the causal trade-off.

**What would you change with real company data?**

I would add contractual provider SLAs, loss and fraud costs, customer promise type, incident logs, experiment assignment and a complete margin definition agreed with Finance.
