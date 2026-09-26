# Prototype Data Dictionary

**Version:** 0.1
**Coverage:** deterministic 10,000-transfer prototype
**Currency convention:** analytical economics are stored in USD unless the field name states another currency

## Relationship map

```text
customers ──< quotes ──1 transfers >── corridors
                          │    │
                          │    ├──1 fees
                          │    ├──1 provider_costs >── providers
                          │    ├──1 settlements
                          │    ├──0..1 refunds
                          │    └──0..1 support_contacts
                          │
                          └── pricing_rules through corridor and customer segment
```

## `customers.csv`

**Grain:** one synthetic customer.

| Field | Type | Description |
| --- | --- | --- |
| `customer_id` | string | Stable synthetic customer key |
| `customer_type` | string | `personal` or `business` |
| `customer_segment` | string | Pricing and behavioural segment |
| `home_country` | string | Two-letter synthetic home-country assignment |
| `signup_date` | date | Synthetic account creation date |
| `risk_tier` | string | Simplified `low`, `medium` or `high` project classification |

## `corridors.csv`

**Grain:** one source-country and target-country route.

| Field | Type | Description |
| --- | --- | --- |
| `corridor_id` | string | Stable corridor key |
| `source_country` | string | Two-letter sending country |
| `target_country` | string | Two-letter receiving country |
| `source_currency` | string | Sending currency code |
| `target_currency` | string | Receiving currency code |
| `transfer_weight` | decimal | Generator sampling weight |
| `variable_fee_bps` | decimal | Base list-price variable fee in basis points |
| `fixed_fee_usd` | decimal | Base list-price fixed fee |
| `expected_instant_rate` | decimal | Synthetic starting instant-rate probability |
| `corridor_cost_bps` | decimal | Synthetic cost adjustment applied to the route |

## `providers.csv`

**Grain:** one fictional payment provider.

| Field | Type | Description |
| --- | --- | --- |
| `provider_id` | string | Stable provider key |
| `provider_name` | string | Fictional provider name |
| `base_cost_bps` | decimal | Starting provider cost rate |
| `base_settlement_hours` | integer | Starting expected settlement time |

## `pricing_rules.csv`

**Grain:** one corridor and customer-segment pricing rule for the prototype period.

| Field | Type | Description |
| --- | --- | --- |
| `pricing_rule_id` | string | Stable pricing-rule key |
| `corridor_id` | string | Corridor covered by the rule |
| `customer_segment` | string | Customer segment covered by the rule |
| `variable_fee_bps` | decimal | Variable list-fee component |
| `fixed_fee_usd` | decimal | Fixed list-fee component |
| `effective_start` | date | First valid date |
| `effective_end` | date | Last valid date |

## `quotes.csv`

**Grain:** one quote accepted into the transfer flow.

| Field | Type | Description |
| --- | --- | --- |
| `quote_id` | string | Stable quote key |
| `customer_id` | string | Customer receiving the quote |
| `corridor_id` | string | Quoted transfer corridor |
| `pricing_rule_id` | string | Pricing rule used |
| `quoted_at` | timestamp | Quote creation time |
| `quote_expires_at` | timestamp | Quote expiry time |
| `volume_usd` | decimal | Transfer amount normalised to USD |
| `source_amount` | decimal | Amount in source currency |
| `target_amount_before_fee` | decimal | Converted target amount before fee treatment |
| `synthetic_fx_rate` | decimal | Fixed project conversion rate between currencies |
| `list_fee_usd` | decimal | Fee before approved price investment |
| `expected_fee_usd` | decimal | Fee expected after approved price investment |

## `transfers.csv`

**Grain:** one attempted cross-border transfer. Exactly 10,000 rows in the prototype.

| Field | Type | Description |
| --- | --- | --- |
| `transfer_id` | string | Stable transfer key |
| `quote_id` | string | Accepted quote key |
| `customer_id` | string | Customer initiating the transfer |
| `corridor_id` | string | Transfer corridor |
| `provider_id` | string | Fictional routed provider |
| `created_at` | timestamp | Transfer initiation time |
| `completed_at` | timestamp | Customer-facing completion time, null when cancelled |
| `transfer_status` | string | `completed` or `cancelled` |
| `payment_method` | string | Synthetic funding method |
| `is_instant` | boolean | Whether completion occurred within 20 seconds |
| `delivery_seconds` | decimal | Seconds from creation to completion |
| `volume_usd` | decimal | Completed or attempted volume in USD |
| `source_currency` | string | Sending currency |
| `target_currency` | string | Receiving currency |

## `fees.csv`

**Grain:** one fee outcome per completed transfer.

| Field | Type | Description |
| --- | --- | --- |
| `fee_id` | string | Stable fee key |
| `transfer_id` | string | Completed transfer key |
| `list_fee_usd` | decimal | Pre-investment configured fee |
| `approved_price_investment_usd` | decimal | Approved reduction from list price |
| `expected_fee_usd` | decimal | Fee that should have been collected |
| `collected_fee_usd` | decimal | Simulated fee actually collected |
| `fee_leakage_usd` | decimal | Positive unexpected shortfall |
| `fee_outcome` | string | `as_expected`, `approved_price_investment` or `unexpected_shortfall` |

## `provider_costs.csv`

**Grain:** one provider-cost outcome per completed transfer.

| Field | Type | Description |
| --- | --- | --- |
| `provider_cost_id` | string | Stable provider-cost key |
| `transfer_id` | string | Completed transfer key |
| `provider_id` | string | Fictional provider key |
| `provider_cost_bps` | decimal | Total synthetic variable provider-cost rate |
| `provider_fixed_cost_usd` | decimal | Synthetic fixed provider cost |
| `provider_cost_usd` | decimal | Total provider cost for the transfer |
| `routing_tier` | string | `standard` or `priority` |

## `settlements.csv`

**Grain:** one expected settlement per completed transfer, including missing outcomes.

| Field | Type | Description |
| --- | --- | --- |
| `settlement_id` | string | Stable settlement key |
| `transfer_id` | string | Completed transfer key |
| `provider_id` | string | Fictional settling provider |
| `expected_settlement_at` | timestamp | Expected settlement time |
| `settled_at` | timestamp | Actual simulated settlement time, null when missing |
| `expected_settlement_usd` | decimal | Expected settlement amount |
| `actual_settlement_usd` | decimal | Actual simulated amount, null when missing |
| `settlement_variance_usd` | decimal | Actual minus expected amount |
| `settlement_status` | string | `matched`, `late`, `amount_mismatch` or `missing` |
| `is_reconciliation_exception` | boolean | Whether the record requires investigation |

## `support_contacts.csv`

**Grain:** zero or one generated support contact per transfer in the prototype.

| Field | Type | Description |
| --- | --- | --- |
| `support_contact_id` | string | Stable support key |
| `transfer_id` | string | Related transfer key |
| `contacted_at` | timestamp | Contact creation time |
| `contact_reason` | string | Simplified reason category |
| `resolution_hours` | decimal | Simulated time to resolution |
| `estimated_support_cost_usd` | decimal | Simplified cost proxy used in unit economics |

## `refunds.csv`

**Grain:** zero or one generated refund per completed transfer in the prototype.

| Field | Type | Description |
| --- | --- | --- |
| `refund_id` | string | Stable refund key |
| `transfer_id` | string | Related completed transfer |
| `refunded_at` | timestamp | Refund initiation time |
| `refund_reason` | string | Simplified reason category |
| `refund_amount_usd` | decimal | Simulated refunded transfer amount |

## Expected nulls

- `transfers.completed_at` and `delivery_seconds` are null for cancelled transfers.
- `settlements.settled_at`, `actual_settlement_usd` and `settlement_variance_usd` are null for missing settlements.
- Optional relationship tables naturally contain fewer rows than `transfers.csv`.

Unexpected nulls in primary keys, foreign keys or required economic fields fail validation.
