# Episode 8: Make the decision defensible

**Status:** Scheduled for Fri, 23 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_08_executive_decision.png`
**Alt text:** Black-and-white hand-drawn executive decision page for the final episode of a synthetic European fintech case. The decision is to protect unit economics without reversing intentional price investment. Action 1 fixes C07 pricing after 215 transfers created $3,960.94 of synthetic exposure, owned by Pricing and Finance with zero new shortfalls as the success measure. Action 2 controls C13/P04 settlement after a 39.7% exception rate versus 4.2% elsewhere, owned by Payments Operations and Provider Management. Action 3 tests C01 routing with a 25% treatment and an estimated $265 contribution uplift, owned by Product and Finance and scaled only if every guardrail holds. The unresolved boundaries are recovery amount, provider cause and production impact.

## Post copy

Eight episodes produced dozens of metrics.

The final page keeps three decisions.

**30 Days Inside a European Fintech [8/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

My recommendation is to protect unit economics without reversing intentional price investment.

1. Correct the C07 pricing configuration

Owner: Pricing Analytics and Finance.

The issue affected 215 business transfers and created $3,960.94 of synthetic exposure.

Correct the rule, review affected records and compare expected with collected fee before daily close.

Success means zero new unexpected shortfalls and a resolution status for every affected record.

2. Repair the C13/P04 settlement control

Owner: Payments Operations and Provider Management.

The route reached a 39.7% exception rate, compared with 4.2% elsewhere.

Keep missing, late and mismatched settlements separate, assign an owner and track unresolved ageing.

Success means returning the route within the agreed control band without growing the backlog.

3. Authorise a controlled C01 routing experiment

Owner: Payments Product and Finance Analytics.

A 25% planning scenario estimates $315.28 lower provider cost and $265.44 higher contribution margin proxy.

It also estimates a 2.77 percentage-point decline in instant delivery and a 0.64 percentage-point increase in support contacts.

I would scale only if contribution improved and the speed, support and reconciliation guardrails remained within limits agreed before the test.

The evidence still has boundaries.

The exposure is not automatically recoverable. The settlement concentration does not prove the provider caused it. The routing scenario sizes an opportunity; it does not forecast the result of changing production traffic.

The project uses 23 dbt models and 168 automated tests to keep each headline number connected to its definition, source records and business rules.

I started with one take-rate decline.

The analysis separated it into approved price investment, unexpected fee leakage, a settlement-control failure and a routing hypothesis worth testing.

That changed the response to each finding.

The final logic is simple: fix what is directly observed, control what is concentrated, test what remains uncertain and monitor what is too small to justify intervention.

That is the standard I wanted this project to meet: enough evidence to decide, and enough honesty to say what could still change it.

Quick glossary

*Contribution margin proxy = collected fee minus provider cost and estimated support cost in this simulation.

*Guardrail = a metric that must stay within an agreed limit while a test is running.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
