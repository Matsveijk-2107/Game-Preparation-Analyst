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

# ---- palette (Feyenoord house style) -------------------------------------
# Brand colours are shared; neutrals + functional accents flip by mode.
FEY = "#E4032E"          # Feyenoord red (their identity + their actions)
FEY_D = "#A8001F"        # deep red
FEY_BRT = "#FF234E"      # bright red highlight

if _LIGHT:
    INK = "#F5F2EA"      # warm paper page background
    INK_2 = "#EDE8DC"    # alternate band
    PANEL = "#FFFFFF"    # white card
    PANEL_2 = "#F1ECE1"  # raised / callout fill
    LINE = "#D2CCBC"     # hairlines / pitch lines
    HAIRLINE_SOFT = "#E4DFD2"
    TEXT = "#17191E"     # near-black ink
    MUTE = "#586172"     # secondary
    FAINT = "#9A958A"    # tertiary
    CB_BLUE = "#1E6FC4"  # our voice (darker for light bg)
    CB_BLUE_D = "#14528F"
    GREEN = "#149A5C"
    GOAL = "#C98A06"     # goals / highlight (deep gold for contrast on paper)
    WARN = "#D9531A"     # conceded / threat
    CREAM = "#B8902F"    # warm gold hairline accent
    EDGE = "#17191E"     # marker outline (dark on paper)
    STROKE_BG = INK      # label halo colour (paper)
    CMAP_HEAT = "Reds"   # density: light -> deep red (reads on paper)
    CMAP_PRESS = "Blues"
else:
    INK = "#0C0D10"      # near-black page background
    INK_2 = "#101116"
    PANEL = "#15161B"
    PANEL_2 = "#1C1E25"
    LINE = "#2C2F39"
    HAIRLINE_SOFT = "#22242C"
    TEXT = "#F4F5F7"
    MUTE = "#A2A8B4"
    FAINT = "#6A7180"
    CB_BLUE = "#2E86DE"
    CB_BLUE_D = "#1B5FB0"
    GREEN = "#19B36B"
    GOAL = "#F4C430"
    WARN = "#FF7B3D"
    CREAM = "#EFE7D2"
    EDGE = "#06101C"
    STROKE_BG = INK
    CMAP_HEAT = "rocket"
    CMAP_PRESS = "mako"

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
def spine(ax, y0=0.062, y1=0.94, x=None):
    """Constant red brand skeleton anchoring the left margin."""
    if x is None:
        x = MX - 0.020
    ax.add_patch(_Rect((x, y0), 0.0045, y1 - y0, color=FEY, zorder=3))


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
