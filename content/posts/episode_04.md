# Episode 4: Isolate the reconciliation hotspot

**Status:** Scheduled for Fri, 9 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_04_reconciliation_hotspot.png`

## Post copy

One corridor-provider pair represented 5.2% of completed transfers and 34.2% of all settlement exceptions.

**30 Days Inside a European Fintech [4/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

In Episode 3, a $146.9k difference between Finance and Operations disappeared once I reconciled their event clocks. The remaining exceptions did not disappear with it.

The next question was whether those exceptions were spread across the operation or concentrated somewhere that a team could act on.

From March to May, the C13/P04 route recorded 52 exceptions across 131 completed transfers.

Its exception rate was 39.7%, around 9.6 times the 4.2% across every other route.

The hotspot contained:

• 24 amount mismatches

• 15 late settlements

• 13 missing settlements

That concentration changes the response, but it does not yet prove that the provider caused the problem.

The pattern could come from provider handling, a corridor configuration or a file-processing control. Removing P04 immediately would turn an observational result into a causal claim.

I built the exception mart at transfer grain and aggregated only for the decision view. Each headline number remains traceable to a transfer ID, expected and actual settlement, amount variance, exception status and event timestamps.

My immediate recommendation would be a route-specific investigation queue:

• assign one owner to the C13/P04 control

• keep missing, late and mismatched settlements separate

• monitor unresolved ageing, not only the daily count

• reconcile amount mismatches to their financial exposure

This gives Payments Operations something they can clear while preserving the evidence needed for a provider or process decision.

If the concentration remains after the control is fixed, the case for a provider escalation becomes stronger. Until then, I would target the workflow rather than blame the whole portfolio.

Next, I will return to the 2.18 bps take-rate decline and separate intentional lower pricing from unexpected leakage.

Quick glossary

*Reconciliation exception = a settlement that is missing, late or different from the expected amount.

*Ageing = how long an exception remains unresolved.

*Reason code = a standard label describing why an exception occurred.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
