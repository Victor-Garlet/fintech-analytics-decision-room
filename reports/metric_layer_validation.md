# Metric Layer Validation

**Run date:** 26 September 2026
**Environment:** Python 3.12, DuckDB 1.5.5, dbt Core 1.12.5, dbt-duckdb 1.11.0
**Result:** PASS

This report contains structural validation evidence. Diagnostic findings and decision logic are documented separately.

## Build result

| Component | Result |
| --- | ---: |
| Raw sources loaded | 11 |
| dbt view models created | 13 |
| dbt table models created | 10 |
| dbt data tests passed | 168 |
| Complete `dbt build` | 191 / 191 passed |
| Warnings | 0 |
| Errors | 0 |

## Raw row counts

| Source | Rows |
| --- | ---: |
| `customers` | 3,500 |
| `corridors` | 20 |
| `providers` | 6 |
| `pricing_rules` | 80 |
| `quotes` | 10,000 |
| `transfers` | 10,000 |
| `fees` | 9,851 |
| `provider_costs` | 9,851 |
| `settlements` | 9,851 |
| `support_contacts` | 404 |
| `refunds` | 50 |

## Decision-mart row counts

| Mart | Grain | Rows |
| --- | --- | ---: |
| `mart_executive_kpis` | Completion month | 13 |
| `mart_corridor_performance` | Completion month and corridor | 245 |
| `mart_provider_performance` | Completion month, provider and routing tier | 81 |
| `mart_take_rate_bridge` | Bridge component | 6 |
| `mart_reporting_period_reconciliation` | Reporting month | 13 |
| `mart_speed_cost_tradeoff` | Analysis period, corridor and route group | 2 |
| `mart_routing_scenario` | Scenario | 1 |
| `mart_fee_leakage_hotspots` | Corridor and customer segment | 1 |
| `mart_reconciliation_exceptions` | Exception transfer | 430 |
| `mart_transfer_unit_economics` | Completed transfer | 9,851 |

Thirteen completion months are expected because transfers can be initiated at the end of the twelve-month generation window and complete after midnight in the following calendar month. The reconciliation layer preserves this event timing rather than truncating it to fit a reporting period.

## Business rules exercised

- Every completed transfer has exactly one fee, provider-cost and expected-settlement outcome.
- Cancelled transfers do not receive those completed-transfer outcomes.
- Fee equations reconcile within the documented rounding tolerance.
- Required monetary inputs are non-negative.
- Completion timestamps and delivery fields follow transfer status.
- Settlement exception flags agree with settlement states.
- Reconciliation, corridor and provider marts preserve their declared grains.
- Monthly executive totals reconcile to the transfer-level economic mart.
- The completion-to-settlement reporting bridge closes within $0.01 for every month.
- The take-rate decomposition reconciles to the observed movement within 0.000001 bps.
- The routing scenario remains inside its declared treatment bounds.

## Reproduction

```bash
make setup
make build
make export
```

Passing this report means the synthetic analytical layer is internally coherent under its stated assumptions. It does not validate a conclusion about Wise or any real payment provider.
