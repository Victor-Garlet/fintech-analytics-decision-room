# Episode 1: Frame the decision

**Status:** Approved
**Visual:** `content/visuals/episode_01_metric_tree.png`

## Post copy

In my simulated fintech, collected take rate fell from 50.23 to 48.05 basis points.

Should Pricing reverse a discount, should Finance investigate a fee shortfall, or should nobody intervene yet?

The KPI alone cannot answer that.

**30 Days Inside a European Fintech [1/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

A 2.18 bps decline could come from very different places:

• customers moved towards lower-priced routes
• list-price yield changed within a segment
• the business deliberately invested in lower customer prices
• the amount collected fell below the approved price

Those explanations should not be treated as the same problem.

A portfolio shift may require no intervention. An approved price investment should be evaluated against customer and growth outcomes. An unexpected shortfall needs investigation and a control fix.

So I did not start with a dashboard.

I started with the decision the analysis needed to support:

How can a European payments fintech lower prices and improve transfer speed without losing control of unit economics?

From there, the work became more specific:

1. Define each metric before calculating it
2. Reconcile volume and fees to the same transfer population
3. Separate list, expected and collected fees
4. Explain the movement before recommending action
5. Connect the result to transfer speed and provider cost

The 2.18 bps decline is the starting signal. It is not the diagnosis.

Next, I'll build the metric contract behind this analysis. If Finance, Pricing and Operations mean different things by “take rate”, every conclusion after that becomes unstable.

Quick glossary

*Take rate = fee revenue as a proportion of transfer volume.  
*Basis point (bp) = 0.01 percentage point.
*Metric contract = an agreed definition covering the formula, filters, level of detail and ownership of a metric.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
