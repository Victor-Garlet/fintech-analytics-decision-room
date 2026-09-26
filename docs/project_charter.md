# Project Charter

## 30 Days Inside a European Fintech

**Project owner:** Victor Moraes Garlet
**Status:** Build complete, publication pending approval
**Version:** 1.1
**Date:** 26 September 2026
**Public language:** English
**Delivery window:** Four weeks, with eight LinkedIn episodes

## Project purpose

This project publicly simulates how a Senior Data Analyst could take a complex commercial and operational question inside a European payments fintech from initial signal to a defensible decision.

The goal is not to reproduce Wise's internal data or claim knowledge of its operations. Wise provides the public business context. All transaction-level data, analytical findings and recommendations are synthetic.

## Public business signal

Wise reported the following figures for Q1 FY2027:

- 11.863 million active customers.
- $69.3 billion in quarterly cross-border volume.
- $714.0 million in net revenue.
- A 0.50% cross-border take rate, down two basis points year over year.
- 77% of transfers completed instantly, up seven percentage points year over year.

Wise publicly explained that part of the lower take rate reflected deliberate investment in lower customer prices. This explanation will be treated as a public fact, not as a hypothesis to challenge.

Source: [Wise Q1 FY27 Trading Update](https://owners.wise.com/news-releases/news-release-details/wise-q1-fy27-trading-update)

## Fictional stakeholder request

> We are lowering prices and increasing transfer speed while volumes continue to grow. Finance and Operations need a reliable view that explains changes in take rate, separates intended price investment and customer mix from avoidable leakage, identifies material reconciliation exceptions and recommends where action is justified.

## Decision owners

- Head of Payments Operations.
- Finance Analytics Lead.
- Pricing or Product Manager.
- Provider Management Lead.

## Decisions the analysis must support

1. Which take-rate movements are expected strategic outcomes and which require investigation?
2. Which corridors, providers or process stages create material reconciliation risk?
3. Where does greater transfer speed justify greater provider cost?
4. Which operational fix or pricing experiment should be prioritised next quarter?

## Hypothesis register

The hypotheses are registered before the full dataset is analysed. A hypothesis is not a conclusion.

| ID | Starting hypothesis | Evidence required | Possible decision consequence |
| --- | --- | --- | --- |
| H1 | Deliberate price investment and customer mix explain most of the headline take-rate movement. | A weighted bridge separating price, mix and unexplained residual movement. | Protect intended price changes and investigate only the remaining unexplained movement. |
| H2 | Finance and Operations can report different totals without either calculation being technically wrong because they use different business events and timestamps. | A metric contract and reconciliation bridge across created, completed and settled events. | Use purpose-specific views connected by an agreed reconciliation rule. |
| H3 | A discount configuration creates avoidable fee leakage in a limited combination of corridor, customer segment and period. | Expected-versus-collected revenue at transfer grain, with configuration and eligibility checks. | Correct the rule, quantify exposure and add a preventive control. |
| H4 | A repeatable settlement exception pattern is concentrated around a provider or process stage rather than spread randomly. | Matched settlement records, tolerances, ageing and exception segmentation. | Prioritise the responsible process or provider instead of applying a broad operational fix. |
| H5 | Improving instant-transfer performance can increase provider cost enough to weaken unit economics in selected corridors. | Corridor and provider analysis combining speed, cost, support contacts and contribution margin proxy. | Apply corridor-specific routing or guardrails rather than maximising speed everywhere. |

## Evidence classification

Every important statement must be labelled internally as one of these three types:

| Type | Meaning | Example |
| --- | --- | --- |
| Public fact | A company-level statement supported by a published source. | Wise reported a 0.50% cross-border take rate in Q1 FY2027. |
| Project assumption | A modelling choice required to make the simulation coherent. | The analytical period contains twelve months of transfer activity. |
| Synthetic result | A finding produced only from the generated transaction-level data. | A specific simulated corridor contains concentrated fee leakage. |

Synthetic findings must never be described as findings about Wise.

## Core scope

- A deterministic synthetic dataset covering customers, quotes, transfers, pricing, fees, FX, settlements, providers, refunds, support contacts and experiments.
- A documented metric contract.
- Staging, intermediate, dimensional, fact and analytical mart layers.
- Data quality tests and reconciliation controls.
- Take-rate decomposition and unit-economics analysis.
- One prioritised experiment or operational intervention.
- A decision-facing web report, designed as the public BI experience, and one-page executive memo.
- Eight LinkedIn episodes and eight supporting visuals.
- A reproducible public repository with limitations and assumptions.

## Deliberate exclusions

- Real Wise customer or internal company data.
- Claims about Wise's internal systems, employees or causes.
- Production fraud detection.
- Predictive machine learning.
- Real-time streaming.
- Airflow orchestration.
- A full application or an unnecessarily large engineering platform.

These exclusions protect the four-week scope and keep the project focused on Senior Data Analyst judgement rather than technical theatre.

## Definition of success

The project is successful when:

- the full analytical path can be reproduced from data generation to final metrics;
- every published number is traceable to a model, definition and source type;
- the key tests pass and intentionally seeded issues are detectable;
- recommendations show expected impact, confidence, effort and relevant guardrails;
- limitations and evidence that could change the recommendation are explicit;
- a non-technical reader can understand the decision without reading the code;
- a technical reader can inspect enough evidence to challenge the method;
- the series creates qualified conversations with analytics, finance, product, operations or recruitment professionals.

Likes and impressions are useful distribution signals, but they are not the primary measure of project quality.

## Public investigation format

The series title remains **30 Days Inside a European Fintech**. Each episode will use a recurring visual label:

**Decision Room | Case 01/08**

Each case should make five elements visible:

1. **Decision at risk:** the decision affected by the problem.
2. **New evidence:** the information added in this episode.
3. **Analytical move:** the method used and why it was appropriate.
4. **Current recommendation:** what should happen based on the evidence available now.
5. **What could change my mind:** the missing evidence or limitation that could change the conclusion.

This format allows each post to stand alone while the complete series still feels like one investigation.

## Technical communication rule

Technical explanations should move through three layers:

1. Everyday meaning.
2. Business consequence.
3. Technical evidence.

When a post depends on specialist language, add a short **Quick glossary** immediately before the mandatory disclosure.

Rules for the glossary:

- Include only one to three terms used in that episode.
- Define each term in one plain-English sentence.
- Explain the meaning in the context of the analysis, not as a textbook definition.
- Repeat a definition in a later episode when it is necessary for that post to stand alone.
- Do not add a glossary when the post is already understandable without it.

Example:

> **Quick glossary**
> **Take rate:** the revenue earned as a percentage of the total transfer volume.
> **Basis point:** one hundredth of a percentage point; 2 basis points equals 0.02 percentage points.

The disclosure remains the final, visually separate block of every post.

## Integrity rules

- Never imply employment, affiliation, endorsement or internal access to Wise.
- Never mix public company figures with synthetic findings without labelling the difference.
- Never publish a result that cannot be reproduced.
- Never choose an analytical conclusion before inspecting the evidence.
- Never add a tool solely to make the stack appear more advanced.
- Never publish a post without Victor's approval.

## Approval gates

1. **Charter approved:** the decision, scope, hypotheses and integrity boundary are clear.
2. **Source register approved:** every public fact has a source, date and permitted use.
3. **Prototype approved:** a 10,000-transfer dataset proves that the grains, relationships and scenarios work.
4. **Metric layer approved:** definitions, timestamps, tolerances and tests are documented.
5. **Analysis approved:** every finding is reproducible and has an honest limitation.
6. **Publication approved:** the post, visual, glossary and disclosure are reviewed together.

## Milestone status and next build task

The foundation milestone was completed on 24 September 2026:

- the source register records six official sources and their permitted use;
- the data dictionary defines eleven prototype tables and their grains;
- the first metric contract separates completion, settlement and pricing time rules;
- the deterministic generator produces exactly 10,000 transfers across 20 corridors;
- all structural, accounting and scenario-detectability checks pass;
- repeated generation with the same configuration produces identical file hashes.

The local metric-layer milestone was completed on 24 September 2026:

- eleven raw sources load reproducibly into DuckDB;
- thirteen staging and intermediate views preserve source and decision grains;
- ten decision-facing marts cover executive KPIs, transfer economics, reconciliation, take-rate movement, leakage and routing trade-offs;
- 168 automated data tests validate keys, relationships, allowed states, accounting equations, event timing, mart reconciliation and scenario bounds;
- the complete dbt build passes 191 of 191 models and tests;
- dbt documentation and lineage artifacts generate successfully;
- a private portfolio-site draft explains the decision, evidence boundary and architecture without revealing unreleased findings.

The diagnostic and decision milestone was completed on 26 September 2026:

- completion-month and settlement-month views reconcile with zero material residual;
- the take-rate bridge separates mix, within-cell yield, approved investment and unintended leakage;
- route-level settlement and pricing-control hotspots are traceable to transfer-grain records;
- the routing opportunity is expressed as a bounded scenario and controlled experiment;
- the executive memo, interview explanations, eight post drafts and eight visuals are prepared;
- the portfolio site presents the final decision and analytical evidence.

Publication and public deployment remain behind Victor's approval gate.
