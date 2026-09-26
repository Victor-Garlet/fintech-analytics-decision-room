# Episode 7: Turn findings into actions

**Status:** Scheduled for Tue, 20 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_07_decision_matrix.png`

## Post copy

I finished the analysis with four findings.

Only one was ready for an immediate fix.

**30 Days Inside a European Fintech [7/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

After six episodes, the work needed a decision order, not another chart.

I placed each finding on a matrix using decision confidence and implementation effort.

That produced four actions.

ACT NOW

Correct the C07 business pricing configuration and add an expected-versus-collected fee check before daily close.

The issue affected 215 transfers and created $3,960.94 of synthetic exposure. The records make it traceable, but recovery still depends on the commercial terms and a record-level review.

CONTROL NOW

Assign an owner to the C13/P04 settlement route and track amount mismatches, late settlements and missing settlements separately.

Its exception rate reached 39.7%, compared with 4.2% elsewhere. Stronger controls are justified. Blaming the provider is not, because the root cause is still unproven.

TEST BEFORE SCALING

Run a controlled C01 routing experiment on eligible, non-urgent transfers.

A 25% planning scenario estimates $315.28 lower provider cost and $265.44 higher contribution margin proxy. It also estimates a 2.77 percentage-point decline in instant delivery and a 0.64 percentage-point increase in support contacts.

Those numbers size the decision. They do not predict the result.

Contribution per unit of volume would be the primary metric, with speed, support and reconciliation as guardrails. I would scale only if contribution improved and every guardrail held.

MONITOR

Keep portfolio mix visible, but do not open another project for a +0.09 bps movement unless it persists or hides a segment-level change.

The matrix matched each finding to an action the evidence could support.

A directly observed configuration failure can justify a fix. An observational comparison can justify an experiment. It cannot justify moving production traffic on its own.

The same analytical pack can contain a defect, a control risk, a hypothesis and a movement that only needs monitoring. Sending all four out as recommendations would create false certainty.

Next, I will turn this work into a one-page leadership recommendation with the decision, owners, controls, experiment and unresolved risks.

Quick glossary

*Planning scenario = an estimate used to size a decision, not a causal prediction.

*Contribution margin proxy = collected fee minus provider cost and estimated support cost in this simulation.

*Guardrail = a metric that must stay within an agreed limit while a test is running.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
