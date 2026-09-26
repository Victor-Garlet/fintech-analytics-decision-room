"""Build the case illustrations used by README.md from the local analytical model.

The figures are SVG so the text remains selectable and the repository can show
them directly. Run this after the dbt build when reported metrics change.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/warehouse/fintech_analytics.duckdb"
OUT = ROOT / "assets"
W = 1200

INK = "#14273B"
MUTED = "#516477"
BG = "#F7FAFC"
WHITE = "#FFFFFF"
LINE = "#C8D5DD"
TEAL = "#087F76"
BLUE = "#2D628F"
AMBER = "#B86D28"
RED = "#C34745"


class Art:
    def __init__(self, title: str, description: str, height: int):
        self.height = height
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-labelledby="title desc">',
            f"<title id=\"title\">{escape(title)}</title>",
            f"<desc id=\"desc\">{escape(description)}</desc>",
            '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M1 1 L8 4.5 L1 8" fill="none" stroke="#91A4B3" stroke-width="1.7"/></marker></defs>',
            f'<rect width="{W}" height="{height}" fill="{BG}"/>',
            f'<rect x="0" y="0" width="7" height="{height}" fill="{TEAL}"/>',
        ]

    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, radius=15, stroke_width=1.5):
        self.items.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    def text(self, x, y, value, size=20, color=INK, weight=400, anchor="start"):
        self.items.append(
            f'<text x="{x}" y="{y}" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'
        )

    def path(self, d, color=LINE, width=2, arrow=False, dash=None):
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        dashed = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{marker}{dashed}/>'
        )

    def circle(self, x, y, r, fill):
        self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def heading(self, eyebrow, title, subtitle):
        self.text(52, 37, eyebrow.upper(), 13, TEAL, 700)
        self.text(52, 72, title, 28, INK, 700)
        self.text(52, 100, subtitle, 16, MUTED)

    def save(self, filename):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / filename).write_text("\n".join([*self.items, "</svg>", ""]), encoding="utf-8")


def node(art, x, y, w, h, title, detail, accent=BLUE):
    art.rect(x, y, w, h, WHITE, LINE)
    art.rect(x, y, 6, h, accent, accent, 3, 0)
    art.text(x + 17, y + 34, title, 19, INK, 700)
    art.text(x + 17, y + 61, detail, 15, MUTED)


def data_map(con):
    counts = {
        table: con.execute(f"select count(*) from raw.{table}").fetchone()[0]
        for table in ("customers", "quotes", "transfers", "fees", "settlements")
    }
    art = Art(
        "Synthetic dataset relationship map",
        "Customers lead to quotes and transfer attempts. Completed transfers have fee, cost and settlement records; support and refunds are optional. Corridors, providers and pricing rules are reference data.",
        455,
    )
    art.heading("02 / Evidence", "A generated business, connected at transfer level", "Eleven source tables, with keys and event grains documented in the data dictionary.")
    node(art, 54, 179, 170, 82, "Customers", f"{counts['customers']:,} records", TEAL)
    node(art, 281, 179, 170, 82, "Quotes", f"{counts['quotes']:,} records", TEAL)
    node(art, 510, 179, 205, 82, "Transfers", f"{counts['transfers']:,} attempts", INK)
    node(art, 803, 126, 335, 72, "Fees + pricing", f"{counts['fees']:,} completed outcomes", AMBER)
    node(art, 803, 215, 335, 72, "Cost + settlements", f"{counts['settlements']:,} settlement records", BLUE)
    node(art, 803, 304, 335, 72, "Support + refunds", "Optional transfer outcomes", BLUE)
    art.path("M224 220 H272", arrow=True)
    art.path("M451 220 H500", arrow=True)
    art.path("M715 220 H750 V162 H793", arrow=True)
    art.path("M715 220 H793", arrow=True)
    art.path("M715 220 H750 V340 H793", arrow=True)
    art.rect(54, 374, 661, 49, "#EAF2F5", "#EAF2F5", 9, 0)
    art.text(73, 405, "Reference tables: 20 corridors · 6 providers · 80 pricing rules", 16, MUTED)
    art.save("02-data-model.svg")


def two_clocks(con):
    cross_month = con.execute(
        """select count(*)
           from raw.transfers t join raw.settlements s using (transfer_id)
           where s.settled_at is not null
             and date_trunc('month', t.completed_at) <> date_trunc('month', s.settled_at)"""
    ).fetchone()[0]
    art = Art(
        "Two reporting clocks",
        "An illustrative transfer completes in June and settles in July. Operations counts its completion in June, while Finance counts the settlement in July. The generated dataset contains cross-month transfers.",
        395,
    )
    art.heading("03 / Metric contract", "One transfer, two valid reporting months", "Illustrative timing example. The event timestamp determines the reporting period.")
    art.text(121, 158, "JUNE", 17, BLUE, 700)
    art.text(1005, 158, "JULY", 17, BLUE, 700)
    art.path("M126 189 H1070", "#9FB0BD", 4, arrow=True)
    art.circle(298, 189, 11, TEAL)
    art.circle(888, 189, 11, BLUE)
    art.text(298, 151, "Completed 30 Jun", 19, INK, 700, "middle")
    art.text(888, 151, "Settled 2 Jul", 19, INK, 700, "middle")
    art.rect(127, 233, 345, 77, WHITE, LINE)
    art.text(148, 265, "Operations", 18, INK, 700)
    art.text(148, 290, "Completion cohort: June", 17, TEAL)
    art.rect(720, 233, 345, 77, WHITE, LINE)
    art.text(741, 265, "Finance", 18, INK, 700)
    art.text(741, 290, "Settlement period: July", 17, BLUE)
    art.text(52, 364, f"{cross_month:,} records in this synthetic snapshot cross a completion-month boundary.", 16, MUTED)
    art.save("03-two-clocks.svg")


def model_flow(con):
    raw = con.execute("select count(*) from information_schema.tables where table_schema='raw'").fetchone()[0]
    marts = con.execute("select count(*) from information_schema.tables where table_schema='marts'").fetchone()[0]
    art = Art(
        "Analytical model flow",
        "Eleven source CSV tables load into DuckDB raw tables, pass through typed dbt staging and two intermediate views, then form ten decision-facing marts. Automated data tests check relationships and reconciliations.",
        390,
    )
    art.heading("04 / Build", "From source records to a number a reader can challenge", "Each layer has a job. Tests guard the hand-offs and the decision metrics.")
    boxes = [
        (52, "CSV snapshot", f"{raw} source tables", TEAL),
        (288, "DuckDB raw", "Faithful local load", BLUE),
        (524, "dbt staging", "Typed source views", BLUE),
        (760, "Intermediate", "Event + fee logic", BLUE),
        (996, "Decision marts", f"{marts} output tables", TEAL),
    ]
    for x, title, detail, accent in boxes:
        node(art, x, 164, 191, 89, title, detail, accent)
    for x in (243, 479, 715, 951):
        art.path(f"M{x} 207 H{x+36}", arrow=True)
    art.rect(52, 286, 1135, 70, "#EAF2F5", "#EAF2F5", 12, 0)
    art.text(75, 316, "Quality gate", 18, TEAL, 700)
    art.text(75, 341, "168 dbt data tests · 23 models · 191/191 build steps passed in the recorded validation run", 17, INK)
    art.save("04-model-flow.svg")


def bridge(con):
    rows = con.execute(
        """select component_code, component_label, impact_bps
           from marts.mart_take_rate_bridge order by component_order"""
    ).fetchall()
    by_code = {code: (label, value) for code, label, value in rows}
    baseline = by_code["baseline"][1]
    final = by_code["comparison"][1]
    art = Art(
        "Synthetic take-rate decomposition",
        "Collected take rate moves from 50.23 to 48.05 basis points. Portfolio mix contributes plus 0.09, within-cell list yield minus 0.02, approved price investment minus 0.57 and fee leakage minus 1.67 basis points.",
        495,
    )
    art.heading("05 / Diagnosis", "A 2.18 bp fall is made of different decisions", "H2 2025 compared with H1 2026. Signed impacts in basis points; all findings are synthetic.")
    art.rect(52, 124, 1096, 69, WHITE, LINE)
    art.text(76, 153, "START", 12, MUTED, 700)
    art.text(76, 180, f"{baseline:.2f} bps", 25, INK, 700)
    art.text(1123, 153, "END", 12, MUTED, 700, "end")
    art.text(1123, 180, f"{final:.2f} bps", 25, INK, 700, "end")
    art.path("M315 159 H866", "#A8B8C3", 2, arrow=True)
    labels = {
        "portfolio_mix": ("Portfolio mix", BLUE),
        "within_cell_yield": ("List-price yield", BLUE),
        "approved_price_investment": ("Approved price investment", TEAL),
        "fee_leakage": ("Unexpected fee leakage", RED),
    }
    zero = 1030
    scale = 415
    for idx, code in enumerate(labels):
        label, color = labels[code]
        value = by_code[code][1]
        y = 238 + idx * 58
        art.text(67, y + 4, label, 18, INK, 600)
        length = abs(value) * scale
        x = zero if value >= 0 else zero - length
        art.rect(round(x, 2), y - 15, round(max(3, length), 2), 26, color, color, 5, 0)
        art.text(1115, y + 4, f"{value:+.2f}", 18, color, 700, "end")
    art.path("M1030 215 V430", "#738A9C", 1.5)
    art.text(52, 472, "Approved lower prices stay. The configuration shortfall is the part to correct.", 17, MUTED)
    art.save("05-take-rate-bridge.svg")


def decision(con):
    fee = con.execute("select sum(fee_leakage_usd) from marts.mart_fee_leakage_hotspots").fetchone()[0]
    scenario = con.execute(
        """select estimated_contribution_margin_uplift_usd,
                  instant_rate_change_percentage_points,
                  support_rate_change_percentage_points
           from marts.mart_routing_scenario"""
    ).fetchone()
    hotspot = con.execute(
        """select count(*), sum(case when s.is_reconciliation_exception then 1 else 0 end)
           from raw.transfers t join raw.settlements s using (transfer_id)
           where t.completed_at >= '2026-03-01' and t.completed_at < '2026-06-01'
             and t.corridor_id='C13' and t.provider_id='P04'"""
    ).fetchone()
    rate = 100 * hotspot[1] / hotspot[0]
    art = Art(
        "Evidence-to-action decision map",
        "The synthetic case recommends correcting the C07 pricing fault, repairing the C13/P04 settlement control and testing the C01 routing hypothesis before a policy change.",
        450,
    )
    art.heading("06 / Decision", "Two fixes. One question for an experiment.", "The action depends on how directly the evidence supports it.")
    entries = [
        (126, TEAL, "FIX NOW", "C07 business pricing rule", f"${fee:,.2f} synthetic leakage", "Direct fee-record evidence"),
        (225, BLUE, "CONTROL NOW", "C13 / P04 settlement route", f"{rate:.1f}% exceptions", "Direct settlement-record evidence"),
        (324, AMBER, "TEST FIRST", "C01 provider routing", f"+${scenario[0]:,.0f} margin proxy", f"Scenario: {scenario[1]:+.2f} pp instant · {scenario[2]:+.2f} pp support"),
    ]
    for y, color, action, title, metric, detail in entries:
        art.rect(52, y, 1096, 82, WHITE, LINE)
        art.rect(52, y, 8, 82, color, color, 3, 0)
        art.text(78, y + 26, action, 13, color, 700)
        art.text(78, y + 56, title, 21, INK, 700)
        art.text(635, y + 39, metric, 21, color, 700)
        art.text(635, y + 65, detail, 15, MUTED)
    art.text(52, 433, "Routing estimates use observed averages. They are a reason to test, not a causal forecast.", 16, MUTED)
    art.save("06-decision-map.svg")


def main():
    con = duckdb.connect(str(DB), read_only=True)
    try:
        data_map(con)
        two_clocks(con)
        model_flow(con)
        bridge(con)
        decision(con)
    finally:
        con.close()
    print("Built 5 README visuals in assets/")


if __name__ == "__main__":
    main()
