"""
Feyenoord opposition analysis, landscape 16:9 presentation deck.
Fuses data-rich figures with an analyst INSIGHT rail + recommendations,
weekly player-comms plan, and authentic video-clip references.
"""
import os
import json
import textwrap
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle

import theme as T
import report_content as C

T.apply()
ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG = os.path.join(ROOT, "output", "figures")
OUT_PDF = os.path.join(ROOT, "output", "Feyenoord_Opposition_Deck.pdf")
EMBLEM = os.path.join(FIG, "emblem.png")
with open(os.path.join(ROOT, "output", "metrics.json"), encoding="utf-8") as f:
    MET = json.load(f)
with open(os.path.join(ROOT, "output", "metrics_ext.json"), encoding="utf-8") as f:
    EXT = json.load(f)

W_IN, H_IN = 13.333, 7.5          # 16:9
MX = 0.045
ASP = H_IN / W_IN


def new_slide():
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, color=T.INK, zorder=-10))
    return fig, ax


def panel(ax, x, y, w, h, color=T.PANEL, ec=T.LINE, lw=1.0, r=0.014, alpha=1.0, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=color, ec=ec, lw=lw, alpha=alpha, zorder=z,
                                mutation_aspect=ASP))


def H(ax, x, y, s, size, color=T.TEXT, weight="bold", ha="left", va="baseline",
      font=T.HEAD_FONT, z=5, alpha=1.0):
    return ax.text(x, y, s, fontsize=size, color=color, fontfamily=font,
                   weight=weight, ha=ha, va=va, zorder=z, alpha=alpha)


def P(ax, x, y, s, size=9.2, color=T.TEXT, ha="left", va="top", width=60, z=5,
      leading=1.34):
    wrapped = "\n".join(textwrap.fill(ln, width=width) for ln in s.split("\n"))
    return ax.text(x, y, wrapped, fontsize=size, color=color, ha=ha, va=va,
                   zorder=z, fontfamily=T.BODY_FONT, linespacing=leading)


def emblem(fig, box):
    img = mpimg.imread(EMBLEM)
    x0, y0, x1, y1 = box
    side = min((x1 - x0), (y1 - y0) / ASP)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = side; h = side / ASP
    a = fig.add_axes([cx - w / 2, cy - h / 2, w, h]); a.imshow(img); a.axis("off")


def header(ax, fig, kicker, title, n):
    ax.add_patch(Rectangle((0, 0.9), 1, 0.1, color=T.PANEL, zorder=0))
    ax.add_patch(Rectangle((0, 0.9), 1, 0.006, color=T.FEY, zorder=2))
    ax.add_patch(Rectangle((MX, 0.918), 0.012, 0.052, color=T.FEY, zorder=3))
    H(ax, MX + 0.022, 0.957, kicker.upper(), 10.5, T.FEY, va="center")
    H(ax, MX + 0.022, 0.927, title, 19, T.TEXT, va="center")
    emblem(fig, (1 - MX - 0.044, 0.912, 1 - MX, 0.988))
    H(ax, 1 - MX - 0.055, 0.945, "FEYENOORD", 10, T.MUTE, ha="right", va="center", alpha=0.8)


def footer(ax, n):
    H(ax, MX, 0.022, "FEYENOORD · OPPOSITION ANALYSIS", 7.5, T.FAINT, va="center")
    H(ax, 0.5, 0.022, f"Prepared by {C.AUTHOR}  ·  Club Brugge Analysis Department",
      7.5, T.FAINT, ha="center", va="center", weight="normal", font=T.BODY_FONT)
    H(ax, 1 - MX, 0.022, f"{n:02d}", 8.5, T.MUTE, ha="right", va="center")


def place_image(fig, path, box):
    x0, y0, x1, y1 = box
    img = mpimg.imread(path)
    ih, iw = img.shape[0], img.shape[1]
    ar = iw / ih
    bw, bh = (x1 - x0) * W_IN, (y1 - y0) * H_IN
    if ar > bw / bh:
        nw = (x1 - x0); nh = nw * W_IN / ar / H_IN
    else:
        nh = (y1 - y0); nw = nh * H_IN * ar / W_IN
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = fig.add_axes([cx - nw / 2, cy - nh / 2, nw, nh]); a.imshow(img); a.axis("off")


def bullets(ax, x, y, items, size=9, gap=0.05, width=44, mcolor=T.FEY, color=T.TEXT):
    yy = y
    for it in items:
        ax.text(x, yy, "▶", fontsize=size - 1.5, color=mcolor, va="top",
                fontfamily="DejaVu Sans", zorder=6)
        w = textwrap.fill(it, width=width)
        ax.text(x + 0.016, yy, w, fontsize=size, color=color, va="top", zorder=6,
                fontfamily=T.BODY_FONT, linespacing=1.3)
        yy -= gap * (1 + w.count("\n") * 0.62) + 0.006
    return yy


def insight_rail(ax, x, y, w, h, headline, points, accent=T.FEY, kicker="KEY INSIGHT"):
    panel(ax, x, y, w, h, color=T.PANEL_2, ec=T.LINE)
    ax.add_patch(Rectangle((x, y + h - 0.006), w, 0.006, color=accent, zorder=2))
    H(ax, x + 0.02, y + h - 0.05, kicker, 9.5, accent, va="center")
    hh = textwrap.fill(headline, width=int(w * 102))
    ax.text(x + 0.02, y + h - 0.082, hh, fontsize=13, color=T.TEXT, va="top",
            fontfamily=T.HEAD_FONT, weight="bold", zorder=6, linespacing=1.08)
    yy = y + h - 0.082 - (hh.count("\n") + 1) * 0.038 - 0.03
    bullets(ax, x + 0.02, yy, points, size=9.2, gap=0.03, width=int(w * 138))


def chip_row(ax, x, y, w, items, vcolor=T.GOAL, vsize=17, lsize=7):
    n = len(items); cw = w / n
    for i, (val, lab) in enumerate(items):
        cx = x + cw * (i + 0.5)
        H(ax, cx, y, str(val), vsize, vcolor, ha="center", va="center")
        ax.text(cx, y - 0.04, lab.upper(), fontsize=lsize, color=T.MUTE, ha="center",
                va="center", fontfamily=T.BODY_FONT, zorder=5)
        if i:
            ax.plot([x + cw * i, x + cw * i], [y - 0.046, y + 0.034], color=T.LINE, lw=0.8)


def short(name):
    parts = name.split()
    if len(parts) >= 2 and parts[-2].lower() in ("da", "de", "van", "der", "dos"):
        return " ".join(parts[-2:])
    return parts[-1] if parts else name


# ===========================================================================
def s_title(pdf):
    fig, ax = new_slide()
    ax.add_patch(Rectangle((0, 0), 1, 1, color=T.INK, zorder=-10))
    ax.add_patch(Rectangle((0, 0.86), 1, 0.14, color=T.PANEL, zorder=0))
    ax.add_patch(Rectangle((0, 0.86), 1, 0.006, color=T.FEY, zorder=2))
    ax.add_patch(Rectangle((MX, 0.892), 0.035, 0.07, color=T.FEY, zorder=3))
    H(ax, MX + 0.05, 0.927, "CLUB BRUGGE · ANALYSIS DEPARTMENT", 13, T.CB_BLUE, va="center")
    emblem(fig, (0.70, 0.30, 0.95, 0.78))
    H(ax, MX, 0.66, "OPPOSITION ANALYSIS", 22, T.MUTE, weight="bold")
    H(ax, MX, 0.50, "FEYENOORD", 70, T.TEXT, weight="bold")
    ax.add_patch(Rectangle((MX, 0.45), 0.55, 0.004, color=T.FEY, zorder=2))
    P(ax, MX, 0.40, C.EXEC_HEADLINE, size=14, color=T.TEXT, width=58, va="top")
    panel(ax, MX, 0.135, 0.62, 0.105, color=T.PANEL)
    H(ax, MX + 0.02, 0.215, "SCOUTING WINDOW", 9, T.FEY, va="center")
    P(ax, MX + 0.02, 0.193, C.DATA_WINDOW, size=10, color=T.TEXT, width=82, va="top")
    P(ax, MX + 0.02, 0.165, C.SOURCE, size=7.3, color=T.MUTE, width=104, va="top")
    H(ax, 1 - MX, 0.20, "PREPARED BY", 9, T.FAINT, ha="right", va="center")
    H(ax, 1 - MX, 0.16, C.AUTHOR, 16, T.TEXT, ha="right", va="center")
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def s_exec(pdf):
    fig, ax = new_slide()
    header(ax, fig, "Executive summary", "The 60-second briefing", 2)
    # profile chips
    panel(ax, MX, 0.74, 1 - 2 * MX, 0.1)
    r = MET["record"]; a = MET["attack"]; d = MET["defense"]
    chip_row(ax, MX + 0.01, 0.79, 1 - 2 * MX - 0.02, [
        (f"{r['W']}-{r['D']}-{r['L']}", "W-D-L"), (f"{r['gf']}-{r['ga']}", "goals"),
        ("58%", "possession"), (a["shots_pg"], "shots/game"), (a["xg_pg"], "xG/game"),
        (r["gf"], "goals (18.3 xG)"), (d["shots_conceded_pg"], "shots conceded/g"),
        (d["xga_pg"], "xGA/game")], vcolor=T.TEXT, vsize=17)
    # five keys, two columns
    H(ax, MX, 0.69, "FIVE THINGS THAT DECIDE THE GAME", 13, T.TEXT, va="top")
    col_x = [MX, 0.52]
    for i, (head, txt) in enumerate(C.EXEC_FIVE):
        cx = col_x[i % 2]; cy = 0.63 - (i // 2) * 0.135
        H(ax, cx, cy, head, 11, T.GOAL, va="top")
        P(ax, cx, cy - 0.032, txt, size=8.8, color=T.MUTE, width=64, va="top")
    # last (5th) full width bottom-left already placed; ok
    footer(ax, 2)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def content(pdf, n, kicker, title, fig_path, fig_box, headline, points,
            accent=T.FEY, chips=None, caption=None, second_fig=None):
    fig, ax = new_slide()
    header(ax, fig, kicker, title, n)
    place_image(fig, os.path.join(FIG, fig_path), fig_box)
    if second_fig:
        place_image(fig, os.path.join(FIG, second_fig[0]), second_fig[1])
    if caption:
        H(ax, fig_box[0], fig_box[1] - 0.018, caption, 7.6, T.FAINT, va="top",
          font=T.BODY_FONT, weight="normal")
    rx = 0.635
    rw = 1 - MX - rx
    if chips:
        insight_rail(ax, rx, 0.40, rw, 0.45, headline, points, accent)
        panel(ax, rx, 0.09, rw, 0.27, color=T.PANEL)
        for i, (val, lab) in enumerate(chips[:4]):
            cx = rx + rw * (0.27 + 0.46 * (i % 2))
            cy = 0.285 - (i // 2) * 0.115
            H(ax, cx, cy, str(val), 18, accent, ha="center", va="center")
            ax.text(cx, cy - 0.042, lab.upper(), fontsize=7, color=T.MUTE,
                    ha="center", va="center", fontfamily=T.BODY_FONT, zorder=5)
        ax.plot([rx + rw * 0.5, rx + rw * 0.5], [0.13, 0.32], color=T.LINE, lw=0.8)
        ax.plot([rx + 0.02, rx + rw - 0.02], [0.225, 0.225], color=T.LINE, lw=0.8)
    else:
        insight_rail(ax, rx, 0.09, rw, 0.76, headline, points, accent)
    footer(ax, n)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def s_players_radar(pdf, n, names, title):
    fig, ax = new_slide()
    header(ax, fig, "Key players", title, n)
    from figures_ext import RADAR_FILES
    cards = {c[0]: c for c in C.PLAYER_CARDS}
    cw = (1 - 2 * MX - 0.04) / 3
    for i, nm in enumerate(names):
        x0 = MX + i * (cw + 0.02)
        panel(ax, x0, 0.06, cw, 0.80)
        ax.add_patch(Rectangle((x0, 0.85), cw, 0.006, color=T.FEY, zorder=2))
        # name/role. The radar PNG + EXT stats are keyed by the names passed in
        # (Szymanski without its diacritic, Danilo by full name); the card copy is keyed
        # by the canonical short name. Resolve display + card explicitly so the role and
        # scouting note still render.
        CARD_ALIAS = {"Sebastian Szymanski": "Sebastian Szymański",
                      "Danilo Pereira da Silva": "Danilo"}
        disp = {"Sebastian Szymanski": "Sebastian Szymański"}.get(nm, nm)
        card = cards.get(nm) or cards.get(CARD_ALIAS.get(nm, nm))
        H(ax, x0 + 0.015, 0.825, disp, 12.5, T.TEXT, va="center")
        if card:
            H(ax, x0 + 0.015, 0.80, card[1], 8, T.FEY, va="center")
        place_image(fig, os.path.join(FIG, RADAR_FILES[nm]),
                    (x0 + 0.005, 0.42, x0 + cw - 0.005, 0.78))
        # note
        if card:
            P(ax, x0 + 0.015, 0.38, card[2], size=8.2, color=T.MUTE,
              width=int(cw * 95), va="top")
        # key stats
        rd = EXT["radars"].get(nm, {})
        mins = rd.get("mins", 0)
        H(ax, x0 + 0.015, 0.10, f"{mins} mins in window", 8, T.FAINT, va="center")
    footer(ax, n)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def s_plan(pdf):
    fig, ax = new_slide()
    header(ax, fig, "Game plan", "The concrete recommendations", 12)
    panel(ax, MX, 0.34, 0.44, 0.5, color=T.PANEL)
    panel(ax, 0.515, 0.34, 0.44, 0.5, color=T.PANEL)
    ax.add_patch(Rectangle((MX, 0.834), 0.44, 0.006, color=T.GOAL, zorder=2))
    ax.add_patch(Rectangle((0.515, 0.834), 0.44, 0.006, color=T.CB_BLUE, zorder=2))
    H(ax, MX + 0.02, 0.805, "WITH THE BALL", 12, T.GOAL, va="top")
    bullets(ax, MX + 0.02, 0.76, C.PLAN_IN, size=8.8, gap=0.052, width=58, mcolor=T.GOAL)
    H(ax, 0.535, 0.805, "WITHOUT THE BALL", 12, T.CB_BLUE, va="top")
    bullets(ax, 0.535, 0.76, C.PLAN_OUT, size=8.8, gap=0.052, width=58, mcolor=T.CB_BLUE)
    H(ax, MX, 0.30, "IN-GAME SCENARIOS", 12, T.TEXT, va="top")
    for i, (head, txt) in enumerate(C.PLAN_SCEN):
        cx = MX + (i % 2) * 0.49; cy = 0.255 - (i // 2) * 0.09
        H(ax, cx, cy, head, 9.5, T.GOAL, va="top")
        P(ax, cx, cy - 0.028, txt, size=8.2, color=T.MUTE, width=58, va="top")
    footer(ax, 12)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def s_week(pdf):
    fig, ax = new_slide()
    header(ax, fig, "Delivery", "What I'd tell the players, day by day", 13)
    P(ax, MX, 0.85, C.WEEK_INTRO, size=9.5, color=T.MUTE, width=150, va="top")
    cw = (1 - 2 * MX - 4 * 0.012) / 5
    for i, (day, txt) in enumerate(C.WEEK_DAYS):
        x0 = MX + i * (cw + 0.012)
        panel(ax, x0, 0.12, cw, 0.65)
        ax.add_patch(Rectangle((x0, 0.764), cw, 0.006, color=T.FEY, zorder=2))
        head = day.split("·")[0].strip()
        sub = day.split("·")[1].strip() if "·" in day else ""
        H(ax, x0 + 0.012, 0.73, head, 13, T.FEY, va="center")
        H(ax, x0 + 0.012, 0.705, sub, 8, T.TEXT, va="center")
        P(ax, x0 + 0.012, 0.675, txt, size=7.6, color=T.MUTE, width=int(cw * 92), va="top")
    footer(ax, 13)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def s_matchplan(pdf):
    fig, ax = new_slide()
    ax.add_patch(Rectangle((0, 0.9), 1, 0.1, color=T.CB_BLUE, zorder=0))
    H(ax, MX, 0.945, "MATCHPLAN · FEYENOORD", 22, "#FFFFFF", va="center")
    emblem(fig, (1 - MX - 0.05, 0.905, 1 - MX, 0.99))
    H(ax, 1 - MX - 0.06, 0.945, "ONE PAGE · PIN IT UP", 9, "#FFFFFF", ha="right",
      va="center", alpha=0.9)
    cols = [
        ("THEIR THREAT", T.FEY, [
            "Left-loading possession side (58% ball, 18.7 shots/g)",
            "Build through Kökçü; left overload (41% entries, 58% crosses)",
            "Clinical: 26 goals from 18.3 xG · 28 big chances",
            "Set-piece danger: 5 SP goals (Trauner, Hancko)",
        ]),
        ("THEIR WEAKNESS", T.WARN, [
            "Concede few but HIGH-quality chances (0.124 xGA/shot)",
            "72% of shots conceded inside the box, on transition",
            "High line + committed full-backs = space in behind",
            "3 set-piece goals conceded in 10 games",
        ]),
        ("OUR PLAN", T.GREEN, [
            "Win-it-and-go: attack in behind the full-backs FAST",
            "Make it transitional, not a possession contest",
            "Compact block, screen Kökçü, force them to cross from deep",
            "Win the box both ends, set pieces are our route",
        ]),
    ]
    cw = (1 - 2 * MX - 2 * 0.02) / 3
    for i, (title, col, items) in enumerate(cols):
        x0 = MX + i * (cw + 0.02)
        panel(ax, x0, 0.18, cw, 0.62, color=T.PANEL)
        ax.add_patch(Rectangle((x0, 0.794), cw, 0.006, color=col, zorder=2))
        H(ax, x0 + 0.02, 0.76, title, 14, col, va="top")
        yy = 0.70
        for it in items:
            ax.text(x0 + 0.02, yy, "▶", fontsize=8, color=col, va="top", zorder=6, fontfamily="DejaVu Sans")
            w = textwrap.fill(it, width=int(cw * 78))
            ax.text(x0 + 0.038, yy, w, fontsize=9.2, color=T.TEXT, va="top",
                    zorder=6, fontfamily=T.BODY_FONT, linespacing=1.3)
            yy -= 0.045 * (1 + w.count("\n") * 0.7) + 0.02
    # three keys strip
    panel(ax, MX, 0.05, 1 - 2 * MX, 0.1, color=T.PANEL_2, ec=T.GOAL, lw=1.2)
    H(ax, MX + 0.02, 0.118, "THE 3 KEYS", 11, T.GOAL, va="center")
    keys = "1 · FORCE THEM LEFT & DEFEND THE BOX      2 · WIN-IT-AND-GO IN BEHIND      3 · WIN SET PIECES BOTH ENDS"
    H(ax, 0.55, 0.10, keys, 11, T.TEXT, ha="center", va="center", font=T.HEAD_FONT)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def s_method(pdf):
    fig, ax = new_slide()
    header(ax, fig, "Appendix", "Method, data & video clips", 15)
    H(ax, MX, 0.83, "HOW THIS WAS BUILT", 12, T.TEXT, va="top")
    P(ax, MX, 0.80, C.METHOD, size=9.2, color=T.MUTE, width=72, va="top")
    H(ax, MX, 0.42, "WHAT I'D ADD WITH MORE TIME / DATA", 11, T.TEXT, va="top")
    bullets(ax, MX, 0.38, [
        "Tracking & possession data to quantify pressing triggers and line height.",
        "Full-season sample to separate stable patterns from noise.",
        "Linked Sportscode clips for every figure, one click to the moment.",
        "Opponent-specific set-piece pack, frame by frame.",
    ], size=9, width=72, gap=0.05)
    # clip references panel (authentic timestamps)
    rx = 0.55
    panel(ax, rx, 0.07, 1 - MX - rx, 0.79, color=T.PANEL_2, ec=T.LINE)
    H(ax, rx + 0.018, 0.82, "KEY CLIPS TO PULL", 11, T.FEY, va="top")
    H(ax, rx + 0.018, 0.795, "Goals conceded, the transition template", 8.5, T.WARN, va="top")
    clips_against = [c for c in EXT["key_clips"] if not c["for"] and c["kind"] == "GOAL"][:8]
    yy = 0.765
    for c in clips_against:
        ax.text(rx + 0.022, yy, f"{c['match']:<16} {c['t']:>6}  {short(c['player'])}  ·  {c['ctx']}",
                fontsize=8, color=T.TEXT, va="top", fontfamily=T.BODY_FONT, zorder=6)
        yy -= 0.032
    H(ax, rx + 0.018, yy - 0.01, "Their goals, patterns to defend", 8.5, T.GOAL, va="top")
    yy -= 0.045
    clips_for = [c for c in EXT["key_clips"] if c["for"] and c["kind"] == "GOAL"][:8]
    for c in clips_for:
        ax.text(rx + 0.022, yy, f"{c['match']:<16} {c['t']:>6}  {short(c['player'])}  ·  {c['ctx']}",
                fontsize=8, color=T.TEXT, va="top", fontfamily=T.BODY_FONT, zorder=6)
        yy -= 0.032
    footer(ax, 15)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def build():
    with PdfPages(OUT_PDF) as pdf:
        s_title(pdf)
        s_exec(pdf)
        content(pdf, 3, "Profile & form", "Dominant, and rarely troubled",
                "01_form.png", (MX, 0.50, 0.63, 0.85),
                "They control games and out-create everyone, beat them only in open, transitional matches.",
                ["xG sits above xGA in 8 of 10 games, a passing contest favours them.",
                 "The only cracks: PSV (3.22 xGA, lost) and Go Ahead (2.52), both open and end-to-end.",
                 "Two shapes (4-2-3-1 / 4-3-3), one constant: Kökçü as the deepest pivot."],
                chips=[(f"{MET['record']['W']}-{MET['record']['D']}-{MET['record']['L']}", "W-D-L"),
                       ("26-11", "goals"), ("1.83", "xG/game"), ("1.21", "xGA/game")],
                caption="Expected goals, match by match",
                second_fig=("09_momentum.png", (MX, 0.18, 0.63, 0.46)))
        content(pdf, 4, "In possession", "How they build and create",
                "03_network.png", (MX, 0.46, 0.63, 0.86),
                "They play through you and load the LEFT, cut Kökçü's time and crowd that channel.",
                ["Only 10% long balls, patient build via Trauner/Hancko, Kökçü dropping in.",
                 "41% of final-third entries and 58% of crosses come down the left.",
                 "18.9 crosses/game but just 25% completed, defend the box and live with it."],
                chips=[("58%", "possession"), ("22.1", "prog passes/g"),
                       ("18.9", "crosses/g"), ("25%", "crosses done")],
                caption="Average positions (build-up shape) · node = involvement",
                second_fig=("11_attackzones.png", (MX, 0.10, 0.63, 0.44)))
        content(pdf, 5, "Attacking threat", "Where the goals come from",
                "02_shotmap.png", (MX, 0.12, 0.50, 0.85),
                "Manufactured central chances and clinical finishing, deny the cutback and the half-space.",
                ["28 big chances, 58% of shots in the box, not a hopeful side.",
                 "Danilo leads scoring (7g, 5.45 xG); threat spread across Kökçü, Dilrosun, Szymański.",
                 "26 goals from 18.3 xG, expect regression, but respect the finishers."],
                chips=[(MET['attack']['shots'], "shots"), (MET['record']['gf'], "goals"),
                       (MET['attack']['xg'], "xG"), (MET['attack']['bigchances'], "big chances")],
                caption="Every shot · size = xG · blue = goals",
                second_fig=("08_players.png", (0.50, 0.30, 0.95, 0.66)))
        content(pdf, 6, "Out of possession", "A mid-block, not a gegenpress",
                "05_press.png", (MX, 0.12, 0.63, 0.85),
                "They invite you in and counter, slow build lets them re-set, so play vertical and fast.",
                ["PPDA 10.8, only 14.5% of defensive actions in the attacking third.",
                 "Recoveries average around halfway, controlled, not frantic.",
                 "We WILL get the ball in our half; the question is how quickly we use it."],
                accent=T.CB_BLUE,
                chips=[(MET['press']['ppda'], "PPDA"), ("x41", "avg recovery"),
                       ("42%", "actions def third"), ("6.8", "high turnovers/g")],
                caption="Defensive actions heat · blue line = avg recovery height")
        content(pdf, 7, "Transitions", "The opening, hurt them in behind",
                "12_transition.png", (MX, 0.30, 0.63, 0.82),
                "Their high line and committed full-backs are the door, win it and go, fast, in behind.",
                ["They concede a higher xG PER SHOT than they create (0.124 vs 0.098).",
                 "72% of shots conceded are inside the box, almost all on transition.",
                 "PSV (3.22 xGA) and Go Ahead (2.52) exploited exactly this."],
                accent=T.WARN,
                chips=[(MET['defense']['xga_per_shot'], "xGA/shot"),
                       ("72%", "conceded in box"), (EXT['transitions']['high_recoveries'], "high recoveries"),
                       (MET['defense']['goals_conceded'], "goals conceded")],
                caption="Left: where they regain · Right: where they get punished")
        content(pdf, 8, "Set pieces", "Live at both ends",
                "07_setpiece.png", (MX, 0.28, 0.63, 0.82),
                "A genuine route to goal for us, and a moment we must defend with full numbers.",
                ["~1 in 5 of their shots is from a set piece (39 shots, 5 goals, 5.8 xG).",
                 "Trauner and Hancko attack the box; Kökçü delivers.",
                 "But they conceded 3 set-piece goals in 10 games, load the box, far post."],
                chips=[(MET['attack']['setpiece_goals'], "SP goals for"),
                       (MET['defense']['setpiece_goals_conceded'], "SP goals against"),
                       (MET['attack']['setpiece_shots'], "SP shots for"),
                       (MET['defense']['setpiece_shots_conceded'], "SP shots against")],
                caption="Set-piece shots, threat (left) and conceded (right)")
        s_players_radar(pdf, 9, ["Orkun Kökçü", "Quinten Timber", "Sebastian Szymanski"],
                        "The spine, control & creation")
        s_players_radar(pdf, 10, ["Javairô Dilrosun", "Dávid Hancko", "Danilo Pereira da Silva"],
                        "The threats, width, build & finishing")
        content(pdf, 11, "Squad overview", "Who does what",
                "10_rankbars.png", (MX, 0.08, 0.63, 0.85),
                "Threat is shared, but the creative load runs through a small core.",
                ["Kökçü & Hancko drive progression; Timber & Szymański create.",
                 "Dilrosun is the dribble threat; Danilo the focal finisher.",
                 "Depth is real, Giménez, Wälemark, Idrissi all contribute off the bench."],
                accent=T.GREEN,
                caption="Squad ranked across the window (per the 10-match sample)")
        s_plan(pdf)
        s_week(pdf)
        s_matchplan(pdf)
        s_method(pdf)
    print("wrote", OUT_PDF)


if __name__ == "__main__":
    build()
