"""All narrative copy for the dossier — sharpened, every line carries a number."""

AUTHOR = "Mats van Eijk"
DATA_WINDOW = "Eredivisie 2022/23 · matchdays 1–10 · 10 matches (7 Aug – 16 Oct 2022)"
SOURCE = "Source: Opta F24 event data + F7 line-ups · every metric computed from raw event feeds"

# Executive summary -----------------------------------------------------------
EXEC_HEADLINE = ("A controlled, left-loading possession side that overwhelms you with volume and "
                 "finishes ruthlessly — but is rarely a counter-attacker itself, and concedes its "
                 "clearest chances when its build-up is pressed and turned over.")

EXEC_PROFILE = [
    ("Record (this window)", "7 W – 2 D – 1 L · 26 scored, 11 conceded"),
    ("Style", "Possession-dominant (58% of passes, range 45–68%); a mid-block, not a press"),
    ("Shape", "5× 4-2-3-1, 5× 4-3-3 — the 4-3-3 is sharper & more left-loaded"),
    ("Attack", "18.7 shots & 1.83 xG/game; out-finishes xG by +7.7 (26 goals vs 18.3)"),
    ("Build-up", "Plays through you (10% long balls), Kökçü the hub, loads the LEFT half-space"),
    ("Where they crack", "29% of shots conceded follow a turnover ≤15s — in their own half"),
]

EXEC_FIVE = [
    ("1 · Make it a transition game — they won't",
     "They keep 58% of the ball but took just ONE fast-break shot in 10 games: a control side, "
     "not a counter side. A passing contest suits them; repeated transitions do not."),
    ("2 · Press their build-up — that's where they crack",
     "29% of the shots they concede (3.9 xGA) come within 15s of a Feyenoord turnover, and those "
     "losses sit in their own half (avg x=32). Win it high and you get a clear look."),
    ("3 · Their damage comes through the LEFT",
     "41% of final-third entries and 58% of crosses come down their left (Hancko & López build, "
     "Idrissi isolates, Szymański drifts in). Overload your defensive right side."),
    ("4 · Strike early — they own the late game",
     "Their one window where xGA beats xG is 15–30' (2.9 xGA, 4 conceded). After 60' they scored "
     "12 and conceded 1. Land the first blow; don't bank on chasing them late."),
    ("5 · Set pieces are live both ways",
     "5 set-piece goals scored, 3 conceded. Corners come mostly from the left to the far post "
     "(48 of 75) — a moment to defend with numbers and to attack as a real route to goal."),
]

# Possession ------------------------------------------------------------------
POSSESSION = [
    ("They play through you, not over you",
     "Only 10% of passes are long; even the keeper (Bijlow) goes long just 37% of the time. They "
     "build from Trauner and Hancko with Kökçü the hub — 888 touches in this window, receiving "
     "around halfway in the left-centre (avg x=55, y=58) and leading the side for progressive "
     "passes (39). The press trigger: engage him as he drops, and screen the lane back to him."),
    ("A clear, verified left-side bias",
     "Their loading zone is the left half-space: 41% of final-third entries and 58% of crosses "
     "arrive from the left (convention checked against López y=80, Idrissi y=80, Hancko y=71 vs "
     "right-back Pedersen y=36). Hancko steps in, the left-back pushes high, Idrissi isolates 1v1 "
     "and Szymański drifts across. The right is more an overlap-and-cross outlet than a hub."),
    ("Volume crossing, modest precision",
     "18.9 crosses a game but only 25% find a team-mate. The threat is repetition and second "
     "balls, not delivery — a disciplined, well-populated box largely neutralises it."),
]

ATTACK = [
    ("Manufactured central chances, ruthless finishing",
     "28 big chances in 10 games and 58% of shots inside the box: they work the ball into "
     "high-value central areas. They are also out-finishing xG by +7.7 (26 goals from 18.3) — "
     "partly a regression risk, but the finishers are real, so the defensive message is concede "
     "nothing clear, not 'they'll miss it'."),
    ("A spread threat behind one finisher",
     "Danilo leads the line and the scoring (7 goals, 5.45 xG); Kökçü adds 4 (incl. penalties), "
     "Dilrosun and Szymański 3 each, Timber arriving from deep. Giménez is the like-for-like "
     "off the bench and forcing his way in."),
    ("Set pieces — a real, repeatable threat",
     "One in five of their shots is from a set piece (39 shots, 5 goals, 5.8 xG). 75 corners, "
     "48 from the LEFT, delivered mostly to the FAR post (only 5% short). Trauner and Hancko "
     "attack the ball; Kökçü delivers. Defend the far post with numbers."),
]

PRESS = [
    ("A mid-block, not a gegenpress",
     "Out of possession they are controlled: PPDA 10.8, only 14.5% of defensive actions in the "
     "attacking third, average recovery just inside their own half (x=41), consistent with a "
     "mid-block. They invite you in, stay compact, and re-establish possession rather than "
     "counter — they took a single fast-break shot all window."),
    ("Two shapes, two problems to solve",
     "The 4-3-3 is the sharper, more left-loaded, tighter version (2.07 xG & 1.07 xGA/game, 43% "
     "left, presses less at PPDA 12.2). The 4-2-3-1 is more balanced but leakier (1.34 xGA/game) "
     "and presses higher (PPDA 9.7) — which also means it offers more space in behind to run into."),
]

# Vulnerabilities (rebuilt around the turnover-to-shot evidence) ---------------
VULN = [
    ("Few chances conceded — but high quality",
     "Just 9.7 shots conceded per game, yet 72% are inside the box and their xGA/shot (0.124) "
     "beats the xG/shot they create (0.098). Opponents get few looks, but clear ones."),
    ("The mechanism: pressed build-up → shot",
     "29% of the shots they concede (28 of 97, 3.9 xGA) arrive within 15 seconds of a Feyenoord "
     "ball-loss — and those losses sit in their OWN half (avg x=32). This is not a 'high line' "
     "story; it is a 'press their build-up' story. Force the turnover in their half and the "
     "chance follows."),
    ("Timing & sample honesty",
     "Their soft window is 15–30' (2.9 xGA, 4 conceded) before they take over. One game (PSV, "
     "3.2 xGA) drives ~27% of all their xGA — so the transition weakness is real but partly "
     "concentrated; respect the sample."),
]

VULN_CAVEAT = ("Honesty check: ~27% of their xGA comes from one game (PSV). The transition edge is "
               "real but partly concentrated — treat it as a lever to confirm on tape, not a guarantee.")

# Key player cards — every line carries a number ------------------------------
PLAYER_CARDS = [
    ("Orkun Kökçü", "10 · Deep pivot",
     "The hub: 888 touches, team-high 39 progressive passes, 16 chances created, 4 goals, plus "
     "penalties and corners. Receives around halfway, left-centre. DENY THE TURN — screen the "
     "pass back to him and stop him facing our goal."),
    ("Quinten Timber", "8 · Box-to-box",
     "Best 1v1 in the side (27 take-ons, 56% won) and team-high 17 chances created from deep, "
     "924 minutes. Arrives in the box (26 box touches). Track his forward runs — he turns "
     "control into penetration."),
    ("Dávid Hancko", "33 · Left centre-back",
     "Engine of the left build-up: #2 progressive passer, 1.9 xG from set pieces, 958 minutes. "
     "He steps into midfield — and the channel he vacates is exactly the space to attack in "
     "transition."),
    ("Sebastian Szymański", "17 · Attacking mid",
     "Between the lines, drifts left: 3 goals, 16 chances created, take-ons at 50%. Assign a "
     "midfielder to pick him up in the half-space before he turns."),
    ("Javairô Dilrosun", "11 · Roaming forward",
     "High-volume dribbler — 46 take-ons but only 35% won, roaming central/right (y=43), "
     "team-high 49 box touches, 3 goals. Containable: show him inside, deny the box entry rather "
     "than dive in."),
    ("Danilo", "9 · Striker",
     "Main finisher: 7 goals from 5.45 xG, plays on the last shoulder. Disciplined depth control "
     "from our centre-backs is essential. Giménez is the like-for-like off the bench."),
]

# Per-card key stats (value, label) — keyed by player name
PLAYER_STATS = {
    "Orkun Kökçü": [("39", "prog passes"), ("16", "chances"), ("888", "touches")],
    "Quinten Timber": [("17", "chances"), ("56%", "take-on win"), ("27", "take-ons")],
    "Dávid Hancko": [("31", "prog passes"), ("1.9", "set-piece xG"), ("958", "minutes")],
    "Sebastian Szymański": [("3", "goals"), ("16", "chances"), ("50%", "take-on win")],
    "Javairô Dilrosun": [("46", "take-ons"), ("35%", "won"), ("49", "box touches")],
    "Danilo": [("7", "goals"), ("5.45", "xG"), ("8", "starts")],
}

# Game plan -------------------------------------------------------------------
PLAN_IN = [
    "Win-it-and-go from their HALF: the moment we turn them over in their build-up, attack — 29% "
    "of the shots they concede start exactly here.",
    "Front-load the threat: target the 15–30' window (their only negative-xG period) and don't "
    "plan to chase them after 60', when they are ruthless.",
    "When set, attack the space behind Hancko's steps with a runner from our right.",
    "Treat set pieces as a primary route to goal — they concede from them; rehearse far-post and "
    "second-phase routines.",
]
PLAN_OUT = [
    "Press the build-up with triggers: jump when it goes back to Trauner/Bijlow or square to the "
    "left-back; screen the lane into Kökçü so he can't turn.",
    "Force them to cross from deep down their left, then defend the box with numbers — win first "
    "AND second contact (only 25% of crosses land).",
    "No isolated 1v1s for our right-back vs the left overload; the winger tracks the high left-back.",
    "Control our line in a mid-block; they barely counter (1 fast-break shot), so the risk is "
    "sustained pressure, not balls in behind — stay compact and patient.",
]
PLAN_SCEN = [
    ("If they line up 4-3-3",
     "Their sharper, more left-loaded shape (2.07 xG, 43% left). Double the left side, and use a "
     "spare man to jump Kökçü; they press less here (PPDA 12.2) so we can build."),
    ("If they line up 4-2-3-1",
     "Leakier (1.34 xGA) and they press higher (PPDA 9.7) — more space in behind. Bait the press "
     "and release runners early into the channels."),
    ("If we lead",
     "Stay in the block, manage set pieces, keep press triggers on their build-up; don't drop so "
     "deep we invite the sustained pressure they thrive on."),
    ("First 30' / after a goal",
     "Their soft window is 15–30'. Start fast and physical, take an early lead — the late game "
     "(60'+: 12 goals, 1 conceded) belongs to them."),
]

# Weekly communication plan ---------------------------------------------------
WEEK_INTRO = ("How I would feed this into the week — the right information, to the right people, in "
              "the right format, at the right time. Players get less, sharper and more visual as the "
              "match nears; never more than three messages a day on the pitch.")

WEEK_DAYS = [
    ("MD-4  ·  Staff alignment",
     "Full dossier to the head coach and assistants. Agree the game-model response: press triggers "
     "on their build-up, block height, set-piece plans, the early-game intent. Lock the 3–4 "
     "headline messages we will drip to players. No player video yet — align the staff story first."),
    ("MD-3  ·  Team — out of possession",
     "Squad meeting (8–10 min). One theme: how they build and where they crack. Clip reel — Kökçü "
     "dropping, the left overload, turnovers that became shots. The ask: 'press the build-up, "
     "screen Kökçü, force them left, win the box.' Back line + keeper unit on the in-behind picture."),
    ("MD-2  ·  Team — in possession & transition",
     "Our route to goal: clips of turnovers in their half and the space behind Hancko's steps; "
     "train transition-to-finish drills mirroring their shape. Wingers/full-backs get a clip pack "
     "on their direct opponent (Idrissi, the high left-back, Pedersen)."),
    ("MD-1  ·  Set pieces & individuals",
     "Set-piece meeting both ways: our far-post marking vs Trauner/Hancko; our attacking routines "
     "vs their box defence. Hand out individual clips (60–90s) to the players who need them — "
     "personal, on their direct duel. Keep it light and confident."),
    ("MD  ·  Reminders only",
     "No new information. A one-page visual in the dressing room: the 3 keys (press their build-up "
     "/ force left & win the box / strike early). 30-second individual reminders. Live: flag from "
     "the bench whether they're in 4-3-3 or 4-2-3-1 and adjust per the plan."),
]

METHOD = ("Every figure and number is computed directly from the raw Opta F24 event feeds and F7 "
          "line-ups for Feyenoord's first ten Eredivisie 2022/23 matches — no third-party "
          "aggregations. The pitch convention is stated and verified: y>66.7 is the attacking "
          "LEFT (cross-checked against known left- and right-sided players). Expected goals (xG) "
          "uses a transparent distance-and-angle geometry model with header and set-piece "
          "adjustments, calibrated so the mean across all shots in the sample matches a "
          "league-typical ~0.11; Feyenoord's own shots average 0.098 — high volume at slightly "
          "below-average quality. Goal totals are quoted as match results (26 for, 11 against); "
          "the shot-event feed attributes 27/10, the small difference being own goals. Transition "
          "chances link each opponent shot to the Feyenoord ball-loss within 15 seconds before it.")

CAVEATS = [
    "Ten matches is a tendency sample, not a verdict — one game (PSV) drives ~27% of the xGA, so "
    "the transition weakness is real but partly concentrated.",
    "Pass-network positions are average on-ball locations (a build-up shape, not a snapshot XI); "
    "edges are inferred from successive same-team events.",
    "With tracking/possession data I'd quantify pressing triggers, line height and off-ball runs; "
    "with the full season I'd separate stable patterns from small-sample noise and lock the XI.",
    "Every figure would ship with linked video — each data point one click from the moment on tape.",
]
