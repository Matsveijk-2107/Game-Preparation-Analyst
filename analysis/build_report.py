"""Feyenoord opposition dossier (A4 PDF) — dark, branded, strict flow layout.

Layout rule: every page is built top-down with a moving `y` cursor; each band
helper draws below the previous and returns the new cursor. Elements therefore
never overlap. Figures are sized to the column width (no lopsided side gaps).
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
OUT_PDF = os.path.join(ROOT, "output",
                       "Feyenoord_Wedstrijdanalyse.pdf" if C.NL
                       else "Feyenoord_Opposition_Analysis.pdf")
EMBLEM = os.path.join(FIG, "emblem.png")   # full-colour Feyenoord crest (the subject)
with open(os.path.join(ROOT, "output", "metrics.json"), encoding="utf-8") as f:
    MET = json.load(f)
with open(os.path.join(ROOT, "output", "metrics_more.json"), encoding="utf-8") as f:
    MORE = json.load(f)

W_IN, H_IN = 8.27, 11.69
MX = 0.062
COLW = 1 - 2 * MX                  # 0.876 live column width
TOP = 0.900                        # content top (below header)
FLOOR = 0.072                      # content floor (above footer)
GAP = 0.020
NPAGES = 13


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------
def new_page():
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, color=T.INK, zorder=-40))
    return fig, ax


def panel(ax, x, y, w, h, color=T.PANEL, ec=T.LINE, lw=1.0, r=0.008, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=color, ec=ec, lw=lw, zorder=z,
                                mutation_aspect=H_IN / W_IN))


def H(ax, x, y, s, size, color=T.TEXT, weight="bold", ha="left", va="baseline",
      font=T.HEAD_FONT, z=6, alpha=1.0):
    return ax.text(x, y, C.L(s), fontsize=size, color=color, fontfamily=font,
                   weight=weight, ha=ha, va=va, zorder=z, alpha=alpha)


def P(ax, x, y, s, size=9.2, color=T.MUTE, ha="left", va="top", width=92, z=6,
      leading=1.36):
    wrapped = "\n".join(textwrap.fill(ln, width=width) for ln in s.split("\n"))
    return ax.text(x, y, wrapped, fontsize=size, color=color, ha=ha, va=va,
                   zorder=z, fontfamily=T.BODY_FONT, linespacing=leading)


def place_emblem(fig, box):
    img = mpimg.imread(EMBLEM)
    x0, y0, x1, y1 = box
    side = min((x1 - x0), (y1 - y0) * H_IN / W_IN)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = fig.add_axes([cx - side / 2, cy - side * W_IN / H_IN / 2,
                      side, side * W_IN / H_IN], zorder=8)
    a.imshow(img); a.axis("off")
    return a


# ---------------------------------------------------------------------------
# branded chrome
# ---------------------------------------------------------------------------
def header(fig, ax, eyebrow, title):
    ax.add_patch(Rectangle((0, 0.928), 1, 0.072, color=T.PANEL_2, zorder=1))
    ax.add_patch(Rectangle((0, 0.9268), 1, 0.0018, color=T.CB_BLUE, zorder=3))
    ax.add_patch(Rectangle((MX - 0.018, 0.946), 0.02, 0.044, color=T.CB_BLUE, zorder=3))
    H(ax, MX + 0.016, 0.976, C.L(eyebrow).upper(), 9.5, T.CB_BLUE, va="center")
    H(ax, MX + 0.016, 0.953, C.L(title), 18, T.TEXT, va="center")
    place_emblem(fig, (1 - MX - 0.05, 0.934, 1 - MX, 0.996))
    H(ax, 1 - MX - 0.064, 0.972, "FEYENOORD", 10, T.TEXT, ha="right", va="center")
    H(ax, 1 - MX - 0.064, 0.953, "OPPOSITION ANALYSIS", 6.6, T.FAINT, ha="right",
      va="center", font=T.BODY_FONT, weight="normal")


def footer(ax, n):
    ax.plot([MX, 1 - MX], [0.042, 0.042], color=T.LINE, lw=0.8)
    ax.add_patch(Rectangle((MX, 0.0235), 0.009, 0.009, color=T.CB_BLUE, zorder=6))
    H(ax, MX + 0.018, 0.0275, "FEYENOORD · OPPOSITION ANALYSIS", 7, T.FAINT, va="center")
    H(ax, 0.5, 0.0275, "Club Brugge · Analysis Department", 7, T.FAINT, ha="center",
      va="center", font=T.BODY_FONT, weight="normal")
    H(ax, 1 - MX, 0.0275, f"{n:02d} / {NPAGES}", 8, T.MUTE, ha="right", va="center")


def chrome(fig, ax, eyebrow, title, n):
    T.page_gradient(fig)
    T.spine(ax, y0=FLOOR, y1=0.924)
    T.ghost_number(ax, n)
    header(fig, ax, eyebrow, title)
    footer(ax, n)


# ---------------------------------------------------------------------------
# flow bands — each draws below `y` and returns the new cursor
# ---------------------------------------------------------------------------
def fig_band(fig, ax, y, path, eyebrow=None, maxh=0.42, capw=COLW):
    top = y
    if eyebrow:
        H(ax, MX, top, C.L(eyebrow).upper(), 9, T.CB_BLUE, va="top")
        top -= 0.026
    img = mpimg.imread(path)
    ar = img.shape[1] / img.shape[0]
    h = capw * W_IN / ar / H_IN
    if h <= maxh:
        a = fig.add_axes([MX + (COLW - capw) / 2, top - h, capw, h], zorder=5)
        a.imshow(img); a.axis("off")
        used = h
    else:                              # too tall -> cap height, center horizontally
        w2 = maxh * H_IN * ar / W_IN
        a = fig.add_axes([0.5 - w2 / 2, top - maxh, w2, maxh], zorder=5)
        a.imshow(img); a.axis("off")
        used = maxh
    return top - used - GAP


def caption(ax, y, s):
    ax.text(MX, y + 0.004, C.L(s), fontsize=7.4, color=T.FAINT, va="top", ha="left",
            fontfamily=T.BODY_FONT, zorder=6)
    return y - 0.016


def stat_band(ax, y, items, vcolor=T.GOAL, hero=None, vsize=18):
    yv = y - 0.022
    n = len(items); cw = COLW / n
    for i, (val, lab) in enumerate(items):
        cx = MX + cw * (i + 0.5)
        H(ax, cx, yv, str(val), vsize, vcolor, ha="center", va="center")
        ax.text(cx, yv - 0.027, C.L(lab).upper(), fontsize=7.0, color=T.MUTE, ha="center",
                va="center", fontfamily=T.BODY_FONT, zorder=6)
        if i > 0:
            ax.plot([MX + cw * i, MX + cw * i], [yv - 0.031, yv + 0.020],
                    color=T.LINE, lw=0.8, zorder=5)
        if hero == i:
            ax.plot([cx - 0.022, cx + 0.022], [yv - 0.016, yv - 0.016],
                    color=T.CB_BLUE, lw=2.2, zorder=6)
    return y - 0.066 - GAP * 0.4


def sec_head(ax, y, s, size=11.5, color=T.TEXT):
    th = size * 0.0013
    ax.add_patch(Rectangle((MX, y - th * 1.3), 0.011, th * 1.9, color=T.CB_BLUE, zorder=6))
    H(ax, MX + 0.020, y, s, size, color, va="center")
    return y - 0.022


def text_blocks(ax, y, items, body=9.0, gap=0.014):
    yy = y
    for head, txt in items:
        sec_head(ax, yy - 0.006, head, 11)
        yy -= 0.026
        P(ax, MX + 0.020, yy, txt, size=body, color=T.MUTE, width=int(COLW * 108))
        n = textwrap.fill(txt, width=int(COLW * 108)).count("\n") + 1
        yy -= n * 0.0168 + gap
    return yy


def bullets(ax, x, y, items, size=9.0, gap=0.026, width=86, color=T.TEXT, mcolor=T.CB_BLUE):
    yy = y
    for it in items:
        ax.add_patch(Rectangle((x, yy - 0.013), 0.0075, 0.0075, color=mcolor, zorder=6))
        w = textwrap.fill(it, width=width)
        ax.text(x + 0.020, yy, w, fontsize=size, color=color, va="top", zorder=6,
                fontfamily=T.BODY_FONT, linespacing=1.32)
        yy -= gap * (1 + w.count("\n")) + 0.006
    return yy


def callout(ax, y, h, title, accent=T.GOAL, fill=T.PANEL_2):
    panel(ax, MX, y - h, COLW, h, color=fill, ec=accent, lw=1.2)
    ax.add_patch(Rectangle((MX, y - 0.006), COLW, 0.006, color=accent, zorder=3))
    H(ax, MX + 0.028, y - 0.030, title, 12.5, accent, va="center")
    return y - 0.052


# ===========================================================================
# PAGES
# ===========================================================================
def page_cover(pdf):
    fig, ax = new_page()
    T.page_gradient(fig)
    # top brand row
    ax.add_patch(Rectangle((MX - 0.018, 0.95), 0.05, 0.05, color=T.CB_BLUE, zorder=3))
    H(ax, MX + 0.05, 0.967, "CLUB BRUGGE · ANALYSIS DEPARTMENT", 11, T.TEXT, va="center")
    ax.plot([MX, 1 - MX], [0.93, 0.93], color=T.LINE, lw=0.8)
    # crest hero, right
    place_emblem(fig, (0.60, 0.66, 0.95, 0.90))
    # wordmark stack
    H(ax, MX, 0.70, "OPPOSITION", 27, T.MUTE)
    H(ax, MX, 0.642, "ANALYSIS", 27, T.MUTE)
    ax.add_patch(Rectangle((MX - 0.018, 0.527), 0.012, 0.066, color=T.CB_BLUE, zorder=3))
    H(ax, MX, 0.545, "FEYENOORD", 56, T.TEXT)
    ax.add_patch(Rectangle((MX, 0.512), COLW, 0.0035, color=T.CB_BLUE, zorder=3))
    P(ax, MX, 0.486, C.EXEC_HEADLINE, size=12.5, color=T.TEXT, width=64)
    # context chip
    panel(ax, MX, 0.300, COLW, 0.092, color=T.PANEL)
    H(ax, MX + 0.025, 0.374, "SCOUTING WINDOW", 8.5, T.CB_BLUE, va="center")
    P(ax, MX + 0.025, 0.353, C.DATA_WINDOW, size=10, color=T.TEXT, width=82)
    P(ax, MX + 0.025, 0.330, C.SOURCE, size=8, color=T.MUTE, width=98)
    # signature
    ax.plot([MX, 1 - MX], [0.16, 0.16], color=T.LINE, lw=0.8)
    H(ax, MX, 0.138, "PREPARED BY", 9, T.FAINT, va="center")
    H(ax, MX, 0.108, C.AUTHOR, 16, T.TEXT, va="center")
    H(ax, 1 - MX, 0.122, "GAME PREPARATION ANALYST · WORK SAMPLE", 8, T.FAINT,
      ha="right", va="center", font=T.BODY_FONT, weight="normal")
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_exec(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Team overview", "The 60-second briefing", 2)
    y = TOP
    panel(ax, MX, y - 0.205, COLW, 0.205)
    H(ax, MX + 0.025, y - 0.022, "TEAM PROFILE", 10, T.CB_BLUE, va="center")
    ax.plot([MX + 0.025, MX + COLW - 0.025], [y - 0.040, y - 0.040], color=T.HAIRLINE_SOFT, lw=0.7)
    ax.plot([MX + 0.345, MX + 0.345], [y - 0.198, y - 0.046], color=T.HAIRLINE_SOFT, lw=0.6)
    yy = y - 0.058
    for k, v in C.EXEC_PROFILE:
        H(ax, MX + 0.025, yy, k, 9, T.MUTE, va="top", font=T.BODY_FONT, weight="bold")
        ax.text(MX + 0.365, yy, v, fontsize=9, color=T.TEXT, va="top",
                fontfamily=T.BODY_FONT, zorder=6)
        yy -= 0.0265
    y = y - 0.205 - GAP * 1.4
    sec_head(ax, y, "FIVE THINGS THAT DECIDE THE GAME", 13)
    yy = y - 0.034
    for head, txt in C.EXEC_FIVE:
        H(ax, MX + 0.020, yy, head, 10.5, T.GOAL, va="top")
        yy -= 0.0225
        t = textwrap.fill(txt, width=104)
        ax.text(MX + 0.020, yy, t, fontsize=9.2, color=T.MUTE, va="top",
                fontfamily=T.BODY_FONT, zorder=6, linespacing=1.32)
        yy -= (t.count("\n") + 1) * 0.0168 + 0.0135
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_probable_xi(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Probable XI", "Their most-used eleven", 3)
    H(ax, MX, TOP, "MOST-USED ELEVEN · LIKELY 4-3-3", 9, T.CB_BLUE, va="top")
    top = TOP - 0.028
    img = mpimg.imread(os.path.join(FIG, "17_probable_xi.png"))
    ar = img.shape[1] / img.shape[0]
    pw = 0.47
    ph = pw * W_IN / ar / H_IN
    a = fig.add_axes([MX, top - ph, pw, ph], zorder=5); a.imshow(img); a.axis("off")
    # right column: THE SHAPE
    rx = MX + pw + 0.028
    rw = (1 - MX) - rx
    panel(ax, rx, top - ph, rw, ph)
    H(ax, rx + 0.022, top - 0.026, "THE SHAPE", 10, T.CB_BLUE, va="center")
    P(ax, rx + 0.022, top - 0.050, C.XI_SHAPE, size=8.7, color=T.MUTE, width=int(rw * 112))
    # bottom: rotation and bench
    by = top - ph - GAP * 1.2
    panel(ax, MX, FLOOR, COLW, by - FLOOR, color=T.PANEL)
    H(ax, MX + 0.025, by - 0.026, "ROTATION & BENCH", 10, T.CB_BLUE, va="center")
    P(ax, MX + 0.025, by - 0.050, C.XI_ROTATION, size=9.0, color=T.MUTE, width=104)
    bullets(ax, MX + 0.025, by - 0.092, C.XI_BENCH,
            size=8.8, width=104, gap=0.026, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_form(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Form & game-state", "Who they are, and how it's gone", 4)
    y = TOP
    y = fig_band(fig, ax, y, os.path.join(FIG, "01_form.png"),
                 eyebrow="Expected goals, match by match", maxh=0.235)
    y = fig_band(fig, ax, y, os.path.join(FIG, "14_gamestate.png"),
                 eyebrow="When they hurt you, and when you hurt them", maxh=0.205)
    y = text_blocks(ax, y, C.FORM_BLOCKS, body=9.0)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_possession(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Attacking tendencies", "How they build and create", 5)
    y = TOP
    y = fig_band(fig, ax, y, os.path.join(FIG, "03_network.png"),
                 eyebrow="Build-up shape · node = involvement, line = pass volume", maxh=0.200)
    y = fig_band(fig, ax, y, os.path.join(FIG, "04_territory.png"),
                 eyebrow="Where they enter the final third", maxh=0.180)
    y = stat_band(ax, y, [
        ("58%", "of all passes"), ("10%", "long balls"),
        (str(MET["progressive_passes_pg"]), "progressive/game"),
        (str(MET["crosses"]["per_game"]), "crosses/game"),
        ("25%", "crosses done")], vcolor=T.TEXT, hero=2)
    h = y - FLOOR
    panel(ax, MX, FLOOR, COLW, h, color=T.PANEL)
    H(ax, MX + 0.025, y - 0.026, "WHAT IT MEANS", 10, T.CB_BLUE, va="center")
    bullets(ax, MX + 0.025, y - 0.050, C.POSS_BULLETS,
            size=8.7, width=104, gap=0.026, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_attack(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Attacking threat", "Where the goals come from", 6)
    y = TOP
    # ---- row: shot map (left) + vertical stat rail (right) ----
    H(ax, MX, y, "EVERY SHOT · SIZE = xG · BLUE = GOALS", 9, T.CB_BLUE, va="top")
    H(ax, 0.55, y, "ATTACKING OUTPUT", 9, T.CB_BLUE, va="top")
    rt = y - 0.028
    sw = 0.45
    img = mpimg.imread(os.path.join(FIG, "02_shotmap.png"))
    ar = img.shape[1] / img.shape[0]
    sh = sw * W_IN / ar / H_IN
    a = fig.add_axes([MX, rt - sh, sw, sh], zorder=5); a.imshow(img); a.axis("off")
    ax.plot([0.525, 0.525], [rt - sh, rt - 0.004], color=T.LINE, lw=0.8, zorder=5)
    rail = [(MET["attack"]["shots"], "shots"), (MET["record"]["gf"], "goals"),
            (MET["attack"]["xg"], "xG"), ("+7.7", "over-performance vs xG"),
            (f"{MET['attack']['box_share']}%", "shots in the box"),
            (MET["attack"]["bigchances"], "big chances created")]
    ry = rt - 0.022
    step = (sh - 0.024) / len(rail)
    for val, lab in rail:
        H(ax, 0.55, ry, str(val), 18, T.GOAL, va="center")
        ax.text(0.645, ry, C.L(lab).upper(), fontsize=7.6, color=T.MUTE, va="center",
                ha="left", fontfamily=T.BODY_FONT, zorder=6)
        ry -= step
    y = rt - sh - GAP
    y = fig_band(fig, ax, y, os.path.join(FIG, "08_players.png"),
                 eyebrow="Top contributors across the window", maxh=0.155)
    y = text_blocks(ax, y, C.ATTACK, body=8.9)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_press(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Defensive tendencies", "Their block & their two shapes", 7)
    y = TOP
    y = fig_band(fig, ax, y, os.path.join(FIG, "05_press.png"),
                 eyebrow="Defensive actions · where they win it back", maxh=0.200)
    y = stat_band(ax, y, [
        (MET["press"]["ppda"], "PPDA"), (f"x{MET['press']['recovery_avg_x']:.0f}", "avg recovery"),
        (f"{MET['press']['def_actions_def_third_pct']}%", "actions def third"),
        (f"{MET['press']['def_actions_att_third_pct']}%", "att third"),
        (MET["press"]["high_turnovers_pg"], "high turnovers/g")], vcolor=T.TEXT)
    y = fig_band(fig, ax, y, os.path.join(FIG, "15_formation.png"),
                 eyebrow="A tale of two shapes · 5 games each", maxh=0.150)
    h = y - FLOOR
    panel(ax, MX, FLOOR, COLW, h, color=T.PANEL)
    H(ax, MX + 0.025, y - 0.026, "READ IT IN-GAME", 10, T.CB_BLUE, va="center")
    bullets(ax, MX + 0.025, y - 0.050, C.PRESS_BULLETS,
            size=8.7, width=104, gap=0.026, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_vuln(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "How to hurt them", "The opening", 8)
    y = TOP
    y = fig_band(fig, ax, y, os.path.join(FIG, "13_transition_press.png"),
                 eyebrow="Ball-losses that became a shot within 15s · blue = led to a goal",
                 maxh=0.235)
    t = MORE["transition"]
    y = stat_band(ax, y, [
        (f"{t['transition_pct']}%", "shots from turnovers"),
        (t["transition_shots"], "transition shots"),
        (t["transition_xga"], "transition xGA"),
        (f"x{t['avg_loss_x']:.0f}", "avg loss (their half)"),
        (MET["record"]["ga"], "goals conceded")], vcolor=T.WARN, hero=0)
    h = y - FLOOR
    y2 = callout(ax, y, h, "THREE WAYS TO HURT THEM", accent=T.GOAL)
    acts = C.VULN_ACTS
    yy = y2
    for hh, tx in acts:
        H(ax, MX + 0.028, yy, hh, 10.5, T.TEXT, va="top")
        yy -= 0.023
        tt = textwrap.fill(tx, width=100)
        ax.text(MX + 0.028, yy, tt, fontsize=8.6, color=T.MUTE, va="top",
                fontfamily=T.BODY_FONT, linespacing=1.32, zorder=6)
        yy -= (tt.count("\n") + 1) * 0.0162 + 0.016
    cav = textwrap.fill(C.VULN_CAVEAT, width=104)
    ax.text(MX + 0.028, FLOOR + 0.028, cav, fontsize=8.0, color=T.WARN, va="bottom",
            fontfamily=T.BODY_FONT, linespacing=1.3, zorder=6, style="italic")
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_setpiece(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Set pieces", "Live at both ends", 9)
    y = TOP
    y = fig_band(fig, ax, y, os.path.join(FIG, "07_setpiece.png"),
                 eyebrow="Set-piece shots · threat (left) vs conceded (right)", maxh=0.180)
    y = fig_band(fig, ax, y, os.path.join(FIG, "18_corner.png"),
                 eyebrow="Their corner delivery and first contact", maxh=0.205)
    sd = MORE["setpiece_delivery"]; a = MET["attack"]; d = MET["defense"]
    y = stat_band(ax, y, [
        (a["setpiece_goals"], "SP goals for"), (d["setpiece_goals_conceded"], "SP goals against"),
        (sd["corners"], "corners"), (f"{sd['from_left']}/{sd['from_right']}", "left/right"),
        (f"{sd['short_pct']}%", "short")], vcolor=T.TEXT)
    h = y - FLOOR
    panel(ax, MX, FLOOR, COLW, h, color=T.PANEL)
    H(ax, MX + 0.025, y - 0.026, "DEFEND IT / ATTACK IT", 10, T.CB_BLUE, va="center")
    bullets(ax, MX + 0.025, y - 0.050, C.SETPIECE_BULLETS,
            size=8.7, width=104, gap=0.026, mcolor=T.CB_BLUE)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_players(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Key players", "Who to plan around", 10)
    cw = 0.428
    gx = COLW - 2 * cw
    x0s = [MX, MX + cw + gx]
    ch = 0.245
    y0 = TOP - 0.004
    for i, (name, role, txt) in enumerate(C.PLAYER_CARDS):
        cx = x0s[i % 2]
        cy = y0 - (i // 2) * (ch + 0.018) - ch
        panel(ax, cx, cy, cw, ch, color=T.PANEL)
        ax.add_patch(Rectangle((cx, cy + ch - 0.006), cw, 0.006, color=T.CB_BLUE, zorder=3))
        H(ax, cx + 0.022, cy + ch - 0.044, name, 13.5, T.TEXT, va="center")
        H(ax, cx + 0.022, cy + ch - 0.072, role, 8.5, T.CB_BLUE, va="center")
        ax.plot([cx + 0.022, cx + cw - 0.022], [cy + ch - 0.090, cy + ch - 0.090],
                color=T.HAIRLINE_SOFT, lw=0.7, zorder=3)
        P(ax, cx + 0.022, cy + ch - 0.106, txt, size=8.6, color=T.MUTE, width=47)
        stats = C.PLAYER_STATS.get(name, [])
        if stats:
            ax.plot([cx + 0.022, cx + cw - 0.022], [cy + 0.058, cy + 0.058],
                    color=T.HAIRLINE_SOFT, lw=0.7, zorder=3)
            inner = cw - 0.044
            for j, (val, lab) in enumerate(stats):
                sx = cx + 0.022 + inner * (j + 0.5) / len(stats)
                H(ax, sx, cy + 0.039, val, 13, T.CB_BLUE, ha="center", va="center")
                ax.text(sx, cy + 0.019, lab.upper(), fontsize=6.2, color=T.MUTE,
                        ha="center", va="center", fontfamily=T.BODY_FONT, zorder=6)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_plan(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Game plan", "The concrete recommendations", 11)
    y = TOP
    cw = 0.428; gx = COLW - 2 * cw; ph = 0.330
    panel(ax, MX, y - ph, cw, ph, color=T.PANEL)
    panel(ax, MX + cw + gx, y - ph, cw, ph, color=T.PANEL)
    ax.add_patch(Rectangle((MX, y - 0.006), cw, 0.006, color=T.GOAL, zorder=3))
    ax.add_patch(Rectangle((MX + cw + gx, y - 0.006), cw, 0.006, color=T.CB_BLUE, zorder=3))
    H(ax, MX + 0.022, y - 0.030, "WITH THE BALL", 11, T.GOAL, va="center")
    bullets(ax, MX + 0.022, y - 0.058, C.PLAN_IN, size=8.4, width=43, gap=0.018, mcolor=T.GOAL)
    H(ax, MX + cw + gx + 0.022, y - 0.030, "WITHOUT THE BALL", 11, T.CB_BLUE, va="center")
    bullets(ax, MX + cw + gx + 0.022, y - 0.058, C.PLAN_OUT, size=8.4, width=43, gap=0.018,
            mcolor=T.CB_BLUE)
    y = y - ph - GAP * 1.6
    sec_head(ax, y, "IN-GAME SCENARIOS", 12)
    yy = y - 0.034
    for head, txt in C.PLAN_SCEN:
        H(ax, MX + 0.020, yy, head, 10, T.GOAL, va="top")
        yy -= 0.0215
        t = textwrap.fill(txt, width=106)
        ax.text(MX + 0.020, yy, t, fontsize=9, color=T.MUTE, va="top",
                fontfamily=T.BODY_FONT, linespacing=1.32, zorder=6)
        yy -= (t.count("\n") + 1) * 0.0168 + 0.018
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_week(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Matchweek delivery", "What I'd tell the players, day by day", 12)
    y = TOP
    P(ax, MX, y, C.WEEK_INTRO, size=9.4, color=T.MUTE, width=108)
    y -= 0.058
    rows = C.WEEK_DAYS
    avail = y - FLOOR
    ch = (avail - GAP * (len(rows) - 1) * 0.5) / len(rows)
    for day, txt in rows:
        panel(ax, MX, y - ch, COLW, ch, color=T.PANEL)
        ax.add_patch(Rectangle((MX, y - ch), 0.006, ch, color=T.CB_BLUE, zorder=3))
        H(ax, MX + 0.028, y - 0.024, day, 11.5, T.TEXT, va="center")
        P(ax, MX + 0.028, y - 0.044, txt, size=8.7, color=T.MUTE, width=104)
        y -= ch + GAP * 0.5
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def page_method(pdf):
    fig, ax = new_page()
    chrome(fig, ax, "Appendix", "Method, honesty & intent", 13)
    y = TOP
    y = sec_head(ax, y, "HOW THIS WAS BUILT", 12) - 0.006
    P(ax, MX + 0.020, y, C.METHOD, size=9.4, color=T.MUTE, width=106)
    n = textwrap.fill(C.METHOD, width=106).count("\n") + 1
    y -= n * 0.0172 + GAP
    y = sec_head(ax, y, "WHAT I'D ADD WITH MORE TIME / DATA", 11.5) - 0.010
    y = bullets(ax, MX + 0.020, y, C.CAVEATS, size=9.0, width=102, gap=0.030, mcolor=T.CB_BLUE)
    h = (y - GAP) - FLOOR
    panel(ax, MX, FLOOR, COLW, h, color=T.PANEL_2, ec=T.LINE)
    H(ax, MX + 0.028, y - GAP - 0.030, "WHY THIS ROLE, WHY THIS WAY", 11, T.CB_BLUE, va="center")
    P(ax, MX + 0.028, y - GAP - 0.052, C.WHY_TEXT, size=9.6, color=T.TEXT, width=98)
    pdf.savefig(fig, facecolor=T.INK); plt.close(fig)


def build():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    with PdfPages(OUT_PDF) as pdf:
        page_cover(pdf)
        page_exec(pdf)
        page_probable_xi(pdf)
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
