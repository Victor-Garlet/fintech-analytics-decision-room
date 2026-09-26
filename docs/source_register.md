# Source Register

**Project:** Fintech Analytics Decision Room
**Last reviewed:** 24 September 2026
**Rule:** public sources establish context and definitions. They do not provide or imply transaction-level truth.

## Public sources

| ID | Source | Published | Accessed | Approved use | Explicit boundary |
| --- | --- | --- | --- | --- | --- |
| S01 | [Wise Q1 FY27 Trading Update](https://owners.wise.com/news-releases/news-release-details/wise-q1-fy27-trading-update) | 17 Jul 2026 | 24 Sep 2026 | Opening business signal and published quarterly figures | Do not infer the internal causes of KPI movements beyond Wise's own explanation |
| S02 | [Wise FY2026 Financial Results](https://owners.wise.com/news-releases/news-release-details/wise-group-plc-reports-full-year-2026-financial-results) | 25 Jun 2026 | 24 Sep 2026 | Historical scale, annual take rate and the public relationship between infrastructure, lower cost and speed | Do not use annual aggregates as transaction-level calibration targets |
| S03 | [Wise Help Centre: Fees for sending money](https://wise.com/help/articles/2522717/fees-for-sending-money) | Current help article | 24 Sep 2026 | Public explanation that transfer cost can depend on amount, payment method and exchange rate | Prototype fee rules are simplified project assumptions, not Wise pricing rules |
| S04 | [Wise Help Centre: Will my transfer be instant?](https://wise.com/help/articles/2932104/will-my-transfer-be-instant) | Current help article | 24 Sep 2026 | Public explanation that delivery speed varies by currency, payment type, working day and transfer circumstances | Prototype instant classification is a documented analytical rule, not a reproduction of Wise operations |
| S05 | [Wise Help Centre: Mid-market exchange rate](https://wise.com/help/articles/2932395/whats-the-mid-market-exchange-rate) | Current help article | 24 Sep 2026 | Plain-language explanation of the mid-market rate and rate display | Prototype FX rates are fixed synthetic configuration values and must not be presented as market data |

## Facts approved for public use

The following company-level facts may be used when their reporting period and source are stated:

| Fact ID | Public fact | Source |
| --- | --- | --- |
| F01 | Wise reported 11.863 million active customers in Q1 FY2027, up 21% year over year. | S01 |
| F02 | Wise reported $69.3 billion in quarterly cross-border volume, up 26% year over year. | S01 |
| F03 | Wise reported $714.0 million in net revenue, up 25% year over year. | S01 |
| F04 | Wise reported a 0.50% cross-border take rate, two basis points lower year over year. | S01 |
| F05 | Wise reported 77% instant transfers, seven percentage points higher year over year. | S01 |
| F06 | Wise said the lower Q1 FY2027 take rate reflected capacity used to invest further in lower customer prices. | S01 |
| F07 | Wise reported an FY2026 cross-border take rate of 0.52%, compared with 0.58% in FY2025. | S02 |
| F08 | Wise explains publicly that transfer fees can vary with amount, payment method and exchange rate. | S03 |
| F09 | Wise explains publicly that transfer delivery time can vary by currency, payment type and timing. | S04 |

## Project assumptions

These choices make the simulation coherent. They are not sourced claims about Wise.

| Assumption ID | Project assumption | Reason | Owner |
| --- | --- | --- | --- |
| A01 | The prototype covers 1 July 2025 to 30 June 2026. | Provides twelve complete months and month-end boundaries for timing analysis. | Project |
| A02 | The prototype contains exactly 10,000 transfers across 20 corridors. | Large enough to test relationships while remaining fast to inspect and regenerate. | Project |
| A03 | All economics are normalised to USD for comparison. | Avoids mixing nominal amounts across currencies in the first analytical layer. | Project |
| A04 | A transfer is classified as instant when completion occurs within 20 seconds. | Clear, reproducible threshold aligned with the public wording used in FY2026 results. | Project |
| A05 | Expected pricing is represented by a fixed component plus variable basis points. | Creates a transparent model for price investment and leakage analysis. | Project |
| A06 | Reconciliation uses a $0.50 absolute tolerance in the prototype. | Supports deterministic classification of immaterial rounding versus exceptions. | Project |
| A07 | Provider names, costs, service levels and corridor assignments are entirely fictional. | Prevents the simulation from implying information about real partners. | Project |
| A08 | Contribution margin proxy includes collected fee revenue, provider cost and estimated support cost only. | Produces a useful decision metric without pretending to model full company profitability. | Project |

## Source-use map

| Project output | Permitted public sources | Synthetic inputs required |
| --- | --- | --- |
| Business question and context | S01, S02 | None for the opening context |
| Fee model explanation | S03 | Pricing rules, approved price investment and fee records |
| Speed analysis | S01, S04 | Completion timestamps, provider routes and provider costs |
| FX explanation | S05 | Fixed synthetic rates from configuration |
| Any corridor or provider finding | None | Generated transaction, settlement, fee and cost data only |

## Evidence checks

Before a number appears in a report or presentation:

1. Identify whether it is a public fact, project assumption or synthetic result.
2. Attach the source ID or reproducible model path.
3. State the reporting period and unit.
4. Confirm that a synthetic result is not worded as a Wise finding.
5. Recheck current help or pricing pages when a claim depends on information that can change.
