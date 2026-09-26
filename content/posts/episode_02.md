# Episode 2: Lock the evidence and metric boundaries

**Status:** Scheduled for Fri, 2 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_02_evidence_boundary.png`

## Post copy

I deliberately hid the planted failure from my own analytical models.

Otherwise, a synthetic case study can become a decorated conclusion: generate the rows, find exactly what you put there, and call it an insight.

**30 Days Inside a European Fintech [2/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

Before investigating a 2.18 bps decline in collected take rate, I put two controls in place.

First, every material statement gets one of three evidence labels:

• Public fact: official disclosures can frame the business question, but they cannot validate fictional customer behaviour.

• Project assumption: thresholds, cost allocations and reporting windows are documented choices that a reviewer can challenge.

• Synthetic result: findings generated inside this dataset belong only to this case.

Second, I wrote a metric contract for collected take rate:

• Formula: collected fee revenue divided by completed transfer volume

• Population: completed transfers only

• Time rule: the month in which the transfer completed

• Grain: one transfer

• Owner: Finance Analytics in the fictional operating model

• Validation: numerator and denominator must reconcile to the same transfer cohort

The formula is simple. The boundaries are what allow Finance, Pricing and Operations to reproduce the number and disagree for a visible reason.

The prototype then generates exactly 10,000 transfer attempts across 20 corridors and 11 related tables. The same configuration produces the same dataset on every run.

If a fee loses its transfer, a settlement loses its provider, or the fee equation no longer closes, the build fails.

The planted scenario configuration also stays outside the analytical layer. The dbt models can see the transactions, but not the answer key.

The result remains synthetic. The process becomes inspectable and reproducible.

At this point, I would leave pricing unchanged until the transfer population and reporting clock reconcile across Finance and Operations. That is the next test.

Quick glossary

*Collected take rate = collected fee revenue as a proportion of completed transfer volume.

*Metric contract = the agreed formula, population, time rule, grain, owner and validation for a metric.

*Fixed seed = a setting that produces the same generated dataset on every run.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
