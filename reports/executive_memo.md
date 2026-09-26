# Executive decision memo

**Decision:** Protect unit economics without masking deliberate price investment.

**Recommendation:** Fix the known pricing leakage and settlement-control failure now. Test, rather than assume, the value of changing provider routing.

## What changed

Collected take rate declined from 50.23 bps in H2 2025 to 48.05 bps in H1 2026.

The 2.18 bps decline contains two materially different events:

- 0.57 bps was approved customer price investment.
- 1.67 bps was unexpected leakage from one corridor and customer segment.

The second item represents $3,960.94 in the simulated dataset. Treating the full decline as a pricing problem would reverse an intentional customer investment and leave the control failure untouched.

## What to do

### 1. Stop the observed leakage

Correct the C07 business pricing configuration, identify all affected fee records and add an automated comparison between expected and collected fee before daily close.

**Success measure:** zero new unexpected shortfalls after release, with all affected records assigned a resolution status.

### 2. Repair the reconciliation control

C13/P04 reached a 39.7% exception rate from March to May, compared with 4.2% elsewhere. Assign a route owner, preserve reason codes and monitor ageing separately for mismatches, late settlements and missing settlements.

**Success measure:** exception rate returns within the portfolio control band without increasing unresolved ageing.

### 3. Test the routing hypothesis

The priority-speed route delivered 98.4% instant transfers at 21.43 bps of provider cost. Other C01 routes delivered 82.7% at 8.67 bps.

A planning scenario that reroutes 25% of eligible priority volume estimates:

- $315.28 lower provider cost;
- $265.44 higher contribution margin proxy;
- 2.77 pp lower corridor instant rate;
- 0.64 pp higher corridor support-contact rate.

These are scenario estimates, not forecasted impact. Proceed only through a controlled test with speed, support and reconciliation guardrails.

## Decision guardrails

- Do not combine approved price investment with fee leakage.
- Do not scale routing changes if instant rate falls beyond the agreed threshold.
- Stop the test if support contacts or reconciliation exceptions worsen materially.
- Review contribution margin, not provider cost in isolation.

## Confidence and limitations

Confidence is high for the pricing and reconciliation controls because both patterns are directly observed in the synthetic records. Confidence is medium for the routing opportunity because provider selection is not random. All transaction-level data and findings in this memo are synthetic and do not describe Wise.
