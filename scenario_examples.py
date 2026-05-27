"""
scenario_examples.py
=====================
Scenario Comparison — Five Climate Intervention Strategies

Starting from the 2025 state estimated by the historical_phase_model,
this module projects 75 years forward under five intervention scenarios:

  Scenario 1 — Business as Usual:
      No significant intervention. Emissions continue to grow.
      Carbon fixation systems continue to degrade.

  Scenario 2a — Announced Decarbonization Only:
      Policy targets met globally. Global emissions decline aggressively
      (~net zero by ~2050). Optimistic assumption.
      No active restoration of carbon fixation systems.
      Fixation systems continue to decline passively.

  Scenario 2b — Realistic Global Decarbonization Only:
      Developed-country emission cuts are partially offset by:
        - developing-country industrialization and energy demand growth
        - population-driven demand growth
      Net global emissions decline only slowly.
      Carbon sinks remain degraded. Degradation release continues.
      Legacy warming pressure remains. No active restoration.
      Result: slower accumulation at best, not CO2 recovery.

  Scenario 3 — Fixation Restoration Only:
      Active restoration of forests, soils, and marine ecosystems.
      No change in emission trajectory (emissions continue growing).
      Fixation capacity recovers gradually.

  Scenario 4 — Integrated Nature-Complementary Approach:
      Aggressive emission reduction (announced decarbonization pace).
      Active restoration of terrestrial and marine carbon fixation systems.
      Both pathways addressed simultaneously.

Purpose: To illustrate that (1) the multi-cause hypothesis implies
different policy priorities than the single-cause (emissions-only) model,
and (2) "decarbonization only" is not a single physical process but a
policy assumption whose real-world effectiveness depends on whether global
total emissions actually decline — which has not been structurally achieved
as of the model's publication date.

COVID-19 note:
  Global emissions temporarily declined in 2020 due to pandemic-related
  activity reductions. This is treated as a temporary external shock, not
  as evidence of sustained structural decarbonization.

Change log (v2):
  - Removed max(0.0, ...) floor from _co2_delta to allow CO2 drawdown.
  - Added co2_pressure (unbounded) alongside co2 (clipped [0,1]).

Change log (v3):
  - Split "Decarbonization Only" into:
      2a. Announced Decarbonization Only  (fast, policy-target pace)
      2b. Realistic Global Decarbonization Only
          (slow net decline; developed cuts offset by developing growth)
  - Added ScenarioParameters for realistic decomposition:
      developed_country_reduction_rate, developing_country_emissions_growth,
      population_energy_demand_growth, industrialization_pressure,
      net_global_decarbonization_rate, realistic_emission_floor.
  - run_scenario gains `realistic_decarb` flag.
  - "Integrated Approach" renamed to "Integrated Nature-Complementary Approach".

⚠️  IMPORTANT LIMITATIONS
    All parameters, rates, and trajectories are HYPOTHETICAL.
    These scenarios are conceptual illustrations, not climate projections.
    They are NOT calibrated against real data and should NOT be used
    for policy decisions, scientific claims, or quantitative comparison
    with IPCC or other validated model outputs.
    See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Clus, Real, Lora
Published: May 2026
License: CC BY-SA 4.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────────
# 1. Starting State (from 2025 estimate of historical_phase_model)
# ─────────────────────────────────────────────────────────────────

@dataclass
class StartingState:
    """
    Approximate starting conditions derived from the
    historical_phase_model simulation output at year 2025.

    All values are HYPOTHETICAL and normalized [0.0, 1.0].
    """
    year: int = 2025

    # System health at 2025 (HYPOTHETICAL end-state of historical model)
    terrestrial_fixation:  float = 0.62
    soil_microbial_health: float = 0.52
    soil_carbon_fixation:  float = 0.58
    ocean_uptake_capacity: float = 0.68
    co2_index:             float = 0.55
    emission_rate:         float = 0.75


# ─────────────────────────────────────────────────────────────────
# 2. Scenario Parameters
# ─────────────────────────────────────────────────────────────────

@dataclass
class ScenarioParameters:
    """
    Parameters controlling the 75-year forward simulation.
    All rates are HYPOTHETICAL and per-year.
    """
    projection_years: int = 75

    # --- Emission trajectories ---
    # HYPOTHETICAL: announced decarbonization rate (policy-target pace; ~net zero by 2050)
    emission_reduction_rate: float = 0.018
    # HYPOTHETICAL: annual emission growth in BAU
    bau_emission_growth: float = 0.004

    # --- Realistic global decarbonization decomposition (v3) ---
    # HYPOTHETICAL: rate at which developed-nation blocs cut annual emissions
    developed_country_reduction_rate:    float = 0.018
    # HYPOTHETICAL: annual emission expansion from developing-nation industrialization
    developing_country_emissions_growth: float = 0.008
    # HYPOTHETICAL: additional demand from global population increase
    population_energy_demand_growth:     float = 0.003
    # HYPOTHETICAL: ongoing industrialization pressure (energy infrastructure buildout)
    industrialization_pressure:          float = 0.004
    # HYPOTHETICAL: net global effective rate = 0.018 - 0.008 - 0.003 - 0.004 = 0.003 / yr
    # Represents a world where developed-country cuts are largely offset by
    # developing-country and population-driven demand growth.
    net_global_decarbonization_rate:     float = 0.003
    # HYPOTHETICAL: emission floor for realistic scenario; represents residual
    # global baseline from developing-world industrialization that is hard to eliminate
    realistic_emission_floor:            float = 0.10

    # --- Fixation restoration rates ---
    # HYPOTHETICAL: annual improvement in terrestrial fixation under active restoration
    terrestrial_restoration_rate: float = 0.008
    # HYPOTHETICAL: annual improvement in soil health under regenerative agriculture
    soil_restoration_rate: float = 0.006
    # HYPOTHETICAL: annual improvement in ocean uptake under marine ecosystem recovery
    ocean_restoration_rate: float = 0.005

    # --- Passive degradation rates (without intervention) ---
    # HYPOTHETICAL: continued passive decline even without new pressure
    passive_terr_decline: float = 0.003
    passive_soil_decline: float = 0.002
    passive_ocean_decline: float = 0.002

    # --- CO₂ balance sensitivity ---
    # HYPOTHETICAL: weights for how each system contributes to CO₂ balance
    terr_co2_weight:   float = 0.35
    soil_co2_weight:   float = 0.25
    ocean_co2_weight:  float = 0.30
    degrad_co2_weight: float = 0.10

    # HYPOTHETICAL: warming feedback into continued fixation decline
    warming_feedback_strength: float = 0.08


# ─────────────────────────────────────────────────────────────────
# 3. Scenario Engine
# ─────────────────────────────────────────────────────────────────

class ScenarioEngine:
    """
    Projects climate system state forward under five scenarios.
    All dynamics are HYPOTHETICAL and conceptual.
    """

    def __init__(
        self,
        start: StartingState,
        params: ScenarioParameters,
    ):
        self.start  = start
        self.params = params

    def _co2_delta(
        self,
        emission: float,
        terr: float,
        soil: float,
        ocean: float,
        p: ScenarioParameters,
    ) -> float:
        """
        HYPOTHETICAL CO₂ balance.
        Positive delta = net accumulation; negative delta = net drawdown.

        Note (v2): the max(0.0, ...) floor has been removed so that
        scenarios with strong fixation recovery can produce genuine CO₂
        drawdown.  The clipped `co2` variable is still clamped in
        run_scenario; the unbounded `co2_pressure` variable is not.
        """
        fixation_removal = (
            p.terr_co2_weight  * terr  +
            p.soil_co2_weight  * soil  +
            p.ocean_co2_weight * ocean
        )
        degradation_input = p.degrad_co2_weight * max(0.0, (0.90 - terr + 0.92 - soil) * 0.5)
        return (emission - fixation_removal * 0.85 + degradation_input) * 0.012

    def run_scenario(
        self,
        name: str,
        reduce_emissions:    bool,
        restore_terrestrial: bool,
        restore_ocean:       bool,
        realistic_decarb:    bool = False,
    ) -> Dict[str, np.ndarray]:
        """
        Run a single scenario for projection_years timesteps.

        Parameters
        ----------
        reduce_emissions     : apply a decarbonization trajectory
        restore_terrestrial  : apply soil and forest restoration
        restore_ocean        : apply marine ecosystem restoration
        realistic_decarb     : when reduce_emissions=True, use the realistic
                               net_global_decarbonization_rate instead of the
                               announced emission_reduction_rate.
                               Represents developed-country cuts partially or
                               largely offset by developing-country growth.
        """
        T  = self.params.projection_years
        p  = self.params
        s  = self.start

        years        = np.arange(s.year, s.year + T)
        emission     = np.zeros(T)
        terr         = np.zeros(T)
        soil         = np.zeros(T)
        ocean        = np.zeros(T)
        co2          = np.zeros(T)   # clipped to [0, 1] — kept for backward compat
        co2_pressure = np.zeros(T)   # unbounded — used for comparison plots

        emission[0]     = s.emission_rate
        terr[0]         = s.terrestrial_fixation
        soil[0]         = s.soil_microbial_health
        ocean[0]        = s.ocean_uptake_capacity
        co2[0]          = s.co2_index
        co2_pressure[0] = s.co2_index

        for t in range(1, T):
            # --- Emission trajectory ---
            if reduce_emissions:
                if realistic_decarb:
                    # HYPOTHETICAL: net global rate after developed cuts are
                    # partially offset by developing-world emissions growth,
                    # population demand, and industrialization pressure.
                    # Floor is higher than announced scenario (residual baseline).
                    emission[t] = max(
                        p.realistic_emission_floor,
                        emission[t - 1] - p.net_global_decarbonization_rate,
                    )
                else:
                    # HYPOTHETICAL: announced policy-target pace (~net zero by 2050)
                    emission[t] = max(0.02, emission[t - 1] - p.emission_reduction_rate)
            else:
                emission[t] = min(1.0, emission[t - 1] + p.bau_emission_growth)

            # --- Warming feedback (HYPOTHETICAL: CO2 index drives continued decline) ---
            warming_pressure = p.warming_feedback_strength * co2[t - 1]

            # --- Terrestrial fixation ---
            if restore_terrestrial:
                terr_change = p.terrestrial_restoration_rate - warming_pressure * 0.5
            else:
                terr_change = -(p.passive_terr_decline + warming_pressure * 0.3)
            terr[t] = max(0.0, min(1.0, terr[t - 1] + terr_change * 0.3))

            # --- Soil carbon fixation ---
            if restore_terrestrial:
                soil_change = p.soil_restoration_rate - warming_pressure * 0.3
            else:
                soil_change = -(p.passive_soil_decline + warming_pressure * 0.2)
            soil[t] = max(0.0, min(1.0, soil[t - 1] + soil_change * 0.3))

            # --- Ocean uptake ---
            if restore_ocean:
                ocean_change = p.ocean_restoration_rate - warming_pressure * 0.2
            else:
                ocean_change = -(p.passive_ocean_decline + warming_pressure * 0.2)
            ocean[t] = max(0.0, min(1.0, ocean[t - 1] + ocean_change * 0.3))

            # --- CO₂ accumulation ---
            delta = self._co2_delta(emission[t], terr[t], soil[t], ocean[t], p)
            co2[t]          = max(0.0, min(1.0, co2[t - 1] + delta))
            co2_pressure[t] = co2_pressure[t - 1] + delta   # unbounded

        return {
            "name":         name,
            "years":        years,
            "emission":     emission,
            "terr":         terr,
            "soil":         soil,
            "ocean":        ocean,
            "co2":          co2,
            "co2_pressure": co2_pressure,
        }

    def run_all(self) -> List[Dict]:
        scenarios = [
            self.run_scenario(
                "1. Business as Usual",
                reduce_emissions=False, restore_terrestrial=False, restore_ocean=False,
            ),
            self.run_scenario(
                "2a. Announced Decarbonization Only",
                reduce_emissions=True,  restore_terrestrial=False, restore_ocean=False,
                realistic_decarb=False,
            ),
            self.run_scenario(
                "2b. Realistic Global Decarbonization Only",
                reduce_emissions=True,  restore_terrestrial=False, restore_ocean=False,
                realistic_decarb=True,
            ),
            self.run_scenario(
                "3. Fixation Restoration Only",
                reduce_emissions=False, restore_terrestrial=True,  restore_ocean=True,
            ),
            self.run_scenario(
                "4. Integrated Nature-Complementary Approach",
                reduce_emissions=True,  restore_terrestrial=True,  restore_ocean=True,
                realistic_decarb=False,
            ),
        ]
        return scenarios


# ─────────────────────────────────────────────────────────────────
# 4. Visualization
# ─────────────────────────────────────────────────────────────────

SCENARIO_COLORS = {
    "1. Business as Usual":                      "#C0392B",   # red
    "2a. Announced Decarbonization Only":         "#F0B27A",   # light orange (optimistic)
    "2b. Realistic Global Decarbonization Only":  "#E67E22",   # dark orange  (realistic)
    "3. Fixation Restoration Only":               "#2980B9",   # blue
    "4. Integrated Nature-Complementary Approach": "#27AE60",  # green
}
SCENARIO_STYLES = {
    "1. Business as Usual":                      "-",
    "2a. Announced Decarbonization Only":         "--",
    "2b. Realistic Global Decarbonization Only":  ":",
    "3. Fixation Restoration Only":               "-.",
    "4. Integrated Nature-Complementary Approach": "-",
}
SCENARIO_WIDTHS = {
    "1. Business as Usual":                      1.5,
    "2a. Announced Decarbonization Only":         1.5,
    "2b. Realistic Global Decarbonization Only":  1.5,
    "3. Fixation Restoration Only":               1.5,
    "4. Integrated Nature-Complementary Approach": 2.2,
}


def plot_scenario_comparison(scenarios: List[Dict]) -> None:
    import os
    os.makedirs("figures", exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        "Scenario Comparison: Five Climate Intervention Strategies (2025–2099)\n"
        "2a = Announced Decarb (optimistic)   |   2b = Realistic Global Decarb (partial offset)\n"
        "⚠ HYPOTHETICAL CONCEPTUAL VALUES — Not climate projections. Not calibrated against real data.",
        fontsize=9, fontweight="bold", color="#8B0000",
    )

    # CO2 panel uses unbounded co2_pressure so clipping does not hide differences
    panels = [
        ("co2_pressure", "CO₂ Pressure (Unbounded Accumulation Index)", axes[0, 0]),
        ("emission",     "Emission Rate",                               axes[0, 1]),
        ("terr",         "Terrestrial Fixation Capacity",               axes[1, 0]),
        ("ocean",        "Ocean CO₂ Uptake Capacity",                   axes[1, 1]),
    ]

    for key, title, ax in panels:
        for sc in scenarios:
            ax.plot(
                sc["years"], sc[key],
                color=SCENARIO_COLORS[sc["name"]],
                linestyle=SCENARIO_STYLES[sc["name"]],
                linewidth=SCENARIO_WIDTHS[sc["name"]],
                label=sc["name"],
            )
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("Year", fontsize=8)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
        ax.tick_params(labelsize=7)

        if key == "co2_pressure":
            ax.set_ylabel("Unbounded accumulation index", fontsize=8)
            ax.axhline(0.55, color="#999", linewidth=0.6, linestyle=":")  # 2025 start
        else:
            ax.set_ylabel("Normalized [0–1]", fontsize=8)
            ax.set_ylim(0, 1.05)
            ax.axhline(0.5, color="#999", linewidth=0.6, linestyle=":")

    plt.tight_layout()
    plt.savefig("figures/scenario_comparison_output.png", dpi=150, bbox_inches="tight")
    print("  -> Saved: figures/scenario_comparison_output.png")
    plt.show()


def print_scenario_summary(scenarios: List[Dict]) -> None:
    checkpoints = [2025, 2035, 2050, 2075, 2099]
    W = 44
    print(f"\n  {'Scenario':<{W}}  {'Year':>4}  {'CO2-P':>7}  {'Emit':>6}  {'Terr':>6}  {'Ocean':>6}")
    print("  " + "-" * (W + 38))
    for sc in scenarios:
        years = sc["years"]
        for chk in checkpoints:
            if chk in years:
                idx = list(years).index(chk)
                print(
                    f"  {sc['name'][:W]:<{W}}  {chk:>4}  "
                    f"{sc['co2_pressure'][idx]:>7.3f}  "
                    f"{sc['emission'][idx]:>6.3f}  "
                    f"{sc['terr'][idx]:>6.3f}  "
                    f"{sc['ocean'][idx]:>6.3f}"
                )
        print()


# ─────────────────────────────────────────────────────────────────
# 5. Main
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("  Scenario Comparison (2025-2099)")
    print("  1. BAU  |  2a. Announced Decarb  |  2b. Realistic Global Decarb")
    print("  3. Fixation Restoration  |  4. Integrated Nature-Complementary")
    print("  WARNING: HYPOTHETICAL CONCEPTUAL MODEL -- See MODEL_LIMITATIONS.md")
    print("=" * 72)

    start     = StartingState()
    params    = ScenarioParameters()
    engine    = ScenarioEngine(start, params)
    scenarios = engine.run_all()

    print_scenario_summary(scenarios)

    sc_bau   = scenarios[0]
    sc_ann   = scenarios[1]   # 2a. Announced
    sc_real  = scenarios[2]   # 2b. Realistic
    sc_fix   = scenarios[3]   # 3.  Fixation
    sc_int   = scenarios[4]   # 4.  Integrated

    print("  CO2 pressure at 2099 (HYPOTHETICAL):")
    for sc in scenarios:
        print(f"    {sc['name']:<46}  {sc['co2_pressure'][-1]:.3f}")

    gap_decarb = sc_real["co2_pressure"][-1] - sc_ann["co2_pressure"][-1]
    print(
        f"\n  Decarbonization realism gap at 2099 (2b minus 2a): {gap_decarb:+.3f}"
        "\n  This gap represents the CO2 cost of developing-world emission"
        "\n  growth offsetting developed-world policy commitments."
        "\n  (HYPOTHETICAL -- depends entirely on assumed offset rates)"
    )
    print(
        "\n  Key conceptual conclusions (HYPOTHETICAL -- illustrative only):"
        "\n  - 2a (Announced Decarb) and 2b (Realistic Decarb) diverge over time"
        "\n    because net global emissions remain higher for much longer in 2b."
        "\n  - Decarbonization alone is not a single physical process."
        "\n    Its effectiveness depends on whether global total emissions actually"
        "\n    decline -- which requires developing economies to also transition."
        "\n  - Fixation restoration alone cannot compensate for continued emissions."
        "\n  - Only the Integrated approach addresses both pathways simultaneously."
        "\n  - COVID-19 (2020) caused a temporary emission shock, not structural"
        "\n    decarbonization. This model does not model temporary shocks."
    )
    print("\n  WARNING: All values are HYPOTHETICAL. See MODEL_LIMITATIONS.md.")
    print("=" * 72)

    plot_scenario_comparison(scenarios)


if __name__ == "__main__":
    main()
