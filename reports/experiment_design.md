# C01 routing experiment

## Decision to inform

Can a defined group of non-urgent C01 transfers move away from the priority-speed route while improving contribution margin within customer-experience guardrails?

## Hypothesis

Rerouting a limited eligible population will reduce provider cost enough to improve contribution margin without an unacceptable decline in instant delivery or an increase in operational friction.

## Eligibility

- C01 transfers currently routed through P02.
- Customer has not selected or paid for an explicit speed commitment.
- Transfer is below the operational risk threshold.
- Alternative provider is available and passes pre-routing health checks.
- Exclude active settlement incidents and customers with an unresolved support case.

## Design

- Randomise eligible transfers at quote acceptance.
- Control retains current routing.
- Treatment applies the alternative routing rule.
- Start with a 25% treatment allocation.
- Stratify by customer segment and transfer-size band.
- Run through at least one complete weekly operating cycle after the minimum sample threshold is reached.

## Metrics

**Primary metric**

- Contribution margin proxy per $1 million of volume.

**Customer guardrails**

- Instant transfer rate.
- P90 delivery time.
- Support contact rate within seven days.
- Refund rate.

**Operational guardrails**

- Reconciliation exception rate.
- Missing settlement rate.
- Settlement ageing.

## Pre-test scenario

The descriptive 25% reroute scenario estimates $315.28 of provider-cost savings and $265.44 of contribution uplift on the observed H1 volume. It also estimates a 2.77 pp decline in corridor instant rate and a 0.64 pp increase in support-contact rate.

The scenario is a sizing input only. It uses observed route averages and does not adjust for selection effects.

## Decision rule

Scale only if the treatment improves the primary metric and all guardrails remain inside thresholds agreed before exposure begins. If the primary metric improves but a guardrail breaches, investigate the affected segment before deciding whether to narrow or stop the treatment.

## Readout

Report absolute and relative effects with uncertainty intervals. Include exposure counts, sample-ratio checks, segment consistency, operational incidents and any changes made during the test. Avoid declaring a winner from a point estimate alone.
