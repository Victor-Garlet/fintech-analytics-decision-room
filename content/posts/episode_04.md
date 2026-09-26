# Episode 4: Isolate the reconciliation hotspot

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_04_reconciliation_hotspot.png`

## Post copy

**30 Days Inside a European Fintech [4/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

The monthly reconciliation rate was getting worse, but the portfolio average hid the operational cause.

From March to May, one corridor-provider pair recorded 52 exceptions across 131 completed transfers.

Its exception rate was 39.7%.

Across every other route, the rate was 4.2%.

The hotspot contained:

• 24 amount mismatches  
• 15 late settlements  
• 13 missing settlements

That pattern changes the response.

A portfolio-wide alert would create noise for teams that cannot act on the issue. A route-level queue can carry the provider, corridor, reason code, owner, financial variance and ageing needed to investigate it.

I built the exception mart at transfer grain, then aggregated only for the decision view. That keeps the headline rate traceable to each settlement record.

The recommended control is route-specific:

• assign an owner to C13/P04  
• separate missing, late and mismatched settlements  
• monitor unresolved ageing, not only the daily count  
• reconcile amount mismatches to their financial exposure

The lesson for me was that a rising exception rate is still only a symptom. The useful analysis identifies where the workflow broke and gives Operations a queue they can actually clear.

Quick glossary  
*Reconciliation exception = a settlement that is missing, late or different from the expected amount.  
*Ageing = how long an exception remains unresolved.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
