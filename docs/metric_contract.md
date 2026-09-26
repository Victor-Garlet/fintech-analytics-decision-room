# Prototype Metric Contract

**Version:** 0.2
**Status:** Implemented in the local dbt metric layer
**Default currency:** USD
**Purpose:** ensure Finance, Operations and Product can disagree visibly about business meaning without silently using different formulas.

## Time rules

| View | Governing timestamp | Intended use |
| --- | --- | --- |
| Customer and product performance | `completed_at` | When the customer-facing transfer outcome occurred |
| Finance settlement view | `settled_at` | When the simulated provider movement was financially settled |
| Demand and funnel view | `created_at` | When the transfer was initiated |
| Pricing view | `quoted_at` and pricing-rule effective date | Which expected price applied when the quote was produced |

A monthly total without its governing timestamp is incomplete and should not be published.

## Core metrics

| Metric | Prototype definition | Grain and filters | Main limitation |
| --- | --- | --- | --- |
| Completed active customers | Distinct `customer_id` with at least one completed transfer in the period | Period, completed transfers | Prototype customers are synthetic and do not reproduce Wise customer behaviour |
| Cross-border volume | Sum of `volume_usd` for completed transfers | Period, completed transfers | Uses fixed synthetic currency conversion rates |
| List fee revenue | Sum of `list_fee_usd` | Completed transfer | Represents the pre-investment configured price, not actual Wise pricing |
| Approved price investment | Sum of `approved_price_investment_usd` | Completed transfer | Captures only the controlled synthetic price reductions |
| Expected fee revenue | Sum of `expected_fee_usd` | Completed transfer | Equals list fee less approved price investment |
| Collected fee revenue | Sum of `collected_fee_usd` | Completed transfer | Excludes broader revenue categories such as card and interest income |
| Fee leakage | Sum of `expected_fee_usd - collected_fee_usd`, floored at zero | Completed transfer, above $0.01 | A diagnostic project definition, not a company accounting term |
| List take rate | `list_fee_revenue / cross_border_volume` | Same period and transfer population | Pre-investment reference only |
| Expected take rate | `expected_fee_revenue / cross_border_volume` | Same period and transfer population | Reflects approved project pricing rules |
| Collected take rate | `collected_fee_revenue / cross_border_volume` | Same period and transfer population | Simplified fee-only measure |
| Instant-transfer rate | Completed transfers delivered in 20 seconds or less divided by completed transfers | Completion period | Does not reproduce every production eligibility rule |
| Reconciliation exception rate | Settlements classified missing, mismatched or late divided by expected settlements | Settlement cohort | Late and amount exceptions have different operational meaning and should also be separated |
| Settlement variance | `actual_settlement_usd - expected_settlement_usd` | Settlement | Missing settlements have no numeric variance and require a separate count |
| Provider cost rate | Provider cost divided by completed volume, expressed in basis points | Corridor, provider, completion period | Synthetic provider contracts and costs |
| Support contact rate | Distinct transfers with a support contact divided by completed transfers | Completion cohort | One generated contact maximum per transfer in prototype |
| Contribution margin proxy | Collected fee minus provider cost minus estimated support cost | Completed transfer | Not company profit; omits payroll, compliance, FX exposure, infrastructure and other costs |

## Reconciliation rules

1. Every completed transfer should produce one expected settlement record.
2. A missing settlement remains a row with no actual settlement timestamp or amount.
3. An absolute settlement variance at or below $0.50 is treated as matched unless it breaches the settlement SLA.
4. A late settlement is an exception even when the amount matches.
5. Completion-month and settlement-month reports must be connected through a visible bridge, not forced into one total.

## Decomposition order

When collected take rate moves, investigate in this order:

1. approved price investment;
2. customer and corridor mix;
3. unintended fee leakage;
4. event-timing or population differences;
5. unexplained residual movement.

This order prevents an intentional lower price from being presented as a defect.

## Ownership and validation map

Ownership here describes the fictional operating model used in the case. It is not a statement about Wise's organisation.

| Metric | Fictional decision owner | Implemented model | Primary validation |
| --- | --- | --- | --- |
| Completed active customers | Product Analytics | `mart_executive_kpis` | Monthly aggregation reconciles to the transfer-grain mart |
| Cross-border volume | Finance Analytics | `mart_executive_kpis` | Completed-transfer population and monthly amount reconciliation |
| List fee revenue | Pricing Analytics | `mart_executive_kpis` | Required fee fields and non-negative economic values |
| Approved price investment | Pricing or Product Manager | `mart_executive_kpis` | `expected = list fee - approved investment` within $0.011 |
| Expected fee revenue | Finance Analytics | `mart_executive_kpis` | Fee equation assertion at transfer grain |
| Collected fee revenue | Finance Analytics | `mart_executive_kpis` | Monthly aggregation reconciles to the transfer-grain mart |
| Fee leakage | Pricing Analytics | `mart_transfer_unit_economics` | `leakage = max(expected - collected, 0)` within $0.011 |
| List, expected and collected take rate | Finance Analytics | `mart_executive_kpis` | Numerator and volume denominator reconcile to one completion cohort |
| Instant-transfer rate | Payments Product | `mart_corridor_performance` | Completion status and delivery fields follow the event contract |
| Reconciliation exception rate | Payments Operations | `mart_executive_kpis` | Every completed transfer has one expected settlement and status logic is consistent |
| Settlement variance | Payments Operations | `mart_reconciliation_exceptions` | Missing outcomes retain null actuals; matched outcomes cannot be exceptions |
| Provider cost rate | Provider Management | `mart_provider_performance` | One non-negative provider-cost record per completed transfer |
| Support contact rate | Customer Operations | `mart_corridor_performance` | Optional contact keys are unique and related to a valid transfer |
| Contribution margin proxy | Finance Analytics | `mart_transfer_unit_economics` | Required components are non-null and non-negative before calculation |

## Change control

A change to a formula, timestamp, inclusion rule or tolerance is a contract change, not a dashboard edit. It must update this document, the relevant dbt model and at least one automated test in the same pull request.
