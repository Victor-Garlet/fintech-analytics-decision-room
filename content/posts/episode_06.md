# Episode 6: Evaluate speed against cost

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_06_speed_cost_tradeoff.png`

## Post copy

**30 Days Inside a European Fintech [6/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

The fastest route in the simulated corridor delivered 98.4% of transfers instantly.

The other routes delivered 82.7%.

On speed alone, the decision looks easy.

Then I added provider cost, support and contribution:

• priority-speed route cost: 21.43 bps  
• other-route cost: 8.67 bps  
• priority-route contribution proxy: 17.68 bps  
• other-route contribution proxy: 28.42 bps

The priority route bought 15.7 percentage points of instant delivery at a 12.76 bps cost premium.

There was another important signal. Its support-contact rate was 1.2%, compared with 4.8% on the other routes.

So a blanket move to the cheaper routes would be difficult to defend. It could improve unit economics while creating slower delivery and more customer contacts.

The comparison is also observational. Provider assignment was not random, so transfer type, customer promise or operational risk may influence both routing and outcomes.

My next step is a controlled test on eligible, non-urgent transfers. Contribution margin is the primary metric. Instant rate, delivery time, support contacts and reconciliation are guardrails.

Averages can identify a trade-off. They cannot tell us what would happen to the same transfer under another route. That is the point where analysis should become experiment design.

Quick glossary  
*Provider cost rate = provider cost divided by transfer volume, expressed in basis points.  
*Guardrail = a metric that must stay within an agreed limit while testing a change.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
