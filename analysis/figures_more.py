"""Elite-tier figures: transition press map, game-state, formation split, corners."""
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
from mplsoccer import Pitch, VerticalPitch
from scipy.ndimage import gaussian_filter

import theme as T

T.apply()
FIG = os.path.join(os.path.dirname(__file__), "..", "output", "figures")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")
STROKE = [pe.withStroke(linewidth=2.4, foreground=T.STROKE_BG)]

MORE = json.load(open(os.path.join(OUT, "metrics_more.json"), encoding="utf-8"))


def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p, bbox_inches="tight", pad_inches=0.16, facecolor=T.INK)
    plt.close(fig)
    print("wrote", name)
    return p


# ---------------------------------------------------------------------------
# 13. Transition press map: Feyenoord ball-losses that became a shot < 15s
# ---------------------------------------------------------------------------
def fig_transition_press():
    losses = MORE["transition"]["losses"]
    xs = np.array([l["x"] for l in losses])
    ys = np.array([l["y"] for l in losses])
    xg = np.array([l["shot_xg"] for l in losses])
    goal = np.array([l["goal"] for l in losses])
    pitch = Pitch(pitch_type="opta", pitch_color=T.INK, line_color=T.LINE,
                  linewidth=1.1, line_zorder=3)
    fig, ax = pitch.draw(figsize=(9.6, 5.4))
    # press zone: their defensive + middle third (where losses cluster)
    ax.axvspan(0, 66.67, color=T.FEY, alpha=0.05, zorder=0)
    ax.axvline(66.67, color=T.LINE, lw=0.8, ls=(0, (4, 4)), zorder=1)
    pitch.scatter(xs[~goal], ys[~goal], s=60 + xg[~goal] * 1500, ax=ax,
                  facecolor=T.WARN, edgecolor="none", alpha=0.5, zorder=4)
    pitch.scatter(xs[goal], ys[goal], s=90 + xg[goal] * 1700, ax=ax,
                  facecolor=T.GOAL, edgecolor=T.EDGE, lw=0.8, alpha=0.95, zorder=5)
    avg = MORE["transition"]["avg_loss_x"]
    ax.axvline(avg, color=T.FEY, lw=2, ls=(0, (5, 3)), zorder=4)
    ax.text(avg + 1, 6, f"avg loss x={avg:.0f}", color=T.FEY, fontsize=8.5,
            fontfamily=T.HEAD_FONT, weight="bold", zorder=6)
    ax.text(33, 104, "PRESS ZONE — losses here become shots against",
            ha="center", fontsize=9.5, color=T.MUTE, fontfamily=T.BODY_FONT)
    ax.text(2, 2, "Feyenoord attacking  →", fontsize=9, color=T.FAINT,
            fontfamily=T.BODY_FONT)
    return save(fig, "13_transition_press.png")


# ---------------------------------------------------------------------------
# 14. Game-state: xG / xGA by 15-minute window
# ---------------------------------------------------------------------------
def fig_gamestate():
    gs = MORE["game_state_15"]
    labels = [g["bucket"] for g in gs]
    xg = [g["xg"] for g in gs]
    xga = [g["xga"] for g in gs]
    x = np.arange(len(gs))
    fig, ax = plt.subplots(figsize=(9.6, 3.5))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.16)
    T.style_axes(ax, grid=True)
    w = 0.4
    ax.bar(x - w/2, xg, w, color=T.FEY, label="xG for", zorder=3)
    ax.bar(x + w/2, xga, w, color=T.CB_BLUE, label="xG against", zorder=3)
    # highlight the soft spot (15-30) and late dominance
    ax.annotate("their soft spot\n2.9 xGA · 4 conceded", xy=(1 + w/2, xga[1]),
                xytext=(1.4, 4.0), fontsize=8, color=T.CB_BLUE, fontfamily=T.BODY_FONT,
                ha="left", arrowprops=dict(arrowstyle="-", color=T.CB_BLUE, lw=0.8))
    ax.annotate("ruthless late\n12 goals 60'+", xy=(4.5, xg[4]),
                xytext=(4.0, 4.3), fontsize=8, color=T.FEY, fontfamily=T.BODY_FONT,
                ha="left", arrowprops=dict(arrowstyle="-", color=T.FEY, lw=0.8))
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.5, color=T.MUTE)
    ax.set_ylim(0, 5.0)
    ax.set_ylabel("Expected goals (10-game total)", fontsize=8.5, color=T.MUTE)
    ax.set_xlabel("Match minute", fontsize=8.5, color=T.MUTE)
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=T.TEXT, ncol=2)
    return save(fig, "14_gamestate.png")


# ---------------------------------------------------------------------------
# 15. Formation split: 4-2-3-1 vs 4-3-3
# ---------------------------------------------------------------------------
def fig_formation():
    fs = MORE["formation_split"]
    a, b = fs["4231"], fs["433"]
    rows = [
        ("xG / game", a["xg_pg"], b["xg_pg"], "{:.2f}"),
        ("xGA / game", a["xga_pg"], b["xga_pg"], "{:.2f}"),
        ("Shots / game", a["shots_pg"], b["shots_pg"], "{:.0f}"),
        ("Left-side entries %", a["left_pct"], b["left_pct"], "{:.0f}%"),
        ("Crosses / game", a["crosses_pg"], b["crosses_pg"], "{:.0f}"),
        ("PPDA (their press)", a["ppda"], b["ppda"], "{:.1f}"),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    fig.subplots_adjust(left=0.30, right=0.97, top=0.80, bottom=0.06)
    y = np.arange(len(rows))[::-1]
    maxv = [max(r[1], r[2]) for r in rows]
    for i, (lab, va, vb, fmt) in zip(y, rows):
        m = max(va, vb) * 1.5 + 1e-9
        ax.barh(i + 0.18, va / m, 0.34, color=T.MUTE, alpha=0.55, zorder=3)
        ax.barh(i - 0.18, vb / m, 0.34, color=T.FEY, zorder=3)
        ax.text(va / m + 0.01, i + 0.18, fmt.format(va), va="center", fontsize=8.5,
                color=T.TEXT, fontfamily=T.HEAD_FONT)
        ax.text(vb / m + 0.01, i - 0.18, fmt.format(vb), va="center", fontsize=8.5,
                color=T.FEY, fontfamily=T.HEAD_FONT, weight="bold")
        ax.text(-0.02, i, lab, va="center", ha="right", fontsize=9, color=T.MUTE,
                fontfamily=T.BODY_FONT)
    ax.set_xlim(0, 0.8); ax.set_yticks([]); ax.set_xticks([])
    ax.set_ylim(-0.7, len(rows) - 0.3)
    for s in ax.spines.values():
        s.set_visible(False)
    # legend above the plot (axes fraction)
    ax.text(0.0, 1.06, "4-2-3-1", color=T.MUTE, fontsize=10.5, fontfamily=T.HEAD_FONT,
            weight="bold", transform=ax.transAxes, va="bottom")
    ax.text(0.16, 1.06, "4-3-3", color=T.FEY, fontsize=10.5, fontfamily=T.HEAD_FONT,
            weight="bold", transform=ax.transAxes, va="bottom")
    ax.text(1.0, 1.06, "5 games each", color=T.FAINT, fontsize=8,
            fontfamily=T.BODY_FONT, transform=ax.transAxes, ha="right", va="bottom")
    return save(fig, "15_formation.png")


# ---------------------------------------------------------------------------
# 16. Corner delivery breakdown
# ---------------------------------------------------------------------------
def fig_corner_delivery():
    sd = MORE["setpiece_delivery"]
    pitch = VerticalPitch(pitch_type="opta", half=True, pad_bottom=-12,
                          pitch_color=T.INK, line_color=T.LINE, linewidth=1.2)
    fig, ax = pitch.draw(figsize=(6.2, 5.6))
    ax.set_ylim(66, 103)
    # corner sources (left y>66.7 -> appears on one side); draw arcs to targets
    # left corner -> from (x~100,y~100); right corner -> (x~100,y~0)
    def arc(x0, y0, x1, y1, color, lw):
        ax.add_patch(FancyArrowPatch((y0, x0), (y1, x1),
                     connectionstyle="arc3,rad=0.25", arrowstyle="-|>",
                     mutation_scale=11, color=color, lw=lw, alpha=0.9, zorder=5))
    # note: VerticalPitch swaps axes; pitch.scatter handles, but FancyArrow uses display
    # Use pitch.lines/scatter instead for safety
    # left corner (more frequent): from top-left corner to far post
    pitch.scatter([100], [100], s=120, ax=ax, color=T.FEY, zorder=6)
    pitch.scatter([100], [0], s=90, ax=ax, color=T.MUTE, zorder=6)
    pitch.lines(100, 100, 94, 38, ax=ax, color=T.FEY, lw=3, alpha=0.8,
                comet=True, zorder=5)
    pitch.lines(100, 0, 94, 60, ax=ax, color=T.MUTE, lw=2.4, alpha=0.7,
                comet=True, zorder=5)
    # target labels
    ax.text(50, 104, "CORNERS — delivery pattern", ha="center", fontsize=9.5,
            color=T.MUTE, fontfamily=T.BODY_FONT)
    return save(fig, "16_corner_delivery.png")


if __name__ == "__main__":
    fig_transition_press()
    fig_gamestate()
    fig_formation()
    # corner delivery is schematic; guard it
    try:
        fig_corner_delivery()
    except Exception as e:
        print("corner fig skipped:", e)
    print("more figures done")
