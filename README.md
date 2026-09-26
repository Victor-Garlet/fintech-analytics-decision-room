# Fintech Analytics Decision Room

**A payments analytics case, from a messy KPI to a decision someone can check.**

Imagine a European fintech that is lowering transfer prices and making payments faster. Its collected take rate falls. Is that an intended investment in customers, a fee configuration error, a change in customer mix, or several things at once?

I built this independent simulation to work through that question. Wise's [public disclosures](docs/source_register.md) inspired the setting. **The customers, transfers, providers, findings and recommendations in this repository are fictional.** I have no affiliation with Wise or access to its internal data.

## The decision in 30 seconds

In the **synthetic** H2 2025 to H1 2026 comparison, collected take rate went from **50.23 to 48.05 basis points**. The bridge separates an intentional **0.57 bp** price investment from **1.67 bps** of unexpected fee leakage in one corridor and customer segment. The simulation also exposes a settlement exception hotspot. A faster route costs more, but the observational comparison does not justify moving traffic without a test.

**My recommendation:** correct the fee configuration, repair the settlement control, then test a limited routing change with customer and operational guardrails. [Read the one-page decision memo](reports/executive_memo.md).

## Pick your route

| If you have... | Start here |
| --- | --- |
| 2 minutes | [The recommendation and its limits](reports/executive_memo.md) |
| 5 minutes | [The findings and supporting numbers](reports/diagnostic_analysis.md) |
| More time | Follow the six steps below, with links to the data, SQL and checks |
| A terminal | [Run the case locally](#run-it-yourself) |

## Follow the work

### 1. Start with the business question

A falling headline metric can hide different causes. The case asks which movements should be preserved, which need a fix, and which require an experiment. I wrote down the decision, hypotheses and evidence rules before interpreting the generated results.

**Open:** [case brief](docs/project_charter.md) · [public source register](docs/source_register.md) · [assumptions](docs/assumptions.md)

### 2. Make the evidence inspectable

A seeded Python generator creates **10,000 transfer attempts**, **3,500 customers** and **11 related source tables** across **20 corridors**. The [scenario settings](config/scenarios.yml) are published, so the observed faults are visible and the snapshot can be regenerated. This is a designed case, not a discovered issue at a real company.

**Open:** [generator](src/fintech_sim/generator.py) · [configuration](config/prototype.yml) · [data dictionary](docs/data_dictionary.md) · [snapshot](data/prototype) · [generation checks](reports/prototype_validation.md)

### 3. Agree on what each number means

Operations counts a transfer when it completes; Finance may count its settlement in another month. I kept those event clocks separate, then connected them with a reconciliation bridge. Fees also stay distinct as list price, approved reduction, expected charge and amount collected.

**Open:** [metric contract](docs/metric_contract.md) · [reporting bridge SQL](dbt_fintech/models/marts/mart_reporting_period_reconciliation.sql) · [bridge test](dbt_fintech/tests/assert_reporting_period_bridge_reconciles.sql)

### 4. Build and test the analytical layer

DuckDB loads the CSV snapshot. dbt moves from typed [staging models](dbt_fintech/models/staging) to a [transfer-level economic model](dbt_fintech/models/intermediate/int_transfer_unit_economics.sql), then to [decision-facing marts](dbt_fintech/models/marts). The stored validation report records **23 models and 168 data tests**, with **191 of 191 build steps passing** at that run.

**Open:** [architecture](docs/architecture.md) · [dbt project](dbt_fintech) · [quality assertions](dbt_fintech/tests) · [validation report](reports/metric_layer_validation.md)

### 5. Separate the findings

| Question | Synthetic finding | Trace it to |
| --- | --- | --- |
| Why did take rate fall? | A **2.18 bp** decline includes **0.57 bp** of approved price investment and **1.67 bps** of fee leakage, worth **$3,960.94** in the simulated period. | [Take-rate bridge](dbt_fintech/models/marts/mart_take_rate_bridge.sql) |
| Where is the settlement risk? | The **C13/P04** route has a **39.7%** exception rate in the target window, versus **4.2%** elsewhere in the comparison. | [Exception mart](dbt_fintech/models/marts/mart_reconciliation_exceptions.sql) |
| Should routing change? | The C01 priority route completes **98.4%** instantly, with **21.43 bps** of provider cost versus **8.67 bps** for other C01 routes. | [Speed and cost mart](dbt_fintech/models/marts/mart_speed_cost_tradeoff.sql) |

The [diagnostic analysis](reports/diagnostic_analysis.md) gives the periods, denominators and limitations behind these summaries. These are properties of the generated dataset, not observations about Wise.

### 6. Turn evidence into a bounded action

The fee shortfall and exception pattern are directly visible in the synthetic records, so the memo recommends targeted controls. Provider assignment was not random, so the cheaper-route comparison remains a hypothesis. The [experiment design](reports/experiment_design.md) sets eligibility, a small treatment, a contribution metric and speed, support and settlement guardrails.

**Open:** [decision memo](reports/executive_memo.md) · [experiment](reports/experiment_design.md) · [decision log](docs/decision_log.md)

## Run it yourself

Use Python 3.12 and `make`. The build runs locally with DuckDB; no cloud account or credentials are needed.

```bash
make setup
make build
```

The build checks the committed snapshot, loads DuckDB, runs the dbt models and tests, generates dbt documentation and exports the decision marts. To regenerate the same snapshot from the published seed and scenario settings:

```bash
make regenerate
```

The settings live in [`config/`](config), the loader and export scripts in [`scripts/`](scripts), and the committed CSVs in [`data/prototype/`](data/prototype). Local warehouse files and generated exports are ignored by Git. The [static case presentation](site) is an additional view of the decision; the analysis and its proof remain in the linked files above.

## What this case can and cannot show

The data deliberately contains pricing, settlement and routing patterns. The tests show that the synthetic records and analytical definitions are internally consistent. They do **not** show that any such pattern exists at Wise. Contribution margin is a proxy that omits several costs, and the routing scenario uses observed averages rather than a causal estimate. Those limits are part of the decision, especially the choice to test routing before changing it.

Built by Victor Moraes Garlet as an independent portfolio simulation.
