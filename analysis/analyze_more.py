"""
Elite-tier additions computed from the raw F24 feed:
  - flank convention validation (stated explicitly)
  - formation split  (4-2-3-1 vs 4-3-3, 5 games each)
  - turnover -> shot-against chains (the transition MECHANISM)
  - set-piece delivery patterns (corner side / target / first contact)
  - game-state & 15-minute profile
  - build-up triggers (where Kökçü receives & progresses)
  - per-match ranges + finishing over-performance
  - duel numbers (take-on attempts & success, flank)

Writes output/metrics_more.json.
"""
import os
import json
from collections import defaultdict

import numpy as np
import pandas as pd

from parse import (load_team, SHOT_TYPES, TYPE_PASS, TYPE_BALL_RECOVERY,
                   TYPE_TACKLE, TYPE_INTERCEPTION, TYPE_FOUL, TYPE_CHALLENGE,
                   TYPE_TAKE_ON, TYPE_DISPOSSESSED, TYPE_TURNOVER, TYPE_GOAL)

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
TEAM = "Feyenoord"


def flank(y):
    return "right" if y < 33.33 else ("left" if y > 66.67 else "central")


def t_secs(row):
    return row["min"] * 60 + row["sec"]


def validate_convention(team):
    """Confirm y>66.7 == LEFT using known wide players."""
    out = {}
    for nm, exp in [("Pedersen", "right"), ("Marcos", "left"), ("Idrissi", "left"),
                    ("Geertruida", "right"), ("Hancko", "left")]:
        sub = team[team.player.str.contains(nm, na=False)]
        if len(sub):
            out[nm] = {"avg_y": round(float(sub.y.mean()), 1),
                       "side": flank(sub.y.mean()), "expected": exp}
    return out


def formation_split(ev, matches):
    rows = {}
    for form in ["4231", "433"]:
        idx = matches[matches.team_formation == form].match_index.tolist()
        te = ev[(ev.match_index.isin(idx)) & (ev.is_team)]
        oe = ev[(ev.match_index.isin(idx)) & (~ev.is_team)]
        tp = te[te.type_id == TYPE_PASS]; op = oe[oe.type_id == TYPE_PASS]
        tsh = te[te.type_id.isin(SHOT_TYPES)]; osh = oe[oe.type_id.isin(SHOT_TYPES)]
        fp = tp[(tp.outcome == 1) & (tp.end_x >= 66.67)]
        flanks = fp.assign(z=fp.end_y.map(flank)).z.value_counts(normalize=True).mul(100).round(0)
        defact = te[te.type_id.isin({TYPE_TACKLE, TYPE_INTERCEPTION, TYPE_FOUL, TYPE_CHALLENGE}) & (te.x >= 40)]
        opp_passes_own = op[op.x <= 60]
        n = len(idx)
        rows[form] = {
            "games": n,
            "poss": round(100 * len(tp) / max(len(tp) + len(op), 1), 1),
            "shots_pg": round(len(tsh) / n, 1),
            "xg_pg": round(float(tsh.xg.sum()) / n, 2),
            "xga_pg": round(float(osh.xg.sum()) / n, 2),
            "left_pct": float(flanks.get("left", 0)),
            "right_pct": float(flanks.get("right", 0)),
            "ppda": round(len(opp_passes_own) / max(len(defact), 1), 1),
            "crosses_pg": round(len(tp[tp.is_cross]) / n, 1),
            "rec_x": round(float(te[te.type_id == TYPE_BALL_RECOVERY].x.mean()), 1),
        }
    return rows


def turnover_to_shot(ev, matches, window=15):
    """For each opponent shot, find Feyenoord's ball-loss within `window` s before.
    Loss coords are in Feyenoord's attacking frame (x=100 toward opp goal)."""
    losses = []
    transition_shots = 0
    total_opp_shots = 0
    for mi in matches.match_index:
        me = ev[ev.match_index == mi].sort_values(["period", "min", "sec"]).reset_index(drop=True)
        team_loss = me[(me.is_team) & (
            (me.type_id == TYPE_DISPOSSESSED) |
            (me.type_id == TYPE_TURNOVER) |
            ((me.type_id == TYPE_PASS) & (me.outcome == 0)) |
            ((me.type_id == TYPE_TAKE_ON) & (me.outcome == 0)))].copy()
        team_loss["ts"] = team_loss.apply(t_secs, axis=1)
        opp_sh = me[(~me.is_team) & (me.type_id.isin(SHOT_TYPES))].copy()
        for _, s in opp_sh.iterrows():
            total_opp_shots += 1
            st = s["min"] * 60 + s["sec"]
            cand = team_loss[(team_loss.period == s["period"]) &
                             (team_loss.ts <= st) & (team_loss.ts >= st - window)]
            if len(cand):
                last = cand.iloc[-1]
                transition_shots += 1
                losses.append({"x": float(last.x), "y": float(last.y),
                               "third": ("att" if last.x >= 66.67 else
                                         "mid" if last.x >= 33.33 else "def"),
                               "shot_xg": float(s.xg), "goal": bool(s.is_goal),
                               "match": int(mi)})
    by_third = defaultdict(int)
    for l in losses:
        by_third[l["third"]] += 1
    return {
        "window_s": window,
        "opp_shots": total_opp_shots,
        "transition_shots": transition_shots,
        "transition_pct": round(100 * transition_shots / max(total_opp_shots, 1)),
        "loss_third": dict(by_third),
        "losses": losses,
        "avg_loss_x": round(np.mean([l["x"] for l in losses]), 1) if losses else 0,
        "transition_xga": round(sum(l["shot_xg"] for l in losses), 2),
    }


def setpiece_delivery(ev):
    team = ev[ev.is_team]
    corners = team[(team.type_id == TYPE_PASS) & (team.is_corner)]
    # corner side from taker y; target zone from end_y; short = short distance
    side = corners.assign(z=corners.y.map(flank)).z.value_counts().to_dict()
    res = {"corners": int(len(corners)),
           "from_left": int(side.get("left", 0)),
           "from_right": int(side.get("right", 0))}
    # delivery target zone RELATIVE to the corner side (near/far post is defined
    # by which side the corner is taken from, not by absolute pitch y).
    box = corners[(corners.end_x >= 83) & corners.end_y.notna()]
    near = far = central = 0
    for r in box.itertuples():
        if 45 <= r.end_y <= 55:
            central += 1
        elif r.y > 66.67:                 # left corner -> near post is high y
            near += 1 if r.end_y > 55 else 0
            far += 1 if r.end_y < 45 else 0
        elif r.y < 33.33:                 # right corner -> near post is low y
            near += 1 if r.end_y < 45 else 0
            far += 1 if r.end_y > 55 else 0
    res["box_deliveries"] = int(len(box))
    res["to_near"], res["to_far"], res["to_central"] = near, far, central
    res["main_target"] = "near" if near >= far and near >= central else (
        "far" if far >= central else "central")
    short = corners[(corners.end_x < 80)]
    res["short_pct"] = round(100 * len(short) / max(len(corners), 1))
    res["completed_pct"] = round(100 * (corners.outcome == 1).mean()) if len(corners) else 0
    return res


def game_state_15(ev, matches):
    team = ev[ev.is_team]; opp = ev[~ev.is_team]
    tsh = team[team.type_id.isin(SHOT_TYPES)]; osh = opp[opp.type_id.isin(SHOT_TYPES)]
    buckets = [(0, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 92)]
    rows = []
    for a, b in buckets:
        f = tsh[(tsh["min"] >= a) & (tsh["min"] < b)]
        g = osh[(osh["min"] >= a) & (osh["min"] < b)]
        rows.append({"bucket": f"{a}-{b if b<92 else 90}",
                     "xg": round(float(f.xg.sum()), 2), "xga": round(float(g.xg.sum()), 2),
                     "goals": int(f.is_goal.sum()), "ga": int(g.is_goal.sum())})
    return rows


def buildup_triggers(ev):
    team = ev[ev.is_team]
    tp = team[(team.type_id == TYPE_PASS)]
    # Kökçü receiving zone: approximate via his pass-origin avg (where he gets on the ball)
    k = team[team.player.str.contains("Orkun", na=False)]
    kp = k[k.type_id == TYPE_PASS]
    # back-line progressive passers
    out = {
        "kokcu_avg_x": round(float(k.x.mean()), 1),
        "kokcu_avg_y": round(float(k.y.mean()), 1),
        "kokcu_touches": int(len(k)),
        "long_from_keeper": 0,
    }
    gk = team[team.player.str.contains("Bijlow", na=False)]
    gkp = gk[gk.type_id == TYPE_PASS]
    out["keeper_long_pct"] = round(100 * gkp.is_long.mean()) if len(gkp) else 0
    out["keeper_passes"] = int(len(gkp))
    return out


def ranges_and_overperf(ev, matches, metrics):
    poss = metrics["possession_per_match"]
    xg = metrics["xg_per_match"]; xga = metrics["xga_per_match"]
    team = ev[ev.is_team]; tsh = team[team.type_id.isin(SHOT_TYPES)]
    goals = int(tsh.is_goal.sum()); xgsum = float(tsh.xg.sum())
    # PSV game contribution to xga/shot
    psv_idx = matches[matches.opp_name == "PSV"].match_index
    opp = ev[~ev.is_team]; osh = opp[opp.type_id.isin(SHOT_TYPES)]
    psv_xga = float(osh[osh.match_index.isin(psv_idx)].xg.sum())
    return {
        "poss_min": min(poss), "poss_max": max(poss),
        "xg_min": min(xg), "xg_max": max(xg),
        "xga_min": min(xga), "xga_max": max(xga),
        "overperf": round(goals - xgsum, 1),
        "goals": goals, "xg": round(xgsum, 1),
        "psv_xga": round(psv_xga, 1),
        "xga_total": round(float(osh.xg.sum()), 1),
        "psv_share_pct": round(100 * psv_xga / max(float(osh.xg.sum()), 1)),
    }


def duels(ev):
    team = ev[ev.is_team]
    out = []
    for nm in ["Idrissi", "Dilrosun", "Szymanski", "Pedersen", "Timber"]:
        sub = team[team.player.str.contains(nm, na=False)]
        to = sub[sub.type_id == TYPE_TAKE_ON]
        att = len(to); win = int((to.outcome == 1).sum())
        out.append({"name": nm, "avg_y": round(float(sub.y.mean()), 1),
                    "flank": flank(sub.y.mean()),
                    "take_on_att": att, "take_on_won": win,
                    "take_on_pct": round(100 * win / att) if att else 0})
    return out


def main():
    ev, matches, players = load_team(TEAM)
    metrics = json.load(open(os.path.join(OUT, "metrics.json"), encoding="utf-8"))
    team = ev[ev.is_team]
    more = {
        "convention": validate_convention(team),
        "formation_split": formation_split(ev, matches),
        "transition": turnover_to_shot(ev, matches),
        "setpiece_delivery": setpiece_delivery(ev),
        "game_state_15": game_state_15(ev, matches),
        "buildup": buildup_triggers(ev),
        "ranges": ranges_and_overperf(ev, matches, metrics),
        "duels": duels(ev),
    }
    with open(os.path.join(OUT, "metrics_more.json"), "w", encoding="utf-8") as f:
        json.dump(more, f, indent=2, ensure_ascii=False)

    print("convention:", {k: (v["side"], v["expected"]) for k, v in more["convention"].items()})
    print("\nformation split:")
    for k, v in more["formation_split"].items():
        print(f"  {k}: {v}")
    print("\ntransition:", {k: more["transition"][k] for k in
                            ["opp_shots", "transition_shots", "transition_pct",
                             "loss_third", "avg_loss_x", "transition_xga"]})
    print("\nset-piece delivery:", more["setpiece_delivery"])
    print("\ngame_state_15:")
    for r in more["game_state_15"]:
        print("  ", r)
    print("\nbuildup:", more["buildup"])
    print("\nranges/overperf:", more["ranges"])
    print("\nduels:")
    for d in more["duels"]:
        print("  ", d)


if __name__ == "__main__":
    main()
