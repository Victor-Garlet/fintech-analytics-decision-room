# Episode 2: Build credible synthetic evidence

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_02_evidence_boundary.png`

## Post copy

**30 Days Inside a European Fintech [2/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

Using synthetic data creates a credibility problem of its own.

If the analyst already knows the answer and simply writes rows that prove it, the project becomes a decorated conclusion.

I used three evidence labels to avoid that:

1. Public fact

Official company disclosures can frame the business model and the question. They cannot validate a fictional transaction-level finding.

2. Project assumption

Definitions such as the instant-transfer threshold, cost allocation and reporting window are documented choices. Someone reviewing the work should be able to challenge them.

3. Synthetic result

The findings come from generated events and belong only to this case.

The prototype contains 10,000 transfer attempts across 20 corridors and 11 source tables. A fixed seed makes the output reproducible. Referential constraints keep customers, quotes, transfers, fees, settlements, providers and support contacts consistent.

I also kept the scenario configuration outside the public analytical layer while investigating. That prevented the dbt models from encoding the answer.

Synthetic data is useful here because it can create known failure modes, then test whether the analytical controls detect them without being told where to look.

For a public case study, the evidence boundary is part of the work. It should be visible before the first insight appears.

Quick glossary  
*Fixed seed = a setting that produces the same generated dataset on every run.  
*Referential integrity = records connect to valid related records, such as a transfer belonging to an existing customer.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
