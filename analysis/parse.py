"""
Opta F24 / F7 parser for the Feyenoord opposition analysis.

Loads every match involving a target team into tidy pandas DataFrames:
  - events_df : one row per on-ball event, key qualifiers expanded, geometry xG on shots
  - players_df: id -> name / position / minutes (per match)
  - matches_df: one row per match (teams, score, venue side for the target)

Opta conventions used here
--------------------------
Pitch coordinates are 0-100 in both axes; attacking direction is always
towards x=100 for the team in possession. Goal mouth centred at y=50.
"""
import os
import glob
import math
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

DATA_ROOT = os.path.join(os.path.dirname(__file__), "..", "Data", "2022-2023")

# --- Opta event type ids we care about -------------------------------------
TYPE_PASS = 1
TYPE_OFFSIDE_PASS = 2
TYPE_TAKE_ON = 3
TYPE_FOUL = 4
TYPE_CORNER_AWARDED = 6
TYPE_TACKLE = 7
TYPE_INTERCEPTION = 8
TYPE_TURNOVER = 9
TYPE_CLEARANCE = 12
TYPE_MISS = 13
TYPE_POST = 14
TYPE_ATTEMPT_SAVED = 15
TYPE_GOAL = 16
TYPE_BALL_RECOVERY = 49
TYPE_DISPOSSESSED = 50
TYPE_AERIAL = 44
TYPE_CHALLENGE = 45
TYPE_BLOCKED_PASS = 74

SHOT_TYPES = {TYPE_MISS, TYPE_POST, TYPE_ATTEMPT_SAVED, TYPE_GOAL}
DEF_ACTION_TYPES = {TYPE_TACKLE, TYPE_INTERCEPTION, TYPE_BALL_RECOVERY,
                    TYPE_CLEARANCE, TYPE_CHALLENGE, TYPE_FOUL}

# --- Qualifier ids ---------------------------------------------------------
Q_LONG_BALL = "1"
Q_CROSS = "2"
Q_FREE_KICK_TAKEN = "5"
Q_CORNER_TAKEN = "6"
Q_THROW_IN = "107"
Q_PASS_END_X = "140"
Q_PASS_END_Y = "141"
Q_ZONE = "56"
Q_HEAD = "15"
Q_BIG_CHANCE = "214"
Q_FROM_CORNER = "25"
Q_SET_PIECE = "24"
Q_FAST_BREAK = "23"
Q_ASSIST = "210"
Q_KEY_PASS = "29"
Q_PENALTY = "9"


def _quals(ev):
    """Return {qualifier_id: value} for an event element."""
    out = {}
    for q in ev.findall("Q"):
        out[q.get("qualifier_id")] = q.get("value")
    return out


# ---------------------------------------------------------------------------
# Geometry-based expected goals (transparent, distance + angle logistic).
# Calibrated to give ~0.76 for a penalty and sensible open-play gradients.
# ---------------------------------------------------------------------------
PITCH_X, PITCH_Y = 105.0, 68.0
GOAL_HALF = 7.32 / 2.0


def geometry_xg(x, y, is_header=False, is_penalty=False, from_set_piece=False):
    if is_penalty:
        return 0.76
    # to metres, goal at (105, 34)
    mx = x / 100.0 * PITCH_X
    my = y / 100.0 * PITCH_Y
    dx = PITCH_X - mx
    dy = my - PITCH_Y / 2.0
    dist = math.hypot(dx, dy)
    # visible goal angle (radians)
    a = math.atan2(GOAL_HALF * 2 * abs(dx) + 1e-9,
                   (dx ** 2 + dy ** 2 - GOAL_HALF ** 2) + 1e-9)
    angle = abs(a)
    # logistic distance+angle model, calibrated so the sample's mean shot
    # value ~ 0.11 (league-typical) with sensible reference points:
    #   6m central ~0.51, penalty spot ~0.20, box edge ~0.08, 25m ~0.02
    z = -0.44 + 1.3 * angle - 0.16 * dist
    if is_header:
        z -= 0.50
    if from_set_piece:
        z -= 0.20
    xg = 1.0 / (1.0 + math.exp(-z))
    return float(np.clip(xg, 0.01, 0.95))


# ---------------------------------------------------------------------------
# F7: player + formation metadata
# ---------------------------------------------------------------------------
def parse_f7(path):
    root = ET.parse(path).getroot()
    players = {}            # pid -> {name, first, last}
    for team in root.findall(".//Team"):
        for pl in team.findall("Player"):
            pid = pl.get("uID", "").lstrip("p")
            nm = pl.find("PersonName")
            first = (nm.findtext("First", "") if nm is not None else "").strip()
            last = (nm.findtext("Last", "") if nm is not None else "").strip()
            players[pid] = {"first": first, "last": last,
                            "name": (first + " " + last).strip()}

    lineups = {}            # team_id -> {formation, players:[{pid,pos,shirt,status,place}]}
    for td in root.findall(".//TeamData"):
        tref = td.get("TeamRef", "").lstrip("t")
        rows = []
        mpl = td.find("PlayerLineUp")
        if mpl is not None:
            for mp in mpl.findall("MatchPlayer"):
                rows.append({
                    "pid": mp.get("PlayerRef", "").lstrip("p"),
                    "pos": mp.get("Position", ""),
                    "shirt": mp.get("ShirtNumber", ""),
                    "status": mp.get("Status", ""),
                    "place": mp.get("Formation_Place", ""),
                })
        lineups[tref] = {"formation": td.get("Formation", ""),
                         "side": td.get("Side", ""), "players": rows}
    return players, lineups


# ---------------------------------------------------------------------------
# Locate matches involving a team and pair F24 with F7
# ---------------------------------------------------------------------------
def _game_header(f24_path):
    for _, elem in ET.iterparse(f24_path, events=("start",)):
        if elem.tag == "Game":
            return dict(elem.attrib)
    return {}


def find_team_matches(team_name="Feyenoord"):
    f24s = glob.glob(os.path.join(DATA_ROOT, "**", "*f24*.xml"), recursive=True)
    out = []
    for f24 in f24s:
        hdr = _game_header(f24)
        if not hdr:
            continue
        ht, at = hdr.get("home_team_name", ""), hdr.get("away_team_name", "")
        if team_name not in (ht, at):
            continue
        folder = os.path.dirname(f24)
        f7s = glob.glob(os.path.join(folder, "*f7*.xml"))
        out.append({"f24": f24, "f7": f7s[0] if f7s else None, "hdr": hdr})
    out.sort(key=lambda r: r["hdr"].get("game_date", ""))
    return out


# ---------------------------------------------------------------------------
# Build the master events DataFrame
# ---------------------------------------------------------------------------
def load_team(team_name="Feyenoord"):
    matches = find_team_matches(team_name)
    all_players = {}
    ev_rows = []
    match_rows = []

    for mi, m in enumerate(matches):
        hdr = m["hdr"]
        game_id = hdr.get("id")
        ht_id, at_id = hdr.get("home_team_id"), hdr.get("away_team_id")
        ht, at = hdr.get("home_team_name"), hdr.get("away_team_name")
        hs, as_ = int(hdr.get("home_score", 0)), int(hdr.get("away_score", 0))
        team_is_home = (ht == team_name)
        team_id = ht_id if team_is_home else at_id
        opp_id = at_id if team_is_home else ht_id
        opp_name = at if team_is_home else ht

        formation = ""
        if m["f7"]:
            players, lineups = parse_f7(m["f7"])
            all_players.update(players)
            if team_id in lineups:
                formation = lineups[team_id]["formation"]

        match_rows.append({
            "match_index": mi, "game_id": game_id, "date": hdr.get("game_date", "")[:10],
            "home": ht, "away": at, "home_score": hs, "away_score": as_,
            "team_is_home": team_is_home, "team_id": team_id, "opp_id": opp_id,
            "opp_name": opp_name, "team_formation": formation,
            "team_gf": hs if team_is_home else as_,
            "team_ga": as_ if team_is_home else hs,
            "venue": "H" if team_is_home else "A",
        })

        root = ET.parse(m["f24"]).getroot()
        for ev in root.iter("Event"):
            tid = int(ev.get("type_id"))
            q = _quals(ev)
            x = float(ev.get("x", 0) or 0)
            y = float(ev.get("y", 0) or 0)
            ev_team = ev.get("team_id")
            row = {
                "match_index": mi, "game_id": game_id,
                "team_id": ev_team,
                "is_team": ev_team == team_id,       # event by the analysed team
                "opp_id": opp_id, "opp_name": opp_name,
                "type_id": tid,
                "period": int(ev.get("period_id", 0) or 0),
                "min": int(ev.get("min", 0) or 0),
                "sec": int(ev.get("sec", 0) or 0),
                "player_id": ev.get("player_id", ""),
                "x": x, "y": y,
                "outcome": int(ev.get("outcome", 0) or 0),
                "end_x": float(q[Q_PASS_END_X]) if Q_PASS_END_X in q else np.nan,
                "end_y": float(q[Q_PASS_END_Y]) if Q_PASS_END_Y in q else np.nan,
                "is_cross": Q_CROSS in q,
                "is_long": Q_LONG_BALL in q,
                "is_corner": Q_CORNER_TAKEN in q,
                "is_freekick": Q_FREE_KICK_TAKEN in q,
                "is_throwin": Q_THROW_IN in q,
                "is_head": Q_HEAD in q,
                "is_bigchance": Q_BIG_CHANCE in q,
                "from_corner": Q_FROM_CORNER in q,
                "from_setpiece": Q_SET_PIECE in q,
                "fast_break": Q_FAST_BREAK in q,
                "is_assist": Q_ASSIST in q,
                "is_keypass": Q_KEY_PASS in q,
            }
            if tid in SHOT_TYPES:
                is_pen = Q_PENALTY in q
                row["is_goal"] = (tid == TYPE_GOAL)
                row["xg"] = geometry_xg(x, y, is_header=row["is_head"],
                                        is_penalty=is_pen,
                                        from_set_piece=row["from_setpiece"] or row["from_corner"])
            ev_rows.append(row)

    events = pd.DataFrame(ev_rows)
    # normalise shot-only columns so boolean indexing is safe across all rows
    if "is_goal" not in events:
        events["is_goal"] = False
    events["is_goal"] = events["is_goal"].fillna(False).astype(bool)
    if "xg" not in events:
        events["xg"] = 0.0
    events["xg"] = pd.to_numeric(events["xg"], errors="coerce").fillna(0.0)
    matches_df = pd.DataFrame(match_rows)
    players_df = pd.DataFrame([
        {"player_id": pid, **info} for pid, info in all_players.items()
    ])
    # attach player names
    name_map = players_df.set_index("player_id")["name"].to_dict() if not players_df.empty else {}
    events["player"] = events["player_id"].map(name_map).fillna("")
    return events, matches_df, players_df


if __name__ == "__main__":
    ev, m, p = load_team("Feyenoord")
    print("events:", len(ev), "matches:", len(m), "players:", len(p))
    print(m[["date", "home", "home_score", "away_score", "away", "team_formation"]].to_string())
    shots = ev[(ev.type_id.isin(SHOT_TYPES)) & (ev.is_team)]
    print("\nFeyenoord shots:", len(shots), "goals:", int(shots.is_goal.sum()),
          "xG:", round(shots.xg.sum(), 1))
    opp_shots = ev[(ev.type_id.isin(SHOT_TYPES)) & (~ev.is_team)]
    print("Opp shots:", len(opp_shots), "goals:", int(opp_shots.is_goal.sum()),
          "xG against:", round(opp_shots.xg.sum(), 1))
