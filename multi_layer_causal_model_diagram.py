"""
multi_layer_causal_model_diagram.py
=====================================
Conceptual diagram: Multi-Layer Causal Model of Global Warming

Layers (top to bottom):
  1  Industrial CO₂ Emissions
  2  Land-Use Change and Deforestation
  3  Soil Degradation and Microbial Decline
  4  Ocean Circulation Weakening and Plankton Decline
  5  Carbon Sink Capacity Reduction
  6  Atmospheric CO₂ Accumulation
  7  Thermal Imbalance and Climate Destabilization
  8  Feedback Loops — Drought / Wildfire / Desertification / Ecosystem Collapse

A curved feedback arrow shows Layer 8 feeding back into Layers 3–5.

DISCLAIMER: Conceptual diagram. Not a measured dataset or validated climate model.

Author : Master (inchacomisho / inchacomusho)
License: CC BY-SA 4.0
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# ── figure setup ─────────────────────────────────────────────────────────────
FW, FH = 14, 14
fig, ax = plt.subplots(figsize=(FW, FH))
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis("off")
fig.patch.set_facecolor("#f0f3f6")
ax.set_facecolor("#f0f3f6")

# ── layer definitions ─────────────────────────────────────────────────────────
# Each entry: (number, label, sublabel, face-color, text-color)
LAYERS = [
    (1, "Industrial CO₂ Emissions",
        "fossil fuels  /  industry  /  energy production",
        "#c0392b", "white"),
    (2, "Land-Use Change and Deforestation",
        "forest clearing  /  monoculture  /  urban expansion",
        "#e67e22", "white"),
    (3, "Soil Degradation and Microbial Decline",
        "chemical over-use  /  tillage  /  organic matter loss",
        "#d4a017", "#2c3e50"),
    (4, "Ocean Circulation Weakening and Plankton Decline",
        "thermal stratification  /  acidification  /  dead-zone expansion",
        "#2980b9", "white"),
    (5, "Carbon Sink Capacity Reduction",
        "land sinks weakened  /  ocean sinks weakened  /  net absorption falls",
        "#8e44ad", "white"),
    (6, "Atmospheric CO₂ Accumulation",
        "emissions + reduced absorption  →  faster atmospheric buildup",
        "#6c3483", "white"),
    (7, "Thermal Imbalance and Climate Destabilization",
        "enhanced greenhouse effect  /  rising SST  /  extreme weather",
        "#e74c3c", "white"),
    (8, "Feedback Loops",
        "drought  /  wildfire  /  desertification  /  ecosystem collapse  →  further sink loss",
        "#2c3e50", "white"),
]

N        = len(LAYERS)
LEFT_X   = 1.5       # left edge of layer boxes
BOX_W    = 9.5       # width of each layer box
BOX_H    = 0.95      # height of each layer box
Y_TOP    = 12.8      # y-centre of first (top) layer
Y_STEP   = 1.35      # vertical distance between layer centres
ARR_X    = LEFT_X + BOX_W / 2   # centre x for vertical arrows

# ── draw layers ───────────────────────────────────────────────────────────────
centres_y = []
for i, (num, label, sublabel, fc, tc) in enumerate(LAYERS):
    cy = Y_TOP - i * Y_STEP
    centres_y.append(cy)

    # shadow rectangle
    shadow = FancyBboxPatch(
        (LEFT_X + 0.08, cy - BOX_H/2 - 0.08),
        BOX_W, BOX_H,
        boxstyle="round,pad=0.12",
        facecolor="#b0b0b0", edgecolor="none",
        linewidth=0, zorder=1, alpha=0.35,
    )
    ax.add_patch(shadow)

    # main rectangle
    p = FancyBboxPatch(
        (LEFT_X, cy - BOX_H/2), BOX_W, BOX_H,
        boxstyle="round,pad=0.12",
        facecolor=fc, edgecolor="#2c3e50",
        linewidth=1.4, zorder=3,
    )
    ax.add_patch(p)

    # layer badge (circle with number on the left)
    badge_x = LEFT_X + 0.55
    badge_circle = plt.Circle((badge_x, cy), 0.32,
                               color="white", zorder=5)
    ax.add_patch(badge_circle)
    ax.text(badge_x, cy, str(num),
            ha="center", va="center",
            fontsize=11, fontweight="bold",
            color=fc if tc == "white" else "#2c3e50",
            zorder=6)

    # layer title
    ax.text(LEFT_X + 1.3, cy + 0.18,
            label,
            ha="left", va="center",
            fontsize=10.5, fontweight="bold", color=tc, zorder=4)
    # sublabel
    ax.text(LEFT_X + 1.3, cy - 0.22,
            sublabel,
            ha="left", va="center",
            fontsize=8.2, color=tc, alpha=0.88, zorder=4)

# ── vertical arrows between layers ───────────────────────────────────────────
for i in range(N - 1):
    y_start = centres_y[i]     - BOX_H / 2 - 0.03
    y_end   = centres_y[i + 1] + BOX_H / 2 + 0.03
    ax.annotate("",
                xy=(ARR_X, y_end), xytext=(ARR_X, y_start),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="#444444", lw=2.2,
                    connectionstyle="arc3,rad=0",
                ),
                zorder=2)

# ── feedback arc : Layer 8 → Layers 3–5 (right margin) ───────────────────────
FB_X = LEFT_X + BOX_W + 1.3   # x-position of the right-side feedback arc

# Start: bottom of Layer 8
y8_bot  = centres_y[7] - BOX_H / 2
# Target range: centre between Layer 3 and Layer 5
y35_mid = (centres_y[2] + centres_y[4]) / 2

# Right-side bracket line
ax.plot([LEFT_X + BOX_W + 0.06, FB_X], [y8_bot, y8_bot],
        color="#e74c3c", lw=1.8, linestyle="dashed", zorder=2)
ax.plot([FB_X, FB_X], [y8_bot, y35_mid],
        color="#e74c3c", lw=1.8, linestyle="dashed", zorder=2)
ax.plot([FB_X, LEFT_X + BOX_W + 0.06], [y35_mid, y35_mid],
        color="#e74c3c", lw=1.8, linestyle="dashed", zorder=2)

# Arrow head pointing left at midpoint on the box edge
ax.annotate("",
            xy=(LEFT_X + BOX_W + 0.06, y35_mid),
            xytext=(LEFT_X + BOX_W + 0.55, y35_mid),
            arrowprops=dict(
                arrowstyle="-|>", color="#e74c3c", lw=1.8,
            ),
            zorder=2)

# Label for the feedback arc
ax.text(FB_X + 0.25, (y8_bot + y35_mid) / 2,
        "feedback\n(warming further\nweakens sinks\nin Layers 3–5)",
        ha="left", va="center",
        fontsize=7.8, color="#c0392b", style="italic",
        rotation=0, zorder=5)

# ── title ─────────────────────────────────────────────────────────────────────
ax.text(FW / 2, 13.65,
        "Multi-Layer Causal Model of Global Warming — Conceptual Diagram",
        ha="center", va="center",
        fontsize=13.5, fontweight="bold", color="#1a2535")

# ── disclaimer ────────────────────────────────────────────────────────────────
ax.text(FW / 2, 0.35,
        "Conceptual diagram. Not a measured dataset or validated climate model.   "
        "•   Author: Master (inchacomisho / inchacomusho)   •   License: CC BY-SA 4.0",
        ha="center", va="center",
        fontsize=7.8, color="#888888", style="italic")

# ── save ──────────────────────────────────────────────────────────────────────
plt.tight_layout()
out = os.path.join(OUT, "multi_layer_causal_model_diagram.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")
