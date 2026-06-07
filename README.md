# Feyenoord — Opposition Analysis

Application work sample for the **Game Preparation Analyst** role at Club Brugge.

A data-driven opposition dossier on **Feyenoord** (Eredivisie 2022/23, matchdays 1–10),
built entirely from raw **Opta F24** event data and **F7** line-ups — no third-party
aggregations. Every figure and number is computed from the feeds.

## Deliverables (`output/`)

- **`Feyenoord_Opposition_Analysis.pdf`** — the 12-page A4 dossier:
  cover · executive summary · profile & form · in possession · attacking threat ·
  out of possession (block & two shapes) · vulnerabilities (how to hurt them) ·
  set pieces · key players · game plan · weekly player-communication plan (MD-4 → MD) ·
  method & appendix.
- **`Feyenoord_Opposition_Deck.pdf`** — a 15-slide presentation version (the staff/
  player-room cut, with per-player percentile radars).

## What's inside the analysis

- **In possession** — build-up shape (pass network), final-third entry tilt, crossing.
- **Out of possession** — block height / PPDA, and a 4-2-3-1 vs 4-3-3 split (5 games each).
- **Vulnerabilities** — turnover→shot chains: ~29% of shots conceded follow a Feyenoord
  ball-loss within 15s, in their own half — i.e. *press their build-up*.
- **Timing** — game-state by 15-minute window (their soft spot is 15–30').
- **Set pieces**, **key-player scouting cards**, a concrete **game plan**, and a
  day-by-day **player-communication plan**.

## Reproducible pipeline

```bash
python analysis/emblem.py        # prepare the crest asset
python analysis/analyze.py       # parse feeds -> output/metrics.json
python analysis/analyze_ext.py   # per-90 table, radars, clips -> metrics_ext.json
python analysis/analyze_more.py  # formation split, transition, set pieces -> metrics_more.json
python analysis/figures.py       # core pitch plots & charts
python analysis/figures_ext.py   # radars, ranking bars, transition map
python analysis/figures_more.py  # transition-press, game-state, formation, corners
python analysis/build_report.py  # compose the A4 dossier PDF
python analysis/build_deck.py    # compose the presentation deck PDF
```

| File | Role |
|------|------|
| `analysis/parse.py` | Opta F24/F7 parser; tidy event/line-up DataFrames; geometry xG model |
| `analysis/analyze*.py` | Tactical metric engines → `metrics*.json` |
| `analysis/figures*.py` | Pitch plots & charts (mplsoccer) |
| `analysis/theme.py` | Visual identity (palette, fonts, signature helpers) |
| `analysis/report_content.py` | All narrative copy |
| `analysis/build_report.py` / `build_deck.py` | Page layout & PDF assembly |

**Theme switch:** the whole pipeline reskins via one env var —
`DOSSIER_THEME=light` (default, print-friendly) or `DOSSIER_THEME=dark` (on-screen).

## Notes on method

- **xG** — transparent distance-and-angle geometry model (with header / set-piece
  adjustments), calibrated so the mean across all shots in the sample matches a
  league-typical ~0.11. A chance-quality decision aid, not a black box.
- **Flank convention** verified explicitly (y>66.7 = attacking left).
- **Goals** quoted as match results (26 for / 11 against); the shot-event feed attributes
  27/10, the small difference being own goals.
- Requires: `pandas`, `numpy`, `matplotlib`, `mplsoccer`, `scipy`, `pillow`.

## Data

The raw **Opta F24/F7 feeds are licensed and are *not* included** in this repository
(excluded via `.gitignore`). The PDFs and derived `metrics*.json` are the shareable
work product.

Prepared by **Mats van Eijk**.
