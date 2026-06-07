"""Generate the analytical figures for the Feyenoord dossier."""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
from mplsoccer import Pitch, VerticalPitch
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap
import theme as T
from parse import (load_team, SHOT_TYPES, DEF_ACTION_TYPES, TYPE_PASS,
                   TYPE_BALL_RECOVERY)

STROKE = [pe.withStroke(linewidth=2.4, foreground=T.STROKE_BG)]


def attack_arrow(ax, x=2, y=2):
    ax.text(x, y, "Attacking  →", fontsize=9, color=T.MUTE,
            fontfamily=T.BODY_FONT)


# house-style colormaps (paper/ink -> Feyenoord red -> bright)
CMAP_RED = LinearSegmentedColormap.from_list(
    "fey_red", [T.INK, "#3A0A14", T.FEY_D, T.FEY, "#FF5A78"])
CMAP_COOL = LinearSegmentedColormap.from_list(
    "fey_cool", [T.INK, "#0E2238", T.CB_BLUE_D, T.CB_BLUE, "#7FB6F0"])

T.apply()
FIG = os.path.join(os.path.dirname(__file__), "..", "output", "figures")
os.makedirs(FIG, exist_ok=True)

EV, MATCHES, PLAYERS = load_team("Feyenoord")
TEAM = EV[EV.is_team].copy()
OPP = EV[~EV.is_team].copy()
M = len(MATCHES)

with open(os.path.join(os.path.dirname(__file__), "..", "output", "metrics.json"),
          encoding="utf-8") as f:
    MET = json.load(f)


def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p, bbox_inches="tight", pad_inches=0.18, facecolor=T.INK)
    plt.close(fig)
    print("wrote", name)
    return p


def short(name):
    """Last name for labels, handling 'da Silva' etc."""
    if not name:
        return ""
    parts = name.split()
    if len(parts) >= 2 and parts[-2].lower() in ("da", "de", "van", "der", "dos"):
        return " ".join(parts[-2:])
    return parts[-1]


# ---------------------------------------------------------------------------
# 1. Form & xG timeline
# ---------------------------------------------------------------------------
def fig_form():
    xg = MET["xg_per_match"]; xga = MET["xga_per_match"]
    games = MET["matches"]
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    fig.subplots_adjust(left=0.065, right=0.985, top=0.80, bottom=0.205)
    x = np.arange(M)
    T.style_axes(ax, grid=True)
    # bklit-style gradient areas
    T.gradient_area(ax, x, xg, T.FEY, lw=2.8, alpha=0.50, label="xG for")
    T.gradient_area(ax, x, xga, T.CB_BLUE, lw=2.4, alpha=0.42, label="xG against")
    for i, g in enumerate(games):
        col = {"W": T.GREEN, "D": T.MUTE, "L": T.WARN}[g["res"]]
        ax.text(i, -0.62, f"{g['venue']} {short(g['opp'])[:8]}", rotation=40,
                ha="right", va="top", fontsize=7.5, color=T.MUTE)
        ax.text(i, max(xg[i], xga[i]) + 0.30, f"{g['gf']}-{g['ga']}",
                ha="center", fontsize=8.5, color=col, fontfamily=T.HEAD_FONT, weight="bold")
    ax.set_xlim(-0.4, M - 0.6); ax.set_ylim(0, 4.4)
    ax.set_xticks([])
    ax.set_ylabel("Expected goals", fontsize=9, color=T.MUTE)
    leg = ax.legend(loc="upper right", frameon=False, fontsize=9.5,
                    labelcolor=T.TEXT, ncol=2, bbox_to_anchor=(1.0, 1.17),
                    handlelength=1.3)
    return save(fig, "01_form.png")


def fig_momentum():
    """Cumulative goals for/against over the window — bklit area style."""
    games = MET["matches"]
    gf = np.cumsum([g["gf"] for g in games])
    ga = np.cumsum([g["ga"] for g in games])
    x = np.arange(M)
    fig, ax = plt.subplots(figsize=(9.6, 3.0))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.16)
    T.style_axes(ax, grid=True)
    T.gradient_area(ax, x, gf, T.FEY, lw=2.8, alpha=0.50, label="goals for")
    T.gradient_area(ax, x, ga, T.CB_BLUE, lw=2.4, alpha=0.40, label="goals against")
    ax.text(M - 1, gf[-1] + 0.6, f"{int(gf[-1])}", color=T.FEY, fontsize=12,
            fontfamily=T.HEAD_FONT, weight="bold", ha="center")
    ax.text(M - 1, ga[-1] + 0.6, f"{int(ga[-1])}", color=T.CB_BLUE, fontsize=11,
            fontfamily=T.HEAD_FONT, weight="bold", ha="center")
    ax.set_xlim(-0.2, M - 0.8); ax.set_ylim(0, max(gf) + 3)
    ax.set_xticks(x)
    ax.set_xticklabels([f"MD{i+1}" for i in range(M)], fontsize=7.5, color=T.MUTE)
    ax.set_ylabel("Cumulative goals", fontsize=9, color=T.MUTE)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5, labelcolor=T.TEXT,
              ncol=2, handlelength=1.3)
    return save(fig, "09_momentum.png")


# ---------------------------------------------------------------------------
# 2. Shot map (for)
# ---------------------------------------------------------------------------
def fig_shotmap():
    sh = TEAM[TEAM.type_id.isin(SHOT_TYPES)].copy()
    pitch = VerticalPitch(pitch_type="opta", half=True, pad_bottom=-8,
                          pitch_color=T.INK, line_color=T.LINE, linewidth=1.2,
                          line_zorder=2)
    fig, ax = pitch.draw(figsize=(6.6, 6.6))
    goals = sh[sh.is_goal]; other = sh[~sh.is_goal]
    pitch.scatter(other.x, other.y, s=60 + other.xg * 1400, ax=ax,
                  facecolor=T.FEY, edgecolor="none", alpha=0.40, zorder=3)
    pitch.scatter(goals.x, goals.y, s=90 + goals.xg * 1600, ax=ax,
                  facecolor=T.GOAL, edgecolor=T.EDGE, linewidth=0.8, alpha=0.95,
                  zorder=4)
    ax.set_ylim(54, 103)
    return save(fig, "02_shotmap.png")


# ---------------------------------------------------------------------------
# 3. Pass network of most-used XI (recipients inferred from next same-team event)
# ---------------------------------------------------------------------------
def fig_network():
    xi = {r["player"] for r in MET["most_used_xi"][:11]}
    # infer recipient = player of the next team event after a completed pass
    df = EV[EV.is_team].sort_values(["match_index"]).reset_index(drop=True)
    avg = {}  # player -> [xs, ys]
    edges = {}  # (a,b) sorted -> count
    for mi in range(M):
        g = TEAM[TEAM.match_index == mi].reset_index(drop=True)
        for i in range(len(g) - 1):
            e = g.iloc[i]
            if e.type_id == TYPE_PASS and e.outcome == 1 and e.player in xi:
                nxt = g.iloc[i + 1]
                if nxt.player in xi and nxt.player != e.player:
                    key = tuple(sorted((e.player, nxt.player)))
                    edges[key] = edges.get(key, 0) + 1
            if e.player in xi:
                avg.setdefault(e.player, [[], []])
                avg[e.player][0].append(e.x); avg[e.player][1].append(e.y)
    pos = {p: (np.mean(v[0]), np.mean(v[1])) for p, v in avg.items() if len(v[0]) > 5}
    touch = {p: len(v[0]) for p, v in avg.items()}

    pitch = Pitch(pitch_type="opta", pitch_color=T.INK, line_color=T.LINE,
                  linewidth=1.1, line_zorder=1)
    fig, ax = pitch.draw(figsize=(9.4, 6.2))
    if edges:
        mx = max(edges.values())
    for (a, b), c in edges.items():
        if a in pos and b in pos and c >= 4:
            x1, y1 = pos[a]; x2, y2 = pos[b]
            ax.plot([x1, x2], [y1, y2], color=T.CB_BLUE,
                    lw=0.6 + 4.5 * c / mx, alpha=0.18 + 0.5 * c / mx, zorder=2)
    tmax = max(touch.values()) if touch else 1
    cxn = np.mean([p[0] for p in pos.values()])
    cyn = np.mean([p[1] for p in pos.values()])
    for p, (x, y) in pos.items():
        s = 190 + 560 * touch[p] / tmax
        pitch.scatter([x], [y], s=s, ax=ax, facecolor=T.FEY, edgecolor=T.TEXT,
                      linewidth=1.1, alpha=0.95, zorder=4)
        sh = next((r["shirt"] for r in MET["most_used_xi"] if r["player"] == p), "")
        ax.text(x, y, str(sh), ha="center", va="center", fontsize=8,
                color=T.TEXT, fontfamily=T.HEAD_FONT, weight="bold", zorder=6,
                path_effects=STROKE)
        # push the name label radially outward from the cluster centroid
        ang = np.arctan2(y - cyn, x - cxn)
        if abs(y - cyn) < 1 and abs(x - cxn) < 1:
            ang = -np.pi / 2
        lx, ly = x + 6.2 * np.cos(ang), y + 5.0 * np.sin(ang)
        ax.text(lx, ly, short(p), ha="center", va="center", fontsize=7.4,
                color=T.TEXT, zorder=7, path_effects=STROKE)
    # crop to the active region so the figure isn't lopsided / mostly empty
    xs = [p[0] for p in pos.values()]
    ax.set_xlim(min(xs) - 12, max(xs) + 14)
    attack_arrow(ax, x=min(xs) - 10, y=3)
    return save(fig, "03_network.png")


# ---------------------------------------------------------------------------
# 4. Build-up / territory heatmap (final-third tilt)
# ---------------------------------------------------------------------------
def fig_territory():
    # passes that END in the final third — shows where they enter + flank tilt
    tp = TEAM[(TEAM.type_id == TYPE_PASS) & (TEAM.outcome == 1) & (TEAM.end_x >= 66.67)]
    pitch = Pitch(pitch_type="opta", pitch_color=T.INK, line_color=T.LINE,
                  linewidth=1.1, line_zorder=3, half=False)
    fig, ax = pitch.draw(figsize=(9.4, 6.2))
    # shade the final third
    ax.axvspan(66.67, 100, color=T.PANEL, alpha=0.35, zorder=0)
    bs = pitch.bin_statistic(tp.end_x, tp.end_y, statistic="count", bins=(12, 12))
    bs["statistic"] = gaussian_filter(bs["statistic"], 0.8)
    pitch.heatmap(bs, ax=ax, cmap=CMAP_RED, alpha=0.95, zorder=1)
    # flank guide lines
    for yy in (33.33, 66.67):
        ax.axhline(yy, color=T.LINE, lw=0.8, ls=(0, (4, 4)), zorder=3, alpha=0.7)
    f = MET["final_third_entry_flank"]
    for yc, key, lab in [(83, "left", "LEFT"), (50, "central", "CENTRAL"),
                         (17, "right", "RIGHT")]:
        ax.text(50, yc, f"{lab}\n{f[key]}%", ha="center", va="center",
                fontsize=12, color=T.TEXT, fontfamily=T.HEAD_FONT, weight="bold",
                zorder=5, path_effects=STROKE)
    ax.text(50, 104, "Where Feyenoord enter the final third  (pass end-points)",
            ha="center", fontsize=9.5, color=T.MUTE, fontfamily=T.BODY_FONT)
    attack_arrow(ax)
    return save(fig, "04_territory.png")


# ---------------------------------------------------------------------------
# 5. Pressing / ball-recovery map (block height)
# ---------------------------------------------------------------------------
def fig_press():
    rec = TEAM[TEAM.type_id == TYPE_BALL_RECOVERY]
    defact = TEAM[TEAM.type_id.isin(DEF_ACTION_TYPES)]
    pitch = Pitch(pitch_type="opta", pitch_color=T.INK, line_color=T.LINE,
                  linewidth=1.1, line_zorder=2)
    fig, ax = pitch.draw(figsize=(9.4, 6.2))
    bs = pitch.bin_statistic(defact.x, defact.y, statistic="count", bins=(18, 12))
    bs["statistic"] = gaussian_filter(bs["statistic"], 0.9)
    pitch.heatmap(bs, ax=ax, cmap=CMAP_COOL, alpha=0.85, zorder=1)
    mx = rec.x.mean()
    ax.axvline(mx, color=T.GOAL, lw=2, ls=(0, (5, 3)), zorder=3)
    ax.text(mx + 1, 64, f"avg recovery\nx = {mx:.0f}", color=T.GOAL, fontsize=8.5,
            fontfamily=T.HEAD_FONT, weight="bold", zorder=4, va="top")
    p = MET["press"]
    ax.text(50, 104, f"PPDA {p['ppda']}   high turnovers {p['high_turnovers_pg']}/game   "
            f"def-third actions {p['def_actions_def_third_pct']}%",
            ha="center", fontsize=9.5, color=T.MUTE, fontfamily=T.BODY_FONT)
    attack_arrow(ax)
    return save(fig, "05_press.png")


# ---------------------------------------------------------------------------
# 6. Vulnerability map: shots conceded (opp shots towards Feyenoord goal)
# ---------------------------------------------------------------------------
def fig_vulnerability():
    sh = OPP[OPP.type_id.isin(SHOT_TYPES)].copy()
    pitch = VerticalPitch(pitch_type="opta", half=True, pad_bottom=-8,
                          pitch_color=T.INK, line_color=T.LINE, linewidth=1.2,
                          line_zorder=2)
    fig, ax = pitch.draw(figsize=(6.6, 6.6))
    goals = sh[sh.is_goal]; other = sh[~sh.is_goal]
    fast = sh[sh.fast_break]
    pitch.scatter(other.x, other.y, s=60 + other.xg * 1400, ax=ax,
                  facecolor=T.CB_BLUE, edgecolor="none", alpha=0.42, zorder=3)
    pitch.scatter(goals.x, goals.y, s=90 + goals.xg * 1600, ax=ax,
                  facecolor=T.WARN, edgecolor=T.EDGE, linewidth=0.8, alpha=0.95, zorder=4)
    if len(fast):
        pitch.scatter(fast.x, fast.y, s=240, ax=ax, facecolor="none",
                      edgecolor=T.GOAL, linewidth=1.8, zorder=5)
    ax.set_ylim(54, 103)
    return save(fig, "06_vulnerability.png")


# ---------------------------------------------------------------------------
# 7. Set-piece shots (for and against)
# ---------------------------------------------------------------------------
def fig_setpiece():
    sf = TEAM[(TEAM.type_id.isin(SHOT_TYPES)) & ((TEAM.from_corner) | (TEAM.from_setpiece))]
    sa = OPP[(OPP.type_id.isin(SHOT_TYPES)) & ((OPP.from_corner) | (OPP.from_setpiece))]
    pitch = VerticalPitch(pitch_type="opta", half=True, pad_bottom=-8,
                          pitch_color=T.INK, line_color=T.LINE, linewidth=1.2)
    fig, axes = pitch.draw(figsize=(9.4, 5.2), ncols=2)
    for ax, df, col, ttl in [
            (axes[0], sf, T.FEY, f"THREAT  •  {len(sf)} shots / {int(sf.is_goal.sum())} goals / {sf.xg.sum():.1f} xG"),
            (axes[1], sa, T.WARN, f"CONCEDED  •  {len(sa)} shots / {int(sa.is_goal.sum())} goals / {sa.xg.sum():.1f} xG")]:
        g = df[df.is_goal]; o = df[~df.is_goal]
        pitch.scatter(o.x, o.y, s=70 + o.xg * 1200, ax=ax, facecolor=col,
                      edgecolor="none", alpha=0.45)
        pitch.scatter(g.x, g.y, s=110 + g.xg * 1400, ax=ax, facecolor=T.GOAL,
                      edgecolor=T.EDGE, linewidth=0.8, alpha=0.95)
        ax.set_ylim(62, 109)
        ax.text(50, 108, ttl, ha="center", va="top", fontsize=10,
                color=T.TEXT, fontfamily=T.HEAD_FONT, weight="bold")
    return save(fig, "07_setpiece.png")


# ---------------------------------------------------------------------------
# 8. Key player contribution chart
# ---------------------------------------------------------------------------
def fig_players():
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 4.4))
    fig.subplots_adjust(left=0.16, right=0.97, top=0.84, bottom=0.08, wspace=1.25)
    panels = [
        ("Goals + xG", MET["players"]["xg"], MET["players"]["scorers"], T.FEY),
        ("Chances created", MET["players"]["chances_created"], None, T.CB_BLUE),
        ("Take-ons completed", MET["players"]["take_ons"], None, T.GREEN),
    ]
    for ax, (title, series, overlay, col) in zip(axes, panels):
        series = series[:6][::-1]
        labels = [short(d["player"]) for d in series]
        vals = [d["value"] for d in series]
        y = np.arange(len(series))
        ax.barh(y, vals, color=col, alpha=0.85, height=0.66)
        if overlay:  # goals overlay on xG panel
            gmap = {short(d["player"]): d["value"] for d in overlay}
            gv = [gmap.get(l, 0) for l in labels]
            ax.scatter(gv, y, color=T.GOAL, s=42, zorder=4, edgecolor=T.EDGE, lw=0.6)
        ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8.5, color=T.TEXT)
        ax.set_title(title, fontsize=10.5, color=T.TEXT, fontfamily=T.HEAD_FONT,
                     weight="bold", loc="left", pad=8)
        for i, v in enumerate(vals):
            ax.text(v, i, f" {v:.0f}" if v == int(v) else f" {v:.1f}",
                    va="center", fontsize=8, color=T.MUTE)
        for s in ["top", "right", "bottom"]:
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(T.LINE)
        ax.tick_params(length=0); ax.set_xticks([])
    axes[0].text(0, 1.18, "gold dot = goals scored", transform=axes[0].transAxes,
                 fontsize=8, color=T.GOAL)
    return save(fig, "08_players.png")


if __name__ == "__main__":
    fig_form()
    fig_momentum()
    fig_shotmap()
    fig_network()
    fig_territory()
    fig_press()
    fig_vulnerability()
    fig_setpiece()
    fig_players()
    print("all figures done")
