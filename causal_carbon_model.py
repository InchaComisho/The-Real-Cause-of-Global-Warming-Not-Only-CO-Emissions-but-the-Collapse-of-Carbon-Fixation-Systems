"""
causal_carbon_model.py
======================
Basic CO₂ Balance Model — Conceptual Framework

Implements two contrasting models of atmospheric CO₂ accumulation:

  Model A — StandardModel (conventional framing):
      ΔCO₂(t) = emissions(t)

  Model B — CausalCarbonModel (this repository's multi-cause framing):
      ΔCO₂(t) = emissions(t)
              − land_fixation_capacity(t)
              − ocean_uptake_capacity(t)
              + ecosystem_degradation_release(t)

The purpose is to show that when fixation systems decline and degradation
releases stored carbon, atmospheric CO₂ accumulates faster than emission
rates alone would predict.

⚠️  IMPORTANT LIMITATIONS
    All parameter values are HYPOTHETICAL, normalized to [0.0, 1.0].
    None of these values have been calibrated against real observational data.
    This model is for CONCEPTUAL ILLUSTRATION ONLY.
    See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Clus, Real, Lora
Published: May 2026
License: CC BY-SA 4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────────
# 1. Parameters
# ─────────────────────────────────────────────────────────────────

@dataclass
class CarbonBalanceParameters:
    """
    All values are normalized [0.0, 1.0] and are HYPOTHETICAL.
    They require calibration against real data before any predictive use.
    """

    # Simulation duration (years)
    duration_years: int = 100

    # --- Emission trajectory ---
    # HYPOTHETICAL: normalized emission rate at start (t=0)
    emission_start: float = 0.10
    # HYPOTHETICAL: normalized emission rate at end (t=duration)
    emission_end: float = 0.65
    # Growth shape: 'linear' or 'accelerating'
    emission_growth: str = "accelerating"

    # --- Land fixation ---
    # HYPOTHETICAL: initial land fixation capacity (pristine = 1.0)
    land_fixation_initial: float = 0.90
    # HYPOTHETICAL: rate of annual decline in land fixation capacity
    # (represents combined effect of deforestation, soil degradation, etc.)
    land_fixation_decline_rate: float = 0.003  # per year

    # --- Ocean uptake ---
    # HYPOTHETICAL: initial ocean CO₂ uptake capacity
    ocean_uptake_initial: float = 0.85
    # HYPOTHETICAL: ocean uptake decline rate (slower than land; accelerates later)
    ocean_uptake_decline_rate: float = 0.001  # per year

    # --- Ecosystem degradation release ---
    # HYPOTHETICAL: base carbon release rate from degrading ecosystems
    # (permafrost thaw, wetland drainage, soil carbon loss)
    degradation_release_base: float = 0.02
    # HYPOTHETICAL: rate at which degradation release grows over time
    degradation_release_growth: float = 0.002  # per year

    # --- CO₂ index scaling ---
    # HYPOTHETICAL: weighting factor for land fixation in CO₂ balance
    land_fixation_weight: float = 0.45
    # HYPOTHETICAL: weighting factor for ocean uptake in CO₂ balance
    ocean_uptake_weight: float = 0.35
    # HYPOTHETICAL: weighting factor for degradation release
    degradation_weight: float = 0.20


# ─────────────────────────────────────────────────────────────────
# 2. Model A: Standard (Emissions-Only) Model
# ─────────────────────────────────────────────────────────────────

class StandardModel:
    """
    Conventional single-cause model.
    Atmospheric CO₂ is treated as driven entirely by emission rates.
    Natural sinks are assumed constant (a simplification).
    """

    def __init__(self, params: CarbonBalanceParameters):
        self.p = params

    def _emission_at(self, t: int) -> float:
        """
        HYPOTHETICAL emission trajectory.
        'accelerating' uses a quadratic ramp; 'linear' is linear.
        """
        frac = t / self.p.duration_years
        if self.p.emission_growth == "accelerating":
            return self.p.emission_start + (self.p.emission_end - self.p.emission_start) * frac ** 1.5
        return self.p.emission_start + (self.p.emission_end - self.p.emission_start) * frac

    def run(self) -> Tuple[np.ndarray, np.ndarray]:
        years = np.arange(self.p.duration_years)
        co2_index = np.zeros(self.p.duration_years)
        for t in range(1, self.p.duration_years):
            # Standard model: CO₂ grows proportionally to emission rate only
            co2_index[t] = co2_index[t - 1] + self._emission_at(t)
        # Normalize to [0, 1] for comparison
        co2_index /= (co2_index[-1] + 1e-9)
        return years, co2_index


# ─────────────────────────────────────────────────────────────────
# 3. Model B: Full Causal Carbon Model
# ─────────────────────────────────────────────────────────────────

class CausalCarbonModel:
    """
    Multi-cause model including fixation system decline.

    ΔCO₂(t) = emissions(t)
             − land_fixation_weight × land_fixation(t)
             − ocean_uptake_weight  × ocean_uptake(t)
             + degradation_weight   × degradation_release(t)

    All fixation and uptake values are HYPOTHETICAL, normalized [0, 1].
    """

    def __init__(self, params: CarbonBalanceParameters):
        self.p = params

    def _emission_at(self, t: int) -> float:
        frac = t / self.p.duration_years
        if self.p.emission_growth == "accelerating":
            return self.p.emission_start + (self.p.emission_end - self.p.emission_start) * frac ** 1.5
        return self.p.emission_start + (self.p.emission_end - self.p.emission_start) * frac

    def run(self) -> Tuple[np.ndarray, np.ndarray, dict]:
        """
        Returns:
            years       : np.ndarray of year indices
            co2_index   : normalized CO₂ accumulation index
            components  : dict of component trajectories for inspection
        """
        T = self.p.duration_years
        years = np.arange(T)

        land_fixation     = np.zeros(T)
        ocean_uptake      = np.zeros(T)
        degradation_rel   = np.zeros(T)
        co2_raw           = np.zeros(T)

        # Initialize
        land_fixation[0]   = self.p.land_fixation_initial
        ocean_uptake[0]    = self.p.ocean_uptake_initial
        degradation_rel[0] = self.p.degradation_release_base

        for t in range(1, T):
            # --- Update fixation and uptake capacities ---
            # HYPOTHETICAL decline rates
            land_fixation[t] = max(0.0,
                land_fixation[t - 1] - self.p.land_fixation_decline_rate)

            ocean_uptake[t] = max(0.0,
                ocean_uptake[t - 1] - self.p.ocean_uptake_decline_rate)

            degradation_rel[t] = min(1.0,
                degradation_rel[t - 1] + self.p.degradation_release_growth)

            # --- CO₂ balance equation ---
            # HYPOTHETICAL: net annual CO₂ accumulation index
            emission      = self._emission_at(t)
            land_removal  = self.p.land_fixation_weight  * land_fixation[t]
            ocean_removal = self.p.ocean_uptake_weight   * ocean_uptake[t]
            degrad_input  = self.p.degradation_weight    * degradation_rel[t]

            delta_co2 = emission - land_removal - ocean_removal + degrad_input
            co2_raw[t] = co2_raw[t - 1] + max(0.0, delta_co2)

        # Normalize to [0, 1]
        scale = co2_raw[-1] + 1e-9
        co2_index = co2_raw / scale

        components = {
            "land_fixation":   land_fixation,
            "ocean_uptake":    ocean_uptake,
            "degradation_rel": degradation_rel,
        }
        return years, co2_index, components


# ─────────────────────────────────────────────────────────────────
# 4. Visualization
# ─────────────────────────────────────────────────────────────────

def plot_model_comparison(
    years_a: np.ndarray,
    co2_a:   np.ndarray,
    years_b: np.ndarray,
    co2_b:   np.ndarray,
    components: dict,
) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(11, 8))
    fig.suptitle(
        "Causal Carbon Balance Model\n"
        "⚠ HYPOTHETICAL CONCEPTUAL VALUES — Not calibrated against real data",
        fontsize=12, fontweight="bold", color="#8B0000",
    )

    # Panel 1: CO₂ index comparison
    ax1 = axes[0]
    ax1.plot(years_a, co2_a, "--", color="#666666", linewidth=2,
             label="Model A: Emissions-only (standard framing)")
    ax1.plot(years_b, co2_b, "-",  color="#C0392B", linewidth=2.5,
             label="Model B: Full causal (emissions + fixation decline + degradation)")
    ax1.fill_between(years_b, co2_a, co2_b,
                     where=(co2_b >= co2_a), alpha=0.15, color="#C0392B",
                     label="Additional CO₂ from fixation collapse")
    ax1.set_ylabel("Normalized CO₂ Index [0–1]")
    ax1.set_title("Atmospheric CO₂ Accumulation: Standard vs. Causal Model")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)
    ax1.set_ylim(0, 1.1)

    # Panel 2: Component trajectories
    ax2 = axes[1]
    ax2.plot(years_b, components["land_fixation"],
             color="#27AE60", linewidth=2, label="Land fixation capacity")
    ax2.plot(years_b, components["ocean_uptake"],
             color="#2980B9", linewidth=2, label="Ocean uptake capacity")
    ax2.plot(years_b, components["degradation_rel"],
             color="#E67E22", linewidth=2, label="Ecosystem degradation release")
    ax2.set_xlabel("Years (relative, t=0 = baseline)")
    ax2.set_ylabel("Normalized Capacity / Rate [0–1]")
    ax2.set_title("Carbon System Component Trajectories (HYPOTHETICAL)")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, 1.1)

    plt.tight_layout()
    plt.savefig("causal_carbon_model_output.png", dpi=150, bbox_inches="tight")
    print("  → Saved: causal_carbon_model_output.png")
    plt.show()


# ─────────────────────────────────────────────────────────────────
# 5. Main
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("  Causal Carbon Balance Model")
    print("  ⚠ HYPOTHETICAL CONCEPTUAL MODEL — See MODEL_LIMITATIONS.md")
    print("=" * 70)

    params = CarbonBalanceParameters()

    # Run Model A (standard)
    model_a = StandardModel(params)
    years_a, co2_a = model_a.run()

    # Run Model B (full causal)
    model_b = CausalCarbonModel(params)
    years_b, co2_b, components = model_b.run()

    # Print summary
    print(f"\n  Model A (emissions-only) final CO₂ index : {co2_a[-1]:.4f}")
    print(f"  Model B (full causal)    final CO₂ index : {co2_b[-1]:.4f}")
    print(f"  Land fixation at end     : {components['land_fixation'][-1]:.4f}")
    print(f"  Ocean uptake at end      : {components['ocean_uptake'][-1]:.4f}")
    print(f"  Degradation release end  : {components['degradation_rel'][-1]:.4f}")
    print(
        "\n  Model B produces higher CO₂ accumulation because:\n"
        "  (1) Land fixation capacity declines over time.\n"
        "  (2) Ocean uptake capacity declines over time.\n"
        "  (3) Ecosystem degradation releases stored carbon.\n"
        "  These effects compound with emissions.\n"
    )
    print("  ⚠ All values above are HYPOTHETICAL. See MODEL_LIMITATIONS.md.")
    print("=" * 70)

    plot_model_comparison(years_a, co2_a, years_b, co2_b, components)


if __name__ == "__main__":
    main()
