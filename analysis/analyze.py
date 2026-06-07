"""
Compute the full tactical metric set for the Feyenoord opposition analysis
and persist it to output/metrics.json. Also prints a readable digest.
"""
import os
import json
import numpy as np
import pandas as pd

from parse import (load_team, find_team_matches, parse_f7, SHOT_TYPES, DEF_ACTION_TYPES,
                   TYPE_PASS, TYPE_BALL_RECOVERY, TYPE_TACKLE, TYPE_INTERCEPTION,
                   TYPE_FOUL, TYPE_CHALLENGE, TYPE_GOAL, TYPE_TAKE_ON,
                   PITCH_X, PITCH_Y)
from collections import Counter, defaultdict


def most_used_xi(team_name):
    """Aggregate F7 starting line-ups: starts, positions, shirt per player."""
    starts = Counter()
    pos = {}
    shirt = {}
    name = {}
    for m in find_team_matches(team_name):
        if not m["f7"]:
            continue
        players, lineups = parse_f7(m["f7"])
        # which team id is ours
        hdr = m["hdr"]
        tid = hdr.get("home_team_id") if hdr.get("home_team_name") == team_name else hdr.get("away_team_id")
        lu = lineups.get(tid)
        if not lu:
            continue
        for p in lu["players"]:
            if p["status"] == "Start":
                pid = p["pid"]
                starts[pid] += 1
                pos[pid] = p["pos"]
                shirt[pid] = p["shirt"]
                name[pid] = players.get(pid, {}).get("name", pid)
    rows = [{"player": name[pid], "pid": pid, "pos": pos[pid],
             "shirt": shirt[pid], "starts": c} for pid, c in starts.most_common()]
    return rows

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
TEAM = "Feyenoord"


def zone_y(y):
    # Opta: attacking to x=100. Treat y<33.3 as one flank, >66.7 the other.
    if y < 33.33:
        return "right"
    if y > 66.67:
        return "left"
    return "central"


def third(x):
    if x < 33.33:
        return "def"
    if x < 66.67:
        return "mid"
    return "att"


def main():
    ev, matches, players = load_team(TEAM)
    M = len(matches)
    team = ev[ev.is_team].copy()
    opp = ev[~ev.is_team].copy()

    metrics = {"team": TEAM, "n_matches": M}

    # ----- results / form -------------------------------------------------
    res = []
    for _, r in matches.iterrows():
        gf, ga = r.team_gf, r.team_ga
        outcome = "W" if gf > ga else ("D" if gf == ga else "L")
        res.append({"date": r.date, "venue": r.venue, "opp": r.opp_name,
                    "gf": int(gf), "ga": int(ga), "res": outcome,
                    "formation": r.team_formation})
    metrics["matches"] = res
    metrics["record"] = {
        "W": sum(x["res"] == "W" for x in res),
        "D": sum(x["res"] == "D" for x in res),
        "L": sum(x["res"] == "L" for x in res),
        "gf": int(matches.team_gf.sum()), "ga": int(matches.team_ga.sum()),
    }
    metrics["formations"] = matches.team_formation.value_counts().to_dict()

    # ----- possession proxy (pass share) ---------------------------------
    tp = team[team.type_id == TYPE_PASS]
    op = opp[opp.type_id == TYPE_PASS]
    metrics["possession_pass_share"] = round(
        100 * len(tp) / (len(tp) + len(op)), 1)
    # per match
    pm = []
    for mi in range(M):
        a = len(tp[tp.match_index == mi]); b = len(op[op.match_index == mi])
        pm.append(round(100 * a / max(a + b, 1), 1))
    metrics["possession_per_match"] = pm

    # ----- shots / xG -----------------------------------------------------
    tsh = team[team.type_id.isin(SHOT_TYPES)].copy()
    osh = opp[opp.type_id.isin(SHOT_TYPES)].copy()
    metrics["attack"] = {
        "shots": len(tsh), "shots_pg": round(len(tsh) / M, 1),
        "goals": int(tsh.is_goal.sum()),
        "xg": round(tsh.xg.sum(), 1), "xg_pg": round(tsh.xg.sum() / M, 2),
        "xg_per_shot": round(tsh.xg.mean(), 3),
        "box_share": round(100 * (tsh.x >= 83).mean(), 1),
        "headed_goals": int(tsh[(tsh.is_goal) & (tsh.is_head)].shape[0]),
        "setpiece_shots": int(tsh[(tsh.from_corner) | (tsh.from_setpiece)].shape[0]),
        "setpiece_goals": int(tsh[(tsh.is_goal) & ((tsh.from_corner) | (tsh.from_setpiece))].shape[0]),
        "setpiece_xg": round(tsh[(tsh.from_corner) | (tsh.from_setpiece)].xg.sum(), 1),
        "fastbreak_shots": int(tsh[tsh.fast_break].shape[0]),
        "bigchances": int(tsh.is_bigchance.sum()),
    }
    metrics["defense"] = {
        "shots_conceded": len(osh), "shots_conceded_pg": round(len(osh) / M, 1),
        "goals_conceded": int(osh.is_goal.sum()),
        "xga": round(osh.xg.sum(), 1), "xga_pg": round(osh.xg.sum() / M, 2),
        "xga_per_shot": round(osh.xg.mean(), 3),
        "box_share_conceded": round(100 * (osh.x >= 83).mean(), 1),
        "setpiece_shots_conceded": int(osh[(osh.from_corner) | (osh.from_setpiece)].shape[0]),
        "setpiece_goals_conceded": int(osh[(osh.is_goal) & ((osh.from_corner) | (osh.from_setpiece))].shape[0]),
        "fastbreak_shots_conceded": int(osh[osh.fast_break].shape[0]),
    }

    # per-match xg / xga
    metrics["xg_per_match"] = [round(tsh[tsh.match_index == mi].xg.sum(), 2) for mi in range(M)]
    metrics["xga_per_match"] = [round(osh[osh.match_index == mi].xg.sum(), 2) for mi in range(M)]

    # ----- flank / progression -------------------------------------------
    fp = tp[(tp.outcome == 1) & (tp.end_x >= 66.67)]  # passes ending in final third
    flank = fp.assign(z=fp.end_y.map(zone_y)).z.value_counts(normalize=True).mul(100).round(1).to_dict()
    metrics["final_third_entry_flank"] = flank
    # crosses
    cr = tp[tp.is_cross]
    metrics["crosses"] = {
        "total": len(cr), "per_game": round(len(cr) / M, 1),
        "completed_pct": round(100 * (cr.outcome == 1).mean(), 1) if len(cr) else 0,
        "by_flank": cr.assign(z=cr.y.map(zone_y)).z.value_counts(normalize=True).mul(100).round(1).to_dict(),
    }
    # progressive passes (>=15 units upfield, ending att third)
    prog = tp[(tp.outcome == 1) & (tp.end_x - tp.x >= 15) & (tp.end_x >= 66.67)]
    metrics["progressive_passes_pg"] = round(len(prog) / M, 1)
    # long ball share
    metrics["long_ball_share"] = round(100 * tp.is_long.mean(), 1)

    # ----- pressing / defensive shape ------------------------------------
    rec = team[team.type_id == TYPE_BALL_RECOVERY]
    defact = team[team.type_id.isin(DEF_ACTION_TYPES)]
    metrics["press"] = {
        "recovery_avg_x": round(rec.x.mean(), 1),
        "def_actions_att_third_pct": round(100 * (defact.x >= 66.67).mean(), 1),
        "def_actions_def_third_pct": round(100 * (defact.x < 33.33).mean(), 1),
        "high_turnovers_pg": round(len(rec[rec.x >= 66.67]) / M, 1),
    }
    # PPDA: opp passes in their own 60% / Feyenoord def actions in att 60%
    opp_passes_own = op[op.x <= 60]
    fey_def_att = team[(team.type_id.isin({TYPE_TACKLE, TYPE_INTERCEPTION, TYPE_FOUL, TYPE_CHALLENGE}))
                       & (team.x >= 40)]
    metrics["press"]["ppda"] = round(len(opp_passes_own) / max(len(fey_def_att), 1), 1)

    # ----- key players ----------------------------------------------------
    # minutes from lineups not parsed per-min; use event involvement as proxy + goals/assists
    pl_goals = team[team.is_goal == True].player.value_counts() if "is_goal" in team else pd.Series(dtype=int)
    pl_goals = team[(team.type_id == TYPE_GOAL)].player.value_counts()
    pl_chances = tp[tp.is_assist].player.value_counts()   # q210 = pass leading to a shot
    pl_shots = tsh.player.value_counts()
    pl_xg = tsh.groupby("player").xg.sum().sort_values(ascending=False)
    pl_takeons = team[(team.type_id == TYPE_TAKE_ON) & (team.outcome == 1)].player.value_counts()
    pl_prog = prog.player.value_counts()
    pl_passes = tp.player.value_counts()

    def top(series, n=6):
        return [{"player": k, "value": round(float(v), 2)} for k, v in series.head(n).items() if k]

    metrics["players"] = {
        "scorers": top(pl_goals), "chances_created": top(pl_chances),
        "shots": top(pl_shots), "xg": top(pl_xg), "take_ons": top(pl_takeons),
        "progressive": top(pl_prog), "passers": top(pl_passes, 8),
    }
    # involvement leaders (touches) for most-used XI proxy
    touches = team[team.player != ""].player.value_counts()
    metrics["touch_leaders"] = top(touches, 14)
    metrics["most_used_xi"] = most_used_xi(TEAM)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    # ---- digest ----
    print(json.dumps({k: metrics[k] for k in
                      ["record", "formations", "possession_pass_share", "attack",
                       "defense", "final_third_entry_flank", "crosses",
                       "progressive_passes_pg", "long_ball_share", "press"]},
                     indent=2, ensure_ascii=False))
    print("\n-- xg/xga per match --")
    for r, xg, xga in zip(res, metrics["xg_per_match"], metrics["xga_per_match"]):
        print(f"  {r['date']} {r['venue']} vs {r['opp']:<16} {r['gf']}-{r['ga']} "
              f"({r['res']})  xG {xg:>4}  xGA {xga:>4}  [{r['formation']}]")
    print("\n-- most used XI --")
    for r in metrics["most_used_xi"][:14]:
        print(f"   #{r['shirt']:>2} {r['player']:<26} {r['pos']:<14} starts={r['starts']}")


if __name__ == "__main__":
    main()
