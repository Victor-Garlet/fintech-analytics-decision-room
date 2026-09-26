# Diagnostic analysis

## Decision

How should a European payments fintech improve price and speed without losing control of unit economics?

This analysis uses a deterministic synthetic dataset. It does not describe Wise's internal performance.

## Executive readout

The H1 2026 collected take rate fell 2.18 bps against the H2 2025 baseline, from 50.23 bps to 48.05 bps. The movement is not one problem:

- 0.57 bps came from approved price investment.
- 1.67 bps came from an unexpected pricing configuration issue.
- Portfolio mix and within-cell list yield almost offset each other.

The leakage is concentrated in one corridor and customer segment. It produced $3,960.94 of simulated lost fees and should be addressed before any broader pricing change.

Two operational patterns require separate treatment:

- A corridor-provider pair reached a 39.7% reconciliation exception rate from March to May 2026, versus 4.2% across all other routes.
- The selected priority-speed route delivered 98.4% instant transfers but cost 21.43 bps, 12.76 bps above the other routes in the same corridor.

The evidence supports one immediate control change and one controlled experiment. It does not support a blanket provider reroute.

## 1. Reporting-period reconciliation

Finance reports settlements when funds settle. Operations reports completed transfers when the customer journey completes. Comparing those totals without a bridge creates a false disagreement.

March 2026 illustrates the timing effect:

| Bridge item | USD |
| --- | ---: |
| Operations completion-cohort expected settlement | 4,513,032.54 |
| Less: current completions settling outside March | (280,485.85) |
| Add: earlier completions settling in March | 134,097.00 |
| Add: same-month settlement variance | (474.07) |
| Finance settlement-period actual | 4,366,169.62 |
| Residual | 0.00 |

The reconciliation model closes every reporting month to a $0.01 tolerance. The correct response is to preserve both views and make the event clock explicit, not force one team onto the other's definition.

### Exception hotspot

From March to May 2026, C13 with provider P04 produced 52 exceptions across 131 completed transfers.

| Scope | Completed transfers | Exceptions | Exception rate |
| --- | ---: | ---: | ---: |
| C13 + P04 | 131 | 52 | 39.7% |
| All other routes | 2,409 | 100 | 4.2% |

The hotspot contains 24 amount mismatches, 15 late settlements and 13 missing settlements. This concentration points to a route-level control or file-handling issue rather than a portfolio-wide settlement failure.

## 2. Take-rate decomposition

The comparison uses weighted H2 2025 and H1 2026 periods. List take-rate movement is split with a symmetric shift-share decomposition at corridor and customer-segment grain. Approved price investment and leakage are then applied as direct fee adjustments.

| Component | Impact, bps | Running take rate, bps |
| --- | ---: | ---: |
| H2 2025 collected take rate | 50.23 | 50.23 |
| Portfolio mix | +0.09 | 50.32 |
| Within-cell list yield | -0.02 | 50.30 |
| Approved price investment | -0.57 | 49.72 |
| Pricing configuration leakage | -1.67 | 48.05 |
| H1 2026 collected take rate |  | 48.05 |

The bridge reconciles to less than 0.000001 bps.

### Leakage concentration

All simulated fee leakage is concentrated in C07 business customers:

| Metric | Result |
| --- | ---: |
| Affected transfers | 215 |
| H1 2026 segment volume | $2,459,883.51 |
| Fee leakage | $3,960.94 |
| Leakage across H1 segment volume | 16.10 bps |
| Share of expected H1 segment fees | 33.3% |

The pattern is consistent with a configuration fault. Because the issue is observed directly in the synthetic fee records, remediation has higher decision confidence than a pricing or routing redesign.

## 3. Speed, cost and customer-service trade-off

The H1 2026 comparison isolates corridor C01.

| Metric | Priority-speed route | Other C01 routes | Difference |
| --- | ---: | ---: | ---: |
| Completed transfers | 250 | 104 | 146 |
| Volume | $988,148.78 | $717,648.96 | $270,499.82 |
| Instant transfer rate | 98.4% | 82.7% | +15.7 pp |
| Provider cost rate | 21.43 bps | 8.67 bps | +12.76 bps |
| Support contact rate | 1.2% | 4.8% | -3.6 pp |
| Contribution margin proxy | 17.68 bps | 28.42 bps | -10.75 bps |

The priority route is faster and generates fewer support contacts. It also has materially weaker unit economics. Observed averages cannot prove that rerouting the same transfer would produce the benchmark outcome, so the next step is an experiment rather than a policy change.

## 4. Recommended sequence

1. Correct the C07 business pricing configuration and reconcile the affected fee records.
2. Add a route-level settlement control for C13/P04, with owner, reason code and ageing threshold.
3. Run a controlled C01 routing test on a small eligible population.
4. Keep approved price investment separate from leakage in the executive scorecard.

## Limitations

- All transfer-level data and findings are synthetic.
- Contribution margin is a proxy. It excludes fixed operating costs and several potential loss components.
- Provider comparisons are observational and may contain selection effects.
- The six-month comparison is suitable for this simulation, not a universal period choice.
- The routing scenario is a planning estimate, not a causal forecast.

## Reproducible assets

- `mart_reporting_period_reconciliation`
- `mart_take_rate_bridge`
- `mart_fee_leakage_hotspots`
- `mart_speed_cost_tradeoff`
- `mart_routing_scenario`
- Singular reconciliation, grain and scenario-boundary tests
