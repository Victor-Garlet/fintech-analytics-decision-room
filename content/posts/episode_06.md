# Episode 6: Evaluate speed against cost

**Status:** Scheduled for Fri, 16 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_06_speed_cost_tradeoff.png`

## Post copy

The fastest route delivered 98.4% of transfers instantly.

It also cost 2.5 times more per unit of volume.

Would I move all traffic to the cheaper route? No.

**30 Days Inside a European Fintech [6/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

After separating price investment from fee leakage, I returned to the original question: can faster transfers justify their cost?

In C01 during H1 2026, I compared 250 completed transfers through the priority-speed provider with 104 through the other providers.

The priority route delivered:

• 98.4% instant transfers

• 21.43 bps provider cost

• 1.2% support-contact rate

• 17.68 bps contribution margin proxy

The other routes delivered:

• 82.7% instant transfers

• 8.67 bps provider cost

• 4.8% support-contact rate

• 28.42 bps contribution margin proxy

The priority route bought 15.7 percentage points of additional instant delivery.

It also added 12.76 bps in provider cost and finished 10.75 bps lower on contribution.

That does not make the expensive route a bad decision. It was faster and coincided with fewer customer contacts.

A blanket move to the cheaper routes could improve unit economics while slowing transfers and creating more work for Support.

But I would not turn this comparison into a routing policy yet.

Provider assignment was not random. Urgency, customer promise, payment method or operational risk could influence both the route selected and the result.

Only eight transfers had a support contact, so that difference is a signal, not a conclusion.

My next step would be a controlled test on eligible, non-urgent transfers, randomised within comparable groups.

Contribution per unit of volume would be the primary metric. Instant rate, delivery time, support contacts and reconciliation exceptions would be guardrails agreed before the test.

I would start with a limited share of traffic and stop or narrow the treatment if a guardrail crossed its threshold.

This analysis shows that the trade-off is worth testing. It does not show what would happen to the same transfer under another route.

That is the line between a useful comparison and an unsupported recommendation.

Next, I will combine the pricing, settlement and routing findings to decide what should be fixed now, controlled operationally or tested before scaling.

Quick glossary

*Basis point (bps) = 0.01 percentage point.

*Contribution margin proxy = collected fee minus provider cost and estimated support cost in this simulation.

*Guardrail = a metric that must stay within an agreed limit while a test is running.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
