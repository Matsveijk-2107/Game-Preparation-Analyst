"""Bilingual narrative for the dossier. Set DOSSIER_LANG=nl for Dutch.

All displayed copy lives here (English + Dutch). Short UI labels used inline in
build_report / figures are translated through the UI dict + L()."""
import os

LANG = os.environ.get("DOSSIER_LANG", "en").lower()
NL = LANG == "nl"

AUTHOR = "Mats van Eijk"

# ===========================================================================
# ENGLISH
# ===========================================================================
_EN = dict(
DATA_WINDOW="Eredivisie 2022/23 · matchdays 1 to 10 · 10 matches (7 Aug to 16 Oct 2022)",
SOURCE="Source: Opta F24 event data and F7 line-ups. Every metric computed from the raw feeds.",
EXEC_HEADLINE=("Feyenoord are a controlled, left-loading possession side. They overwhelm you "
    "with volume and finish ruthlessly, but they rarely counter, and the clearest chances they "
    "give up come when their own build-up is pressed and turned over."),
EXEC_PROFILE=[
    ("Record (this window)", "7 W, 2 D, 1 L. 26 scored, 11 conceded."),
    ("Style", "Possession-led (58%), in a mid-block out of possession."),
    ("Shape", "Five games 4-2-3-1, five 4-3-3; the 4-3-3 is sharper."),
    ("Attack", "18.7 shots and 1.83 xG a game, and they out-finish it."),
    ("Build-up", "They play through you (10% long balls) and load the left."),
    ("Where they crack", "Almost a third of shots conceded follow a turnover."),
],
EXEC_FIVE=[
    ("1.  Make it a transition game, because they will not",
     "They keep 58% of the ball, yet they managed a single fast-break shot in ten games. This is a "
     "control side, not a counter side. A patient passing contest is exactly what they want, so "
     "the more we turn the match into repeated transitions, the more uncomfortable they become."),
    ("2.  Press their build-up, that is where they crack",
     "Almost a third of the shots they concede (3.9 xGA) arrive within fifteen seconds of a "
     "Feyenoord turnover, and those turnovers happen in their own half. Win the ball high and a "
     "clear chance usually follows, so we commit to pressing the first phase rather than sitting off."),
    ("3.  Their threat runs down the left",
     "Forty-one per cent of their final-third entries and 58% of their crosses come from the left, "
     "where Hancko and the left-back build and Idrissi isolates one-against-one. We overload our "
     "defensive right and we never leave our right-back on his own."),
    ("4.  Strike early, because they own the late game",
     "The only fifteen-minute window where they are out-chanced is 15 to 30 minutes (2.9 xGA, four "
     "conceded). After the hour they are ruthless: twelve goals scored, one conceded. Landing the "
     "first blow matters more against this side than against most."),
    ("5.  The box is a battleground at both ends",
     "They scored five set-piece goals and conceded three. Their corners come mainly from the left "
     "and are aimed at the near post, and their open-play crossing finds a team-mate only a quarter "
     "of the time, so defending our box and threatening theirs both pay off."),
],
ATTACK=[
    ("They manufacture central chances, and they finish them",
     "This is not a hopeful side. They created 28 big chances in ten games and take 58% of their "
     "shots from inside the box, working the ball into the highest-value areas before they pull the "
     "trigger. They are also finishing well above expectation, 26 goals from 18.3 xG, so the "
     "message for our back line is simple: give them nothing clean, and do not bank on them missing."),
    ("The goals are spread behind one main finisher",
     "Danilo leads the line and the scoring with seven goals from 5.45 xG, but the threat does not "
     "stop with him. Kökçü chips in from midfield and the spot, Dilrosun and Szymański weigh in "
     "from wide and between the lines, and Timber arrives late from deep. Giménez is the "
     "like-for-like off the bench, so the plan cannot revolve around stopping one player."),
    ("Set pieces are a genuine route to goal",
     "Around one in five of their shots comes from a set piece (39 shots, five goals, 5.8 xG). "
     "Their corners come mostly from the left and are aimed at the near post, with Trauner and "
     "Hancko attacking the ball and Kökçü delivering. We defend these with full numbers and "
     "concentration on the near post, and we treat our own set pieces as a real chance to hurt them."),
],
VULN_CAVEAT=("One honest note: roughly a quarter of the xG they conceded comes from a single game "
    "(PSV). The transition weakness is real, but it is partly concentrated, so treat it as a lever "
    "to confirm on video rather than a guarantee."),
PLAYER_CARDS=[
    ("Orkun Kökçü", "10 · Deep pivot",
     "The heartbeat of the side: 888 touches, a team-high 39 progressive passes, 16 chances and "
     "four goals, plus the set pieces. He drops to receive around halfway, just left of centre. "
     "Get tight and stop him turning, and the build-up slows right down."),
    ("Quinten Timber", "8 · Box-to-box",
     "Their best one-against-one player (27 take-ons at 56%) and top creator from deep with 17 "
     "chances, across 924 minutes. He covers ground and arrives in the box. Whoever marks him has "
     "to track his forward runs, not just his starting position."),
    ("Dávid Hancko", "33 · Left centre-back",
     "The engine of the left-sided build-up and their second most progressive passer, with a "
     "set-piece threat too (1.9 xG). He steps into midfield to move the ball, and the space he "
     "leaves behind is exactly where we want to attack in transition."),
    ("Sebastian Szymański", "17 · Attacking mid",
     "Plays between the lines and drifts to the left. Three goals, 16 chances created, take-ons "
     "landing at 50%. A midfielder has to pick him up in the half-space before he turns, because "
     "once he is facing our goal he hurts you."),
    ("Javairô Dilrosun", "11 · Roaming forward",
     "A high-volume dribbler who roams across the front, on average slightly to the right. He "
     "tries plenty (46 take-ons) but lands only 35%, with a team-high 49 box touches. Stay patient, "
     "show him inside and deny the entry rather than diving in."),
    ("Danilo", "9 · Striker",
     "Their main finisher, seven goals from 5.45 xG, living on the last shoulder. Disciplined depth "
     "from our centre-backs is essential. Giménez is the like-for-like off the bench, so the threat "
     "barely changes when he comes on."),
],
PLAYER_STATS={
    "Orkun Kökçü": [("39", "prog passes"), ("16", "chances"), ("888", "touches")],
    "Quinten Timber": [("17", "chances"), ("56%", "take-on win"), ("27", "take-ons")],
    "Dávid Hancko": [("31", "prog passes"), ("1.9", "set-piece xG"), ("614", "minutes")],
    "Sebastian Szymański": [("3", "goals"), ("16", "chances"), ("50%", "take-on win")],
    "Javairô Dilrosun": [("46", "take-ons"), ("35%", "won"), ("49", "box touches")],
    "Danilo": [("7", "goals"), ("5.45", "xG"), ("8", "starts")],
},
PLAN_IN=[
    "Win it and go. Nearly a third of the shots they concede begin with a turnover in their half.",
    "Front-load the game: target the 15 to 30 minute window and do not bank on chasing them late.",
    "Attack the channel Hancko vacates when he steps in, with a runner breaking from our right.",
    "Use our set pieces. They concede from them, so rehearse far-post and second-phase routines.",
],
PLAN_OUT=[
    "Press their first phase. Trigger on the pass back to Trauner or Bijlow and screen the lane "
    "into Kökçü.",
    "Force them to cross from deep on the left, then win the box, both first contact and second ball.",
    "No isolated duels for our right-back against their left; the winger tracks the overlapping back.",
    "Hold a connected mid-block. They barely counter, so the danger is sustained pressure, not "
    "balls in behind.",
],
PLAN_SCEN=[
    ("If they set up in 4-3-3",
     "Their sharper, more left-loaded shape (2.07 xG a game, 43% of entries left). Double up on "
     "that side and use a spare man to jump Kökçü. They press less here (PPDA 12.2), so we can "
     "afford to build."),
    ("If they set up in 4-2-3-1",
     "More balanced but leakier (1.34 xGA) and they press higher (PPDA 9.7), which leaves space "
     "behind. Bait the press and release runners early into the channels."),
    ("If we go in front",
     "Stay in the block, manage the set pieces and keep the press triggers live on their build-up. "
     "Do not drop so deep that we invite the sustained pressure they thrive on."),
    ("First half-hour, or after a goal",
     "Their soft window is 15 to 30 minutes, so start fast and try to take an early lead. The "
     "closing stages belong to them: twelve goals after the hour, only one conceded."),
],
WEEK_INTRO=("Here is how I would feed this into the week: the right information, to the right "
    "people, in the right format, at the right time. The players get less, sharper and more visual "
    "as the match approaches, and never more than three messages a day once we are out on the grass."),
WEEK_DAYS=[
    ("MD-4 · Staff alignment",
     "The full dossier goes to the head coach and assistants, and we agree the game-model response: "
     "the press triggers on their build-up, our block height, the set-piece plans and the early-game "
     "intent. We lock the three or four headline messages we will drip to the players. No player "
     "video yet; we align the staff story first."),
    ("MD-3 · Team, out of possession",
     "An eight to ten minute squad meeting on one theme: how they build and where they crack. A "
     "short clip reel of Kökçü dropping in, the left-sided overload and turnovers that became "
     "shots. The single ask is to press the build-up, screen Kökçü, force them left and win the "
     "box. The back line and keeper get their own unit meeting on the space in behind."),
    ("MD-2 · Team, in possession and transition",
     "Our route to goal: clips of turnovers won in their half and the space behind Hancko's steps, "
     "then we train it with transition-to-finish drills that mirror their shape. Wingers and "
     "full-backs get an individual clip pack on their direct opponent (Idrissi, the high left-back, "
     "Pedersen)."),
    ("MD-1 · Set pieces and individuals",
     "A set-piece meeting both ways: our near-post marking against Trauner and Hancko, and our own "
     "attacking routines against their box defence. Individual clips of 60 to 90 seconds go to the "
     "players who need them, personal and focused on their direct duel. Keep it light and confident."),
    ("MD · Reminders only",
     "No new information today. A one-page visual in the dressing room with the three keys: press "
     "their build-up, force them left and win the box, and strike early. Thirty-second individual "
     "reminders. Live from the bench we flag whether they are in 4-3-3 or 4-2-3-1 and adjust."),
],
METHOD=("Every figure and number in this dossier is computed directly from the raw Opta F24 event "
    "feeds and F7 line-ups for Feyenoord's first ten Eredivisie 2022/23 matches, with no "
    "third-party aggregations. The pitch convention is stated and checked: a y value above 66.7 is "
    "the attacking left, verified against known left and right-sided players. Expected goals uses a "
    "transparent distance-and-angle model with adjustments for headers and set pieces, calibrated "
    "so the average shot in the sample is worth roughly the league-typical 0.11. Feyenoord's own "
    "shots average 0.098. Goal totals are quoted as match results (26 for, 11 against); the "
    "shot-event feed attributes 27 and 10, the small difference being own goals."),
CAVEATS=[
    "Ten matches is a sample of tendencies, not a verdict. One game (PSV) drives about a quarter of "
    "the xG conceded, so the transition weakness is real but partly concentrated.",
    "The pass-network positions are average on-ball locations, so they show a build-up shape rather "
    "than a snapshot XI, and the links are inferred from successive events on the ball.",
    "With tracking and possession data I would quantify the pressing triggers, the line height and "
    "the off-ball runs, and a full season would separate stable patterns from small-sample noise.",
    "In a club setting every figure would ship with linked video, so each data point is one click "
    "away from the moment on tape.",
],
# --- texts moved out of build_report so they translate too -----------------
FORM_BLOCKS=[
    ("Dominant, and rarely troubled",
     "Seven wins from ten and 26 goals tell the story, and the underlying numbers back it up: "
     "their xG sits above their xG-against in eight of the ten games. They control matches and "
     "out-create opponents, so a patient passing contest plays straight into their hands."),
    ("The exceptions are the lesson",
     "The two blue spikes are where it went wrong for them. The 3-4 defeat at PSV (3.2 xGA) and "
     "the 4-3 win at Go Ahead Eagles (2.5 xGA) were both open, end-to-end games full of "
     "transitions. That is the kind of match we want to recreate."),
    ("Strike early, fear the late game",
     "The only fifteen-minute window where they are out-chanced is 15 to 30 minutes (2.9 xGA, "
     "four conceded). After the hour they took over completely, scoring twelve and conceding "
     "one. The first goal matters more here than it does against most sides."),
],
POSS_BULLETS=[
    "They play through you, not over the top. Only one pass in ten is long, and Kökçü (888 "
    "touches, 39 progressive passes) drops in to set the tempo around halfway. Screen the lane "
    "back into his feet and the build-up tends to stall.",
    "The bias is clearly to the left: 41% of their final-third entries and 58% of their crosses "
    "come down that side, with Hancko and the left-back building, Idrissi isolating and "
    "Szymański drifting across.",
    "The crossing is high in volume but modest in quality, 18.9 a game at 25% completion. A "
    "well-populated box and a focus on the second ball takes most of the sting out of it.",
    "On the right, Pedersen pushes high as an overlap-and-cross outlet rather than a creator, "
    "so our left side has to be alert to the runner underneath him.",
],
PRESS_BULLETS=[
    "In the 4-3-3 they are sharper and more left-loaded (2.07 xG, 43% of entries left, 1.07 "
    "xGA) and they press less (PPDA 12.2). Against this shape we build patiently and double up "
    "on their left.",
    "In the 4-2-3-1 they are more balanced but leakier (1.34 xGA) and they press a touch higher "
    "(PPDA 9.7), which leaves more room behind. Here we bait the press and release runners "
    "early into that space.",
    "Either way they sit in a mid-block and recover around halfway rather than hunting high up "
    "the pitch, so we will get time on the ball in our own half. What we do with that time is "
    "the whole game.",
],
SETPIECE_BULLETS=[
    "Defending theirs: their corners come mostly from the left and are aimed at the near post (42 "
    "of 70 box deliveries; only 5% are short). We attack the near post and the first contact, put "
    "bodies on Trauner and Hancko, and win the central second ball.",
    "Attacking theirs: they conceded three set-piece goals in ten games and their open-play "
    "crossing finds a team-mate only a quarter of the time, so we overload their box, target "
    "the far post and work the second phase.",
    "Recycling: their full-backs commit forward to attacking corners, which means a cleared set "
    "piece becomes our transition trigger. The first outlet has to break immediately into the "
    "space they leave behind.",
],
VULN_ACTS=[
    ("Press their build-up, do not sit off",
     "Close to a third of the shots they concede (3.9 xGA) come within fifteen seconds of a "
     "turnover, and those turnovers happen in their own half (average x of 32). Trigger the "
     "press on the pass back to Trauner or Bijlow and screen Kökçü so he cannot turn. This is "
     "our single clearest route to a chance against them."),
    ("Make it transitional, and strike early",
     "Their only sub-par window is 15 to 30 minutes (2.9 xGA), and after the hour they are "
     "ruthless: twelve goals scored, one conceded. Take an early lead and keep the game open, "
     "because they barely counter themselves (one fast-break shot in the whole window)."),
    ("Win the box on set pieces",
     "They conceded three set-piece goals in ten games and their crossing only lands a quarter "
     "of the time. We defend our box with full numbers, then go after theirs: load the far "
     "post and play for the second ball."),
],
XI_SHAPE=("They split the window evenly between a 4-2-3-1 and a 4-3-3, but the 4-3-3 shown here is "
    "their sharper, more left-loaded version and the one to prepare for first.\n\nBijlow builds "
    "with Trauner and Hancko, Kökçü drops in as the single pivot, and Timber and Szymański play "
    "ahead of him with licence to drift and arrive in the box.\n\nThe width and the danger come "
    "from the left. Pedersen on the right is more of an overlapping outlet, and Danilo leads the "
    "line on the last shoulder."),
XI_ROTATION=("The spine is settled, so the eleven above is a confident base rather than a guess: "
    "Bijlow, Trauner, Timber and Dilrosun started all ten matches, with Kökçü, Hancko, Pedersen "
    "and Danilo close behind."),
XI_BENCH=[
    "Geertruida and Rasmussen are the main defensive alternatives and can both step into midfield.",
    "López and Hartman cover at left-back, the source of most of their attacking width.",
    "Giménez is the like-for-like striker off the bench and is pushing Danilo hard for the shirt.",
],
WHY_TEXT=("Opposition analysis is only useful if it changes behaviour on the pitch. My priority was "
    "to move from a large, raw event dataset to a small number of clear, evidence-backed messages a "
    "coach can install and a player can remember: structure, patterns, vulnerabilities, key "
    "players and scenarios, each tied to a concrete action and a way to communicate it through the "
    "week. That translation, done consistently, accurately and on time, is the job."),
)

# ===========================================================================
# NEDERLANDS
# ===========================================================================
_NL = dict(
DATA_WINDOW="Eredivisie 2022/23 · speeldagen 1 tot 10 · 10 wedstrijden (7 aug tot 16 okt 2022)",
SOURCE="Bron: Opta F24 event-data en F7 opstellingen. Elke metric berekend uit de ruwe feeds.",
EXEC_HEADLINE=("Feyenoord is een gecontroleerde, links-belaste balbezitploeg. Ze overweldigen je "
    "met volume en zijn ijzersterk in de afronding, maar ze counteren zelf zelden, en de grootste "
    "kansen geven ze weg wanneer hun eigen opbouw onder druk wordt gezet en veroverd."),
EXEC_PROFILE=[
    ("Resultaten (deze periode)", "7 W, 2 G, 1 V. 26 gemaakt, 11 tegen."),
    ("Stijl", "Balbezit-gericht (58%), in een middenblok, geen hoge druk."),
    ("Opstelling", "Vijf keer 4-2-3-1, vijf keer 4-3-3; de 4-3-3 is scherper."),
    ("Aanval", "18.7 schoten en 1.83 xG per duel, en ze maken er meer van."),
    ("Opbouw", "Ze spelen door je heen (10% lange ballen) en belasten links."),
    ("Waar ze kraken", "Bijna een derde van de tegenschoten volgt op balverlies."),
],
EXEC_FIVE=[
    ("1.  Maak er een omschakelingsduel van, want zij doen dat niet",
     "Ze houden 58% van de bal, maar kwamen in tien duels tot één counterschot. Dit is een "
     "controleploeg, geen counterploeg. Een geduldige positiestrijd is precies wat zij willen, dus "
     "hoe meer we de wedstrijd vol omschakelingen krijgen, hoe ongemakkelijker zij worden."),
    ("2.  Zet druk op hun opbouw, daar kraken ze",
     "Bijna een derde van de schoten die ze toestaan (3.9 xGA) valt binnen vijftien seconden na "
     "balverlies van Feyenoord, en dat balverlies gebeurt op de eigen helft. Verover de bal hoog "
     "en er volgt meestal een grote kans, dus we zetten de eerste fase onder druk in plaats van af "
     "te wachten."),
    ("3.  Hun dreiging loopt over links",
     "41% van hun intredes in de laatste lijn en 58% van hun voorzetten komen van links, waar "
     "Hancko en de linksback opbouwen en Idrissi één-tegen-één isoleert. We overbelasten onze "
     "defensieve rechterkant en laten onze rechtsback nooit alleen."),
    ("4.  Sla vroeg toe, want het late spel is van hen",
     "Het enige kwartier waarin ze worden overklast is 15 tot 30 minuten (2.9 xGA, vier tegen). Na "
     "het uur zijn ze meedogenloos: twaalf goals gemaakt, één tegen. De eerste tik uitdelen telt "
     "tegen deze ploeg zwaarder dan tegen de meeste."),
    ("5.  De zestien is een slagveld aan beide kanten",
     "Ze maakten vijf goals uit standaardsituaties en kregen er drie tegen. Hun corners komen "
     "vooral van links en zijn gericht op de eerste paal, en hun voorzetten in open spel vinden "
     "maar een kwart van de keren een ploeggenoot, dus zowel onze zestien verdedigen als die van "
     "hen bedreigen loont."),
],
ATTACK=[
    ("Ze creëren centrale kansen, en ze maken ze af",
     "Dit is geen hoopvolle ploeg. Ze creëerden 28 grote kansen in tien duels en nemen 58% van hun "
     "schoten van binnen de zestien, door de bal eerst in de meest waardevolle zones te brengen. "
     "Ze scoren ook ruim boven verwachting, 26 goals uit 18.3 xG, dus de boodschap voor onze "
     "verdediging is simpel: geef niets weg en reken er niet op dat ze missen."),
    ("De goals zijn verdeeld achter één vaste afmaker",
     "Danilo leidt de aanval en de productie met zeven goals uit 5.45 xG, maar de dreiging stopt "
     "niet bij hem. Kökçü pikt zijn goals mee vanuit het middenveld en van de stip, Dilrosun en "
     "Szymański dragen bij vanaf de flank en tussen de linies, en Timber duikt laat op vanuit de "
     "diepte. Giménez is de gelijkwaardige optie vanaf de bank, dus het plan kan niet draaien om "
     "het stoppen van één speler."),
    ("Standaardsituaties zijn een echte route naar een goal",
     "Ongeveer één op de vijf schoten komt uit een standaardsituatie (39 schoten, vijf goals, 5.8 "
     "xG). Hun corners komen vooral van links en zijn gericht op de eerste paal, met Trauner en "
     "Hancko die de bal aanvallen en Kökçü die aanlevert. We verdedigen deze met volledige "
     "bezetting en focus op de eerste paal, en behandelen onze eigen standaardsituaties als een "
     "echte kans om toe te slaan."),
],
VULN_CAVEAT=("Eén eerlijke kanttekening: ongeveer een kwart van de xG die ze tegenkregen komt uit "
    "één wedstrijd (PSV). De zwakte in omschakeling is reëel, maar deels geconcentreerd, dus "
    "behandel het als een hefboom om op beeld te bevestigen, niet als een garantie."),
PLAYER_CARDS=[
    ("Orkun Kökçü", "10 · Diepe spelverdeler",
     "Het kloppend hart van de ploeg: 888 baltouches, een ploegtopper met 39 progressieve passes, "
     "16 kansen en vier goals, plus de standaardsituaties. Hij zakt uit om rond de middenlijn aan "
     "te nemen, net links van het centrum. Sta er kort op en laat hem niet draaien, dan stokt de "
     "opbouw."),
    ("Quinten Timber", "8 · Box-to-box",
     "Hun beste één-tegen-één-speler (27 dribbels aan 56%) en topcreatieveling vanuit de diepte "
     "met 17 kansen, over 924 minuten. Hij maakt meters en duikt op in de zestien. Wie hem dekt "
     "moet zijn loopacties naar voren volgen, niet alleen zijn startpositie."),
    ("Dávid Hancko", "33 · Centrale verdediger links",
     "De motor van de links-georiënteerde opbouw en hun op één na meest progressieve passer, met "
     "ook dreiging bij standaardsituaties (1.9 xG). Hij stapt in het middenveld om de bal te laten "
     "lopen, en de ruimte die hij achterlaat is precies waar wij in omschakeling willen aanvallen."),
    ("Sebastian Szymański", "17 · Aanvallende middenvelder",
     "Speelt tussen de linies en zakt naar links af. Drie goals, 16 kansen gecreëerd, dribbels aan "
     "50%. Een middenvelder moet hem in de halve ruimte oppikken voordat hij draait, want zodra "
     "hij met het gezicht naar ons doel staat doet hij pijn."),
    ("Javairô Dilrosun", "11 · Zwervende aanvaller",
     "Een dribbelaar met veel volume die voorin rondzwerft, gemiddeld iets naar rechts. Hij "
     "probeert veel (46 dribbels) maar slaagt er maar in 35%, met een ploegtopper van 49 "
     "baltouches in de zestien. Blijf geduldig, stuur hem naar binnen en ontneem de inzet in "
     "plaats van in te duiken."),
    ("Danilo", "9 · Spits",
     "Hun vaste afmaker, zeven goals uit 5.45 xG, levend op de laatste schouder. Gedisciplineerd "
     "dieptebeheer van onze centrale verdedigers is essentieel. Giménez is de gelijkwaardige optie "
     "vanaf de bank, dus de dreiging verandert nauwelijks als hij invalt."),
],
PLAYER_STATS={
    "Orkun Kökçü": [("39", "progr. passes"), ("16", "kansen"), ("888", "baltouches")],
    "Quinten Timber": [("17", "kansen"), ("56%", "dribbels gewonnen"), ("27", "dribbels")],
    "Dávid Hancko": [("31", "progr. passes"), ("1.9", "standaard-xG"), ("614", "minuten")],
    "Sebastian Szymański": [("3", "goals"), ("16", "kansen"), ("50%", "dribbels gewonnen")],
    "Javairô Dilrosun": [("46", "dribbels"), ("35%", "gewonnen"), ("49", "touches in 16")],
    "Danilo": [("7", "goals"), ("5.45", "xG"), ("8", "basisplaatsen")],
},
PLAN_IN=[
    "Verover en ga. Bijna een derde van de schoten die ze toestaan begint met balverlies op hun helft.",
    "Belast de eerste fase: mik op het kwartier 15 tot 30 minuten en reken niet op laat achtervolgen.",
    "Val de ruimte aan die Hancko achterlaat als hij instapt, met een loper die vanaf rechts indraait.",
    "Gebruik onze standaardsituaties. Ze geven er goals uit weg, dus oefen tweede-paal- en "
    "tweede-fase-varianten.",
],
PLAN_OUT=[
    "Zet druk op hun eerste fase. Trigger op de terugspeelbal naar Trauner of Bijlow en knijp de "
    "lijn naar Kökçü dicht.",
    "Dwing ze van diep links voor te zetten, win dan de zestien, zowel het eerste contact als de "
    "tweede bal.",
    "Geen geïsoleerde duels voor onze rechtsback tegen hun linkerkant; de winger volgt de "
    "opkomende back.",
    "Houd een aaneengesloten middenblok. Ze counteren nauwelijks, dus het gevaar is aanhoudende "
    "druk, geen ballen in de diepte.",
],
PLAN_SCEN=[
    ("Als ze 4-3-3 spelen",
     "Hun scherpere, meer links-belaste vorm (2.07 xG per duel, 43% van de intredes links). Verdubbel "
     "op die kant en gebruik een vrije man om Kökçü op te pikken. Ze zetten hier minder druk (PPDA "
     "12.2), dus we kunnen rustig opbouwen."),
    ("Als ze 4-2-3-1 spelen",
     "Evenwichtiger maar kwetsbaarder achterin (1.34 xGA) en ze zetten hoger druk (PPDA 9.7), wat ruimte achterin "
     "laat. Lok de druk uit en stuur lopers vroeg de diepte in."),
    ("Als we op voorsprong komen",
     "Blijf in het blok, beheer de standaardsituaties en houd de druktriggers op hun opbouw scherp. "
     "Zak niet zo diep dat we de aanhoudende druk uitlokken waar zij van leven."),
    ("Eerste half uur, of na een goal",
     "Hun zwakke kwartier is 15 tot 30 minuten, dus begin snel en probeer een vroege voorsprong te "
     "pakken. De slotfase is van hen: twaalf goals na het uur, slechts één tegen."),
],
WEEK_INTRO=("Zo zou ik dit door de week voeden: de juiste informatie, aan de juiste mensen, in de "
    "juiste vorm, op het juiste moment. De spelers krijgen het minder, scherper en visueler "
    "naarmate de wedstrijd nadert, en nooit meer dan drie boodschappen per dag zodra we op het veld "
    "staan."),
WEEK_DAYS=[
    ("MD-4 · Afstemming met de staf",
     "Het volledige dossier gaat naar de hoofdtrainer en assistenten, en we bepalen het "
     "spelmodel-antwoord: de druktriggers op hun opbouw, onze blokhoogte, de standaardsituatieplannen "
     "en de intentie voor de openingsfase. We leggen de drie of vier kernboodschappen vast die we de "
     "spelers gaan voeden. Nog geen spelersvideo; eerst het staf-verhaal afstemmen."),
    ("MD-3 · Team, zonder bal",
     "Een teammeeting van acht tot tien minuten over één thema: hoe ze opbouwen en waar ze kraken. "
     "Een korte clipreel van Kökçü die uitzakt, de linkse overbelasting en balverlies dat schoten "
     "werd. De enige vraag: zet druk op de opbouw, knijp Kökçü dicht, dwing ze naar links en win de "
     "zestien. De verdediging en keeper krijgen hun eigen linie-overleg over de ruimte in de diepte."),
    ("MD-2 · Team, met bal en omschakeling",
     "Onze route naar een goal: clips van balverovering op hun helft en de ruimte achter het instappen "
     "van Hancko, daarna trainen we het met omschakeling-naar-afronding-vormen die hun opstelling "
     "nabootsen. Vleugelspelers en backs krijgen een individueel clippakket over hun directe "
     "tegenstander (Idrissi, de hoge linksback, Pedersen)."),
    ("MD-1 · Standaardsituaties en individuen",
     "Een standaardsituatie-meeting in beide richtingen: onze eerste-paaldekking tegen Trauner en "
     "Hancko, en onze eigen aanvallende varianten tegen hun zestien-verdediging. Individuele clips "
     "van 60 tot 90 seconden gaan naar de spelers die ze nodig hebben, persoonlijk en gericht op hun "
     "directe duel. Houd het licht en zelfverzekerd."),
    ("MD · Alleen herinneringen",
     "Vandaag geen nieuwe informatie. Een visual van één pagina in de kleedkamer met de drie sleutels: "
     "zet druk op hun opbouw, dwing ze naar links en win de zestien, en sla vroeg toe. Individuele "
     "herinneringen van dertig seconden. Live vanaf de bank melden we of ze 4-3-3 of 4-2-3-1 spelen "
     "en passen we aan."),
],
METHOD=("Elke figuur en elk getal in dit dossier is rechtstreeks berekend uit de ruwe Opta F24 "
    "event-feeds en F7 opstellingen voor Feyenoords eerste tien Eredivisie-duels van 2022/23, "
    "zonder externe aggregaties. De veldconventie is benoemd en gecontroleerd: een y-waarde boven "
    "66.7 is de aanvallende linkerkant, geverifieerd aan de hand van bekende links- en "
    "rechtsspelers. Expected goals gebruikt een transparant afstand-en-hoekmodel met correcties "
    "voor koppen en standaardsituaties, gekalibreerd zodat het gemiddelde schot in de steekproef "
    "ongeveer de competitietypische 0.11 waard is. Feyenoords eigen schoten zijn gemiddeld 0.098 "
    "waard. Doelpunttotalen staan als wedstrijduitslagen (26 voor, 11 tegen); de schot-feed wijst "
    "27 en 10 toe, met als klein verschil eigen goals."),
CAVEATS=[
    "Tien wedstrijden is een steekproef van tendensen, geen oordeel. Eén duel (PSV) levert ongeveer "
    "een kwart van de tegen-xG, dus de zwakte in omschakeling is reëel maar deels geconcentreerd.",
    "De posities in het passnetwerk zijn gemiddelde balposities, dus ze tonen een opbouwvorm in "
    "plaats van een momentopname-elftal, en de verbindingen zijn afgeleid uit opeenvolgende acties.",
    "Met tracking- en balbezitdata zou ik de druktriggers, de lijnhoogte en de loopacties zonder bal "
    "kwantificeren, en een volledig seizoen zou stabiele patronen scheiden van ruis uit een kleine "
    "steekproef.",
    "In een clubomgeving zou elke figuur met gekoppelde video komen, zodat elk datapunt één klik "
    "van het moment op beeld verwijderd is.",
],
FORM_BLOCKS=[
    ("Dominant, en zelden in de problemen",
     "Zeven zeges uit tien en 26 goals vertellen het verhaal, en de onderliggende cijfers "
     "bevestigen het: hun xG ligt in acht van de tien duels boven hun tegen-xG. Ze controleren "
     "wedstrijden en creëren meer dan de tegenstander, dus een geduldige positiestrijd speelt hen "
     "recht in de kaart."),
    ("De uitzonderingen zijn de les",
     "De twee blauwe pieken zijn waar het misging voor hen. De 3-4-nederlaag bij PSV (3.2 xGA) en "
     "de 4-3-zege bij Go Ahead Eagles (2.5 xGA) waren allebei open duels vol omschakeling, van doel "
     "tot doel. Dat is het soort wedstrijd dat wij willen creëren."),
    ("Sla vroeg toe, vrees het late spel",
     "Het enige kwartier waarin ze worden overklast is 15 tot 30 minuten (2.9 xGA, vier tegen). Na "
     "het uur namen ze volledig over, met twaalf goals voor en één tegen. De eerste goal telt hier "
     "zwaarder dan tegen de meeste ploegen."),
],
POSS_BULLETS=[
    "Ze spelen door je heen, niet over je heen. Slechts één op de tien passes is lang, en Kökçü "
    "(888 baltouches, 39 progressieve passes) zakt uit om rond de middenlijn het tempo te bepalen. "
    "Knijp de lijn naar zijn voeten dicht en de opbouw stokt meestal.",
    "De voorkeur ligt duidelijk links: 41% van hun intredes in de laatste lijn en 58% van hun "
    "voorzetten komen van die kant, met Hancko en de linksback in de opbouw, Idrissi die isoleert "
    "en Szymański die overhelt.",
    "Het voorzetten gebeurt in groot volume maar bescheiden kwaliteit, 18.9 per duel aan 25% "
    "aankomst. Een goed bezette zestien en focus op de tweede bal halen er de meeste angel uit.",
    "Rechts komt Pedersen hoog op als overlap-en-voorzet-uitweg in plaats van als creatieveling, "
    "dus onze linkerkant moet alert zijn op de loper onder hem door.",
],
PRESS_BULLETS=[
    "In de 4-3-3 zijn ze scherper en meer links-belast (2.07 xG, 43% van de intredes links, 1.07 "
    "xGA) en zetten ze minder druk (PPDA 12.2). Tegen deze vorm bouwen we geduldig op en verdubbelen "
    "we op hun linkerkant.",
    "In de 4-2-3-1 zijn ze evenwichtiger maar kwetsbaarder achterin (1.34 xGA) en zetten ze iets hoger druk (PPDA "
    "9.7), wat meer ruimte achterin laat. Hier lokken we de druk uit en sturen we lopers vroeg die "
    "ruimte in.",
    "Hoe dan ook zitten ze in een middenblok en veroveren ze rond de middenlijn in plaats van hoog "
    "te jagen, dus we krijgen tijd op de bal op onze eigen helft. Wat we met die tijd doen is de "
    "hele wedstrijd.",
],
SETPIECE_BULLETS=[
    "Hun standaarden verdedigen: hun corners komen vooral van links en zijn gericht op de eerste "
    "paal (42 van 70 inzetten in de zestien; slechts 5% kort). We vallen de eerste paal en het "
    "eerste contact aan, zetten lichamen op Trauner en Hancko en winnen de centrale tweede bal.",
    "Hun zestien aanvallen: ze kregen drie goals uit standaardsituaties tegen in tien duels en hun "
    "voorzetten in open spel vinden maar een kwart van de keren een ploeggenoot, dus we overbelasten "
    "hun zestien, mikken op de tweede paal en spelen op de tweede fase.",
    "Herwinnen: hun backs schuiven op om corners aan te vallen, wat betekent dat een weggewerkte "
    "standaardsituatie onze omschakelingstrigger wordt. De eerste uitweg moet meteen de ruimte in "
    "die zij achterlaten.",
],
VULN_ACTS=[
    ("Zet druk op hun opbouw, wacht niet af",
     "Bijna een derde van de schoten die ze toestaan (3.9 xGA) valt binnen vijftien seconden na "
     "balverlies, en dat balverlies gebeurt op hun eigen helft (gemiddelde x van 32). Trigger de "
     "druk op de terugspeelbal naar Trauner of Bijlow en knijp Kökçü dicht zodat hij niet kan "
     "draaien. Dit is onze duidelijkste route naar een kans tegen hen."),
    ("Maak er een omschakelingsduel van, en sla vroeg toe",
     "Hun enige zwakke kwartier is 15 tot 30 minuten (2.9 xGA), en na het uur zijn ze meedogenloos: "
     "twaalf goals gemaakt, één tegen. Pak een vroege voorsprong en houd het duel open, want ze "
     "counteren zelf nauwelijks (één counterschot in de hele periode)."),
    ("Win de zestien bij standaardsituaties",
     "Ze kregen drie goals uit standaardsituaties tegen in tien duels en hun voorzetten komen maar "
     "een kwart van de keren aan. We verdedigen onze zestien met volledige bezetting en gaan dan op "
     "die van hen af: bezet de tweede paal en speel op de tweede bal."),
],
XI_SHAPE=("Ze verdeelden de periode gelijk over een 4-2-3-1 en een 4-3-3, maar de 4-3-3 die hier "
    "staat is hun scherpere, meer links-belaste versie en die om eerst op voor te bereiden.\n\nBijlow "
    "bouwt op met Trauner en Hancko, Kökçü zakt uit als enige controleur, en Timber en Szymański "
    "spelen voor hem met vrijheid om te zwerven en in de zestien op te duiken.\n\nDe breedte en de "
    "dreiging komen van links. Pedersen rechts is meer een opkomende uitweg, en Danilo leidt de "
    "aanval op de laatste schouder."),
XI_ROTATION=("De ruggengraat ligt vast, dus het elftal hierboven is een zelfverzekerde basis en geen "
    "gok: Bijlow, Trauner, Timber en Dilrosun stonden alle tien de duels in de basis, met Kökçü, "
    "Hancko, Pedersen en Danilo daar vlak achter."),
XI_BENCH=[
    "Geertruida en Rasmussen zijn de belangrijkste defensieve alternatieven en kunnen beiden het "
    "middenveld in stappen.",
    "López en Hartman dekken linksback af, de bron van het grootste deel van hun aanvallende breedte.",
    "Giménez is de gelijkwaardige spits vanaf de bank en zit Danilo dicht op de hielen.",
],
WHY_TEXT=("Tegenstanderanalyse is alleen nuttig als ze het gedrag op het veld verandert. Mijn "
    "prioriteit was om van een grote, ruwe dataset naar een klein aantal heldere, met bewijs "
    "onderbouwde boodschappen te gaan die een trainer kan installeren en een speler kan onthouden: "
    "structuur, patronen, kwetsbaarheden, sleutelspelers en scenario's, elk gekoppeld aan een "
    "concrete actie en een manier om die door de week te communiceren. Die vertaling, consistent, "
    "nauwkeurig en op tijd gedaan, is het werk."),
)

# ---- expose chosen language as module-level names --------------------------
globals().update(_NL if NL else _EN)

# ---- short UI labels (build_report + figures) ------------------------------
UI = {
    # chrome eyebrows / titles
    "Team overview": "Teamoverzicht", "The 60-second briefing": "De briefing van 60 seconden",
    "Probable XI": "Vermoedelijke opstelling", "Their most-used eleven": "Hun meest gebruikte elftal",
    "Form & game-state": "Vorm & wedstrijdverloop", "Who they are, and how it's gone":
        "Wie ze zijn, en hoe het ging",
    "Attacking tendencies": "Aanvallende tendensen", "How they build and create":
        "Hoe ze opbouwen en creëren",
    "Attacking threat": "Aanvallende dreiging", "Where the goals come from": "Waar de goals vandaan komen",
    "Defensive tendencies": "Verdedigende tendensen", "Their block & their two shapes":
        "Hun blok & hun twee vormen",
    "How to hurt them": "Hoe je ze pijn doet", "The opening": "De opening",
    "Set pieces": "Standaardsituaties", "Live at both ends": "Gevaarlijk aan beide kanten",
    "Key players": "Sleutelspelers", "Who to plan around": "Om wie je het plan bouwt",
    "Game plan": "Wedstrijdplan", "The concrete recommendations": "De concrete aanbevelingen",
    "Matchweek delivery": "Communicatie door de week",
    "What I'd tell the players, day by day": "Wat ik de spelers zou vertellen, dag voor dag",
    "Appendix": "Bijlage", "Method, honesty & intent": "Methode, eerlijkheid & intentie",
    "OPPOSITION ANALYSIS": "WEDSTRIJDANALYSE",
    "FEYENOORD · OPPOSITION ANALYSIS": "FEYENOORD · WEDSTRIJDANALYSE",
    "Club Brugge · Analysis Department": "Club Brugge · Analyseafdeling",
    # cover
    "CLUB BRUGGE · ANALYSIS DEPARTMENT": "CLUB BRUGGE · ANALYSEAFDELING",
    "OPPOSITION": "TEGENSTANDER", "ANALYSIS": "ANALYSE",
    "SCOUTING WINDOW": "SCOUTINGPERIODE", "PREPARED BY": "OPGESTELD DOOR",
    "GAME PREPARATION ANALYST · WORK SAMPLE": "GAME PREPARATION ANALYST · WERKVOORBEELD",
    # section / panel headers
    "TEAM PROFILE": "TEAMPROFIEL",
    "FIVE THINGS THAT DECIDE THE GAME": "VIJF DINGEN DIE DE WEDSTRIJD BEPALEN",
    "MOST-USED ELEVEN · LIKELY 4-3-3": "MEEST GEBRUIKTE ELFTAL · WAARSCHIJNLIJK 4-3-3",
    "THE SHAPE": "DE OPSTELLING", "ROTATION & BENCH": "ROTATIE & BANK",
    "WHAT IT MEANS": "WAT HET BETEKENT", "READ IT IN-GAME": "LEES HET TIJDENS DE WEDSTRIJD",
    "ATTACKING OUTPUT": "AANVALLENDE OUTPUT",
    "THREE WAYS TO HURT THEM": "DRIE MANIEREN OM ZE PIJN TE DOEN",
    "DEFEND IT / ATTACK IT": "VERDEDIGEN / AANVALLEN",
    "WITH THE BALL": "MET DE BAL", "WITHOUT THE BALL": "ZONDER DE BAL",
    "IN-GAME SCENARIOS": "SCENARIO'S TIJDENS DE WEDSTRIJD",
    "HOW THIS WAS BUILT": "HOE DIT IS GEMAAKT",
    "WHAT I'D ADD WITH MORE TIME / DATA": "WAT IK MET MEER TIJD / DATA ZOU TOEVOEGEN",
    "WHY THIS ROLE, WHY THIS WAY": "WAAROM DEZE ROL, WAAROM ZO",
    # figure eyebrows / captions
    "Expected goals, match by match": "Expected goals, per wedstrijd",
    "When they hurt you, and when you hurt them": "Wanneer zij jou pijn doen, en jij hen",
    "Build-up shape · node = involvement, line = pass volume":
        "Opbouwvorm · stip = betrokkenheid, lijn = passvolume",
    "Where they enter the final third": "Waar ze de laatste lijn betreden",
    "EVERY SHOT · SIZE = xG · BLUE = GOALS": "ELK SCHOT · GROOTTE = xG · BLAUW = GOALS",
    "Top contributors across the window": "Belangrijkste spelers in de periode",
    "Defensive actions · where they win it back": "Verdedigende acties · waar ze de bal heroveren",
    "A tale of two shapes · 5 games each": "Een verhaal van twee vormen · elk 5 duels",
    "Ball-losses that became a shot within 15s · blue = led to a goal":
        "Balverlies dat binnen 15s een schot werd · blauw = leidde tot een goal",
    "Set-piece shots · threat (left) vs conceded (right)":
        "Schoten uit standaard · dreiging (links) vs tegen (rechts)",
    "Their corner delivery and first contact": "Hun cornervoorzet en eerste contact",
    # stat-strip labels
    "of all passes": "van alle passes", "long balls": "lange ballen",
    "progressive/game": "progressief/duel", "crosses/game": "voorzetten/duel",
    "crosses done": "voorzetten aan", "shots": "schoten", "goals": "goals", "xG": "xG",
    "over-performance vs xG": "boven verwachting vs xG", "shots in the box": "schoten in de 16",
    "big chances created": "grote kansen", "PPDA": "PPDA", "avg recovery": "gem. herovering",
    "actions def third": "acties verd. derde", "att third": "aanv. derde",
    "high turnovers/g": "hoge veroveringen/d",
    "shots from turnovers": "schoten uit balverlies", "transition shots": "omschakelschoten",
    "transition xGA": "omschakel-xGA", "avg loss (their half)": "gem. verlies (eigen helft)",
    "goals conceded": "tegengoals", "SP goals for": "standaard-goals voor",
    "SP goals against": "standaard-goals tegen", "corners": "corners",
    "left/right": "links/rechts", "short": "kort",
    # figure in-chart text
    "xG for": "xG voor", "xG against": "xG tegen",
    "goals for": "goals voor", "goals against": "goals tegen",
    "Cumulative goals": "Cumulatieve goals",
    "Expected goals (10-game total)": "Expected goals (totaal 10 duels)",
    "Match minute": "Wedstrijdminuut",
    "Attacking  →": "Aanvalsrichting  →",
    "Feyenoord attacking  →": "Feyenoord aanvalsrichting  →",
    "FINAL-THIRD ENTRIES": "INTREDES LAATSTE LIJN",
    "LEFT": "LINKS", "CENTRAL": "CENTRAAL", "RIGHT": "RECHTS",
    "Where Feyenoord enter the final third (pass end-points)":
        "Waar Feyenoord de laatste lijn betreedt (eindpunten passes)",
    "PRESS ZONE · losses here become shots against":
        "DRUKZONE · balverlies hier wordt een schot tegen",
    "their soft spot\n2.9 xGA · 4 conceded": "zwakke fase\n2.9 xGA · 4 tegen",
    "ruthless late\n12 goals after 60'": "meedogenloos laat\n12 goals na 60'",
    "xG / game": "xG / duel", "xGA / game": "xGA / duel", "Shots / game": "Schoten / duel",
    "Left-side entries %": "Intredes links %", "Crosses / game": "Voorzetten / duel",
    "PPDA (their press)": "PPDA (hun druk)", "5 games each": "elk 5 duels",
    "Goals + xG": "Goals + xG", "Chances created": "Kansen gecreëerd",
    "Take-ons completed": "Dribbels geslaagd",
    "Goals + xG panel: bars = xG · blue number = goals scored":
        "Goals + xG-paneel: balken = xG · blauw getal = goals",
    # f-string fragments
    "THREAT": "DREIGING", "CONCEDED": "TEGEN",
    "high turnovers": "hoge veroveringen", "def-third actions": "acties verd. derde",
    "/game": "/d",
    "avg recovery  x=": "gem. herovering  x=", "avg loss  x=": "gem. verlies  x=",
    "left corners": "corners links", "right corners": "corners rechts",
    "mostly to the near post": "vooral naar de eerste paal",
    "mostly to the far post": "vooral naar de tweede paal", "short corners": "kort genomen",
    "percentile vs squad": "percentiel t.o.v. selectie",
    "FIRST HALF": "EERSTE HELFT", "SECOND HALF": "TWEEDE HELFT",
}


def L(s):
    """Translate a short UI label when LANG=nl (pass-through otherwise)."""
    if not NL:
        return s
    return UI.get(s, s)
