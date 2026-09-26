from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


DATE_COLUMNS = {
    "customers": ["signup_date"],
    "pricing_rules": ["effective_start", "effective_end"],
    "quotes": ["quoted_at", "quote_expires_at"],
    "transfers": ["created_at", "completed_at"],
    "settlements": ["expected_settlement_at", "settled_at"],
    "support_contacts": ["contacted_at"],
    "refunds": ["refunded_at"],
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _load_tables(project_root: Path) -> dict[str, pd.DataFrame]:
    data_directory = project_root / "data" / "prototype"
    names = [
        "customers",
        "corridors",
        "providers",
        "pricing_rules",
        "quotes",
        "transfers",
        "fees",
        "provider_costs",
        "settlements",
        "support_contacts",
        "refunds",
    ]
    tables: dict[str, pd.DataFrame] = {}
    for name in names:
        tables[name] = pd.read_csv(
            data_directory / f"{name}.csv",
            parse_dates=DATE_COLUMNS.get(name),
        )
    return tables


def _between(series: pd.Series, start: str, end: str) -> pd.Series:
    return series.between(pd.Timestamp(start), pd.Timestamp(end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))


def _check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def validate_prototype(project_root: Path, write_report: bool = True) -> dict[str, Any]:
    project_root = project_root.resolve()
    config = _load_yaml(project_root / "config" / "prototype.yml")
    scenarios = _load_yaml(project_root / "config" / "private" / "prototype_scenarios.yml")
    tables = _load_tables(project_root)
    customers = tables["customers"]
    corridors = tables["corridors"]
    providers = tables["providers"]
    quotes = tables["quotes"]
    transfers = tables["transfers"]
    fees = tables["fees"]
    provider_costs = tables["provider_costs"]
    settlements = tables["settlements"]
    support = tables["support_contacts"]
    refunds = tables["refunds"]
    checks: list[dict[str, Any]] = []

    expected_transfer_count = int(config["project"]["transfer_count"])
    _check(
        checks,
        "Exactly 10,000 transfer rows",
        len(transfers) == expected_transfer_count,
        f"observed={len(transfers):,}; expected={expected_transfer_count:,}",
    )

    key_checks = [
        (customers, "customer_id", "Customer keys are unique"),
        (quotes, "quote_id", "Quote keys are unique"),
        (transfers, "transfer_id", "Transfer keys are unique"),
        (fees, "fee_id", "Fee keys are unique"),
        (provider_costs, "provider_cost_id", "Provider-cost keys are unique"),
        (settlements, "settlement_id", "Settlement keys are unique"),
    ]
    for frame, key, name in key_checks:
        _check(checks, name, frame[key].notna().all() and frame[key].is_unique, f"rows={len(frame):,}")

    foreign_key_checks = [
        (transfers["customer_id"], customers["customer_id"], "Transfer customers resolve"),
        (transfers["quote_id"], quotes["quote_id"], "Transfer quotes resolve"),
        (transfers["corridor_id"], corridors["corridor_id"], "Transfer corridors resolve"),
        (transfers["provider_id"], providers["provider_id"], "Transfer providers resolve"),
        (fees["transfer_id"], transfers["transfer_id"], "Fee transfers resolve"),
        (settlements["transfer_id"], transfers["transfer_id"], "Settlement transfers resolve"),
        (support["transfer_id"], transfers["transfer_id"], "Support transfers resolve"),
        (refunds["transfer_id"], transfers["transfer_id"], "Refund transfers resolve"),
    ]
    for child, parent, name in foreign_key_checks:
        missing = int((~child.isin(set(parent))).sum())
        _check(checks, name, missing == 0, f"unresolved={missing}")

    completed = transfers.loc[transfers["transfer_status"] == "completed"]
    _check(
        checks,
        "Every completed transfer has one fee record",
        len(fees) == len(completed) and fees["transfer_id"].is_unique,
        f"completed={len(completed):,}; fees={len(fees):,}",
    )
    _check(
        checks,
        "Every completed transfer has one settlement record",
        len(settlements) == len(completed) and settlements["transfer_id"].is_unique,
        f"completed={len(completed):,}; settlements={len(settlements):,}",
    )
    _check(
        checks,
        "Fee equation reconciles",
        np.allclose(
            fees["list_fee_usd"] - fees["approved_price_investment_usd"],
            fees["expected_fee_usd"],
            atol=0.02,
        )
        and np.allclose(
            fees["expected_fee_usd"] - fees["collected_fee_usd"],
            fees["fee_leakage_usd"],
            atol=0.02,
        ),
        "list - approved = expected; expected - collected = leakage",
    )
    _check(
        checks,
        "Core economic values are non-negative",
        bool(
            (transfers["volume_usd"] > 0).all()
            and (fees[["list_fee_usd", "expected_fee_usd", "collected_fee_usd", "fee_leakage_usd"]] >= 0).all().all()
            and (provider_costs["provider_cost_usd"] >= 0).all()
        ),
        "volume, fees, leakage and provider costs checked",
    )

    timeline = settlements.merge(
        completed[["transfer_id", "completed_at"]], on="transfer_id", how="left", validate="one_to_one"
    )
    settled_rows = timeline["settled_at"].notna()
    cross_month = settled_rows & (
        timeline["completed_at"].dt.to_period("M") != timeline["settled_at"].dt.to_period("M")
    )
    _check(
        checks,
        "Completion and settlement timing create a visible period bridge",
        int(cross_month.sum()) >= 100,
        f"cross_month_transfers={int(cross_month.sum()):,}",
    )

    fee_analysis = (
        fees.merge(
            transfers[["transfer_id", "customer_id", "corridor_id", "created_at", "volume_usd"]],
            on="transfer_id",
            how="left",
            validate="one_to_one",
        )
        .merge(customers[["customer_id", "customer_segment"]], on="customer_id", how="left", validate="many_to_one")
    )
    leakage = scenarios["discount_configuration_leakage"]
    leakage_target = (
        (fee_analysis["corridor_id"] == leakage["corridor_id"])
        & (fee_analysis["customer_segment"] == leakage["customer_segment"])
        & _between(fee_analysis["created_at"], leakage["start_date"], leakage["end_date"])
    )
    leakage_control = (
        (fee_analysis["corridor_id"] == leakage["corridor_id"])
        & (fee_analysis["customer_segment"] == leakage["customer_segment"])
        & ~_between(fee_analysis["created_at"], leakage["start_date"], leakage["end_date"])
    )
    target_leakage_bps = (
        fee_analysis.loc[leakage_target, "fee_leakage_usd"].sum()
        / fee_analysis.loc[leakage_target, "volume_usd"].sum()
        * 10_000
    )
    control_leakage_bps = (
        fee_analysis.loc[leakage_control, "fee_leakage_usd"].sum()
        / fee_analysis.loc[leakage_control, "volume_usd"].sum()
        * 10_000
        if fee_analysis.loc[leakage_control, "volume_usd"].sum() > 0
        else 0.0
    )
    _check(
        checks,
        "Pricing configuration leakage is detectable",
        int(leakage_target.sum()) >= 25 and target_leakage_bps >= 14 and control_leakage_bps < 1,
        f"target_rows={int(leakage_target.sum())}; target={target_leakage_bps:.2f}bps; control={control_leakage_bps:.2f}bps",
    )

    settlement_analysis = settlements.merge(
        completed[["transfer_id", "corridor_id", "completed_at"]],
        on="transfer_id",
        how="left",
        validate="one_to_one",
    )
    pattern = scenarios["settlement_exception_pattern"]
    settlement_target = (
        (settlement_analysis["corridor_id"] == pattern["corridor_id"])
        & (settlement_analysis["provider_id"] == pattern["provider_id"])
        & _between(settlement_analysis["completed_at"], pattern["start_date"], pattern["end_date"])
    )
    settlement_control = ~settlement_target
    target_exception_rate = settlement_analysis.loc[
        settlement_target, "is_reconciliation_exception"
    ].mean()
    control_exception_rate = settlement_analysis.loc[
        settlement_control, "is_reconciliation_exception"
    ].mean()
    _check(
        checks,
        "Settlement exception pattern is detectable",
        int(settlement_target.sum()) >= 30
        and target_exception_rate >= 0.25
        and target_exception_rate >= control_exception_rate * 4,
        f"target_rows={int(settlement_target.sum())}; target={target_exception_rate:.1%}; control={control_exception_rate:.1%}",
    )

    speed_analysis = completed.merge(
        provider_costs[["transfer_id", "provider_cost_bps", "routing_tier"]],
        on="transfer_id",
        how="left",
        validate="one_to_one",
    )
    speed = scenarios["speed_cost_tradeoff"]
    speed_target = (
        (speed_analysis["corridor_id"] == speed["corridor_id"])
        & (speed_analysis["provider_id"] == speed["provider_id"])
        & _between(speed_analysis["created_at"], speed["start_date"], speed["end_date"])
    )
    speed_control = (
        (speed_analysis["corridor_id"] == speed["corridor_id"])
        & ~speed_target
    )
    target_instant_rate = speed_analysis.loc[speed_target, "is_instant"].mean()
    control_instant_rate = speed_analysis.loc[speed_control, "is_instant"].mean()
    target_cost_bps = speed_analysis.loc[speed_target, "provider_cost_bps"].mean()
    control_cost_bps = speed_analysis.loc[speed_control, "provider_cost_bps"].mean()
    _check(
        checks,
        "Speed and provider-cost trade-off is detectable",
        int(speed_target.sum()) >= 50
        and target_instant_rate >= 0.92
        and target_instant_rate > control_instant_rate
        and target_cost_bps >= control_cost_bps + 8,
        (
            f"target_rows={int(speed_target.sum())}; instant={target_instant_rate:.1%} vs {control_instant_rate:.1%}; "
            f"cost={target_cost_bps:.2f}bps vs {control_cost_bps:.2f}bps"
        ),
    )

    total_volume = completed["volume_usd"].sum()
    summary = {
        "transfers": int(len(transfers)),
        "completed_transfers": int(len(completed)),
        "customers": int(len(customers)),
        "corridors": int(len(corridors)),
        "completed_volume_usd": float(total_volume),
        "collected_take_rate_bps": float(fees["collected_fee_usd"].sum() / total_volume * 10_000),
        "approved_price_investment_bps": float(
            fees["approved_price_investment_usd"].sum() / total_volume * 10_000
        ),
        "fee_leakage_bps": float(fees["fee_leakage_usd"].sum() / total_volume * 10_000),
        "instant_rate": float(completed["is_instant"].mean()),
        "reconciliation_exception_rate": float(settlements["is_reconciliation_exception"].mean()),
        "support_contact_rate": float(support["transfer_id"].nunique() / len(transfers)),
        "refund_rate": float(refunds["transfer_id"].nunique() / len(completed)),
    }
    all_passed = all(check["passed"] for check in checks)
    result = {"all_passed": all_passed, "checks": checks, "summary": summary}

    if write_report:
        report_path = project_root / "reports" / "prototype_validation.md"
        status = "PASS" if all_passed else "FAIL"
        lines = [
            "# Prototype Validation Report",
            "",
            f"**Status:** {status}  ",
            "**Dataset:** Synthetic 10,000-transfer prototype  ",
            "**Warning:** This internal report contains scenario-validation detail. Do not publish it before the related episodes.",
            "",
            "## Dataset summary",
            "",
            f"- Transfers: {summary['transfers']:,}",
            f"- Completed transfers: {summary['completed_transfers']:,}",
            f"- Customers: {summary['customers']:,}",
            f"- Corridors: {summary['corridors']:,}",
            f"- Completed volume: ${summary['completed_volume_usd']:,.2f}",
            f"- Collected fee take rate: {summary['collected_take_rate_bps']:.2f} bps",
            f"- Approved price investment: {summary['approved_price_investment_bps']:.2f} bps",
            f"- Fee leakage: {summary['fee_leakage_bps']:.2f} bps",
            f"- Instant rate: {summary['instant_rate']:.1%}",
            f"- Reconciliation exception rate: {summary['reconciliation_exception_rate']:.1%}",
            "",
            "## Automated checks",
            "",
            "| Result | Check | Evidence |",
            "| --- | --- | --- |",
        ]
        for check in checks:
            marker = "PASS" if check["passed"] else "FAIL"
            lines.append(f"| {marker} | {check['check']} | {check['detail']} |")
        lines.extend(
            [
                "",
                "## Interpretation",
                "",
                "Passing this report means the prototype is structurally coherent and the controlled scenarios are analytically detectable. It does not validate a conclusion about Wise or any real payment provider.",
                "",
            ]
        )
        report_path.write_text("\n".join(lines), encoding="utf-8")
        result["report_path"] = str(report_path)
    return result
