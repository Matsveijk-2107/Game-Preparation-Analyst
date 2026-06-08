"""Shared visual identity — Feyenoord house style (red / black / white).

Theme is mode-switchable via the DOSSIER_THEME env var ("light" default, or "dark").
All names are stable so every figure/report module reskins automatically.
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon
from scipy.interpolate import make_interp_spline

THEME = os.environ.get("DOSSIER_THEME", "light").lower()
_LIGHT = THEME != "dark"

# ---- palette --------------------------------------------------------------
# LIGHT = Club Brugge house style: royal BLUE + BLACK on WHITE only
# (neutral greys are tints of black/white). No other hues are used.
if _LIGHT:
    INK = "#FFFFFF"          # white page background
    INK_2 = "#F4F8FD"        # barely-there gradient top
    PANEL = "#F4F7FC"        # card
    PANEL_2 = "#E9F1FB"      # raised / callout / header band
    LINE = "#CAD7E7"         # hairlines / pitch lines
    HAIRLINE_SOFT = "#E4EBF4"
    TEXT = "#0E1722"         # near-black ink
    MUTE = "#33414F"         # secondary (dark slate, readable on white)
    FAINT = "#637186"        # tertiary (captions)
    CB_BLUE = "#0A57B0"      # Club Brugge royal blue (brand + 'our' series + goals)
    CB_BLUE_D = "#063A78"
    FEY = "#16191F"          # near-black: opponent / primary data series
    FEY_D = "#000000"
    FEY_BRT = "#2A2F37"
    GOAL = "#0A57B0"         # goals / highlights -> royal blue (readable two-tone)
    WARN = "#3C4A5C"         # dark slate: conceded / threat (neutral)
    GREEN = "#4E94D8"        # mid blue: positive fills (e.g. take-ons)
    CREAM = "#0A57B0"        # warm accent removed; reuse blue
    EDGE = "#FFFFFF"         # white marker outline to separate overlaps
    STROKE_BG = "#FFFFFF"    # white label halo
    CMAP_HEAT = "Blues"
    CMAP_PRESS = "Greys"
else:
    INK = "#0A0B0F"; INK_2 = "#12141C"; PANEL = "#15171F"; PANEL_2 = "#1C1F2A"
    LINE = "#2B2F3C"; HAIRLINE_SOFT = "#23262F"; TEXT = "#F6F7FA"; MUTE = "#9DA6B6"
    FAINT = "#646D7D"; CB_BLUE = "#1E73E6"; CB_BLUE_D = "#10468F"
    FEY = "#E4032E"; FEY_D = "#A8001F"; FEY_BRT = "#FF234E"
    GOAL = "#F4C430"; WARN = "#FF7B3D"; GREEN = "#1FBE76"
    CREAM = "#E7D9B4"; EDGE = "#05060A"; STROKE_BG = "#0A0B0F"
    CMAP_HEAT = "rocket"; CMAP_PRESS = "mako"

RED_DEEP = FEY_D
RED_BRT = FEY_BRT
BLUE_DEEP = CB_BLUE_D

HEAD_FONT = "Bahnschrift"
BODY_FONT = "Segoe UI"


def apply():
    mpl.rcParams.update({
        "figure.facecolor": INK,
        "savefig.facecolor": INK,
        "axes.facecolor": INK,
        "font.family": BODY_FONT,
        "text.color": TEXT,
        "axes.edgecolor": LINE,
        "axes.labelcolor": TEXT,
        "xtick.color": MUTE,
        "ytick.color": MUTE,
        "axes.grid": False,
        "figure.dpi": 150,
        "savefig.dpi": 200,
    })


def head(ax, x, y, s, size=15, color=TEXT, weight="bold", **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontfamily=HEAD_FONT,
                   weight=weight, **kw)


def body(ax, x, y, s, size=9.5, color=TEXT, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontfamily=BODY_FONT, **kw)


def kicker(ax, x, y, s, color=FEY, size=9):
    return ax.text(x, y, s.upper(), fontsize=size, color=color,
                   fontfamily=HEAD_FONT, weight="bold", alpha=0.95)


# ---------------------------------------------------------------------------
# bklit / shadcn-style gradient area: smooth line + vertical gradient fill
# ---------------------------------------------------------------------------
def gradient_area(ax, x, y, color, baseline=0.0, lw=2.6, alpha=0.55,
                  smooth=True, points=300, zorder=3, label=None, dots=True):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if smooth and len(x) >= 4:
        xs = np.linspace(x.min(), x.max(), points)
        spl = make_interp_spline(x, y, k=3)
        ys = np.clip(spl(xs), baseline, None)
    else:
        xs, ys = x, y
    ax.plot(xs, ys, color=color, lw=lw, zorder=zorder + 1, label=label,
            solid_capstyle="round")
    # gradient image clipped to the area under the curve
    grad = np.empty((256, 1, 4))
    grad[:, 0, :3] = to_rgb(color)
    grad[:, 0, 3] = np.linspace(alpha, 0.0, 256)
    ytop = max(ys.max(), baseline + 1e-6)
    im = ax.imshow(grad, aspect="auto", origin="upper",
                   extent=[xs.min(), xs.max(), baseline, ytop],
                   zorder=zorder)
    verts = np.vstack([np.column_stack([xs, ys]),
                       [xs[-1], baseline], [xs[0], baseline]])
    clip = Polygon(verts, closed=True, transform=ax.transData)
    im.set_clip_path(clip)
    if dots:
        ax.scatter(x, y, s=26, color=color, zorder=zorder + 2,
                   edgecolor=EDGE, linewidth=1.1)
    return xs, ys


def style_axes(ax, grid=True):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(LINE)
        ax.spines[s].set_linewidth(0.8)
    ax.tick_params(length=0)
    if grid:
        ax.grid(axis="y", color=LINE, alpha=0.45, lw=0.6, zorder=0)


# ---- shared layout constants ---------------------------------------------
W_IN, H_IN = 8.27, 11.69   # A4 portrait, shared for aspect math
MX = 0.062                  # canonical side margin

import matplotlib.image as _mpimg          # noqa: E402
from matplotlib.patches import Rectangle as _Rect, Polygon as _Poly  # noqa: E402


# ---------------------------------------------------------------------------
# Signature house-style moves (operate on a full-page axes, coords 0..1)
# ---------------------------------------------------------------------------
def spine(ax, y0=0.062, y1=0.94, x=None, color=CB_BLUE):
    """Constant brand skeleton anchoring the left margin (Club Brugge blue)."""
    if x is None:
        x = MX - 0.020
    ax.add_patch(_Rect((x, y0), 0.0045, y1 - y0, color=color, zorder=3))


def ghost_number(ax, n, x=0.992, y=0.012):
    """Oversized faint page numeral bleeding off the corner (texture, not content)."""
    ax.text(x, y, f"{n:02d}", fontsize=150, color=PANEL, fontfamily=HEAD_FONT,
            weight="bold", ha="right", va="bottom", zorder=0, alpha=1.0)


def ignition_tick(ax, x, y, h=0.022, w=0.014, color=FEY):
    """Small red square to the left of a section head — brand mark cascade."""
    ax.add_patch(_Rect((x, y), w, h, color=color, zorder=5,
                       transform=ax.transAxes if False else ax.transData))


def hero_underline(ax, cx, y, width_frac, color=FEY):
    """2px red underline centred under a hero number."""
    ax.plot([cx - width_frac / 2, cx + width_frac / 2], [y, y], color=color,
            lw=2.2, zorder=6, solid_capstyle="butt")


def crest_watermark(fig, emblem_path, center=(0.5, 0.30), width=0.5, alpha=0.05):
    """Ghost-print the crest (desaturated) behind whitespace."""
    try:
        img = _mpimg.imread(emblem_path).astype(float)
    except Exception:
        return
    if img.ndim == 3 and img.shape[2] >= 3:
        grey = img[..., :3].mean(axis=2, keepdims=True)
        img = img.copy()
        img[..., :3] = grey
    h = width * W_IN / H_IN
    cx, cy = center
    a = fig.add_axes([cx - width / 2, cy - h / 2, width, h], zorder=0)
    a.imshow(img, alpha=alpha)
    a.axis("off")
    return a


def page_gradient(fig, glow=True):
    """Rich branded page background: subtle vertical gradient + faint red glow."""
    ax = fig.add_axes([0, 0, 1, 1], zorder=-30)
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    top = np.array(to_rgb(INK_2)); bot = np.array(to_rgb(INK))
    g = np.linspace(0, 1, 256).reshape(-1, 1, 1)
    img = top.reshape(1, 1, 3) * (1 - g) + bot.reshape(1, 1, 3) * g
    ax.imshow(img, extent=[0, 1, 0, 1], aspect="auto", origin="upper", zorder=-30)
    if glow:
        yy, xx = np.mgrid[0:240, 0:170]
        d = np.hypot((xx - 170) / 120, (yy - 0) / 150)        # glow at top-right
        a = np.clip(0.09 * np.exp(-(d ** 2)), 0, 0.09)
        rgba = np.zeros((240, 170, 4)); rgba[..., :3] = to_rgb(CB_BLUE); rgba[..., 3] = a
        ax.imshow(rgba, extent=[0.62, 1.0, 0.66, 1.0], aspect="auto", origin="upper", zorder=-29)
    return ax


def jersey_split(ax, x0, y0, x1, y1, alpha=0.10):
    """Abstracted Feyenoord half-and-half: left red wash, hard seam at mid."""
    xm = (x0 + x1) / 2
    ax.add_patch(_Rect((x0, y0), xm - x0, y1 - y0, color=FEY, alpha=alpha, zorder=0))
    ax.plot([xm, xm], [y0, y1], color=FEY, lw=1.0, alpha=0.5, zorder=1)


def diagonal_cut(ax, y_base=0.50, x0=0.0, x1=0.62, rise=0.018):
    """Thin red parallelogram slicing toward the wordmark — forward momentum."""
    pts = [(x0, y_base), (x1, y_base + rise), (x1, y_base + rise - 0.006),
           (x0, y_base - 0.006)]
    ax.add_patch(_Poly(pts, closed=True, color=FEY, zorder=2))
    pts2 = [(x0, y_base - 0.006), (x1, y_base + rise - 0.006),
            (x1, y_base + rise - 0.010), (x0, y_base - 0.010)]
    ax.add_patch(_Poly(pts2, closed=True, color=FEY_D, zorder=2))
