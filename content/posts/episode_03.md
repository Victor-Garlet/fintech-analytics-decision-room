# Episode 3: Reconcile the event clocks

**Status:** Scheduled for Tue, 6 Oct 2026 at 08:00 Europe/Dublin
**Visual:** `content/visuals/episode_03_two_reporting_clocks.png`

## Post copy

Finance reported $4.366m for March. Operations reported $4.513m.

Neither team had made a mistake.

**30 Days Inside a European Fintech [3/8]**

I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision.

In Episode 2, I locked the metric boundaries before investigating the 2.18 bps take-rate decline. The next check was whether Finance and Operations were even looking at the same month. They were not.

Operations grouped expected settlements by completed_at, when the customer journey finished. Finance grouped actual cash movement by settled_at, when funds settled.

That created a $146.9k apparent gap. Treating it as leakage or loss would have sent the investigation in the wrong direction.

I built a reconciliation bridge at transfer grain:

• Operations completion cohort: $4,513,032.54

• Less March completions settled outside March: $280,485.85

• Add earlier completions settled during March: $134,097.00

• Less same-month settlement variance: $474.07

• Finance settlement view: $4,366,169.62

• Unexplained residual: $0.00

Once timing was separated from value movement, the disagreement disappeared.

The decision was not to force both teams onto one clock.

Operations needs completion month to understand product and customer experience. Finance needs settlement month for cash movement and financial control. Replacing either view would make one team's analysis less useful.

So the model keeps both timestamps, exposes carry-in and carry-out items, and tests every reporting month to a one-cent tolerance.

That changes the conversation from “whose number is right?” to “which event does this decision need?”

At this stage, I would not classify the March difference as a financial loss or change pricing because of it. I would publish both views with the bridge, assign joint ownership to Finance Analytics and Payments Operations, and investigate only the residual or exceptions that remain after timing is reconciled.

Timing explained this gap. But it did not explain every settlement exception. One corridor-provider pair still looked very different from the rest. That is next.

Quick glossary

*Event clock = the business timestamp used to assign a record to a reporting period.

*Carry-in / carry-out = activity entering or leaving the month because completion and settlement happened in different periods.

*Reconciliation bridge = a calculation that explains how one valid total moves to another.

Disclosure: This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports.
