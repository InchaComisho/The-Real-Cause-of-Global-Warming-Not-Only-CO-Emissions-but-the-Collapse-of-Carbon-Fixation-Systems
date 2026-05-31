"""
carbon_sink_collapse_diagram.py
================================
Conceptual causal diagram: Carbon Sink Collapse Framework

Nodes:
  CO2 Emissions | Forests | Soils | Oceans | Plankton | Microbial Ecosystems
  → Weakened Carbon Sinks → Reduced Absorption Capacity
  → Atmospheric CO2 Accumulation → Warming / Thermal Imbalance
  → Feedback Loop

DISCLAIMER: Conceptual diagram. Not a measured dataset or validated climate model.

Author : Master (inchacomisho / inchacomusho)
License: CC BY-SA 4.0
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# ── figure setup ─────────────────────────────────────────────────────────────
FW, FH = 15, 12
fig, ax = plt.subplots(figsize=(FW, FH))
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis("off")
fig.patch.set_facecolor("#f0f3f6")
ax.set_facecolor("#f0f3f6")

# ── colour palette ────────────────────────────────────────────────────────────
C = dict(
    emission="#c0392b",
    forest  ="#27ae60",
    soil    ="#8B5E3C",
    ocean   ="#2980b9",
    plankton="#16a085",
    microbe ="#6c3483",
    weakened="#7f8c8d",
    reduced ="#d35400",
    atm_co2 ="#8e44ad",
    warming ="#e74c3c",
    feedback="#2c3e50",
    arrow_dk="#444444",
)

# ── helpers ───────────────────────────────────────────────────────────────────
def box(cx, cy, w, h, text, fc, tc="white", fs=9.5, lh=1.35):
    p = FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.15",
        facecolor=fc, edgecolor="#2c3e50",
        linewidth=1.4, zorder=3,
    )
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fs, fontweight="bold", color=tc, zorder=4,
            multialignment="center", linespacing=lh)

def mini_box(cx, cy, w, h, text, fc, fs=8.2):
    p = FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.10",
        facecolor=fc, edgecolor="#ffffff",
        linewidth=1.0, zorder=5,
    )
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fs, fontweight="bold", color="white", zorder=6,
            multialignment="center", linespacing=1.25)

def arr(x1, y1, x2, y2, col, lw=2.0, rad=0.0, ls="solid"):
    ax.annotate("",
                xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=col, lw=lw,
                    connectionstyle=f"arc3,rad={rad}",
                    linestyle=ls,
                ),
                zorder=2)

# ─── TITLE ────────────────────────────────────────────────────────────────────
ax.text(7.5, 11.55,
        "Carbon Sink Collapse Framework — Conceptual Causal Diagram",
        ha="center", va="center",
        fontsize=14, fontweight="bold", color="#1a2535")

# ─── LEFT COLUMN : CO2 EMISSIONS ─────────────────────────────────────────────
box(3.2, 10.3, 5.2, 0.85,
    "CO₂ Emissions\n(fossil fuels  /  land-use change  /  industry)",
    C["emission"], fs=9.2)

# ─── RIGHT CLUSTER : NATURAL CARBON SINK CONTAINER ───────────────────────────
# Outer container
cont = FancyBboxPatch(
    (7.1, 9.2), 7.6, 2.0,
    boxstyle="round,pad=0.18",
    facecolor="#ecf0f1", edgecolor="#95a5a6",
    linewidth=1.4, zorder=2,
)
ax.add_patch(cont)
ax.text(10.9, 11.1, "Natural Carbon Sinks",
        ha="center", va="center",
        fontsize=9.8, fontweight="bold", color="#2c3e50", zorder=3)

# Five individual component mini-boxes inside the container
mini_box(8.2,  10.4, 1.6, 0.60, "Forests",    C["forest"])
mini_box(9.9,  10.4, 1.6, 0.60, "Soils",      C["soil"])
mini_box(11.6, 10.4, 1.6, 0.60, "Oceans",     C["ocean"])
mini_box(9.05, 9.55, 1.7, 0.60, "Plankton",   C["plankton"])
mini_box(11.25,9.55, 2.1, 0.60, "Microbial\nEcosystems", C["microbe"])

# Arrow from container bottom to Weakened Carbon Sinks
arr(10.9, 9.2, 10.9, 8.35, C["weakened"], lw=2.0)

# ─── WEAKENED CARBON SINKS ───────────────────────────────────────────────────
box(10.9, 7.9, 5.6, 0.80,
    "Weakened Carbon Sinks\n(degraded  /  fragmented  /  over-stressed)",
    C["weakened"], fs=9.0)

arr(10.9, 7.50, 10.9, 6.95, C["reduced"], lw=2.0)

# ─── REDUCED ABSORPTION CAPACITY ─────────────────────────────────────────────
box(10.9, 6.50, 5.6, 0.80,
    "Reduced Absorption Capacity\n(less CO₂ absorbed per year)",
    C["reduced"], fs=9.0)

# ─── ATMOSPHERIC CO2 ACCUMULATION ────────────────────────────────────────────
# Wide central box
box(7.3, 5.0, 11.8, 0.90,
    "Atmospheric CO₂ Accumulation\n"
    "( emissions  +  reduced absorption  →  faster atmospheric buildup )",
    C["atm_co2"], fs=9.8)

# Arrow: CO2 Emissions (left column) → Atmospheric CO2
arr(3.2, 9.875, 3.2, 5.45, C["emission"], lw=2.3, rad=0.0)

# Arrow: Reduced Absorption → Atmospheric CO2 (right side, diagonal)
arr(10.9, 6.10, 10.9, 5.45, C["reduced"], lw=2.0)

# ─── WARMING / THERMAL IMBALANCE ─────────────────────────────────────────────
box(7.3, 3.5, 11.0, 0.85,
    "Warming / Thermal Imbalance\n"
    "(enhanced greenhouse effect  →  global temperature rise / heat accumulation)",
    C["warming"], fs=9.8)

arr(7.3, 4.55, 7.3, 3.925, C["atm_co2"], lw=2.5)

# ─── FEEDBACK LOOP ───────────────────────────────────────────────────────────
box(7.3, 2.05, 11.5, 0.80,
    "Feedback Loop:  drought  /  wildfire  /  desertification  /  ecosystem collapse\n"
    "→  further weakening of carbon sinks",
    C["feedback"], fs=9.0)

arr(7.3, 3.075, 7.3, 2.45, C["warming"], lw=2.0)

# Dashed feedback arc on right margin: Feedback → Weakened Carbon Sinks
ax.annotate("",
            xy=(13.5, 7.9), xytext=(13.5, 1.65),
            arrowprops=dict(
                arrowstyle="-|>", color=C["warming"], lw=1.8,
                linestyle="dashed",
                connectionstyle="arc3,rad=0.0",
            ),
            zorder=2)
ax.text(14.35, 5.0, "feedback\n(warming\nfurther\nweakens\nsinks)",
        ha="center", va="center",
        fontsize=7.8, color=C["warming"], style="italic", zorder=5)

# connecting lines from feedback right-edge to right-margin arrow
ax.plot([13.05, 13.5], [2.05, 2.05], color=C["warming"],
        lw=1.6, linestyle="dashed", zorder=2)
ax.plot([13.05, 13.5], [7.9,  7.9 ], color=C["warming"],
        lw=1.6, linestyle="dashed", zorder=2)

# ─── DISCLAIMER ──────────────────────────────────────────────────────────────
ax.text(7.5, 0.35,
        "Conceptual diagram. Not a measured dataset or validated climate model.   "
        "•   Author: Master (inchacomisho / inchacomusho)   •   License: CC BY-SA 4.0",
        ha="center", va="center",
        fontsize=7.8, color="#888888", style="italic")

# ─── SAVE ────────────────────────────────────────────────────────────────────
plt.tight_layout()
out = os.path.join(OUT, "carbon_sink_collapse_diagram.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")
