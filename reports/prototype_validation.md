# Prototype Validation Report

**Status:** PASS  
**Dataset:** Synthetic 10,000-transfer prototype  
**Scope:** Structural and scenario-detectability checks for this synthetic case.

## Dataset summary

- Transfers: 10,000
- Completed transfers: 9,851
- Customers: 3,500
- Corridors: 20
- Completed volume: $47,373,819.71
- Collected fee take rate: 49.14 bps
- Approved price investment: 0.29 bps
- Fee leakage: 0.84 bps
- Instant rate: 68.2%
- Reconciliation exception rate: 4.4%

## Automated checks

| Result | Check | Evidence |
| --- | --- | --- |
| PASS | Exactly 10,000 transfer rows | observed=10,000; expected=10,000 |
| PASS | Customer keys are unique | rows=3,500 |
| PASS | Quote keys are unique | rows=10,000 |
| PASS | Transfer keys are unique | rows=10,000 |
| PASS | Fee keys are unique | rows=9,851 |
| PASS | Provider-cost keys are unique | rows=9,851 |
| PASS | Settlement keys are unique | rows=9,851 |
| PASS | Transfer customers resolve | unresolved=0 |
| PASS | Transfer quotes resolve | unresolved=0 |
| PASS | Transfer corridors resolve | unresolved=0 |
| PASS | Transfer providers resolve | unresolved=0 |
| PASS | Fee transfers resolve | unresolved=0 |
| PASS | Settlement transfers resolve | unresolved=0 |
| PASS | Support transfers resolve | unresolved=0 |
| PASS | Refund transfers resolve | unresolved=0 |
| PASS | Every completed transfer has one fee record | completed=9,851; fees=9,851 |
| PASS | Every completed transfer has one settlement record | completed=9,851; settlements=9,851 |
| PASS | Fee equation reconciles | list - approved = expected; expected - collected = leakage |
| PASS | Core economic values are non-negative | volume, fees, leakage and provider costs checked |
| PASS | Completion and settlement timing create a visible period bridge | cross_month_transfers=884 |
| PASS | Pricing configuration leakage is detectable | target_rows=215; target=18.00bps; control=0.00bps |
| PASS | Settlement exception pattern is detectable | target_rows=131; target=39.7%; control=3.9% |
| PASS | Speed and provider-cost trade-off is detectable | target_rows=250; instant=98.4% vs 76.7%; cost=20.99bps vs 8.10bps |

## Interpretation

Passing this report means the prototype is structurally coherent and the controlled scenarios are analytically detectable. It does not validate a conclusion about Wise or any real payment provider.
