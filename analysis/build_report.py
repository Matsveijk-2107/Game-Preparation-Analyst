"""Compose the Feyenoord opposition dossier (A4 PDF) — Feyenoord house style."""
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
OUT_PDF = os.path.join(ROOT, "output", "Feyenoord_Opposition_Analysis.pdf")
EMBLEM = os.path.join(FIG, "emblem.png")
with open(os.path.join(ROOT, "output", "metrics.json"), encoding="utf-8") as f:
    MET = json.load(f)
with open(os.path.join(ROOT, "output", "metrics_more.json"), encoding="utf-8") as f:
    MORE = json.load(f)

W_IN, H_IN = 8.27, 11.69
MX = 0.062
CONTENT_TOP = 0.915
FLOOR = 0.072            # shared content baseline above footer


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------
def new_page():
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, color=T.INK, zorder=-10))
    return fig, ax


def panel(ax, x, y, w, h, color=T.PANEL, ec=T.LINE, lw=1.0, r=0.008, alpha=1.0, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=color, ec=ec, lw=lw, alpha=alpha, zorder=z,
                                mutation_aspect=H_IN / W_IN))


def H(ax, x, y, s, size, color=T.TEXT, weight="bold", ha="left", va="baseline",
      font=T.HEAD_FONT, z=5, alpha=1.0):
    return ax.text(x, y, s, fontsize=size, color=color, fontfamily=font,
                   weight=weight, ha=ha, va=va, zorder=z, alpha=alpha)


def P(ax, x, y, s, size=9.2, color=T.TEXT, ha="left", va="top", width=92, z=5,
      leading=1.34):
    wrapped = "\n".join(textwrap.fill(line, width=width) for line in s.split("\n"))
    return ax.text(x, y, wrapped, fontsize=size, color=color, ha=ha, va=va,
                   zorder=z, fontfamily=T.BODY_FONT, linespacing=leading)


def sec_head(ax, x, y, s, size=11.5, color=T.TEXT, tick=True):
    """Section head with a red ignition tick to its left."""
    if tick:
        th = size * 0.0013
        ax.add_patch(Rectangle((x, y - th * 0.5), 0.011, th * 1.7, color=T.FEY, zorder=6))
        H(ax, x + 0.020, y, s, size, color, va="center")
        return x + 0.020
    H(ax, x, y, s, size, color, va="center")
    return x


def fig_label(ax, x, y, s):
    H(ax, x, y, s.upper(), 9, T.FEY, va="top")


def caption(ax, x, y, s):
    ax.text(x, y, s, fontsize=7.5, color=T.FAINT, va="top", ha="left",
            fontfamily=T.BODY_FONT, zorder=5)


def place_emblem(fig, box):
    img = mpimg.imread(EMBLEM)
    x0, y0, x1, y1 = box
    side = min((x1 - x0), (y1 - y0) * H_IN / W_IN)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = side; h = side * W_IN / H_IN
    a = fig.add_axes([cx - w / 2, cy - h / 2, w, h]); a.imshow(img); a.axis("off")
    return a


def place_image(fig, path, box):
    x0, y0, x1, y1 = box
    img = mpimg.imread(path)
    img_ar = img.shape[1] / img.shape[0]
    bw, bh = (x1 - x0) * W_IN, (y1 - y0) * H_IN
    if img_ar > bw / bh:
        new_w = (x1 - x0); new_h = new_w * W_IN / img_ar / H_IN
    else:
        new_h = (y1 - y0); new_w = new_h * H_IN * img_ar / W_IN
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = fig.add_axes([cx - new_w / 2, cy - new_h / 2, new_w, new_h])
    a.imshow(img); a.axis("off")
    return a


def header(fig, ax, kicker, title):
    ax.add_patch(Rectangle((0, 0.945), 1, 0.055, color=T.PANEL_2, zorder=0))
    ax.add_patch(Rectangle((0, 0.9448), 1, 0.0016, color=T.FEY, zorder=2))
    ax.add_patch(Rectangle((MX, 0.951), 0.018, 0.034, color=T.FEY, zorder=2))
    H(ax, MX + 0.03, 0.976, kicker.upper(), 9.5, T.FEY, va="center")
    H(ax, MX + 0.03, 0.955, title, 17, T.TEXT, va="center")
    place_emblem(fig, (1 - MX - 0.052, 0.949, 1 - MX, 0.992))
    H(ax, 1 - MX - 0.062, 0.966, "FEYENOORD", 10.5, T.MUTE, ha="right", va="center", alpha=0.85)
    ax.plot([MX, 1 - MX], [0.9405, 0.9405], color=T.LINE, lw=0.8, zorder=2)


def footer(ax, n):
    ax.plot([MX, 1 - MX], [0.038, 0.038], color=T.LINE, lw=0.8)
    ax.add_patch(Rectangle((MX, 0.0205, ), 0.009, 0.009, color=T.FEY, zorder=5))
    H(ax, MX + 0.018, 0.024, "OPPOSITION ANALYSIS · GAME PREPARATION", 7.5, T.FAINT, va="center")
    H(ax, 0.5, 0.024, f"Prepared by {C.AUTHOR}", 7.5, T.FAINT, ha="center", va="center",
      weight="normal", font=T.BODY_FONT)
    H(ax, 1 - MX, 0.024, f"{n:02d}", 8.5, T.MUTE, ha="right", va="center")


def chrome(fig, ax, kicker, title, n, spine=True):
    if spine:
        T.spine(ax)
        T.ghost_number(ax, n)
    header(fig, ax, kicker, title)
    footer(ax, n)


def stat_strip(ax, x, y, w, items, vcolor=T.GOAL, vsize=20, hero=None):
    n = len(items); cw = w / n
    for i, (val, lab) in enumerate(items):
        cx = x + cw * (i + 0.5)
        H(ax, cx, y, str(val), vsize, vcolor, ha="center", va="center")
        ax.text(cx, y - 0.027, lab.upper(), fontsize=7.0, color=T.MUTE, ha="center",
                va="center", fontfamily=T.BODY_FONT, zorder=5)
        if i > 0:
            ax.plot([x + cw * i, x + cw * i], [y - 0.031, y + 0.020], color=T.LINE, lw=0.8, zorder=4)
        if hero == i:
            T.hero_underline(ax, cx, y - 0.016, 0.045)


def bullets(ax, x, y, items, size=9.2, gap=0.026, width=86, color=T.TEXT, mcolor=T.FEY):
    yy = y
    for it in items:
        ax.text(x, yy, "—", fontsize=size, color=mcolor, va="top",
                fontfamily=T.HEAD_FONT, weight="bold", zorder=5)
        wrapped = textwrap.fill(it, width=width)
        ax.text(x + 0.022, yy, wrapped, fontsize=size, color=color, va="top",
                zorder=5, fontfamily=T.BODY_FONT, linespacing=1.32)
        yy -= gap * (1 + wrapped.count("\n")) + 0.006
    return yy


def blocks(ax, x, y, items, w=0.876, title_size=11, body_size=9.2, gap=0.013, tick=True):
    yy = y
    for head, txt in items:
        sec_head(ax, x, yy, head, title_size, T.TEXT, tick=tick)
        yy -= 0.024
        t = P(ax, x, yy, txt, size=body_size, color=T.MUTE, width=int(w * 108), va="top")
        n = textwrap.fill(txt, width=int(w * 108)).count("\n") + 1
        yy -= n * 0.0168 + gap
    return yy


# ===========================================================================
# PAGES
# ===========================================================================
def page_cover(pdf):
    fig, ax = new_page()
    ax.add_patch(Rectangle((0, 0.92), 1, 0.08, color=T.PANEL_2, zorder=0))
    ax.add_patch(Rectangle((0, 0.9185), 1, 0.0016, color=T.FEY, zorder=2))
    ax.add_patch(Rectangle((MX, 0.935), 0.05, 0.05, color=T.FEY, zorder=2))
    H(ax, MX + 0.075, 0.955, "CLUB BRUGGE · ANALYSIS DEPARTMENT", 11, T.CB_BLUE, va="center")
    # crest watermark + emblem
    T.crest_watermark(fig, EMBLEM, center=(0.5, 0.235), width=0.46, alpha=0.05)
    place_emblem(fig, (0.60, 0.655, 0.945, 0.90))
    # red title block flush to the left margin (jersey nod), wordmark in white over ink
    ax.add_patch(Rectangle((0, 0.527), MX + 0.012, 0.066, color=T.FEY, zorder=2))
    H(ax, MX, 0.71, "OPPOSITION", 30, T.MUTE, weight="bold")
    H(ax, MX, 0.645, "ANALYSIS", 30, T.MUTE, weight="bold")
    H(ax, MX, 0.545, "FEYENOORD", 58, T.TEXT, weight="bold")
    ax.add_patch(Rectangle((MX, 0.512), 0.876, 0.0035, color=T.FEY, zorder=3))
    P(ax, MX, 0.487, C.EXEC_HEADLINE, size=12.5, color=T.TEXT, width=66, va="top")
    # data chip
    panel(ax, MX, 0.305, 0.876, 0.092, color=T.PANEL)
    H(ax, MX + 0.025, 0.378, "SCOUTING WINDOW", 8.5, T.FEY, va="center")
    P(ax, MX + 0.025, 0.358, C.DATA_WINDOW, size=10, color=T.TEXT, width=82, va="top")
    P(ax, MX + 0.025, 0.334, C.SOURCE, size=8, color=T.MUTE, width=98, va="top")
    ax.plot([MX, MX + 0.30], [0.295, 0.295], color=T.CREAM, lw=0.8, zorder=4)  # cream premium hairline
    H(ax, MX, 0.16, "PREPARED BY", 9, T.FAINT, va="center")
    H(ax, MX, 0.128, C.AUTHOR, 16, T.TEXT, va="center")
    H(ax, 1 - MX, 0.128, "GAME PREPARATION ANALYST — APPLICATION WORK SAMPLE", 8, T.FAINT,
      ha="right", va="center", font=T.BODY_FONT, weight="normal")
    ax.plot([MX, 1 - MX], [0.10, 0.10], color=T.LINE, lw=0.8)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_exec(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Executive summary", "The 60-second briefing", 2)
    panel(ax, MX, 0.695, 0.876, 0.205)
    H(ax, MX + 0.025, 0.882, "TEAM PROFILE", 10, T.FEY, va="top")
    ax.plot([MX + 0.025, MX + 0.851], [0.868, 0.868], color=T.HAIRLINE_SOFT, lw=0.7)
    yy = 0.853
    ax.plot([MX + 0.345, MX + 0.345], [0.715, 0.862], color=T.HAIRLINE_SOFT, lw=0.6)
    for k, v in C.EXEC_PROFILE:
        H(ax, MX + 0.025, yy, k, 9, T.MUTE, va="top", font=T.BODY_FONT, weight="bold")
        ax.text(MX + 0.365, yy, v, fontsize=9, color=T.TEXT, va="top",
                fontfamily=T.BODY_FONT, zorder=5)
        yy -= 0.0265
    sec_head(ax, MX, 0.655, "FIVE THINGS THAT DECIDE THE GAME", 13, T.TEXT)
    yy = 0.618
    for head, txt in C.EXEC_FIVE:
        H(ax, MX + 0.020, yy, head, 10.5, T.GOAL, va="top")
        yy -= 0.023
        t = textwrap.fill(txt, width=104)
        ax.text(MX + 0.020, yy, t, fontsize=9.2, color=T.MUTE, va="top",
                fontfamily=T.BODY_FONT, zorder=5, linespacing=1.32)
        yy -= (t.count("\n") + 1) * 0.0168 + 0.0145
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_form(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Profile & form", "Who they are, and how it's gone", 3)
    fig_label(ax, MX, 0.910, "Expected goals, match by match")
    place_image(fig, os.path.join(FIG, "01_form.png"), (MX, 0.655, 1 - MX, 0.890))
    fig_label(ax, MX, 0.640, "When they hurt you, and when you hurt them")
    place_image(fig, os.path.join(FIG, "14_gamestate.png"), (MX, 0.458, 1 - MX, 0.622))
    yy = blocks(ax, MX, 0.425, [
        ("Dominant, rarely troubled",
         "Seven wins from ten, 26 goals, an xG line above their xGA in eight of ten games. They "
         "control matches and out-create opponents — a passing contest favours them."),
        ("The exceptions are the lesson",
         "The two spikes — the 3-4 loss at PSV (3.2 xGA) and the 4-3 win at Go Ahead (2.5 xGA) — "
         "were open, transitional, end-to-end games. That is the template to beat them."),
        ("Strike early, fear the late game",
         "Their only window where xGA beats xG is 15–30' (2.9 xGA, 4 conceded). After 60' they "
         "scored 12 and conceded 1. Land the first blow."),
    ], body_size=9.0)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_possession(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "In possession", "How they build and create", 4)
    place_image(fig, os.path.join(FIG, "03_network.png"), (MX, 0.635, 1 - MX, 0.915))
    caption(ax, MX, 0.622, "Average on-ball positions (build-up shape) · node = involvement · line = pass volume")
    place_image(fig, os.path.join(FIG, "04_territory.png"), (MX, 0.40, 1 - MX, 0.612))
    stat_strip(ax, MX, 0.365, 0.876, [
        ("58%", "of all passes"), ("10%", "long balls"),
        (str(MET["progressive_passes_pg"]), "progressive/game"),
        (str(MET["crosses"]["per_game"]), "crosses/game"),
        ("25%", "crosses done")], vcolor=T.TEXT, vsize=18, hero=2)
    panel(ax, MX, FLOOR, 0.876, 0.245, color=T.PANEL)
    H(ax, MX + 0.025, 0.295, "WHAT IT MEANS", 10, T.CB_BLUE, va="top")
    bullets(ax, MX + 0.025, 0.268, [
        "They play through you, not over you — Kökçü (888 touches, 39 progressive passes) drops to "
        "set tempo around halfway. Screen the lane back to him and the build-up stalls.",
        "Verified LEFT bias: 41% of final-third entries and 58% of crosses come from the left "
        "(Hancko & López build, Idrissi isolates, Szymański drifts in).",
        "Volume crossing, modest precision (18.9/game at 25%): a well-populated box and the second "
        "ball largely neutralises it.",
    ], size=8.7, width=104, gap=0.030, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_attack(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Attacking threat", "Where the goals come from", 5)
    place_image(fig, os.path.join(FIG, "02_shotmap.png"), (MX, 0.595, 0.55, 0.905))
    caption(ax, MX, 0.583, "Every shot · size = xG · gold = goals")
    place_image(fig, os.path.join(FIG, "08_players.png"), (0.50, 0.60, 1 - MX, 0.905))
    caption(ax, 0.515, 0.585, "Top contributors across the window")
    stat_strip(ax, MX, 0.545, 0.876, [
        (MET["attack"]["shots"], "shots"), (MET["record"]["gf"], "goals"),
        (MET["attack"]["xg"], "xG"), ("+7.7", "vs xG"),
        (f"{MET['attack']['box_share']}%", "in box"),
        (MET["attack"]["bigchances"], "big chances")], vcolor=T.GOAL, vsize=18, hero=3)
    blocks(ax, MX, 0.49, C.ATTACK, body_size=9.0)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_press(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Out of possession", "Their block & their two shapes", 6)
    place_image(fig, os.path.join(FIG, "05_press.png"), (MX, 0.635, 1 - MX, 0.915))
    p = MET["press"]
    stat_strip(ax, MX, 0.60, 0.876, [
        (p["ppda"], "PPDA"), (f"x{p['recovery_avg_x']:.0f}", "avg recovery"),
        (f"{p['def_actions_def_third_pct']}%", "actions def third"),
        (f"{p['def_actions_att_third_pct']}%", "att third"),
        (p["high_turnovers_pg"], "high turnovers/g")], vcolor=T.TEXT, vsize=18)
    fig_label(ax, MX, 0.555, "A tale of two shapes — 5 games each")
    place_image(fig, os.path.join(FIG, "15_formation.png"), (MX, 0.345, 0.60, 0.545))
    sec_head(ax, 0.63, 0.545, "MID-BLOCK, NOT A PRESS", 10.5, T.TEXT)
    P(ax, 0.63, 0.515, C.PRESS[0][1], size=8.6, color=T.MUTE, width=44, va="top")
    sec_head(ax, 0.63, 0.41, "TWO SHAPES", 10.5, T.TEXT)
    P(ax, 0.63, 0.382, C.PRESS[1][1], size=8.6, color=T.MUTE, width=44, va="top")
    panel(ax, MX, FLOOR, 0.876, 0.20, color=T.PANEL)
    H(ax, MX + 0.025, 0.255, "READ IT IN-GAME", 10, T.CB_BLUE, va="top")
    bullets(ax, MX + 0.025, 0.228, [
        "4-3-3 = their sharper, more left-loaded shape (2.07 xG, 43% left, 1.07 xGA) and presses "
        "less (PPDA 12.2) — build patiently, double the left.",
        "4-2-3-1 = more balanced but leakier (1.34 xGA) and presses higher (PPDA 9.7) — bait the "
        "press, release runners early into the space behind.",
    ], size=8.8, width=104, gap=0.030, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_vuln(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Vulnerabilities", "How to hurt Feyenoord", 7)
    place_image(fig, os.path.join(FIG, "13_transition_press.png"), (MX, 0.60, 1 - MX, 0.905))
    caption(ax, MX, 0.588, "Feyenoord ball-losses that became a shot against within 15s · gold = led to a goal")
    t = MORE["transition"]
    stat_strip(ax, MX, 0.563, 0.876, [
        (f"{t['transition_pct']}%", "shots from turnovers"),
        (t["transition_shots"], "transition shots"),
        (t["transition_xga"], "transition xGA"),
        (f"x{t['avg_loss_x']:.0f}", "avg loss (their half)"),
        (MET["record"]["ga"], "goals conceded")], vcolor=T.WARN, vsize=18, hero=0)
    panel(ax, MX, FLOOR, 0.876, 0.446, color=T.PANEL_2, ec=T.GOAL, lw=1.2)
    ax.add_patch(Rectangle((MX, FLOOR + 0.440), 0.876, 0.006, color=T.GOAL, zorder=2))
    H(ax, MX + 0.03, 0.496, "THREE WAYS TO HURT THEM", 13, T.GOAL, va="top")
    acts = [
        ("Press their build-up — don't sit off",
         "29% of the shots they concede (3.9 xGA) come within 15s of a turnover, and those losses "
         "are in THEIR OWN half (avg x=32). Trigger the press on the pass back to Trauner/Bijlow "
         "and screen Kökçü — this is the single clearest route to a chance."),
        ("Make it transitional, and strike early",
         "Their only sub-par window is 15–30' (2.9 xGA, 4 conceded); after 60' they are ruthless "
         "(12 goals, 1 against). Take an early lead and keep the game open — they barely counter "
         "(1 fast-break shot all window)."),
        ("Win the box on set pieces",
         "Three set-piece goals conceded in ten games. Their crossing lands only 25% — defend the "
         "far post with numbers, then attack their box: a genuine, repeatable route to goal."),
    ]
    yy = 0.458
    for h, tx in acts:
        H(ax, MX + 0.03, yy, h, 10.5, T.TEXT, va="top")
        yy -= 0.024
        tt = textwrap.fill(tx, width=100)
        ax.text(MX + 0.03, yy, tt, fontsize=8.7, color=T.MUTE, va="top",
                fontfamily=T.BODY_FONT, linespacing=1.34, zorder=5)
        yy -= (tt.count("\n") + 1) * 0.0166 + 0.020
    # honesty caveat pinned near the panel foot
    ax.plot([MX + 0.03, MX + 0.846], [0.108, 0.108], color=T.HAIRLINE_SOFT, lw=0.7)
    cav = textwrap.fill(C.VULN_CAVEAT, width=104)
    ax.text(MX + 0.03, 0.097, cav, fontsize=8.2, color=T.WARN, va="top",
            fontfamily=T.BODY_FONT, linespacing=1.3, zorder=5, style="italic")
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_setpiece(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Set pieces", "Live at both ends", 8)
    place_image(fig, os.path.join(FIG, "07_setpiece.png"), (MX, 0.60, 1 - MX, 0.905))
    sd = MORE["setpiece_delivery"]
    a = MET["attack"]; d = MET["defense"]
    stat_strip(ax, MX, 0.56, 0.876, [
        (a["setpiece_goals"], "SP goals for"), (d["setpiece_goals_conceded"], "SP goals against"),
        (sd["corners"], "corners"), (f"{sd['from_left']}/{sd['from_right']}", "left/right"),
        (f"{sd['short_pct']}%", "short")], vcolor=T.TEXT, vsize=18)
    sec_head(ax, MX, 0.515, "WHAT THEY DO", 11, T.TEXT)
    P(ax, MX + 0.020, 0.49, C.ATTACK[2][1], size=9.0, color=T.MUTE, width=104, va="top")
    panel(ax, MX, FLOOR, 0.876, 0.27, color=T.PANEL)
    H(ax, MX + 0.025, 0.32, "DEFEND IT / ATTACK IT", 10, T.CB_BLUE, va="top")
    bullets(ax, MX + 0.025, 0.292, [
        "DEFEND: corners come mostly from their left to the far post (48 of 75, only 5% short). "
        "Load the far post, put bodies on Trauner & Hancko, win the first contact.",
        "ATTACK: they concede 3 set-piece goals in 10 games and their open-play crossing is only "
        "25% accurate — overload the box, target the far post and the second phase.",
        "RECYCLE: with their full-backs committed to attacking corners, our cleared set pieces are "
        "a transition trigger — first outlet runs immediately.",
    ], size=8.8, width=104, gap=0.030, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_players(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Key players", "Who to plan around", 9)
    cw, ch = 0.428, 0.255
    gx = 1 - 2 * MX - 2 * cw
    x0s = [MX, MX + cw + gx]
    y0 = 0.655
    for i, (name, role, txt) in enumerate(C.PLAYER_CARDS):
        cx = x0s[i % 2]
        cy = y0 - (i // 2) * (ch + 0.020)
        panel(ax, cx, cy, cw, ch)
        ax.add_patch(Rectangle((cx, cy + ch - 0.006), cw, 0.006, color=T.FEY, zorder=2))
        H(ax, cx + 0.022, cy + ch - 0.046, name, 13.5, T.TEXT, va="center")
        H(ax, cx + 0.022, cy + ch - 0.076, role, 8.5, T.FEY, va="center")
        ax.plot([cx + 0.022, cx + cw - 0.022], [cy + ch - 0.094, cy + ch - 0.094],
                color=T.HAIRLINE_SOFT, lw=0.7, zorder=3)
        P(ax, cx + 0.022, cy + ch - 0.112, txt, size=8.7, color=T.MUTE, width=47, va="top")
        # key-stat row pinned to the card bottom
        stats = C.PLAYER_STATS.get(name, [])
        if stats:
            ax.plot([cx + 0.022, cx + cw - 0.022], [cy + 0.060, cy + 0.060],
                    color=T.HAIRLINE_SOFT, lw=0.7, zorder=3)
            inner = cw - 0.044
            for j, (val, lab) in enumerate(stats):
                sx = cx + 0.022 + inner * (j + 0.5) / len(stats)
                H(ax, sx, cy + 0.040, val, 13, T.FEY, ha="center", va="center")
                ax.text(sx, cy + 0.020, lab.upper(), fontsize=6.2, color=T.MUTE,
                        ha="center", va="center", fontfamily=T.BODY_FONT, zorder=5)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_plan(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Game plan", "The concrete recommendations", 10)
    cw = 0.428; gx = 1 - 2 * MX - 2 * cw
    panel(ax, MX, 0.55, cw, 0.345, color=T.PANEL)
    panel(ax, MX + cw + gx, 0.55, cw, 0.345, color=T.PANEL)
    ax.add_patch(Rectangle((MX, 0.889), cw, 0.006, color=T.GOAL, zorder=2))
    ax.add_patch(Rectangle((MX + cw + gx, 0.889), cw, 0.006, color=T.CB_BLUE, zorder=2))
    H(ax, MX + 0.022, 0.868, "WITH THE BALL", 11, T.GOAL, va="top")
    bullets(ax, MX + 0.022, 0.838, C.PLAN_IN, size=8.5, width=43, gap=0.020, mcolor=T.GOAL)
    H(ax, MX + cw + gx + 0.022, 0.868, "WITHOUT THE BALL", 11, T.CB_BLUE, va="top")
    bullets(ax, MX + cw + gx + 0.022, 0.838, C.PLAN_OUT, size=8.5, width=43, gap=0.020, mcolor=T.CB_BLUE)
    sec_head(ax, MX, 0.51, "IN-GAME SCENARIOS", 12, T.TEXT)
    yy = 0.475
    for head, txt in C.PLAN_SCEN:
        H(ax, MX + 0.020, yy, head, 10, T.GOAL, va="top")
        yy -= 0.022
        t = textwrap.fill(txt, width=106)
        ax.text(MX + 0.020, yy, t, fontsize=9, color=T.MUTE, va="top",
                fontfamily=T.BODY_FONT, linespacing=1.32, zorder=5)
        yy -= (t.count("\n") + 1) * 0.0168 + 0.020
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_week(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Delivery", "What I'd tell the players, day by day", 11)
    P(ax, MX, 0.905, C.WEEK_INTRO, size=9.5, color=T.MUTE, width=108, va="top")
    yy = 0.845
    for day, txt in C.WEEK_DAYS:
        panel(ax, MX, yy - 0.122, 0.876, 0.122)
        ax.add_patch(Rectangle((MX, yy - 0.122), 0.006, 0.122, color=T.FEY, zorder=2))
        H(ax, MX + 0.028, yy - 0.024, day, 11.5, T.TEXT, va="center")
        P(ax, MX + 0.028, yy - 0.046, txt, size=8.7, color=T.MUTE, width=104, va="top")
        yy -= 0.136
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_method(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Appendix", "Method, honesty & intent", 12)
    T.crest_watermark(fig, EMBLEM, center=(0.5, 0.30), width=0.42, alpha=0.04)
    sec_head(ax, MX, 0.905, "HOW THIS WAS BUILT", 12, T.TEXT)
    P(ax, MX + 0.020, 0.878, C.METHOD, size=9.6, color=T.MUTE, width=104, va="top")
    sec_head(ax, MX, 0.715, "WHAT I'D ADD WITH MORE TIME / DATA", 11.5, T.TEXT)
    bullets(ax, MX + 0.020, 0.685, C.CAVEATS, size=9.4, width=100, gap=0.038, mcolor=T.FEY)
    panel(ax, MX, 0.205, 0.876, 0.235, color=T.PANEL_2, ec=T.LINE)
    H(ax, MX + 0.028, 0.408, "WHY THIS ROLE, WHY THIS WAY", 11, T.CB_BLUE, va="top")
    P(ax, MX + 0.028, 0.378,
      "Opposition analysis is only useful if it changes behaviour on the pitch. My priority was to "
      "move from a large, raw event dataset to a small number of clear, evidence-backed messages a "
      "coach can install and a player can remember — structure, patterns, vulnerabilities, key "
      "players and scenarios, each tied to a concrete action and a way to communicate it through "
      "the week. That translation — done consistently, accurately and on time — is the job.",
      size=10.0, color=T.TEXT, width=92, va="top")
    # signature block
    ax.plot([MX, 1 - MX], [0.155, 0.155], color=T.LINE, lw=0.8)
    H(ax, MX, 0.135, "PREPARED BY", 8.5, T.FAINT, va="center")
    H(ax, MX, 0.108, C.AUTHOR, 15, T.TEXT, va="center")
    H(ax, 1 - MX, 0.118, "Feyenoord opposition analysis · application work sample", 8.5,
      T.FAINT, ha="right", va="center", font=T.BODY_FONT, weight="normal")
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def build():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    with PdfPages(OUT_PDF) as pdf:
        page_cover(pdf)
        page_exec(pdf)
        page_form(pdf)
        page_possession(pdf)
        page_attack(pdf)
        page_press(pdf)
        page_vuln(pdf)
        page_setpiece(pdf)
        page_players(pdf)
        page_plan(pdf)
        page_week(pdf)
        page_method(pdf)
    print("wrote", OUT_PDF)


if __name__ == "__main__":
    build()
