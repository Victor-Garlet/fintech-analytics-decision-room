# Episode 7: Turn findings into actions

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_07_decision_matrix.png`

## Post copy

**30 Days Inside a European Fintech [7/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

At this point, I had three findings with different levels of confidence.

Treating them as one recommendation would have been a mistake.

The decision matrix separated them by confidence and implementation effort.

Act now:

Fix the C07 business pricing configuration. The $3,960.94 leakage is directly observed in the fee records, concentrated and traceable.

Plan and control:

Repair the C13/P04 settlement workflow. A 39.7% exception rate and clear reason codes provide enough evidence to assign an owner and introduce ageing controls.

Test before scaling:

Run a controlled C01 routing experiment. A 25% planning scenario estimates $315.28 lower provider cost and $265.44 higher contribution proxy. It also estimates a 2.77 pp decline in instant rate and a 0.64 pp increase in support-contact rate.

Those scenario numbers are not a forecast. They use observed route averages and help size the decision.

For the experiment, I would use contribution per unit of volume as the primary metric, then stop or narrow the treatment if speed, support or reconciliation breaches a pre-agreed guardrail.

This is where I think senior analytical work becomes visible: the output is not another insight. It is a clear distinction between what the business should fix, what it should monitor and what it still needs to learn.

Quick glossary  
*Planning scenario = an estimate used to size a decision, not a causal prediction.  
*Treatment = the group exposed to the proposed change in an experiment.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
