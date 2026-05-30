"""
feedback_loop_simulation.py
============================
Positive Feedback Loop Simulation — Forest, Soil, and Ocean

This module simulates three positive (self-amplifying) feedback loops
between global warming and carbon fixation system degradation.

Positive feedback loops are cycles in which an initial disturbance
causes a response that amplifies the original disturbance, rather than
correcting it.

The three loops modeled here:

  Loop 1 — Forest Feedback:
    Warming → drought/heat stress → forest dieback
    → reduced terrestrial fixation
    → CO₂ accumulation → more warming
    [Example: Amazon dieback under sustained drought]

  Loop 2 — Soil Feedback:
    Warming → accelerated soil microbial respiration
    → net soil carbon loss
    → CO₂ release → more warming
    [Example: permafrost thaw, tropical soil carbon release]

  Loop 3 — Ocean Feedback:
    Warming → ocean stratification
    → phytoplankton nutrient limitation
    → weakened biological carbon pump
    → CO₂ accumulation → more warming

A combined simulation shows how these loops interact and amplify each other.

⚠️  IMPORTANT LIMITATIONS
    All coupling coefficients, gain parameters, and thresholds are HYPOTHETICAL.
    This is a conceptual illustration, not a calibrated prediction model.
    Real-world feedback dynamics are nonlinear, regionally variable,
    and involve timescales not captured here.
    See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Cruz, Real, Lola
Published: May 2026
License: CC BY-SA 4.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────────
# 1. Parameters (all HYPOTHETICAL)
# ─────────────────────────────────────────────────────────────────

@dataclass
class FeedbackParameters:
    """
    All values are HYPOTHETICAL, normalized, and require calibration.
    """
    timesteps: int = 200

    # --- Initial conditions ---
    # HYPOTHETICAL: starting warming anomaly (relative, normalized)
    initial_warming: float = 0.10
    # HYPOTHETICAL: starting CO2 index
    initial_co2: float = 0.15
    # HYPOTHETICAL: starting forest health
    initial_forest: float = 0.82
    # HYPOTHETICAL: starting soil carbon stock
    initial_soil_carbon: float = 0.80
    # HYPOTHETICAL: starting ocean stratification (0 = none, 1 = maximum)
    initial_stratification: float = 0.10
    # HYPOTHETICAL: starting phytoplankton biomass
    initial_phytoplankton: float = 0.85

    # --- Loop 1: Forest Feedback coupling strengths (HYPOTHETICAL) ---
    # How much warming drives forest stress
    warming_to_forest_stress: float = 0.30
    # How much forest loss reduces fixation
    forest_loss_to_co2: float = 0.25
    # CO2 warming feedback gain
    co2_to_warming: float = 0.18

    # --- Loop 2: Soil Feedback coupling strengths (HYPOTHETICAL) ---
    # How much warming accelerates soil respiration
    warming_to_soil_resp: float = 0.25
    # How much soil carbon loss contributes to CO2
    soil_loss_to_co2: float = 0.20
    # Respiration rate increase per unit warming
    resp_acceleration: float = 0.015

    # --- Loop 3: Ocean Feedback coupling strengths (HYPOTHETICAL) ---
    # How much warming increases stratification
    warming_to_stratification: float = 0.20
    # How much stratification reduces phytoplankton
    strat_to_phyto_loss: float = 0.30
    # How much phytoplankton loss reduces ocean CO2 uptake
    phyto_to_ocean_co2: float = 0.22

    # --- Global CO2-to-warming sensitivity (HYPOTHETICAL) ---
    global_co2_warming_sensitivity: float = 0.15

    # --- Stabilizing resistance (HYPOTHETICAL) ---
    # Natural damping / inertia in each system
    forest_resilience:     float = 0.05   # forest recovery rate if stress removed
    soil_stabilization:    float = 0.02   # passive soil carbon stabilization
    ocean_mixing:          float = 0.03   # natural ocean mixing against stratification


# ─────────────────────────────────────────────────────────────────
# 2. Individual Loop Simulators
# ─────────────────────────────────────────────────────────────────

class ForestFeedbackLoop:
    """
    Loop 1: Warming → Forest Stress → Fixation Loss → CO₂ → Warming
    HYPOTHETICAL coupling. Not a validated forest model.
    """

    def __init__(self, params: FeedbackParameters):
        self.p = params

    def simulate(self) -> Dict[str, np.ndarray]:
        T  = self.p.timesteps
        warming      = np.zeros(T)
        forest_health= np.zeros(T)
        co2_index    = np.zeros(T)

        warming[0]      = self.p.initial_warming
        forest_health[0]= self.p.initial_forest
        co2_index[0]    = self.p.initial_co2

        for t in range(1, T):
            # Warming drives forest stress
            forest_stress = self.p.warming_to_forest_stress * warming[t - 1]
            # Forest recovers partially (resilience)
            forest_recovery = self.p.forest_resilience * (1.0 - forest_health[t - 1])
            forest_health[t] = max(0.0, min(1.0,
                forest_health[t - 1] - forest_stress * 0.01 + forest_recovery * 0.005))

            # Forest loss contributes to CO2
            forest_co2_input = self.p.forest_loss_to_co2 * (self.p.initial_forest - forest_health[t])
            co2_index[t] = min(1.0,
                co2_index[t - 1] + forest_co2_input * 0.008)

            # CO2 drives further warming
            warming[t] = min(1.0,
                warming[t - 1] + self.p.co2_to_warming * co2_index[t] * 0.005)

        return {"warming": warming, "forest_health": forest_health, "co2_index": co2_index}


class SoilFeedbackLoop:
    """
    Loop 2: Warming → Soil Respiration → Soil Carbon Loss → CO₂ → Warming
    HYPOTHETICAL coupling. Not a validated soil carbon model.
    """

    def __init__(self, params: FeedbackParameters):
        self.p = params

    def simulate(self) -> Dict[str, np.ndarray]:
        T  = self.p.timesteps
        warming       = np.zeros(T)
        soil_carbon   = np.zeros(T)
        respiration   = np.zeros(T)
        co2_index     = np.zeros(T)

        warming[0]     = self.p.initial_warming
        soil_carbon[0] = self.p.initial_soil_carbon
        respiration[0] = 0.05   # HYPOTHETICAL: baseline respiration rate
        co2_index[0]   = self.p.initial_co2

        for t in range(1, T):
            # Warming accelerates microbial respiration
            resp_increase = self.p.warming_to_soil_resp * warming[t - 1] * self.p.resp_acceleration
            respiration[t] = min(1.0, respiration[t - 1] + resp_increase)

            # Respiration depletes soil carbon stock
            soil_loss = respiration[t] * 0.008
            soil_stabilization = self.p.soil_stabilization * soil_carbon[t - 1] * 0.003
            soil_carbon[t] = max(0.0,
                soil_carbon[t - 1] - soil_loss + soil_stabilization)

            # Soil carbon loss releases CO2
            carbon_released = self.p.soil_loss_to_co2 * max(0.0, soil_carbon[t - 1] - soil_carbon[t])
            co2_index[t] = min(1.0,
                co2_index[t - 1] + carbon_released * 0.015)

            # CO2 drives further warming
            warming[t] = min(1.0,
                warming[t - 1] + self.p.global_co2_warming_sensitivity * co2_index[t] * 0.004)

        return {
            "warming": warming,
            "soil_carbon": soil_carbon,
            "respiration": respiration,
            "co2_index": co2_index,
        }


class OceanFeedbackLoop:
    """
    Loop 3: Warming → Stratification → Phytoplankton Loss → Biological Pump Weakens → CO₂ → Warming
    HYPOTHETICAL coupling. Not a validated ocean carbon model.
    """

    def __init__(self, params: FeedbackParameters):
        self.p = params

    def simulate(self) -> Dict[str, np.ndarray]:
        T  = self.p.timesteps
        warming          = np.zeros(T)
        stratification   = np.zeros(T)
        phytoplankton    = np.zeros(T)
        bio_pump         = np.zeros(T)
        co2_index        = np.zeros(T)

        warming[0]       = self.p.initial_warming
        stratification[0]= self.p.initial_stratification
        phytoplankton[0] = self.p.initial_phytoplankton
        bio_pump[0]      = phytoplankton[0] * 0.90
        co2_index[0]     = self.p.initial_co2

        for t in range(1, T):
            # Warming increases stratification
            strat_increase = self.p.warming_to_stratification * warming[t - 1] * 0.008
            ocean_mix = self.p.ocean_mixing * 0.003
            stratification[t] = max(0.0, min(1.0,
                stratification[t - 1] + strat_increase - ocean_mix))

            # Stratification reduces phytoplankton (nutrient limitation)
            phyto_loss = self.p.strat_to_phyto_loss * stratification[t] * 0.006
            phytoplankton[t] = max(0.0, min(1.0,
                phytoplankton[t - 1] - phyto_loss))

            # Phytoplankton drives biological pump efficiency
            bio_pump[t] = phytoplankton[t] * 0.85

            # Weakened biological pump reduces ocean CO2 removal
            pump_loss = self.p.phyto_to_ocean_co2 * max(0.0, self.p.initial_phytoplankton - phytoplankton[t])
            co2_index[t] = min(1.0,
                co2_index[t - 1] + pump_loss * 0.010)

            # CO2 drives further warming
            warming[t] = min(1.0,
                warming[t - 1] + self.p.global_co2_warming_sensitivity * co2_index[t] * 0.004)

        return {
            "warming": warming,
            "stratification": stratification,
            "phytoplankton": phytoplankton,
            "bio_pump": bio_pump,
            "co2_index": co2_index,
        }


# ─────────────────────────────────────────────────────────────────
# 3. Combined Feedback Simulation
# ─────────────────────────────────────────────────────────────────

class CombinedFeedbackSimulation:
    """
    Runs all three feedback loops simultaneously, with shared
    warming and CO₂ state variables coupling them together.

    HYPOTHETICAL: the coupling between loops is a simplified
    linear summation. Real interactions are more complex.
    """

    def __init__(self, params: FeedbackParameters):
        self.p = params

    def simulate(self) -> Dict[str, np.ndarray]:
        T = self.p.timesteps
        warming        = np.zeros(T)
        co2_index      = np.zeros(T)
        forest_health  = np.zeros(T)
        soil_carbon    = np.zeros(T)
        phytoplankton  = np.zeros(T)
        stratification = np.zeros(T)

        warming[0]        = self.p.initial_warming
        co2_index[0]      = self.p.initial_co2
        forest_health[0]  = self.p.initial_forest
        soil_carbon[0]    = self.p.initial_soil_carbon
        phytoplankton[0]  = self.p.initial_phytoplankton
        stratification[0] = self.p.initial_stratification

        for t in range(1, T):
            w  = warming[t - 1]
            c  = co2_index[t - 1]

            # ── Forest loop ──
            fh = forest_health[t - 1]
            forest_stress    = self.p.warming_to_forest_stress * w * 0.010
            forest_recovery  = self.p.forest_resilience * (1.0 - fh) * 0.005
            forest_health[t] = max(0.0, min(1.0, fh - forest_stress + forest_recovery))
            forest_co2_delta = self.p.forest_loss_to_co2 * max(0.0, self.p.initial_forest - forest_health[t]) * 0.008

            # ── Soil loop ──
            sc = soil_carbon[t - 1]
            resp_rate       = 0.05 + self.p.warming_to_soil_resp * w * self.p.resp_acceleration
            soil_loss       = resp_rate * 0.007
            soil_stab       = self.p.soil_stabilization * sc * 0.003
            soil_carbon[t]  = max(0.0, min(1.0, sc - soil_loss + soil_stab))
            soil_co2_delta  = self.p.soil_loss_to_co2 * max(0.0, sc - soil_carbon[t]) * 0.015

            # ── Ocean loop ──
            st  = stratification[t - 1]
            phy = phytoplankton[t - 1]
            strat_increase      = self.p.warming_to_stratification * w * 0.008
            stratification[t]   = max(0.0, min(1.0, st + strat_increase - self.p.ocean_mixing * 0.003))
            phyto_loss          = self.p.strat_to_phyto_loss * stratification[t] * 0.005
            phytoplankton[t]    = max(0.0, min(1.0, phy - phyto_loss))
            ocean_co2_delta     = self.p.phyto_to_ocean_co2 * max(0.0, self.p.initial_phytoplankton - phytoplankton[t]) * 0.010

            # ── Combined CO₂ and warming update ──
            total_co2_delta = forest_co2_delta + soil_co2_delta + ocean_co2_delta
            co2_index[t] = min(1.0, c + total_co2_delta)
            warming[t]   = min(1.0, w + self.p.global_co2_warming_sensitivity * co2_index[t] * 0.006)

        return {
            "warming":       warming,
            "co2_index":     co2_index,
            "forest_health": forest_health,
            "soil_carbon":   soil_carbon,
            "phytoplankton": phytoplankton,
            "stratification":stratification,
        }


# ─────────────────────────────────────────────────────────────────
# 4. Visualization
# ─────────────────────────────────────────────────────────────────

def plot_feedback_results(
    forest_data: dict,
    soil_data:   dict,
    ocean_data:  dict,
    combined:    dict,
) -> None:
    T = len(combined["warming"])
    t = np.arange(T)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(
        "Positive Feedback Loop Simulation: Forest · Soil · Ocean\n"
        "⚠ HYPOTHETICAL CONCEPTUAL VALUES — Not calibrated against real data",
        fontsize=11, fontweight="bold", color="#8B0000",
    )

    # Panel 1: Forest Feedback
    ax = axes[0, 0]
    ax.plot(t, forest_data["warming"],      color="#C0392B", label="Warming index")
    ax.plot(t, forest_data["forest_health"],color="#27AE60", label="Forest health")
    ax.plot(t, forest_data["co2_index"],    color="#7F8C8D", linestyle="--", label="CO₂ index")
    ax.set_title("Loop 1: Forest Feedback\n(Warming → Dieback → CO₂ → Warming)", fontsize=9)
    ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_ylim(0, 1.05)

    # Panel 2: Soil Feedback
    ax = axes[0, 1]
    ax.plot(t, soil_data["warming"],     color="#C0392B", label="Warming index")
    ax.plot(t, soil_data["soil_carbon"], color="#8B4513", label="Soil carbon stock")
    ax.plot(t, soil_data["respiration"], color="#E67E22", linestyle="--", label="Respiration rate")
    ax.plot(t, soil_data["co2_index"],   color="#7F8C8D", linestyle=":", label="CO₂ index")
    ax.set_title("Loop 2: Soil Feedback\n(Warming → Respiration → Soil Loss → CO₂)", fontsize=9)
    ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_ylim(0, 1.05)

    # Panel 3: Ocean Feedback
    ax = axes[1, 0]
    ax.plot(t, ocean_data["warming"],        color="#C0392B", label="Warming index")
    ax.plot(t, ocean_data["phytoplankton"],  color="#2980B9", label="Phytoplankton biomass")
    ax.plot(t, ocean_data["stratification"], color="#1ABC9C", linestyle="--", label="Stratification")
    ax.plot(t, ocean_data["bio_pump"],       color="#2471A3", linestyle=":", label="Bio pump efficiency")
    ax.plot(t, ocean_data["co2_index"],      color="#7F8C8D", linestyle="-.", label="CO₂ index")
    ax.set_title("Loop 3: Ocean Feedback\n(Warming → Stratification → Phyto Loss → CO₂)", fontsize=9)
    ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_ylim(0, 1.05)

    # Panel 4: Combined
    ax = axes[1, 1]
    ax.plot(t, combined["warming"],       color="#C0392B", linewidth=2,   label="Combined warming")
    ax.plot(t, combined["co2_index"],     color="#7F8C8D", linewidth=2,   linestyle="--", label="Combined CO₂ index")
    ax.plot(t, combined["forest_health"], color="#27AE60", linewidth=1.5, label="Forest health")
    ax.plot(t, combined["soil_carbon"],   color="#8B4513", linewidth=1.5, label="Soil carbon")
    ax.plot(t, combined["phytoplankton"], color="#2980B9", linewidth=1.5, label="Phytoplankton")
    ax.set_title("Combined: All Three Loops Active Simultaneously", fontsize=9)
    ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_ylim(0, 1.05)

    for ax in axes.flat:
        ax.set_xlabel("Timestep (relative)")
        ax.set_ylabel("Normalized value [0–1]")

    plt.tight_layout()
    plt.savefig("feedback_loop_simulation_output.png", dpi=150, bbox_inches="tight")
    print("  → Saved: feedback_loop_simulation_output.png")
    plt.show()


# ─────────────────────────────────────────────────────────────────
# 5. Main
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("  Positive Feedback Loop Simulation")
    print("  Forest · Soil · Ocean positive feedback loops")
    print("  ⚠ HYPOTHETICAL CONCEPTUAL MODEL — See MODEL_LIMITATIONS.md")
    print("=" * 70)

    params = FeedbackParameters()

    loop1 = ForestFeedbackLoop(params).simulate()
    loop2 = SoilFeedbackLoop(params).simulate()
    loop3 = OceanFeedbackLoop(params).simulate()
    comb  = CombinedFeedbackSimulation(params).simulate()

    T = params.timesteps
    print(f"\n  At timestep {T - 1} (end of simulation):")
    print(f"  Loop 1 (Forest) — Warming: {loop1['warming'][-1]:.3f}  CO₂: {loop1['co2_index'][-1]:.3f}  "
          f"Forest health: {loop1['forest_health'][-1]:.3f}")
    print(f"  Loop 2 (Soil)   — Warming: {loop2['warming'][-1]:.3f}  CO₂: {loop2['co2_index'][-1]:.3f}  "
          f"Soil carbon:   {loop2['soil_carbon'][-1]:.3f}")
    print(f"  Loop 3 (Ocean)  — Warming: {loop3['warming'][-1]:.3f}  CO₂: {loop3['co2_index'][-1]:.3f}  "
          f"Phytoplankton: {loop3['phytoplankton'][-1]:.3f}")
    print(f"  Combined        — Warming: {comb['warming'][-1]:.3f}  CO₂: {comb['co2_index'][-1]:.3f}")
    print("\n  ⚠ All values above are HYPOTHETICAL. See MODEL_LIMITATIONS.md.")
    print("=" * 70)

    plot_feedback_results(loop1, loop2, loop3, comb)


if __name__ == "__main__":
    main()
