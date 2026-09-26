# Episode 5: Decompose take rate

**Status:** Scheduled for Tue, 13 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_05_take_rate_waterfall.png`

## Post copy

Only 0.57 of the 2.18 bps take-rate decline came from an approved decision to lower prices.

Another 1.67 bps came from an unexpected pricing configuration issue.

**30 Days Inside a European Fintech [5/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

After Episode 4's settlement-control hotspot, I returned to the original commercial question.

Collected take rate fell from 50.23 bps in H2 2025 to 48.05 bps in H1 2026.

If I stopped at the headline, Pricing could be asked to reverse lower customer prices even though most of the decline came from something else.

The bridge separated four effects:

• portfolio mix: +0.09 bps

• within-segment list yield: -0.02 bps

• approved price investment: -0.57 bps

• pricing configuration leakage: -1.67 bps

I compared two six-month windows, weighted by transfer volume, and used a symmetric shift-share decomposition at corridor and customer-segment grain.

That separates customers moving between segments from pricing changes within the same segment. I then applied approved price investment and the difference between expected and collected fees.

The displayed components are rounded. Using unrounded values, the bridge closes with a residual below 0.000001 bps.

The leakage was concentrated in C07 business customers. It affected 215 transfers and created $3,960.94 of simulated fee exposure, equal to 33.3% of the expected fees for that segment in H1.

That leads to two different decisions.

The approved price investment should remain visible and be evaluated against customer and growth outcomes. The configuration issue needs a control response: correct the rule, reconcile the affected records and compare expected with collected fees before daily close.

I would keep list, expected and collected take rate visible together. A single collected metric cannot show whether revenue moved because of strategy or because a control failed.

Before treating the $3,960.94 as recoverable revenue, I would still confirm the pricing terms and whether past charges can be corrected. The analysis quantifies the exposure. It does not decide recoverability.

Next, I will test whether faster transfers justify their higher provider cost once support contacts and contribution margin are included.

Quick glossary

*Take-rate bridge = a breakdown of the movements between two take-rate values.

*Portfolio mix = the effect of volume moving between customer segments or corridors with different prices.

*Fee leakage = the unexpected difference between the fee that should have been collected and the fee actually collected.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
