# Episode 8: Make the decision defensible

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_08_executive_decision.png`

## Post copy

**30 Days Inside a European Fintech [8/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

The final deliverable is one decision page.

The recommendation:

Protect unit economics without masking intentional price investment.

Three actions sit underneath it.

1. Correct the pricing leakage

One corridor and business segment produced $3,960.94 of simulated lost fees. Fix the configuration, reconcile affected records and test expected against collected fee before daily close.

2. Repair the settlement control

One corridor-provider pair reached a 39.7% exception rate. Give the route an owner and track amount mismatch, lateness, missing settlement and unresolved ageing separately.

3. Test a limited routing change

The priority-speed route is materially faster and more expensive. A 25% reroute scenario improves the contribution proxy by $265.44, with estimated trade-offs of -2.77 pp in instant rate and +0.64 pp in support contacts.

I would not ship that routing policy from descriptive data. I would run the controlled experiment described in the previous post and require all guardrails to clear before scaling.

The technical project behind this page includes deterministic Python generation, DuckDB, 23 dbt models, 168 automated tests, reconciliation controls, decision marts and eight reproducible visuals.

The biggest lesson from the series is that analysis becomes useful when every number has a definition, every finding has a confidence level and every recommendation says what happens next.

Quick glossary  
*Contribution margin proxy = collected fee minus provider and estimated support costs in this simulation.  
*Decision guardrail = a limit that protects customer or operational outcomes while pursuing the primary goal.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
