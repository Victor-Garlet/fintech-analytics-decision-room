# Episode 3: Reconcile the event clocks

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_03_two_reporting_clocks.png`

## Post copy

**30 Days Inside a European Fintech [3/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

Finance and Operations reported different March totals.

Both numbers were correct.

Operations grouped transfers by completion date. That produced $4.513m of expected settlements for the March completion cohort.

Finance grouped cash movement by settlement date. That produced $4.366m settled in March.

The gap came from event timing:

• $280.5k of March completions settled outside March  
• $134.1k of earlier completions settled during March  
• same-month settlement variance contributed another -$474

After those items, the bridge closed to $0.00.

This is why a metric contract needs more than a formula. It needs the event timestamp, grain, owner, allowed lag and reconciliation rule.

I kept both views in the model:

• completion month for product and customer-experience analysis  
• settlement month for cash and financial control

Forcing one team to adopt the other's clock would make one use case worse. The analytical job is to make the two views reconcilable and prevent them from being compared without context.

The model now carries opening and closing timing items explicitly and tests every month to a one-cent tolerance.

When two teams disagree on a metric, I now check the event clock before checking the arithmetic.

Quick glossary  
*Grain = what one row represents.  
*Completion cohort = transfers grouped by when the customer journey completed.  
*Settlement period = transfers grouped by when funds settled.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
