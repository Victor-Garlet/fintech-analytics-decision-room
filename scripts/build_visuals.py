from __future__ import annotations

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "fintech_analytics.duckdb"
OUTPUT_DIRECTORY = PROJECT_ROOT / "content" / "visuals"

INK = "#17141c"
PAPER = "#f8f7f3"
WHITE = "#ffffff"
PURPLE = "#6f3cff"
PURPLE_SOFT = "#eee9ff"
ORANGE = "#ff6b35"
ORANGE_SOFT = "#fff0e8"
MUTED = "#69636f"
LINE = "#d9d5df"


def base_figure(episode: int, title: str, subtitle: str):
    fig = plt.figure(figsize=(12, 15), facecolor=PAPER)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.text(0.07, 0.94, f"30 DAYS INSIDE A EUROPEAN FINTECH  {episode}/8", color=PURPLE, fontsize=12, fontweight="bold")
    fig.text(0.07, 0.865, title, color=INK, fontsize=31, fontweight="bold", linespacing=1.05)
    fig.text(0.07, 0.81, subtitle, color=MUTED, fontsize=14, linespacing=1.35)
    fig.text(0.07, 0.035, "Synthetic transaction data  |  Independent portfolio simulation", color=MUTED, fontsize=9)
    fig.text(0.93, 0.035, "Victor Moraes Garlet", color=INK, fontsize=9, fontweight="bold", ha="right")
    return fig, ax


def card(ax, x: float, y: float, width: float, height: float, facecolor: str = WHITE, edgecolor: str = INK):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.8,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    return patch


def save(fig, filename: str):
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIRECTORY / filename, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def fetch_one(connection, query: str):
    return connection.execute(query).fetchone()


def build_episode_01(connection):
    rows = connection.execute(
        """
        select component_code, component_label, impact_bps
        from marts.mart_take_rate_bridge
        order by component_order
        """
    ).fetchall()
    values = {code: (label, value) for code, label, value in rows}
    change = values["comparison"][1] - values["baseline"][1]

    fig = plt.figure(figsize=(12, 15), facecolor=WHITE)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rough_card(x, y, width, height, linewidth=2.7):
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=linewidth,
            edgecolor=INK,
            facecolor=WHITE,
        )
        patch.set_sketch_params(scale=1.2, length=90, randomness=2.5)
        ax.add_patch(patch)

    def rough_line(xs, ys, linewidth=2.2):
        line, = ax.plot(xs, ys, color=INK, linewidth=linewidth, zorder=0)
        line.set_sketch_params(scale=1.2, length=90, randomness=2.5)

    baseline = values["baseline"][1]
    comparison = values["comparison"][1]

    fig.text(0.50, 0.955, "30 DAYS INSIDE A EUROPEAN FINTECH  ·  1/8", ha="center", color=INK, fontsize=13, fontweight="bold")
    fig.text(0.50, 0.865, "TAKE RATE FELL.\nWHAT ACTUALLY MOVED?", ha="center", color=INK, fontsize=34, fontweight="bold", linespacing=1.0)
    fig.text(0.50, 0.79, "one metric. four possible explanations.", ha="center", color=INK, fontsize=16)

    rough_card(0.16, 0.60, 0.68, 0.13, 3.0)
    ax.text(0.50, 0.685, "COLLECTED TAKE RATE", ha="center", color=INK, fontsize=14, fontweight="bold")
    ax.text(0.50, 0.645, f"{baseline:.2f}  →  {comparison:.2f} bps", ha="center", color=INK, fontsize=28, fontweight="bold")
    ax.text(0.50, 0.612, f"CHANGE   {change:+.2f} bps", ha="center", color=INK, fontsize=14, family="monospace")

    rough_line([0.50, 0.50], [0.60, 0.56])
    rough_line([0.25, 0.75], [0.56, 0.56])
    rough_line([0.25, 0.25], [0.56, 0.535])
    rough_line([0.75, 0.75], [0.56, 0.535])
    rough_line([0.50, 0.50], [0.56, 0.405])
    rough_line([0.25, 0.75], [0.405, 0.405])
    rough_line([0.25, 0.25], [0.405, 0.38])
    rough_line([0.75, 0.75], [0.405, 0.38])

    branches = [
        (0.06, 0.46, "PORTFOLIO MIX?", "customers moved to\ndifferent routes"),
        (0.54, 0.46, "LIST-PRICE YIELD?", "pricing changed inside\na segment"),
        (0.06, 0.305, "APPROVED INVESTMENT?", "intentional lower\ncustomer pricing"),
        (0.54, 0.305, "UNEXPECTED SHORTFALL?", "collected fee below\napproved price"),
    ]
    for x, y, heading, body in branches:
        rough_card(x, y, 0.40, 0.105)
        ax.text(x + 0.20, y + 0.068, heading, ha="center", color=INK, fontsize=14, fontweight="bold")
        ax.text(x + 0.20, y + 0.027, body, ha="center", color=INK, fontsize=11, linespacing=1.15)

    ax.text(0.50, 0.20, "DIAGNOSIS BEFORE ACTION.", ha="center", color=INK, fontsize=24, fontweight="bold")
    rough_line([0.32, 0.68], [0.188, 0.188], 2.0)
    fig.text(0.50, 0.075, "Synthetic transaction data  |  Independent simulation", ha="center", color=INK, fontsize=10)
    fig.text(0.92, 0.035, "Victor Moraes Garlet", ha="right", color=INK, fontsize=10, fontweight="bold")
    save(fig, "episode_01_metric_tree.png")


def build_episode_02():
    fig = plt.figure(figsize=(12, 15), facecolor=WHITE)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rough_card(x, y, width, height, linewidth=2.5):
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=linewidth,
            edgecolor=INK,
            facecolor=WHITE,
        )
        patch.set_sketch_params(scale=1.2, length=90, randomness=2.5)
        ax.add_patch(patch)

    def rough_line(xs, ys, linewidth=2.2):
        line, = ax.plot(xs, ys, color=INK, linewidth=linewidth)
        line.set_sketch_params(scale=1.2, length=90, randomness=2.5)

    fig.text(0.50, 0.955, "30 DAYS INSIDE A EUROPEAN FINTECH  ·  2/8", ha="center", color=INK, fontsize=13, fontweight="bold")
    fig.text(0.50, 0.865, "BEFORE THE FIRST INSIGHT,\nLOCK THE BOUNDARIES.", ha="center", color=INK, fontsize=32, fontweight="bold", linespacing=1.0)
    fig.text(0.50, 0.785, "public fact  ≠  project assumption  ≠  synthetic result", ha="center", color=INK, fontsize=15)

    evidence = [
        (0.055, "PUBLIC FACT", "frames the\nquestion"),
        (0.365, "PROJECT ASSUMPTION", "defines the\nsimulation"),
        (0.675, "SYNTHETIC RESULT", "supports this\ncase only"),
    ]
    for x, heading, body in evidence:
        rough_card(x, 0.585, 0.27, 0.115)
        ax.text(x + 0.135, 0.655, heading, ha="center", color=INK, fontsize=11, fontweight="bold")
        ax.text(x + 0.135, 0.61, body, ha="center", color=INK, fontsize=12, linespacing=1.15)

    rough_line([0.50, 0.50], [0.585, 0.545])
    rough_card(0.10, 0.39, 0.80, 0.13, 3.0)
    ax.text(0.50, 0.475, "METRIC CONTRACT", ha="center", color=INK, fontsize=15, fontweight="bold")
    ax.text(0.50, 0.43, "FORMULA  ·  POPULATION  ·  TIME  ·  GRAIN  ·  OWNER  ·  VALIDATION", ha="center", color=INK, fontsize=12, family="monospace")

    rough_line([0.50, 0.50], [0.39, 0.35])
    rough_card(0.18, 0.235, 0.64, 0.085)
    ax.text(0.50, 0.285, "MODELS SEE EVENTS", ha="center", color=INK, fontsize=15, fontweight="bold")
    ax.text(0.50, 0.252, "not the planted answer key", ha="center", color=INK, fontsize=12)

    ax.text(0.50, 0.155, "AGREE ON THE METRIC BEFORE ACTING.", ha="center", color=INK, fontsize=21, fontweight="bold")
    rough_line([0.29, 0.71], [0.143, 0.143], 2.0)
    fig.text(0.50, 0.075, "Synthetic transaction data  |  Independent simulation", ha="center", color=INK, fontsize=10)
    fig.text(0.92, 0.035, "Victor Moraes Garlet", ha="right", color=INK, fontsize=10, fontweight="bold")
    save(fig, "episode_02_evidence_boundary.png")


def build_episode_03(connection):
    row = fetch_one(
        connection,
        """
        select operations_expected_settlement_usd, carry_out_expected_settlement_usd,
               carry_in_actual_settlement_usd, same_month_settlement_variance_usd,
               finance_actual_settlement_usd, bridge_residual_usd
        from marts.mart_reporting_period_reconciliation
        where reporting_month = date '2026-03-01'
        """,
    )
    start, carry_out, carry_in, variance, finance, residual = row

    fig = plt.figure(figsize=(12, 15), facecolor=WHITE)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rough_card(x, y, width, height, linewidth=2.5):
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=linewidth,
            edgecolor=INK,
            facecolor=WHITE,
        )
        patch.set_sketch_params(scale=1.2, length=90, randomness=2.5)
        ax.add_patch(patch)

    def rough_line(xs, ys, linewidth=2.2):
        line, = ax.plot(xs, ys, color=INK, linewidth=linewidth)
        line.set_sketch_params(scale=1.2, length=90, randomness=2.5)

    fig.text(0.50, 0.955, "30 DAYS INSIDE A EUROPEAN FINTECH  ·  3/8", ha="center", color=INK, fontsize=13, fontweight="bold")
    fig.text(0.50, 0.865, "TWO TOTALS.\nBOTH RIGHT.", ha="center", color=INK, fontsize=36, fontweight="bold", linespacing=1.0)
    fig.text(0.50, 0.785, "March 2026  ·  one ledger, different event clocks", ha="center", color=INK, fontsize=15)

    rough_card(0.08, 0.595, 0.35, 0.125, 3.0)
    ax.text(0.255, 0.675, "OPERATIONS", ha="center", color=INK, fontsize=14, fontweight="bold")
    ax.text(0.255, 0.635, f"${start / 1_000_000:.3f}m", ha="center", color=INK, fontsize=25, fontweight="bold")
    ax.text(0.255, 0.605, "completed in March", ha="center", color=INK, fontsize=12)

    rough_card(0.57, 0.595, 0.35, 0.125, 3.0)
    ax.text(0.745, 0.675, "FINANCE", ha="center", color=INK, fontsize=14, fontweight="bold")
    ax.text(0.745, 0.635, f"${finance / 1_000_000:.3f}m", ha="center", color=INK, fontsize=25, fontweight="bold")
    ax.text(0.745, 0.605, "settled in March", ha="center", color=INK, fontsize=12)

    rough_line([0.255, 0.255], [0.595, 0.555])
    rough_line([0.745, 0.745], [0.595, 0.555])
    rough_line([0.255, 0.745], [0.555, 0.555])
    rough_line([0.50, 0.50], [0.555, 0.52])

    rough_card(0.08, 0.355, 0.84, 0.14, 3.0)
    ax.text(0.50, 0.465, "RECONCILIATION BRIDGE", ha="center", color=INK, fontsize=15, fontweight="bold")
    bridge_items = [
        (0.22, "CARRY OUT", f"-${carry_out / 1_000:.1f}k"),
        (0.50, "CARRY IN", f"+${carry_in / 1_000:.1f}k"),
        (0.78, "VARIANCE", f"-${abs(variance):,.0f}"),
    ]
    for x, heading, amount in bridge_items:
        ax.text(x, 0.415, heading, ha="center", color=INK, fontsize=11, fontweight="bold")
        ax.text(x, 0.378, amount, ha="center", color=INK, fontsize=17, fontweight="bold", family="monospace")
    rough_line([0.355, 0.355], [0.37, 0.44], 1.7)
    rough_line([0.645, 0.645], [0.37, 0.44], 1.7)

    display_residual = 0.0 if abs(residual) < 0.005 else residual
    rough_line([0.50, 0.50], [0.355, 0.32])
    rough_card(0.22, 0.225, 0.56, 0.075)
    ax.text(0.50, 0.265, f"UNEXPLAINED RESIDUAL   ${display_residual:,.2f}", ha="center", color=INK, fontsize=18, fontweight="bold")

    ax.text(0.50, 0.15, "KEEP BOTH CLOCKS. RECONCILE THE DIFFERENCE.", ha="center", color=INK, fontsize=21, fontweight="bold")
    rough_line([0.25, 0.75], [0.138, 0.138], 2.0)
    fig.text(0.50, 0.075, "Synthetic transaction data  |  Independent simulation", ha="center", color=INK, fontsize=10)
    fig.text(0.92, 0.035, "Victor Moraes Garlet", ha="right", color=INK, fontsize=10, fontweight="bold")
    save(fig, "episode_03_two_reporting_clocks.png")


def build_episode_04(connection):
    rows = connection.execute(
        """
        with scoped as (
            select *, corridor_id = 'C13' and provider_id = 'P04' as hotspot
            from intermediate.int_reconciliation_bridge
            where completion_month between date '2026-03-01' and date '2026-05-01'
        )
        select
            case when hotspot then 'C13 + P04' else 'All other routes' end as route_group,
            count(*) as completed_transfers,
            sum(case when is_reconciliation_exception then 1 else 0 end) as exceptions,
            100.0 * avg(case when is_reconciliation_exception then 1.0 else 0 end) as exception_rate
        from scoped
        group by 1
        order by exception_rate desc
        """
    ).fetchall()
    reason_rows = connection.execute(
        """
        select settlement_status, count(*)
        from intermediate.int_reconciliation_bridge
        where corridor_id = 'C13' and provider_id = 'P04'
          and is_reconciliation_exception
          and completion_month between date '2026-03-01' and date '2026-05-01'
        group by settlement_status
        order by count(*) desc
        """
    ).fetchall()

    route_metrics = {row[0]: row for row in rows}
    hotspot = route_metrics["C13 + P04"]
    rest = route_metrics["All other routes"]
    total_transfers = hotspot[1] + rest[1]
    total_exceptions = hotspot[2] + rest[2]
    transfer_share = 100.0 * hotspot[1] / total_transfers
    exception_share = 100.0 * hotspot[2] / total_exceptions
    rate_multiple = hotspot[3] / rest[3]
    reason_counts = {reason: count for reason, count in reason_rows}

    fig = plt.figure(figsize=(12, 15), facecolor=WHITE)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rough_card(x, y, width, height, linewidth=2.5):
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=linewidth,
            edgecolor=INK,
            facecolor=WHITE,
        )
        patch.set_sketch_params(scale=1.2, length=90, randomness=2.5)
        ax.add_patch(patch)

    def rough_line(xs, ys, linewidth=2.2):
        line, = ax.plot(xs, ys, color=INK, linewidth=linewidth)
        line.set_sketch_params(scale=1.2, length=90, randomness=2.5)

    fig.text(0.50, 0.955, "30 DAYS INSIDE A EUROPEAN FINTECH  ·  4/8", ha="center", color=INK, fontsize=13, fontweight="bold")
    fig.text(0.50, 0.865, "ONE ROUTE CARRIED\n34% OF THE EXCEPTIONS.", ha="center", color=INK, fontsize=33, fontweight="bold", linespacing=1.0)
    fig.text(0.50, 0.785, f"{transfer_share:.1f}% of completed transfers  ·  March to May 2026", ha="center", color=INK, fontsize=15)

    rough_card(0.07, 0.555, 0.38, 0.16, 3.0)
    ax.text(0.26, 0.675, "HOTSPOT  ·  C13 + P04", ha="center", color=INK, fontsize=13, fontweight="bold")
    ax.text(0.26, 0.625, f"{hotspot[3]:.1f}%", ha="center", color=INK, fontsize=30, fontweight="bold")
    ax.text(0.26, 0.585, f"{hotspot[2]} exceptions / {hotspot[1]} transfers", ha="center", color=INK, fontsize=12)

    rough_card(0.55, 0.555, 0.38, 0.16, 3.0)
    ax.text(0.74, 0.675, "ALL OTHER ROUTES", ha="center", color=INK, fontsize=13, fontweight="bold")
    ax.text(0.74, 0.625, f"{rest[3]:.1f}%", ha="center", color=INK, fontsize=30, fontweight="bold")
    ax.text(0.74, 0.585, f"{rest[2]} exceptions / {rest[1]:,} transfers", ha="center", color=INK, fontsize=12)

    rough_line([0.45, 0.55], [0.635, 0.635], 2.2)
    ax.text(0.50, 0.655, f"{rate_multiple:.1f}×", ha="center", color=INK, fontsize=15, fontweight="bold")

    rough_card(0.08, 0.345, 0.84, 0.14, 3.0)
    ax.text(0.50, 0.455, f"HOTSPOT BREAKDOWN  ·  {exception_share:.1f}% OF ALL EXCEPTIONS", ha="center", color=INK, fontsize=14, fontweight="bold")
    breakdown = [
        (0.22, reason_counts["amount_mismatch"], "AMOUNT MISMATCH"),
        (0.50, reason_counts["late"], "LATE"),
        (0.78, reason_counts["missing"], "MISSING"),
    ]
    for x, count, label in breakdown:
        ax.text(x, 0.405, f"{count}", ha="center", color=INK, fontsize=24, fontweight="bold")
        ax.text(x, 0.37, label, ha="center", color=INK, fontsize=10, fontweight="bold")
    rough_line([0.355, 0.355], [0.36, 0.43], 1.7)
    rough_line([0.645, 0.645], [0.36, 0.43], 1.7)

    ax.text(0.50, 0.215, "TARGET THE CONTROL, NOT THE WHOLE PORTFOLIO.", ha="center", color=INK, fontsize=21, fontweight="bold")
    rough_line([0.22, 0.78], [0.202, 0.202], 2.0)
    ax.text(0.50, 0.165, "concentration identifies where to investigate  ·  it does not prove the cause", ha="center", color=INK, fontsize=12)
    fig.text(0.50, 0.075, "Synthetic transaction data  |  Independent simulation", ha="center", color=INK, fontsize=10)
    fig.text(0.92, 0.035, "Victor Moraes Garlet", ha="right", color=INK, fontsize=10, fontweight="bold")
    save(fig, "episode_04_reconciliation_hotspot.png")


def build_episode_05(connection):
    rows = connection.execute(
        """
        select component_code, component_label, impact_bps, running_take_rate_bps, is_total
        from marts.mart_take_rate_bridge
        order by component_order
        """
    ).fetchall()
    values = {
        code: {"label": label, "impact": impact, "running": running, "is_total": is_total}
        for code, label, impact, running, is_total in rows
    }
    affected_transfers, leakage_usd = fetch_one(
        connection,
        """
        select affected_transfers, fee_leakage_usd
        from marts.mart_fee_leakage_hotspots
        order by fee_leakage_usd desc
        limit 1
        """,
    )
    total_change = values["comparison"]["impact"] - values["baseline"]["impact"]
    leakage_share = 100.0 * abs(values["fee_leakage"]["impact"] / total_change)

    fig = plt.figure(figsize=(12, 15), facecolor=WHITE)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rough_card(x, y, width, height, linewidth=2.5):
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=linewidth,
            edgecolor=INK,
            facecolor=WHITE,
        )
        patch.set_sketch_params(scale=1.2, length=90, randomness=2.5)
        ax.add_patch(patch)

    def rough_line(xs, ys, linewidth=2.2):
        line, = ax.plot(xs, ys, color=INK, linewidth=linewidth)
        line.set_sketch_params(scale=1.2, length=90, randomness=2.5)

    fig.text(0.50, 0.955, "30 DAYS INSIDE A EUROPEAN FINTECH  ·  5/8", ha="center", color=INK, fontsize=13, fontweight="bold")
    fig.text(0.50, 0.865, "THE KPI FELL 2.18 BPS.\nTHE CAUSES NEEDED DIFFERENT ACTIONS.", ha="center", color=INK, fontsize=30, fontweight="bold", linespacing=1.0)
    fig.text(0.50, 0.785, "weighted H2 2025  →  H1 2026", ha="center", color=INK, fontsize=15)

    rough_card(0.08, 0.615, 0.30, 0.11, 3.0)
    ax.text(0.23, 0.685, "START", ha="center", color=INK, fontsize=12, fontweight="bold")
    ax.text(0.23, 0.64, f"{values['baseline']['impact']:.2f} BPS", ha="center", color=INK, fontsize=26, fontweight="bold")

    rough_line([0.38, 0.62], [0.67, 0.67], 2.7)
    ax.text(0.50, 0.69, f"{total_change:.2f} BPS", ha="center", color=INK, fontsize=17, fontweight="bold")
    ax.text(0.615, 0.67, "→", ha="center", va="center", color=INK, fontsize=22, fontweight="bold")

    rough_card(0.62, 0.615, 0.30, 0.11, 3.0)
    ax.text(0.77, 0.685, "END", ha="center", color=INK, fontsize=12, fontweight="bold")
    ax.text(0.77, 0.64, f"{values['comparison']['impact']:.2f} BPS", ha="center", color=INK, fontsize=26, fontweight="bold")

    components = [
        (0.055, "MIX", values["portfolio_mix"]["impact"], "portfolio shift"),
        (0.285, "LIST YIELD", values["within_cell_yield"]["impact"], "within segment"),
        (0.515, "PRICE INVESTMENT", values["approved_price_investment"]["impact"], "approved"),
        (0.745, "FEE LEAKAGE", values["fee_leakage"]["impact"], "unexpected"),
    ]
    for x, heading, impact, note in components:
        rough_card(x, 0.425, 0.20, 0.115, 3.2 if heading == "FEE LEAKAGE" else 2.2)
        ax.text(x + 0.10, 0.505, heading, ha="center", color=INK, fontsize=10, fontweight="bold")
        ax.text(x + 0.10, 0.465, f"{impact:+.2f}", ha="center", color=INK, fontsize=21, fontweight="bold", family="monospace")
        ax.text(x + 0.10, 0.438, note, ha="center", color=INK, fontsize=9)

    rough_card(0.08, 0.255, 0.38, 0.09, 2.8)
    ax.text(0.27, 0.312, "PROTECT THE PRICE DECISION", ha="center", color=INK, fontsize=13, fontweight="bold")
    ax.text(0.27, 0.277, "evaluate customer and growth outcomes", ha="center", color=INK, fontsize=10)

    rough_card(0.54, 0.255, 0.38, 0.09, 2.8)
    ax.text(0.73, 0.312, "FIX THE CONTROL FAILURE", ha="center", color=INK, fontsize=13, fontweight="bold")
    ax.text(0.73, 0.277, "reconcile records and test before close", ha="center", color=INK, fontsize=10)

    ax.text(0.50, 0.19, f"{leakage_share:.0f}% OF THE NET DECLINE CAME FROM LEAKAGE.", ha="center", color=INK, fontsize=19, fontweight="bold")
    rough_line([0.28, 0.72], [0.177, 0.177], 2.0)
    ax.text(0.50, 0.145, f"{affected_transfers} affected transfers  ·  ${leakage_usd:,.2f} synthetic exposure", ha="center", color=INK, fontsize=10)
    ax.text(0.50, 0.125, "components rounded for display  ·  unrounded bridge residual < 0.000001 bps", ha="center", color=INK, fontsize=9)
    fig.text(0.50, 0.075, "Synthetic transaction data  |  Independent simulation", ha="center", color=INK, fontsize=10)
    fig.text(0.92, 0.035, "Victor Moraes Garlet", ha="right", color=INK, fontsize=10, fontweight="bold")
    save(fig, "episode_05_take_rate_waterfall.png")


def build_episode_06(connection):
    rows = connection.execute(
        """
        select route_group, completed_transfers, instant_transfer_rate * 100,
               provider_cost_rate_bps, support_contact_rate * 100,
               contribution_margin_proxy_bps
        from marts.mart_speed_cost_tradeoff
        order by provider_cost_rate_bps desc
        """
    ).fetchall()
    priority = next(row for row in rows if row[0] == "priority_speed_route")
    other = next(row for row in rows if row[0] == "other_routes")
    instant_gap = priority[2] - other[2]
    cost_gap = priority[3] - other[3]
    contribution_gap = priority[5] - other[5]
    cost_multiple = priority[3] / other[3]
    support_events = round(priority[1] * priority[4] / 100 + other[1] * other[4] / 100)

    fig = plt.figure(figsize=(12, 15), facecolor=WHITE)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rough_card(x, y, width, height, linewidth=2.5):
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=linewidth,
            edgecolor=INK,
            facecolor=WHITE,
        )
        patch.set_sketch_params(scale=1.2, length=90, randomness=2.5)
        ax.add_patch(patch)

    def rough_line(xs, ys, linewidth=2.2):
        line, = ax.plot(xs, ys, color=INK, linewidth=linewidth)
        line.set_sketch_params(scale=1.2, length=90, randomness=2.5)

    fig.text(0.50, 0.955, "30 DAYS INSIDE A EUROPEAN FINTECH  ·  6/8", ha="center", color=INK, fontsize=13, fontweight="bold")
    fig.text(0.50, 0.865, f"98.4% INSTANT.\n{cost_multiple:.1f}× THE COST.", ha="center", color=INK, fontsize=36, fontweight="bold", linespacing=1.0)
    fig.text(0.50, 0.785, "C01  ·  H1 2026  ·  completed transfers", ha="center", color=INK, fontsize=15)

    route_cards = [
        (0.055, "PRIORITY-SPEED ROUTE", priority),
        (0.525, "OTHER ROUTES", other),
    ]
    for x, heading, row in route_cards:
        _, transfers, instant, cost, support, contribution = row
        rough_card(x, 0.485, 0.42, 0.235, 3.0)
        ax.text(x + 0.21, 0.68, heading, ha="center", color=INK, fontsize=13, fontweight="bold")
        ax.text(x + 0.21, 0.635, f"{instant:.1f}% INSTANT", ha="center", color=INK, fontsize=25, fontweight="bold")
        ax.text(x + 0.21, 0.585, f"{cost:.2f} bps cost", ha="center", color=INK, fontsize=15, family="monospace")
        ax.text(x + 0.21, 0.545, f"{contribution:.2f} bps contribution", ha="center", color=INK, fontsize=15, family="monospace")
        ax.text(x + 0.21, 0.505, f"{support:.1f}% support  ·  n={transfers}", ha="center", color=INK, fontsize=11)

    ax.text(0.50, 0.60, "VS", ha="center", va="center", color=INK, fontsize=14, fontweight="bold")

    rough_card(0.07, 0.32, 0.86, 0.105, 2.8)
    tradeoffs = [
        (0.22, f"+{instant_gap:.1f} pp", "INSTANT RATE"),
        (0.50, f"+{cost_gap:.2f} bps", "PROVIDER COST"),
        (0.78, f"{contribution_gap:.2f} bps", "CONTRIBUTION"),
    ]
    for x, value, label in tradeoffs:
        ax.text(x, 0.375, value, ha="center", color=INK, fontsize=20, fontweight="bold", family="monospace")
        ax.text(x, 0.34, label, ha="center", color=INK, fontsize=10, fontweight="bold")
    rough_line([0.355, 0.355], [0.34, 0.40], 1.7)
    rough_line([0.645, 0.645], [0.34, 0.40], 1.7)

    ax.text(0.50, 0.245, "TEST THE TRADE-OFF. DON'T ASSUME THE CAUSE.", ha="center", color=INK, fontsize=21, fontweight="bold")
    rough_line([0.19, 0.81], [0.232, 0.232], 2.0)
    ax.text(0.50, 0.195, "controlled test on eligible, non-urgent transfers", ha="center", color=INK, fontsize=13)
    ax.text(0.50, 0.165, "contribution primary  ·  speed, support and reconciliation as guardrails", ha="center", color=INK, fontsize=11)
    ax.text(0.50, 0.125, f"observational comparison  ·  only {support_events} support events", ha="center", color=INK, fontsize=10)
    fig.text(0.50, 0.075, "Synthetic transaction data  |  Independent simulation", ha="center", color=INK, fontsize=10)
    fig.text(0.92, 0.035, "Victor Moraes Garlet", ha="right", color=INK, fontsize=10, fontweight="bold")
    save(fig, "episode_06_speed_cost_tradeoff.png")


def build_episode_07():
    fig, ax = base_figure(
        7,
        "An insight is unfinished until\nsomeone knows what to change.",
        "Observed controls become actions. Descriptive trade-offs become experiments.",
    )
    matrix = fig.add_axes((0.14, 0.22, 0.72, 0.50), facecolor=WHITE)
    matrix.set_xlim(0, 10)
    matrix.set_ylim(0, 10)
    matrix.spines[:].set_color(INK)
    matrix.axvline(5, color=LINE, linewidth=1.5)
    matrix.axhline(5, color=LINE, linewidth=1.5)
    matrix.set_xticks([])
    matrix.set_yticks([])
    matrix.set_xlabel("Implementation effort  →", color=MUTED, labelpad=16)
    matrix.set_ylabel("Decision confidence  →", color=MUTED, labelpad=16)
    matrix.text(0.3, 9.4, "ACT NOW", color=PURPLE, fontsize=11, fontweight="bold")
    matrix.text(5.3, 9.4, "PLAN AND CONTROL", color=INK, fontsize=11, fontweight="bold")
    matrix.text(0.3, 4.4, "MONITOR", color=MUTED, fontsize=11, fontweight="bold")
    matrix.text(5.3, 4.4, "TEST BEFORE SCALING", color=ORANGE, fontsize=11, fontweight="bold")

    actions = [
        (2.0, 8.1, "Fix C07 pricing\nconfiguration", PURPLE),
        (6.7, 7.4, "Repair C13/P04\nsettlement control", INK),
        (6.8, 2.3, "Run C01 routing\nexperiment", ORANGE),
        (2.2, 2.0, "Watch portfolio\nmix", MUTED),
    ]
    for x, y, label, color in actions:
        matrix.scatter(x, y, s=460, color=color, edgecolor=INK, linewidth=1.3, zorder=3)
        matrix.text(x, y - 0.85, label, ha="center", va="top", fontsize=10, color=INK, fontweight="bold")
    fig.text(0.50, 0.13, "Recommendation: stop the known leak first. Test the routing hypothesis second.", ha="center", color=INK, fontsize=16, fontweight="bold")
    save(fig, "episode_07_decision_matrix.png")


def build_episode_08(connection):
    leakage = fetch_one(connection, "select fee_leakage_usd from marts.mart_fee_leakage_hotspots limit 1")[0]
    scenario = fetch_one(
        connection,
        """
        select estimated_contribution_margin_uplift_usd,
               instant_rate_change_percentage_points,
               support_rate_change_percentage_points
        from marts.mart_routing_scenario
        """,
    )
    hotspot = fetch_one(
        connection,
        """
        select 100.0 * avg(case when is_reconciliation_exception then 1.0 else 0 end)
        from intermediate.int_reconciliation_bridge
        where corridor_id = 'C13' and provider_id = 'P04'
          and completion_month between date '2026-03-01' and date '2026-05-01'
        """,
    )[0]

    fig, ax = base_figure(
        8,
        "What I would put in front of a\nfintech leadership team.",
        "One decision page: evidence, action, test and guardrails.",
    )
    card(ax, 0.07, 0.60, 0.86, 0.14, PURPLE_SOFT)
    ax.text(0.11, 0.70, "DECISION", color=PURPLE, fontsize=10, fontweight="bold")
    ax.text(0.11, 0.655, "Protect unit economics without masking\nintentional price investment.", color=INK, fontsize=18, fontweight="bold", linespacing=1.25)

    cards = [
        (0.07, 0.37, "ACT NOW", f"Recover the ${leakage:,.0f}\npricing leakage pattern", PURPLE_SOFT, PURPLE),
        (0.365, 0.37, "CONTROL", f"Repair the route with a\n{hotspot:.1f}% exception rate", WHITE, INK),
        (0.66, 0.37, "TEST", f"25% reroute scenario\n+${scenario[0]:,.0f} contribution", ORANGE_SOFT, ORANGE),
    ]
    for x, y, tag, body, fill, accent in cards:
        card(ax, x, y, 0.27, 0.17, fill)
        ax.text(x + 0.025, y + 0.125, tag, color=accent, fontsize=10, fontweight="bold")
        ax.text(x + 0.025, y + 0.055, body, color=INK, fontsize=13, fontweight="bold", linespacing=1.35)

    card(ax, 0.07, 0.16, 0.86, 0.15, WHITE)
    ax.text(0.11, 0.265, "EXPERIMENT GUARDRAILS", color=ORANGE, fontsize=10, fontweight="bold")
    ax.text(0.11, 0.215, f"Instant rate\n{scenario[1]:+.2f} pp", color=INK, fontsize=13, fontweight="bold", linespacing=1.35)
    ax.text(0.40, 0.215, f"Support rate\n{scenario[2]:+.2f} pp", color=INK, fontsize=13, fontweight="bold", linespacing=1.35)
    ax.text(0.69, 0.215, "Reconciliation\nno worse", color=INK, fontsize=13, fontweight="bold", linespacing=1.35)
    ax.text(0.11, 0.18, "The scenario is a hypothesis. Ship only after a controlled test clears the guardrails.", color=MUTED, fontsize=11)
    save(fig, "episode_08_executive_decision.png")


def main() -> int:
    if not WAREHOUSE_PATH.exists():
        raise SystemExit("Warehouse not found. Run `make dbt-build` first.")
    with duckdb.connect(str(WAREHOUSE_PATH), read_only=True) as connection:
        build_episode_01(connection)
        build_episode_02()
        build_episode_03(connection)
        build_episode_04(connection)
        build_episode_05(connection)
        build_episode_06(connection)
        build_episode_07()
        build_episode_08(connection)
    print(f"Created 8 visuals in {OUTPUT_DIRECTORY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
