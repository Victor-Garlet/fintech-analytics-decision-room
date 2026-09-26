from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


CUSTOMER_SEGMENTS = [
    "personal_standard",
    "personal_high_value",
    "business_smb",
    "business_scaleup",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _random_timestamps(
    rng: np.random.Generator,
    start: pd.Timestamp,
    end: pd.Timestamp,
    size: int,
) -> pd.DatetimeIndex:
    span_seconds = int((end - start).total_seconds())
    offsets = rng.integers(0, span_seconds + 1, size=size)
    return pd.DatetimeIndex(start + pd.to_timedelta(offsets, unit="s"))


def _between(series: pd.Series, start: str, end: str) -> pd.Series:
    return series.between(pd.Timestamp(start), pd.Timestamp(end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))


def _generate_customers(
    rng: np.random.Generator,
    count: int,
    period_end: pd.Timestamp,
    corridors: pd.DataFrame,
) -> pd.DataFrame:
    customer_type = rng.choice(["personal", "business"], size=count, p=[0.78, 0.22])
    customer_segment = np.empty(count, dtype=object)

    personal_mask = customer_type == "personal"
    business_mask = ~personal_mask
    customer_segment[personal_mask] = rng.choice(
        ["personal_standard", "personal_high_value"],
        size=int(personal_mask.sum()),
        p=[0.82, 0.18],
    )
    customer_segment[business_mask] = rng.choice(
        ["business_smb", "business_scaleup"],
        size=int(business_mask.sum()),
        p=[0.78, 0.22],
    )

    country_weights = corridors.groupby("source_country", as_index=False)["transfer_weight"].sum()
    country_weights["transfer_weight"] = country_weights["transfer_weight"] / country_weights["transfer_weight"].sum()
    home_country = rng.choice(
        country_weights["source_country"].to_numpy(),
        size=count,
        p=country_weights["transfer_weight"].to_numpy(),
    )
    signup_dates = _random_timestamps(
        rng,
        pd.Timestamp("2022-01-01"),
        period_end - pd.Timedelta(days=1),
        count,
    ).normalize()

    return pd.DataFrame(
        {
            "customer_id": [f"CUS{i:06d}" for i in range(1, count + 1)],
            "customer_type": customer_type,
            "customer_segment": customer_segment,
            "home_country": home_country,
            "signup_date": signup_dates,
            "risk_tier": rng.choice(["low", "medium", "high"], size=count, p=[0.70, 0.27, 0.03]),
        }
    )


def _generate_pricing_rules(
    corridors: pd.DataFrame,
    period_start: pd.Timestamp,
    period_end: pd.Timestamp,
) -> pd.DataFrame:
    segment_bps_adjustment = {
        "personal_standard": 0.0,
        "personal_high_value": -3.0,
        "business_smb": -4.0,
        "business_scaleup": -8.0,
    }
    segment_fixed_adjustment = {
        "personal_standard": 0.00,
        "personal_high_value": -0.05,
        "business_smb": -0.05,
        "business_scaleup": -0.10,
    }

    rows: list[dict[str, Any]] = []
    rule_number = 1
    for corridor in corridors.to_dict("records"):
        for segment in CUSTOMER_SEGMENTS:
            rows.append(
                {
                    "pricing_rule_id": f"PR{rule_number:04d}",
                    "corridor_id": corridor["corridor_id"],
                    "customer_segment": segment,
                    "variable_fee_bps": round(
                        corridor["variable_fee_bps"] + segment_bps_adjustment[segment], 2
                    ),
                    "fixed_fee_usd": round(
                        max(0.20, corridor["fixed_fee_usd"] + segment_fixed_adjustment[segment]), 2
                    ),
                    "effective_start": period_start.normalize(),
                    "effective_end": period_end.normalize(),
                }
            )
            rule_number += 1
    return pd.DataFrame(rows)


def _generate_quotes_transfers_and_fees(
    rng: np.random.Generator,
    config: dict[str, Any],
    domain: dict[str, Any],
    scenarios: dict[str, Any],
    customers: pd.DataFrame,
    corridors: pd.DataFrame,
    providers: pd.DataFrame,
    pricing_rules: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    project = config["project"]
    generation = config["generation"]
    count = int(project["transfer_count"])
    start = pd.Timestamp(project["period_start"])
    end = pd.Timestamp(project["period_end"]) + pd.Timedelta(hours=23)

    corridor_weights = corridors["transfer_weight"].to_numpy(dtype=float)
    corridor_weights = corridor_weights / corridor_weights.sum()
    selected_corridors = rng.choice(corridors["corridor_id"], size=count, p=corridor_weights)
    quoted_at = pd.Series(_random_timestamps(rng, start, end, count), name="quoted_at")

    selected_customers = rng.choice(customers["customer_id"], size=count)
    leakage = scenarios["discount_configuration_leakage"]
    leakage_period = _between(quoted_at, leakage["start_date"], leakage["end_date"])
    leakage_corridor = selected_corridors == leakage["corridor_id"]
    prefer_target_segment = (
        leakage_period
        & leakage_corridor
        & (rng.random(count) < float(leakage["target_segment_probability"]))
    )
    target_customer_pool = customers.loc[
        customers["customer_segment"] == leakage["customer_segment"], "customer_id"
    ].to_numpy()
    selected_customers[prefer_target_segment] = rng.choice(
        target_customer_pool, size=int(prefer_target_segment.sum())
    )

    work = pd.DataFrame(
        {
            "quote_id": [f"QUO{i:07d}" for i in range(1, count + 1)],
            "transfer_id": [f"TRF{i:07d}" for i in range(1, count + 1)],
            "customer_id": selected_customers,
            "corridor_id": selected_corridors,
            "quoted_at": quoted_at,
        }
    )
    work = work.merge(
        customers[["customer_id", "customer_type", "customer_segment"]],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )
    work = work.merge(corridors, on="corridor_id", how="left", validate="many_to_one")

    segment_volume_mu = {
        "personal_standard": 6.30,
        "personal_high_value": 8.10,
        "business_smb": 8.75,
        "business_scaleup": 10.05,
    }
    segment_volume_sigma = {
        "personal_standard": 0.85,
        "personal_high_value": 0.90,
        "business_smb": 0.95,
        "business_scaleup": 0.95,
    }
    mu = work["customer_segment"].map(segment_volume_mu).to_numpy(dtype=float)
    sigma = work["customer_segment"].map(segment_volume_sigma).to_numpy(dtype=float)
    work["volume_usd"] = np.clip(rng.lognormal(mu, sigma), 25, 250_000).round(2)

    work = work.merge(
        pricing_rules,
        on=["corridor_id", "customer_segment"],
        how="left",
        validate="many_to_one",
        suffixes=("", "_pricing"),
    )

    work["list_fee_usd"] = (
        work["fixed_fee_usd_pricing"]
        + work["volume_usd"] * work["variable_fee_bps_pricing"] / 10_000
    ).round(2)

    price_investment = scenarios["approved_price_investment"]
    approved_mask = (
        work["corridor_id"].isin(price_investment["corridors"])
        & _between(work["quoted_at"], price_investment["start_date"], price_investment["end_date"])
    )
    approved_reduction = np.where(
        approved_mask,
        work["volume_usd"] * float(price_investment["reduction_bps"]) / 10_000,
        0.0,
    )
    minimum_fee = work["fixed_fee_usd_pricing"].to_numpy(dtype=float)
    work["expected_fee_usd"] = np.maximum(
        minimum_fee,
        work["list_fee_usd"].to_numpy(dtype=float) - approved_reduction,
    ).round(2)

    currency_to_usd = domain["currencies"]
    work["synthetic_fx_rate"] = (
        work["source_currency"].map(currency_to_usd)
        / work["target_currency"].map(currency_to_usd)
    ).round(6)
    work["source_amount"] = (
        work["volume_usd"] / work["source_currency"].map(currency_to_usd)
    ).round(2)
    work["target_amount_before_fee"] = (
        work["volume_usd"] / work["target_currency"].map(currency_to_usd)
    ).round(2)

    provider_ids = providers["provider_id"].to_numpy()
    base_provider_weights = np.array([0.20, 0.19, 0.17, 0.16, 0.16, 0.12], dtype=float)
    selected_providers = rng.choice(provider_ids, size=count, p=base_provider_weights)

    speed = scenarios["speed_cost_tradeoff"]
    speed_eligible = (
        (work["corridor_id"] == speed["corridor_id"])
        & _between(work["quoted_at"], speed["start_date"], speed["end_date"])
    )
    speed_route = speed_eligible & (rng.random(count) < float(speed["target_provider_probability"]))
    selected_providers[speed_route] = speed["provider_id"]

    settlement_pattern = scenarios["settlement_exception_pattern"]
    settlement_eligible = (
        (work["corridor_id"] == settlement_pattern["corridor_id"])
        & _between(work["quoted_at"], settlement_pattern["start_date"], settlement_pattern["end_date"])
    )
    settlement_route = settlement_eligible & (
        rng.random(count) < float(settlement_pattern["target_provider_probability"])
    )
    selected_providers[settlement_route] = settlement_pattern["provider_id"]
    work["provider_id"] = selected_providers

    work["created_at"] = work["quoted_at"] + pd.to_timedelta(rng.integers(60, 601, size=count), unit="s")
    is_completed = rng.random(count) < float(generation["completed_transfer_probability"])
    work["transfer_status"] = np.where(is_completed, "completed", "cancelled")
    work["payment_method"] = rng.choice(
        ["bank_transfer", "debit_card", "credit_card", "account_balance"],
        size=count,
        p=[0.48, 0.24, 0.08, 0.20],
    )

    instant_probability = work["expected_instant_rate"].to_numpy(dtype=float)
    speed_mask = (
        speed_eligible
        & (work["provider_id"] == speed["provider_id"])
        & is_completed
    )
    instant_probability[speed_mask] = float(speed["instant_probability"])
    is_instant = (rng.random(count) < instant_probability) & is_completed
    work["is_instant"] = is_instant

    delivery_seconds = np.full(count, np.nan)
    delivery_seconds[is_instant] = rng.integers(
        2,
        int(generation["instant_threshold_seconds"]) + 1,
        size=int(is_instant.sum()),
    )
    slower_completed = is_completed & ~is_instant
    slower_seconds = np.clip(
        rng.lognormal(mean=np.log(5 * 3600), sigma=1.05, size=int(slower_completed.sum())),
        30 * 60,
        4 * 24 * 3600,
    )
    delivery_seconds[slower_completed] = slower_seconds
    work["delivery_seconds"] = np.round(delivery_seconds, 0)
    completed_at = work["created_at"] + pd.to_timedelta(
        np.nan_to_num(delivery_seconds, nan=0.0), unit="s"
    )
    work["completed_at"] = completed_at.where(is_completed, pd.NaT)

    quotes = work[
        [
            "quote_id",
            "customer_id",
            "corridor_id",
            "pricing_rule_id",
            "quoted_at",
            "volume_usd",
            "source_amount",
            "target_amount_before_fee",
            "synthetic_fx_rate",
            "list_fee_usd",
            "expected_fee_usd",
        ]
    ].copy()
    quotes["quote_expires_at"] = quotes["quoted_at"] + pd.Timedelta(minutes=30)
    quotes = quotes[
        [
            "quote_id",
            "customer_id",
            "corridor_id",
            "pricing_rule_id",
            "quoted_at",
            "quote_expires_at",
            "volume_usd",
            "source_amount",
            "target_amount_before_fee",
            "synthetic_fx_rate",
            "list_fee_usd",
            "expected_fee_usd",
        ]
    ]

    transfers = work[
        [
            "transfer_id",
            "quote_id",
            "customer_id",
            "corridor_id",
            "provider_id",
            "created_at",
            "completed_at",
            "transfer_status",
            "payment_method",
            "is_instant",
            "delivery_seconds",
            "volume_usd",
            "source_currency",
            "target_currency",
        ]
    ].copy()

    completed = work.loc[is_completed].copy()
    leakage_mask = (
        (completed["corridor_id"] == leakage["corridor_id"])
        & (completed["customer_segment"] == leakage["customer_segment"])
        & _between(completed["quoted_at"], leakage["start_date"], leakage["end_date"])
    )
    unintended_reduction = np.where(
        leakage_mask,
        completed["volume_usd"] * float(leakage["leakage_bps"]) / 10_000,
        0.0,
    )
    completed["collected_fee_usd"] = np.maximum(
        0.01,
        completed["expected_fee_usd"].to_numpy(dtype=float) - unintended_reduction,
    ).round(2)
    completed["approved_price_investment_usd"] = (
        completed["list_fee_usd"] - completed["expected_fee_usd"]
    ).clip(lower=0).round(2)
    completed["fee_leakage_usd"] = (
        completed["expected_fee_usd"] - completed["collected_fee_usd"]
    ).clip(lower=0).round(2)
    completed["fee_outcome"] = np.select(
        [
            completed["fee_leakage_usd"] > 0.01,
            completed["approved_price_investment_usd"] > 0.01,
        ],
        ["unexpected_shortfall", "approved_price_investment"],
        default="as_expected",
    )
    fees = completed[
        [
            "transfer_id",
            "list_fee_usd",
            "approved_price_investment_usd",
            "expected_fee_usd",
            "collected_fee_usd",
            "fee_leakage_usd",
            "fee_outcome",
        ]
    ].copy()
    fees.insert(0, "fee_id", [f"FEE{i:07d}" for i in range(1, len(fees) + 1)])

    return quotes, transfers, fees


def _generate_provider_costs(
    rng: np.random.Generator,
    transfers: pd.DataFrame,
    corridors: pd.DataFrame,
    providers: pd.DataFrame,
    scenarios: dict[str, Any],
) -> pd.DataFrame:
    completed = transfers.loc[transfers["transfer_status"] == "completed"].copy()
    completed = completed.merge(
        corridors[["corridor_id", "corridor_cost_bps"]],
        on="corridor_id",
        how="left",
        validate="many_to_one",
    ).merge(
        providers[["provider_id", "base_cost_bps"]],
        on="provider_id",
        how="left",
        validate="many_to_one",
    )

    speed = scenarios["speed_cost_tradeoff"]
    speed_mask = (
        (completed["corridor_id"] == speed["corridor_id"])
        & (completed["provider_id"] == speed["provider_id"])
        & _between(completed["created_at"], speed["start_date"], speed["end_date"])
    )
    cost_noise = rng.normal(0.0, 0.45, size=len(completed))
    completed["provider_cost_bps"] = (
        completed["base_cost_bps"]
        + completed["corridor_cost_bps"]
        + cost_noise
        + np.where(speed_mask, float(speed["cost_surcharge_bps"]), 0.0)
    ).clip(lower=1.0).round(3)
    completed["provider_fixed_cost_usd"] = 0.18
    completed["provider_cost_usd"] = (
        completed["provider_fixed_cost_usd"]
        + completed["volume_usd"] * completed["provider_cost_bps"] / 10_000
    ).round(2)
    completed["routing_tier"] = np.where(speed_mask, "priority", "standard")

    output = completed[
        [
            "transfer_id",
            "provider_id",
            "provider_cost_bps",
            "provider_fixed_cost_usd",
            "provider_cost_usd",
            "routing_tier",
        ]
    ].copy()
    output.insert(0, "provider_cost_id", [f"PCO{i:07d}" for i in range(1, len(output) + 1)])
    return output


def _generate_settlements(
    rng: np.random.Generator,
    config: dict[str, Any],
    transfers: pd.DataFrame,
    providers: pd.DataFrame,
    scenarios: dict[str, Any],
) -> pd.DataFrame:
    completed = transfers.loc[transfers["transfer_status"] == "completed"].copy()
    completed = completed.merge(
        providers[["provider_id", "base_settlement_hours"]],
        on="provider_id",
        how="left",
        validate="many_to_one",
    )

    jitter = rng.integers(-1, 3, size=len(completed))
    base_hours = (completed["base_settlement_hours"] + jitter).clip(lower=1)
    expected_at = completed["completed_at"] + pd.to_timedelta(base_hours, unit="h")

    timing = scenarios["metric_timing_mismatch"]
    month_end_eligible = completed["completed_at"].dt.day >= int(timing["month_end_day"])
    force_cross_month = month_end_eligible & (
        rng.random(len(completed)) < float(timing["cross_month_probability"])
    )
    next_month_start = (
        completed["completed_at"].dt.to_period("M").dt.to_timestamp("M") + pd.Timedelta(days=1)
    )
    added_hours = rng.integers(
        int(timing["added_delay_hours_min"]),
        int(timing["added_delay_hours_max"]) + 1,
        size=len(completed),
    )
    expected_at = expected_at.where(
        ~force_cross_month,
        next_month_start + pd.to_timedelta(added_hours, unit="h"),
    )

    status = np.full(len(completed), "matched", dtype=object)
    random_outcome = rng.random(len(completed))
    pattern = scenarios["settlement_exception_pattern"]
    pattern_mask = (
        (completed["corridor_id"] == pattern["corridor_id"])
        & (completed["provider_id"] == pattern["provider_id"])
        & _between(completed["completed_at"], pattern["start_date"], pattern["end_date"])
    ).to_numpy()

    target_mismatch = float(pattern["mismatch_probability"])
    target_missing = target_mismatch + float(pattern["missing_probability"])
    target_late = target_missing + float(pattern["late_probability"])
    status[pattern_mask & (random_outcome < target_mismatch)] = "amount_mismatch"
    status[pattern_mask & (random_outcome >= target_mismatch) & (random_outcome < target_missing)] = "missing"
    status[pattern_mask & (random_outcome >= target_missing) & (random_outcome < target_late)] = "late"

    control_mask = ~pattern_mask
    status[control_mask & (random_outcome < 0.012)] = "amount_mismatch"
    status[control_mask & (random_outcome >= 0.012) & (random_outcome < 0.018)] = "missing"
    status[control_mask & (random_outcome >= 0.018) & (random_outcome < 0.036)] = "late"

    settled_at = expected_at + pd.to_timedelta(rng.integers(-20, 31, size=len(completed)), unit="m")
    late_mask = status == "late"
    settled_at = settled_at.where(
        ~late_mask,
        expected_at + pd.to_timedelta(rng.integers(24, 73, size=len(completed)), unit="h"),
    )
    missing_mask = status == "missing"
    settled_at = settled_at.where(~missing_mask, pd.NaT)

    expected_amount = completed["volume_usd"].to_numpy(dtype=float)
    actual_amount = expected_amount + rng.normal(0.0, 0.06, size=len(completed))
    mismatch_mask = status == "amount_mismatch"
    mismatch_size = rng.uniform(5.0, 75.0, size=len(completed)) * rng.choice([-1, 1], size=len(completed))
    actual_amount[mismatch_mask] = expected_amount[mismatch_mask] + mismatch_size[mismatch_mask]
    actual_amount[missing_mask] = np.nan
    actual_amount = np.round(actual_amount, 2)
    expected_amount = np.round(expected_amount, 2)
    variance = np.round(actual_amount - expected_amount, 2)

    output = pd.DataFrame(
        {
            "settlement_id": [f"SET{i:07d}" for i in range(1, len(completed) + 1)],
            "transfer_id": completed["transfer_id"].to_numpy(),
            "provider_id": completed["provider_id"].to_numpy(),
            "expected_settlement_at": expected_at.to_numpy(),
            "settled_at": settled_at.to_numpy(),
            "expected_settlement_usd": expected_amount,
            "actual_settlement_usd": actual_amount,
            "settlement_variance_usd": variance,
            "settlement_status": status,
            "is_reconciliation_exception": status != "matched",
        }
    )
    return output


def _generate_support_contacts(
    rng: np.random.Generator,
    config: dict[str, Any],
    transfers: pd.DataFrame,
    settlements: pd.DataFrame,
) -> pd.DataFrame:
    exception_transfers = set(
        settlements.loc[settlements["is_reconciliation_exception"], "transfer_id"]
    )
    is_exception = transfers["transfer_id"].isin(exception_transfers).to_numpy()
    is_cancelled = (transfers["transfer_status"] == "cancelled").to_numpy()
    is_noninstant = (~transfers["is_instant"]).to_numpy() & ~is_cancelled
    probability = np.full(
        len(transfers),
        float(config["generation"]["support_contact_base_probability"]),
    )
    probability += np.where(is_noninstant, 0.035, 0.0)
    probability += np.where(is_exception, 0.18, 0.0)
    probability += np.where(is_cancelled, 0.06, 0.0)
    probability = np.clip(probability, 0, 0.45)
    selected = rng.random(len(transfers)) < probability
    contacts = transfers.loc[selected].copy()
    selected_exception = contacts["transfer_id"].isin(exception_transfers)
    reason = np.where(
        selected_exception,
        "settlement_or_recipient_issue",
        np.where(
            contacts["transfer_status"].eq("cancelled"),
            "cancelled_transfer",
            np.where(~contacts["is_instant"], "transfer_delay", "general_transfer_question"),
        ),
    )
    resolution_hours = np.clip(rng.lognormal(1.4, 0.8, size=len(contacts)), 0.2, 72.0)
    contacted_at = contacts["created_at"] + pd.to_timedelta(
        rng.integers(1, 49, size=len(contacts)), unit="h"
    )

    return pd.DataFrame(
        {
            "support_contact_id": [f"SUP{i:07d}" for i in range(1, len(contacts) + 1)],
            "transfer_id": contacts["transfer_id"].to_numpy(),
            "contacted_at": contacted_at.to_numpy(),
            "contact_reason": reason,
            "resolution_hours": np.round(resolution_hours, 2),
            "estimated_support_cost_usd": np.round(4.5 + resolution_hours * 0.35, 2),
        }
    )


def _generate_refunds(
    rng: np.random.Generator,
    config: dict[str, Any],
    transfers: pd.DataFrame,
    settlements: pd.DataFrame,
) -> pd.DataFrame:
    completed = transfers.loc[transfers["transfer_status"] == "completed"].copy()
    exception_transfers = set(
        settlements.loc[settlements["settlement_status"] == "amount_mismatch", "transfer_id"]
    )
    probability = np.full(len(completed), float(config["generation"]["refund_probability"]))
    probability += np.where(completed["transfer_id"].isin(exception_transfers), 0.015, 0.0)
    selected = rng.random(len(completed)) < probability
    refunds = completed.loc[selected].copy()
    reasons = rng.choice(
        ["customer_request", "recipient_issue", "duplicate_payment", "processing_error"],
        size=len(refunds),
        p=[0.48, 0.27, 0.15, 0.10],
    )
    refunded_at = refunds["completed_at"] + pd.to_timedelta(
        rng.integers(1, 11, size=len(refunds)), unit="D"
    )
    return pd.DataFrame(
        {
            "refund_id": [f"REF{i:07d}" for i in range(1, len(refunds) + 1)],
            "transfer_id": refunds["transfer_id"].to_numpy(),
            "refunded_at": refunded_at.to_numpy(),
            "refund_reason": reasons,
            "refund_amount_usd": refunds["volume_usd"].to_numpy(),
        }
    )


def _write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, date_format="%Y-%m-%dT%H:%M:%S", float_format="%.6f")


def generate_prototype(project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    config_path = project_root / "config" / "prototype.yml"
    domain_path = project_root / "config" / "domain.yml"
    scenario_path = project_root / "config" / "scenarios.yml"
    config = _load_yaml(config_path)
    domain = _load_yaml(domain_path)
    scenarios = _load_yaml(scenario_path)
    rng = np.random.default_rng(int(config["project"]["seed"]))

    output_directory = project_root / config["project"]["output_directory"]
    output_directory.mkdir(parents=True, exist_ok=True)

    corridors = pd.DataFrame(domain["corridors"])
    providers = pd.DataFrame(domain["providers"])
    period_start = pd.Timestamp(config["project"]["period_start"])
    period_end = pd.Timestamp(config["project"]["period_end"])
    customers = _generate_customers(
        rng,
        int(config["project"]["customer_count"]),
        period_end,
        corridors,
    )
    pricing_rules = _generate_pricing_rules(corridors, period_start, period_end)
    quotes, transfers, fees = _generate_quotes_transfers_and_fees(
        rng,
        config,
        domain,
        scenarios,
        customers,
        corridors,
        providers,
        pricing_rules,
    )
    provider_costs = _generate_provider_costs(
        rng, transfers, corridors, providers, scenarios
    )
    settlements = _generate_settlements(
        rng, config, transfers, providers, scenarios
    )
    support_contacts = _generate_support_contacts(
        rng, config, transfers, settlements
    )
    refunds = _generate_refunds(rng, config, transfers, settlements)

    tables = {
        "customers": customers,
        "corridors": corridors,
        "providers": providers,
        "pricing_rules": pricing_rules,
        "quotes": quotes,
        "transfers": transfers,
        "fees": fees,
        "provider_costs": provider_costs,
        "settlements": settlements,
        "support_contacts": support_contacts,
        "refunds": refunds,
    }
    for name, frame in tables.items():
        _write_csv(frame, output_directory / f"{name}.csv")

    digest = hashlib.sha256()
    for path in [config_path, domain_path, scenario_path]:
        digest.update(path.read_bytes())
    manifest = {
        "project": config["project"]["name"],
        "seed": int(config["project"]["seed"]),
        "period_start": config["project"]["period_start"],
        "period_end": config["project"]["period_end"],
        "config_sha256": digest.hexdigest(),
        "row_counts": {name: int(len(frame)) for name, frame in tables.items()},
        "synthetic_data": True,
    }
    (output_directory / "generation_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest
