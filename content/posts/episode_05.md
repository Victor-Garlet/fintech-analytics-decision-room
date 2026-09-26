# Episode 5: Decompose take rate

**Status:** Draft for approval  
**Visual:** `content/visuals/episode_05_take_rate_waterfall.png`

## Post copy

**30 Days Inside a European Fintech [5/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

The collected take rate fell from 50.23 bps to 48.05 bps.

The 2.18 bps decline was not one commercial event.

I decomposed the movement between H2 2025 and H1 2026:

• portfolio mix: +0.09 bps  
• within-segment list yield: -0.02 bps  
• approved price investment: -0.57 bps  
• pricing configuration leakage: -1.67 bps

The bridge reconciles back to the reported take rate with a residual below 0.000001 bps.

The actionable finding was concentrated in one corridor and one business segment. It affected 215 transfers and created $3,960.94 of simulated fee leakage.

This matters because the approved price investment and the leakage both reduce collected revenue. If the scorecard combines them, a pricing team may be asked to reverse a deliberate customer decision while the control failure continues.

I would keep three measures visible together:

• list take rate  
• expected take rate after approved investment  
• collected take rate after unexpected shortfall

The recommended action is to correct the pricing configuration, identify the affected records and test expected versus collected fee before daily close.

The decomposition separated a strategic choice from an avoidable loss and assigned the right action to each.

Quick glossary  
*List yield = fee expected from the published pricing rule before approved discounts.  
*Fee leakage = the unexpected difference between expected and collected fee.

This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
