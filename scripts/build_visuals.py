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
    deltas = [-carry_out, carry_in, variance]
    labels = ["Operations\ncompletion cohort", "Carry out", "Carry in", "Same-month\nvariance", "Finance\nsettlement view"]

    fig, _ = base_figure(
        3,
        "Finance and Operations were\nboth right.",
        "March 2026 uses two valid event clocks. A bridge makes them comparable.",
    )
    ax = fig.add_axes((0.10, 0.22, 0.82, 0.48), facecolor=PAPER)
    ax.spines[:].set_visible(False)
    ax.tick_params(axis="x", length=0, labelsize=10)
    ax.tick_params(axis="y", colors=MUTED)
    ax.grid(axis="y", color=LINE, linewidth=0.8, alpha=0.7)

    positions = range(5)
    running = start
    ax.bar(0, start / 1_000_000, color=PURPLE, width=0.62)
    ax.text(0, start / 1_000_000 + 0.08, f"${start / 1_000_000:.2f}m", ha="center", fontweight="bold")
    for i, delta in enumerate(deltas, start=1):
        next_value = running + delta
        bottom = min(running, next_value) / 1_000_000
        height = max(abs(delta) / 1_000_000, 0.018)
        color = ORANGE if delta < 0 else PURPLE
        ax.bar(i, height, bottom=bottom, color=color, width=0.62)
        label = f"{delta / 1_000_000:+.2f}m" if abs(delta) >= 10_000 else f"{delta:+,.0f}"
        ax.text(i, bottom + height + 0.08, label, ha="center", color=color, fontweight="bold")
        ax.plot([i - 0.69, i - 0.31], [running / 1_000_000, running / 1_000_000], color=MUTED, linewidth=1)
        running = next_value
    ax.bar(4, finance / 1_000_000, color=INK, width=0.62)
    ax.text(4, finance / 1_000_000 + 0.08, f"${finance / 1_000_000:.2f}m", ha="center", fontweight="bold")
    ax.set_xticks(list(positions), labels)
    ax.set_ylabel("USD millions", color=MUTED)
    ax.set_ylim(0, max(start, finance) / 1_000_000 + 0.7)
    display_residual = 0.0 if abs(residual) < 0.005 else residual
    fig.text(0.50, 0.13, f"Bridge residual: ${display_residual:,.2f}", ha="center", color=PURPLE, fontsize=20, fontweight="bold")
    fig.text(0.50, 0.095, "Different timestamps created the disagreement. The accounting still closes.", ha="center", color=MUTED, fontsize=12)
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

    fig, _ = base_figure(
        4,
        "The transfer completed. The money\nstill did not reconcile.",
        "One corridor-provider pair made the control problem visible.",
    )
    ax = fig.add_axes((0.13, 0.42, 0.74, 0.30), facecolor=PAPER)
    groups = [row[0] for row in rows]
    rates = [row[3] for row in rows]
    bars = ax.bar(groups, rates, color=[ORANGE, PURPLE], width=0.55)
    ax.spines[:].set_visible(False)
    ax.grid(axis="y", color=LINE, linewidth=0.8)
    ax.set_ylabel("Exception rate", color=MUTED)
    ax.set_ylim(0, 45)
    ax.set_yticks([0, 10, 20, 30, 40], ["0%", "10%", "20%", "30%", "40%"])
    ax.tick_params(axis="x", length=0, labelsize=12)
    for bar, row in zip(bars, rows):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2, f"{row[3]:.1f}%\n{row[2]:.0f} exceptions", ha="center", fontweight="bold", color=INK)

    card_ax = fig.add_axes((0.11, 0.16, 0.78, 0.17))
    card_ax.set_xlim(0, 1)
    card_ax.set_ylim(0, 1)
    card_ax.axis("off")
    card(card_ax, 0, 0, 1, 1, WHITE)
    card_ax.text(0.05, 0.75, "HOTSPOT BREAKDOWN", color=ORANGE, fontsize=10, fontweight="bold")
    x_positions = [0.18, 0.50, 0.82]
    for x, (reason, count) in zip(x_positions, reason_rows):
        card_ax.text(x, 0.42, f"{count}", ha="center", color=INK, fontsize=24, fontweight="bold")
        card_ax.text(x, 0.18, reason.replace("_", " ").title(), ha="center", color=MUTED, fontsize=10)
    save(fig, "episode_04_reconciliation_hotspot.png")


def build_episode_05(connection):
    rows = connection.execute(
        """
        select component_code, component_label, impact_bps, running_take_rate_bps, is_total
        from marts.mart_take_rate_bridge
        order by component_order
        """
    ).fetchall()
    fig, _ = base_figure(
        5,
        "Where did the basis points go?",
        "H2 2025 baseline to H1 2026 comparison, weighted by transfer volume.",
    )
    ax = fig.add_axes((0.10, 0.22, 0.82, 0.49), facecolor=PAPER)
    ax.spines[:].set_visible(False)
    ax.grid(axis="y", color=LINE, linewidth=0.8)
    ax.tick_params(axis="x", length=0, labelsize=9)
    ax.tick_params(axis="y", colors=MUTED)

    x = list(range(len(rows)))
    bottoms = []
    heights = []
    colors = []
    labels = []
    prior = 0.0
    for code, label, impact, running, is_total in rows:
        labels.append(label.replace(" collected", "\ncollected").replace(" price", "\nprice").replace(" configuration", "\nconfiguration"))
        if is_total:
            bottoms.append(0)
            heights.append(impact)
            colors.append(INK if code == "comparison" else PURPLE)
        else:
            bottoms.append(min(prior, running))
            heights.append(abs(impact))
            colors.append(PURPLE if impact >= 0 or code == "approved_price_investment" else ORANGE)
        prior = running
    bars = ax.bar(x, heights, bottom=bottoms, color=colors, width=0.66)
    for i in range(1, len(rows) - 1):
        previous_running = rows[i - 1][3]
        ax.plot([i - 0.67, i - 0.33], [previous_running, previous_running], color=MUTED, linewidth=1)
    for bar, row in zip(bars, rows):
        code, _, impact, running, is_total = row
        label = f"{impact:.2f}" if is_total else f"{impact:+.2f}"
        y = bar.get_y() + bar.get_height() + 0.22
        ax.text(bar.get_x() + bar.get_width() / 2, y, label, ha="center", fontweight="bold", color=ORANGE if code == "fee_leakage" else INK)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Basis points", color=MUTED)
    ax.set_ylim(0, 55)
    fig.text(0.50, 0.135, "-2.18 bps total  |  -1.67 bps from one pricing configuration issue", ha="center", color=INK, fontsize=17, fontweight="bold")
    save(fig, "episode_05_take_rate_waterfall.png")


def build_episode_06(connection):
    rows = connection.execute(
        """
        select route_group, instant_transfer_rate * 100, provider_cost_rate_bps,
               support_contact_rate * 100, contribution_margin_proxy_bps, volume_usd
        from marts.mart_speed_cost_tradeoff
        order by provider_cost_rate_bps desc
        """
    ).fetchall()
    fig, _ = base_figure(
        6,
        "Faster transfers can still be the\nwrong operational choice.",
        "The fastest route wins on speed. The decision changes when cost enters the frame.",
    )
    ax = fig.add_axes((0.13, 0.31, 0.74, 0.40), facecolor=PAPER)
    ax.spines[:].set_visible(False)
    ax.grid(color=LINE, linewidth=0.8)
    for route, instant, cost, support, contribution, volume in rows:
        color = ORANGE if route == "priority_speed_route" else PURPLE
        label = "Priority speed route" if route == "priority_speed_route" else "Other routes"
        ax.scatter(cost, instant, s=volume / 320, color=color, edgecolor=INK, linewidth=1.3, alpha=0.95)
        offset = (0.55, -2.7) if route == "priority_speed_route" else (0.55, 1.0)
        ax.text(cost + offset[0], instant + offset[1], f"{label}\n{instant:.1f}% instant  |  {cost:.1f} bps cost", color=INK, fontsize=11, fontweight="bold")
    ax.set_xlabel("Provider cost rate (bps)", color=MUTED)
    ax.set_ylabel("Instant transfer rate", color=MUTED)
    ax.set_yticks([80, 85, 90, 95, 100], ["80%", "85%", "90%", "95%", "100%"])
    ax.set_xlim(5, 25)
    ax.set_ylim(78, 101)

    priority = next(row for row in rows if row[0] == "priority_speed_route")
    other = next(row for row in rows if row[0] == "other_routes")
    fig.text(0.12, 0.20, f"+{priority[1] - other[1]:.1f} pp", color=PURPLE, fontsize=26, fontweight="bold")
    fig.text(0.12, 0.17, "instant speed", color=MUTED, fontsize=11)
    fig.text(0.43, 0.20, f"+{priority[2] - other[2]:.1f} bps", color=ORANGE, fontsize=26, fontweight="bold")
    fig.text(0.43, 0.17, "provider cost", color=MUTED, fontsize=11)
    fig.text(0.73, 0.20, f"{priority[4] - other[4]:.1f} bps", color=ORANGE, fontsize=26, fontweight="bold")
    fig.text(0.73, 0.17, "contribution gap", color=MUTED, fontsize=11)
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
