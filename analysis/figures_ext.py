"""Extra presentation-grade figures: radars, squad ranking bars, attack
zones by half, transition map."""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from mplsoccer import VerticalPitch, Pitch
from matplotlib.patches import FancyArrow

import theme as T
from figures import EV, TEAM, OPP, MET, save, short, STROKE
from parse import SHOT_TYPES, TYPE_BALL_RECOVERY, TYPE_PASS

T.apply()
FIG = os.path.join(os.path.dirname(__file__), "..", "output", "figures")
with open(os.path.join(os.path.dirname(__file__), "..", "output", "metrics_ext.json"),
          encoding="utf-8") as f:
    EXT = json.load(f)
PT = pd.DataFrame(EXT["player_table"])


# ---------------------------------------------------------------------------
# Radar (percentile vs squad)
# ---------------------------------------------------------------------------
def fig_radar(name, fname):
    axes_lbl = EXT["radar_axes"]
    vals = EXT["radars"][name]["values"]
    n = len(axes_lbl)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ang = np.r_[ang, ang[:1]]
    v = np.r_[vals, vals[:1]]
    fig, ax = plt.subplots(figsize=(4.4, 4.4), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(T.INK); ax.set_facecolor(T.INK)
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    for r in (25, 50, 75, 100):
        ax.plot(np.linspace(0, 2 * np.pi, 200), [r] * 200, color=T.LINE, lw=0.6, alpha=0.6)
    ax.plot(ang, v, color=T.FEY, lw=2.3)
    ax.fill(ang, v, color=T.FEY, alpha=0.32)
    ax.scatter(ang[:-1], v[:-1], color=T.FEY, s=22, zorder=5, edgecolor=T.EDGE, lw=0.8)
    ax.set_xticks(ang[:-1])
    ax.set_xticklabels(axes_lbl, fontsize=7.6, color=T.MUTE, fontfamily=T.BODY_FONT)
    ax.set_yticks([]); ax.set_ylim(0, 100)
    ax.spines["polar"].set_color(T.LINE)
    ax.set_title("percentile vs squad", fontsize=7.5, color=T.FAINT, pad=8)
    return save(fig, fname)


# ---------------------------------------------------------------------------
# Squad ranking bars (multi-panel)
# ---------------------------------------------------------------------------
def fig_rankbars():
    panels = [
        ("xG", "xg", T.FEY), ("Shots", "shots", T.FEY),
        ("Chances created", "chances", T.CB_BLUE), ("Take-ons", "take_ons", T.GREEN),
        ("Progressive passes", "prog", T.CB_BLUE), ("Ball recoveries", "recoveries", T.GREEN),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(11.5, 5.0))
    fig.subplots_adjust(left=0.10, right=0.985, top=0.92, bottom=0.05,
                        wspace=0.95, hspace=0.42)
    for ax, (title, col, color) in zip(axes.ravel(), panels):
        d = PT.sort_values(col, ascending=False).head(8)[::-1]
        labels = [short(p) for p in d.player]
        y = np.arange(len(d))
        ax.barh(y, d[col], color=color, alpha=0.85, height=0.66)
        ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7.6, color=T.TEXT)
        ax.set_title(title, fontsize=10, color=T.TEXT, fontfamily=T.HEAD_FONT,
                     weight="bold", loc="left", pad=6)
        for i, v in enumerate(d[col]):
            ax.text(v, i, f" {v:.1f}" if col == "xg" else f" {int(v)}",
                    va="center", fontsize=7.4, color=T.MUTE)
        for s in ["top", "right", "bottom"]:
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(T.LINE); ax.tick_params(length=0); ax.set_xticks([])
    return save(fig, "10_rankbars.png")


# ---------------------------------------------------------------------------
# Attack zones by half (costados-style arrows)
# ---------------------------------------------------------------------------
def fig_attackzones():
    az = EXT["attack_zones_half"]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.6))
    for ax, (half, ttl) in zip(axes, [("h1", "FIRST HALF"), ("h2", "SECOND HALF")]):
        p = VerticalPitch(pitch_type="opta", half=False, pitch_color=T.INK,
                          line_color=T.LINE, linewidth=1.0)
        p.draw(ax=ax)
        z = az[half]
        # three vertical lanes, arrow size ~ share
        lanes = [("left", 83, T.FEY), ("central", 50, T.FEY), ("right", 17, T.FEY)]
        for key, xc, col in lanes:
            share = z[key]
            w = 3 + share / 100 * 22
            ax.annotate("", xy=(xc, 86), xytext=(xc, 55),
                        arrowprops=dict(arrowstyle="-|>", color=col,
                                        lw=w / 3, alpha=0.45 + share / 200,
                                        mutation_scale=18))
            ax.text(xc, 48, f"{int(share)}%", ha="center", va="top", fontsize=12,
                    color=T.TEXT, fontfamily=T.HEAD_FONT, weight="bold",
                    path_effects=STROKE)
        ax.set_title(ttl, fontsize=10, color=T.MUTE, fontfamily=T.HEAD_FONT,
                     weight="bold", pad=4)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02, wspace=0.05)
    return save(fig, "11_attackzones.png")


# ---------------------------------------------------------------------------
# Transition map: where they win it (recoveries) + where they're punished
# ---------------------------------------------------------------------------
def fig_transition():
    team = EV[EV.is_team]
    rec = team[team.type_id == TYPE_BALL_RECOVERY]
    osh = OPP[OPP.type_id.isin(SHOT_TYPES)]
    fig = plt.figure(figsize=(11.4, 4.8))
    # left: recoveries
    ax1 = fig.add_axes([0.02, 0.06, 0.46, 0.88])
    p1 = Pitch(pitch_type="opta", pitch_color=T.INK, line_color=T.LINE, linewidth=1.0)
    p1.draw(ax=ax1)
    high = rec[rec.x >= 66.67]; mid = rec[(rec.x >= 33.33) & (rec.x < 66.67)]
    low = rec[rec.x < 33.33]
    p1.scatter(low.x, low.y, ax=ax1, s=24, color=T.FAINT, alpha=0.5)
    p1.scatter(mid.x, mid.y, ax=ax1, s=30, color=T.CB_BLUE, alpha=0.6)
    p1.scatter(high.x, high.y, ax=ax1, s=60, color=T.GREEN, alpha=0.85,
               edgecolor=T.EDGE, linewidth=0.6)
    ax1.axvline(rec.x.mean(), color=T.GOAL, lw=1.6, ls=(0, (5, 3)))
    ax1.set_title("WHERE THEY WIN IT BACK  ·  green = high turnovers",
                  fontsize=9, color=T.TEXT, fontfamily=T.HEAD_FONT, weight="bold", pad=6)
    ax1.text(2, 2, "Attacking  →", fontsize=8, color=T.MUTE, fontfamily=T.BODY_FONT)
    # right: where they concede (final third, attacking towards goal)
    ax2 = fig.add_axes([0.52, 0.06, 0.46, 0.88])
    p2 = VerticalPitch(pitch_type="opta", half=True, pad_bottom=-12,
                       pitch_color=T.INK, line_color=T.LINE, linewidth=1.0)
    p2.draw(ax=ax2)
    g = osh[osh.is_goal]; o = osh[~osh.is_goal]
    p2.scatter(o.x, o.y, ax=ax2, s=40 + o.xg * 900, color=T.CB_BLUE, alpha=0.45)
    p2.scatter(g.x, g.y, ax=ax2, s=70 + g.xg * 1100, color=T.WARN, alpha=0.95,
               edgecolor=T.EDGE, linewidth=0.7)
    ax2.set_ylim(54, 103)
    ax2.set_title("WHERE THEY GET PUNISHED  ·  orange = goals conceded",
                  fontsize=9, color=T.TEXT, fontfamily=T.HEAD_FONT, weight="bold", pad=6)
    return save(fig, "12_transition.png")


RADAR_FILES = {
    "Orkun Kökçü": "r_kokcu.png",
    "Quinten Timber": "r_timber.png",
    "Sebastian Szymanski": "r_szymanski.png",
    "Javairô Dilrosun": "r_dilrosun.png",
    "Dávid Hancko": "r_hancko.png",
    "Danilo Pereira da Silva": "r_danilo.png",
}

if __name__ == "__main__":
    for nm, fn in RADAR_FILES.items():
        if nm in EXT["radars"]:
            fig_radar(nm, fn)
    fig_rankbars()
    fig_attackzones()
    fig_transition()
    print("ext figures done")
