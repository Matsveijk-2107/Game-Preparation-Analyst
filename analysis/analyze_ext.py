"""
Extended metrics for the presentation deck: minutes, per-90 player table
(radars + ranking bars), attack zones by half, transitions, and authentic
clip moments (match + timestamp) drawn from the raw event feed.

Writes output/metrics_ext.json (merged with metrics.json by the deck builder).
"""
import os
import json
from collections import defaultdict

import numpy as np
import pandas as pd

from parse import (load_team, find_team_matches, parse_f7, SHOT_TYPES,
                   TYPE_PASS, TYPE_BALL_RECOVERY, TYPE_TACKLE, TYPE_INTERCEPTION,
                   TYPE_TAKE_ON, TYPE_GOAL, TYPE_AERIAL, TYPE_CLEARANCE)

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
TEAM = "Feyenoord"
TYPE_SUB_OFF, TYPE_SUB_ON = 18, 19


def zone_y(y):
    if y < 33.33:
        return "right"
    if y > 66.67:
        return "left"
    return "central"


def compute_minutes(ev, matches):
    fmatches = find_team_matches(TEAM)
    mins = defaultdict(float)
    apps = defaultdict(int)
    for mi, m in enumerate(fmatches):
        me = ev[ev.match_index == mi]
        if me.empty:
            continue
        match_len = int(me["min"].max()) + 1
        tev = me[me.is_team]
        offs = {r.player_id: r.min for r in tev[tev.type_id == TYPE_SUB_OFF].itertuples()}
        ons = {r.player_id: r.min for r in tev[tev.type_id == TYPE_SUB_ON].itertuples()}
        if not m["f7"]:
            continue
        players, lineups = parse_f7(m["f7"])
        hdr = m["hdr"]
        tid = hdr.get("home_team_id") if hdr.get("home_team_name") == TEAM else hdr.get("away_team_id")
        lu = lineups.get(tid, {}).get("players", [])
        for p in lu:
            pid = p["pid"]
            if p["status"] == "Start":
                end = offs.get(pid, match_len)
                mins[pid] += max(end, 0); apps[pid] += 1
            elif pid in ons:
                start = ons[pid]; end = offs.get(pid, match_len)
                mins[pid] += max(end - start, 0); apps[pid] += 1
    return mins, apps


def player_table(ev, mins):
    team = ev[ev.is_team].copy()
    name = team.groupby("player_id")["player"].first().to_dict()
    sh = team[team.type_id.isin(SHOT_TYPES)]
    tp = team[team.type_id == TYPE_PASS]
    rows = []
    for pid, mn in mins.items():
        if mn < 1 or not name.get(pid):
            continue
        pe = team[team.player_id == pid]
        pp = tp[tp.player_id == pid]
        psh = sh[sh.player_id == pid]
        comp = pp[pp.outcome == 1]
        prog = comp[(comp.end_x - comp.x >= 15) & (comp.end_x >= 66.67)]
        d = {
            "pid": pid, "player": name[pid], "mins": round(mn),
            "shots": len(psh), "goals": int(psh.is_goal.sum()),
            "xg": round(float(psh.xg.sum()), 2),
            "chances": int(pp.is_assist.sum()),
            "take_ons": int(pe[(pe.type_id == TYPE_TAKE_ON) & (pe.outcome == 1)].shape[0]),
            "prog": len(prog),
            "passes": int(comp.shape[0]),
            "pass_pct": round(100 * (pp.outcome == 1).mean(), 1) if len(pp) else 0,
            "box_touches": int(pe[(pe.x >= 83) & (pe.y.between(21, 79))].shape[0]),
            "recoveries": int(pe[pe.type_id == TYPE_BALL_RECOVERY].shape[0]),
            "def_actions": int(pe[pe.type_id.isin({TYPE_TACKLE, TYPE_INTERCEPTION,
                                                   TYPE_CLEARANCE})].shape[0]),
            "crosses": int(pp[pp.is_cross].shape[0]),
        }
        per90 = {k: round(d[k] / mn * 90, 2) for k in
                 ["shots", "xg", "chances", "take_ons", "prog", "passes",
                  "box_touches", "recoveries", "def_actions", "crosses"]}
        d.update({f"{k}_p90": v for k, v in per90.items()})
        rows.append(d)
    return pd.DataFrame(rows).sort_values("mins", ascending=False)


# radar axes (label, column, higher_is_better)
RADAR_AXES = [
    ("Goal threat\n(xG/90)", "xg_p90"),
    ("Shots/90", "shots_p90"),
    ("Chances\ncreated/90", "chances_p90"),
    ("Take-ons/90", "take_ons_p90"),
    ("Progressive\npasses/90", "prog_p90"),
    ("Pass\ncompletion", "pass_pct"),
    ("Box\ntouches/90", "box_touches_p90"),
    ("Defensive\nactions/90", "def_actions_p90"),
]


def radar_percentiles(df, qual_min=270):
    q = df[df.mins >= qual_min].copy()
    pct = q.copy()
    for _, col in RADAR_AXES:
        ranks = q[col].rank(pct=True)
        pct[col + "_pct"] = (ranks * 100).round(0)
    return pct


def key_clips(ev, matches):
    """Goals + big chances for and against, with match + timestamp."""
    mmeta = {r.match_index: r for r in matches.itertuples()}
    clips = []
    for _, e in ev[ev.type_id.isin(SHOT_TYPES)].iterrows():
        if not (e.is_goal or e.is_bigchance):
            continue
        m = mmeta[e.match_index]
        ctx = ("set piece" if (e.from_corner or e.from_setpiece)
               else ("fast break" if e.fast_break else "open play"))
        clips.append({
            "match": f"{'H' if m.team_is_home else 'A'} {m.opp_name}",
            "date": m.date, "t": f"{int(e['min'])}:{int(e['sec']):02d}",
            "min": int(e["min"]), "player": e.player, "for": bool(e.is_team),
            "kind": "GOAL" if e.is_goal else "big chance", "ctx": ctx,
            "xg": round(float(e.xg), 2),
        })
    clips.sort(key=lambda c: (not c["for"], c["date"], c["min"]))
    return clips


def attack_zones_by_half(ev):
    team = ev[ev.is_team]
    out = {}
    for half, pid in [("h1", 1), ("h2", 2)]:
        fp = team[(team.type_id == TYPE_PASS) & (team.outcome == 1) &
                  (team.end_x >= 66.67) & (team.period == pid)]
        z = fp.assign(z=fp.end_y.map(zone_y)).z.value_counts(normalize=True).mul(100).round(0)
        out[half] = {k: float(z.get(k, 0)) for k in ["left", "central", "right"]}
    return out


def transitions(ev):
    team = ev[ev.is_team]; opp = ev[~ev.is_team]
    rec = team[team.type_id == TYPE_BALL_RECOVERY]
    osh = opp[opp.type_id.isin(SHOT_TYPES)]
    return {
        "high_recoveries": int((rec.x >= 66.67).sum()),
        "mid_recoveries": int(((rec.x >= 33.33) & (rec.x < 66.67)).sum()),
        "fast_break_shots_for": int(team[(team.type_id.isin(SHOT_TYPES)) & team.fast_break].shape[0]),
        "fast_break_shots_against": int(osh[osh.fast_break].shape[0]),
        "fast_break_goals_against": int(osh[(osh.fast_break) & (osh.is_goal)].shape[0]),
        "fast_break_xga": round(float(osh[osh.fast_break].xg.sum()), 2),
    }


def main():
    ev, matches, players = load_team(TEAM)
    mins, apps = compute_minutes(ev, matches)
    df = player_table(ev, mins)
    pct = radar_percentiles(df)

    # players to feature (by name)
    feature = ["Orkun Kökçü", "Quinten Timber", "Sebastian Szymanski",
               "Javairô Dilrosun", "Dávid Hancko", "Danilo Pereira da Silva"]
    radars = {}
    for nm in feature:
        row = pct[pct.player == nm]
        if row.empty:
            row = df[df.player == nm]
            if row.empty:
                continue
        r = row.iloc[0]
        radars[nm] = {
            "mins": int(df[df.player == nm].iloc[0]["mins"]) if (df.player == nm).any() else 0,
            "values": [float(r.get(col + "_pct", 50)) for _, col in RADAR_AXES],
            "raw": {col: float(df[df.player == nm].iloc[0][col]) for _, col in RADAR_AXES
                    if (df.player == nm).any()},
        }

    ext = {
        "radar_axes": [a for a, _ in RADAR_AXES],
        "radars": radars,
        "attack_zones_half": attack_zones_by_half(ev),
        "transitions": transitions(ev),
        "key_clips": key_clips(ev, matches),
        "player_table": df.to_dict(orient="records"),
    }
    with open(os.path.join(OUT, "metrics_ext.json"), "w", encoding="utf-8") as f:
        json.dump(ext, f, indent=2, ensure_ascii=False)

    print("minutes leaders:")
    print(df[["player", "mins", "goals", "xg", "chances", "take_ons", "prog"]].head(14).to_string(index=False))
    print("\ntransitions:", ext["transitions"])
    print("\nattack zones by half:", ext["attack_zones_half"])
    print(f"\nkey clips: {len(ext['key_clips'])} (for={sum(c['for'] for c in ext['key_clips'])}, "
          f"against={sum(not c['for'] for c in ext['key_clips'])})")
    print("radars built for:", list(radars.keys()))


if __name__ == "__main__":
    main()
