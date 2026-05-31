"""
carbon_sink_regeneration_strategy_map.py
==========================================
Conceptual strategy map: Carbon Sink Regeneration

Nine regeneration strategies arranged radially around a central hub,
all pointing toward a shared goal of restored carbon fixation capacity.

Strategies:
  1  Soil Regeneration
  2  Humus Formation
  3  Organic Waste Circulation
  4  Desert Regeneration
  5  Forest and Vegetation Recovery
  6  Ocean Oxygenation and Plankton Support
  7  Water-Cycle Restoration
  8  Microbial Ecosystem Recovery
  9  Direct Planetary Cooling (complementary thermal intervention)

DISCLAIMER: Conceptual diagram. Not a measured dataset or validated climate model.

Author : Master (inchacomisho / inchacomusho)
License: CC BY-SA 4.0
"""

import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# ── figure setup ─────────────────────────────────────────────────────────────
FW, FH = 15, 13
fig, ax = plt.subplots(figsize=(FW, FH))
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis("off")
fig.patch.set_facecolor("#f0f5f0")
ax.set_facecolor("#f0f5f0")

# ── helpers ───────────────────────────────────────────────────────────────────
def draw_box(cx, cy, w, h, text, fc, tc="white", fs=8.8, bold=True, lh=1.35):
    p = FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.14",
        facecolor=fc, edgecolor="#2c3e50",
        linewidth=1.3, zorder=3,
    )
    ax.add_patch(p)
    kw = dict(ha="center", va="center", fontsize=fs, color=tc,
               zorder=4, multialignment="center", linespacing=lh)
    if bold:
        kw["fontweight"] = "bold"
    ax.text(cx, cy, text, **kw)

def draw_arrow_to_hub(sx, sy, tx, ty, col, lw=1.8):
    """Draw a straight arrow from strategy box edge toward the hub."""
    ax.annotate("",
                xy=(tx, ty), xytext=(sx, sy),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=col, lw=lw,
                    connectionstyle="arc3,rad=0.0",
                ),
                zorder=2)

# ── central hub ───────────────────────────────────────────────────────────────
HUB_X, HUB_Y = 7.5, 6.7
HUB_W, HUB_H = 3.8, 1.45
HUB_COLOR = "#1a6b3c"

draw_box(HUB_X, HUB_Y, HUB_W, HUB_H,
         "Carbon Sink\nRegeneration\nStrategy",
         HUB_COLOR, fs=11.0, lh=1.3)

# ── strategy definitions ──────────────────────────────────────────────────────
# (label, sublabel, face-color, icon-char, radius, angle-degrees)
# Angles are spread from 30° to 330° (avoiding the bottom where the goal box is)
STRATEGIES = [
    ("Soil\nRegeneration",
     "min. tillage\norganic matter return",
     "#5d8a3c", 4.5, 95),
    ("Humus\nFormation",
     "compost  /  biochar\nstable carbon storage",
     "#7a6a3c", 4.5, 140),
    ("Organic Waste\nCirculation",
     "return carbon to soil\nreduce incineration",
     "#c0873a", 4.5, 175),
    ("Desert\nRegeneration",
     "pioneer plants\nartificial lakes",
     "#b5822a", 4.5, 215),
    ("Forest and\nVegetation Recovery",
     "halt clearing\ndiverse agroforestry",
     "#2e7d32", 4.5, 250),
    ("Ocean Oxygenation\nand Plankton Support",
     "vertical mixing support\nphytoplankton recovery",
     "#1565c0", 4.5, 290),
    ("Water-Cycle\nRestoration",
     "watershed forests\nwetland recovery",
     "#0288d1", 4.5, 325),
    ("Microbial Ecosystem\nRecovery",
     "reduce chemical inputs\ndiversify crops",
     "#6a1b9a", 4.5, 10),
    ("Direct Planetary\nCooling",
     "UMC / OBS — conceptual\ncomplementary thermal support",
     "#37474f", 4.5, 50),
]

BOX_W = 3.0
BOX_H = 1.15
HUB_R = min(HUB_W, HUB_H) / 2   # hub half-size for arrow target

for label, sublabel, fc, radius, angle_deg in STRATEGIES:
    a = math.radians(angle_deg)
    cx = HUB_X + radius * math.cos(a)
    cy = HUB_Y + radius * math.sin(a)

    # Draw strategy box
    draw_box(cx, cy, BOX_W, BOX_H, label, fc, fs=8.8)

    # Sub-label below box (small italic)
    ax.text(cx, cy - BOX_H/2 - 0.28,
            sublabel,
            ha="center", va="top",
            fontsize=7.0, color="#555555", style="italic",
            multialignment="center", linespacing=1.25, zorder=4)

    # Arrow: from box face nearest hub → hub edge
    # Direction vector from box center to hub center
    dx = HUB_X - cx
    dy = HUB_Y - cy
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist  # unit vector

    # Start: box edge closest to hub
    half_w = BOX_W / 2
    half_h = BOX_H / 2
    # clamp to box edge
    if abs(ux) * half_h > abs(uy) * half_w:
        t = half_w / abs(ux)
    else:
        t = half_h / abs(uy)
    sx = cx + ux * t + ux * 0.08
    sy = cy + uy * t + uy * 0.08

    # End: hub edge
    hub_half = max(HUB_W, HUB_H) / 2
    tx = HUB_X - ux * (HUB_W / 2 + 0.05)
    ty = HUB_Y - uy * (HUB_H / 2 + 0.05)

    draw_arrow_to_hub(sx, sy, tx, ty, col=fc, lw=1.7)

# ── GOAL BOX at the bottom ────────────────────────────────────────────────────
GOAL_X, GOAL_Y = 7.5, 1.55
draw_box(GOAL_X, GOAL_Y, 7.5, 1.10,
         "Restored Carbon Fixation Capacity\n"
         "( combined emission reduction + sink regeneration )",
         "#0d4f30", fs=10.5)

# Arrow hub → goal
ax.annotate("",
            xy=(GOAL_X, GOAL_Y + 0.55), xytext=(HUB_X, HUB_Y - HUB_H/2 - 0.05),
            arrowprops=dict(
                arrowstyle="-|>", color="#1a6b3c", lw=2.5,
                connectionstyle="arc3,rad=0.0",
            ),
            zorder=2)

# ── LEGEND for DPC note ───────────────────────────────────────────────────────
ax.text(0.35, 1.2,
        "Note: Direct Planetary Cooling (DPC) is a conceptual framework\n"
        "proposed as a complementary thermal intervention, not a standalone solution.\n"
        "All strategies require scientific validation.",
        ha="left", va="bottom",
        fontsize=7.2, color="#555555", style="italic",
        multialignment="left", linespacing=1.3, zorder=5)

# ── TITLE ─────────────────────────────────────────────────────────────────────
ax.text(FW / 2, 12.6,
        "Carbon Sink Regeneration Strategy Map — Conceptual Integration",
        ha="center", va="center",
        fontsize=13.5, fontweight="bold", color="#1a2535")

# ── DISCLAIMER ────────────────────────────────────────────────────────────────
ax.text(FW / 2, 0.30,
        "Conceptual diagram. Not a measured dataset or validated climate model.   "
        "•   Author: Master (inchacomisho / inchacomusho)   •   License: CC BY-SA 4.0",
        ha="center", va="center",
        fontsize=7.8, color="#888888", style="italic")

# ── SAVE ──────────────────────────────────────────────────────────────────────
plt.tight_layout()
out = os.path.join(OUT, "carbon_sink_regeneration_strategy_map.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")
