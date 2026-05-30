"""
intervention_technology_model.py
==================================
Conceptual Technology-Intervention Scenario Model

This model extends the multi-cause carbon fixation framework to include
direct natural-complementary technology interventions alongside conventional
emission-reduction and natural-restoration pathways.

Technologies modelled (all HYPOTHETICAL effects):

  OBS  — Ocean Breathing System
         deep-ocean oxygenation, vertical circulation support,
         plankton productivity recovery, ocean carbon uptake enhancement

  OTU  — Ocean Thermal / Upwelling Unit
         controlled nutrient upwelling, surface biological productivity support,
         ocean metabolic recovery

  UMC  — Ultrasonic Mist Cooling
         evaporative cooling, urban heat reduction,
         surface thermal stress reduction

  HRS  — Humus Recycling System
         food loss, organic waste, leaves, and biomass -> humus precursor,
         soil microbial recovery, soil carbon storage increase,
         water retention improvement

  DGS  — Desert Greening Support
         humus import / export model, soil formation support,
         vegetation expansion into degraded / arid land,
         new terrestrial carbon fixation area

Five scenarios are compared (2025-2099):

  1. Baseline                        no intervention; emissions grow
  2. Decarbonization Only            emissions cut aggressively; no tech
  3. Natural Sink Restoration Only   forest / soil / ocean restored; no tech
  4. Direct Cooling Technologies Only  OBS + OTU + UMC + HRS + DGS; no decarb
  5. Full Integrated Nature-Complementary System  all pathways combined

State variables tracked every year:
  co2_pressure       unbounded CO2 accumulation index
  land_fixation      terrestrial carbon fixation capacity      [0-1]
  ocean_uptake       ocean carbon uptake capacity              [0-1]
  thermal_stress     surface thermal stress index              [0-1]
  ecosystem_recovery composite ecosystem health index          [0-1]

Deployment scale factors allow technologies to be evaluated at:
  local        (0.001)   neighborhood / experimental plot
  city         (0.010)   city-scale network
  regional     (0.050)   regional deployment
  continental  (0.200)   continental infrastructure
  planetary    (1.000)   full global deployment

The sixth output panel shows how CO2 pressure at 2099 changes as the
technology deployment scale sweeps from local to planetary, illustrating
the minimum scale required to achieve meaningful planetary-level impact.

WARNING  All parameters are HYPOTHETICAL and normalized.
         OBS, OTU, and UMC are proposed technologies whose real-world
         effects have NOT been validated in field studies.
         This model requires field validation, ecological risk assessment,
         and scale testing before any real-world application.
         It is NOT a prediction model and NOT a policy tool.
         See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Cruz, Real, Lola
Published: May 2026
License: CC BY-SA 4.0
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------
# 1.  Scale factors
# -----------------------------------------------------------------

SCALE_FACTORS: Dict[str, float] = {
    "local":       0.001,
    "city":        0.010,
    "regional":    0.050,
    "continental": 0.200,
    "planetary":   1.000,
}


# -----------------------------------------------------------------
# 2.  Starting state  (2025 estimates, inherited from prior models)
# -----------------------------------------------------------------

@dataclass
class TechStartingState:
    """
    2025 starting conditions.
    All values HYPOTHETICAL and normalized to [0-1] unless noted.
    terrestrial_fixation, soil_microbial_health, ocean_uptake_capacity,
    co2_pressure, emission_rate  are inherited from historical_phase_model.py
    and scenario_examples.py.
    thermal_stress and new_vegetation_area are new variables for this model.
    """
    year: int = 2025

    terrestrial_fixation:  float = 0.62   # HYPOTHETICAL
    soil_microbial_health: float = 0.52   # HYPOTHETICAL
    ocean_uptake_capacity: float = 0.68   # HYPOTHETICAL
    co2_pressure:          float = 0.55   # HYPOTHETICAL
    emission_rate:         float = 0.75   # HYPOTHETICAL
    thermal_stress:        float = 0.42   # HYPOTHETICAL  0 = no stress, 1 = extreme
    new_vegetation_area:   float = 0.00   # fraction of restorable degraded land
                                          # with new vegetation cover (via DGS)


# -----------------------------------------------------------------
# 3.  Technology parameters
# -----------------------------------------------------------------

@dataclass
class TechParameters:
    """
    All rates are HYPOTHETICAL per-year values.
    None are calibrated against observational data.
    Technology effects are additionally multiplied by scale_factor [0-1].
    See MODEL_LIMITATIONS.md for full disclosure.
    """
    projection_years: int = 75

    # ---- Emission trajectories ----
    emission_reduction_rate: float = 0.018   # HYPOTHETICAL: ~net-zero by 2050
    bau_emission_growth:     float = 0.004   # HYPOTHETICAL: BAU annual growth

    # ---- Natural sink restoration (passive natural rates) ----
    terrestrial_restoration_rate: float = 0.008  # HYPOTHETICAL
    soil_restoration_rate:        float = 0.006  # HYPOTHETICAL
    ocean_restoration_rate:       float = 0.005  # HYPOTHETICAL
    passive_terr_decline:         float = 0.003  # HYPOTHETICAL: without intervention
    passive_soil_decline:         float = 0.002  # HYPOTHETICAL
    passive_ocean_decline:        float = 0.002  # HYPOTHETICAL

    # ---- OBS: Ocean Breathing System ----
    # Hypothetical annual improvement per unit scale_factor
    obs_ocean_health_rate: float = 0.008  # HYPOTHETICAL: deep-O2 -> ocean health
    obs_plankton_recovery: float = 0.005  # HYPOTHETICAL: plankton productivity
    obs_uptake_boost:      float = 0.004  # HYPOTHETICAL: direct CO2 uptake enhance

    # ---- OTU: Ocean Thermal / Upwelling Unit ----
    otu_upwelling_rate:    float = 0.006  # HYPOTHETICAL: nutrient upwelling
    otu_recovery_rate:     float = 0.004  # HYPOTHETICAL: metabolic recovery

    # ---- UMC: Ultrasonic Mist Cooling ----
    umc_thermal_rate:      float = 0.012  # HYPOTHETICAL: thermal stress reduction/yr
    umc_land_benefit:      float = 0.003  # HYPOTHETICAL: indirect land fixation gain

    # ---- HRS: Humus Recycling System ----
    hrs_soil_rate:         float = 0.010  # HYPOTHETICAL: soil microbial recovery
    hrs_terr_boost:        float = 0.005  # HYPOTHETICAL: land fixation improvement

    # ---- DGS: Desert Greening Support ----
    dgs_greening_rate:     float = 0.005  # HYPOTHETICAL: fraction of restorable land/yr
    dgs_max_new_area:      float = 0.300  # HYPOTHETICAL: max restorable fraction
    dgs_fixation_boost:    float = 0.300  # HYPOTHETICAL: max add. fixation at full area

    # ---- CO2 balance weights ----
    terr_co2_weight:   float = 0.35   # HYPOTHETICAL
    soil_co2_weight:   float = 0.25   # HYPOTHETICAL
    ocean_co2_weight:  float = 0.30   # HYPOTHETICAL
    degrad_co2_weight: float = 0.10   # HYPOTHETICAL

    # ---- Thermal stress dynamics ----
    thermal_bau_growth:    float = 0.005  # HYPOTHETICAL: BAU annual thermal growth
    thermal_co2_feedback:  float = 0.006  # HYPOTHETICAL: CO2 pressure -> thermal
    thermal_land_coupling: float = 0.120  # HYPOTHETICAL: thermal -> land fixation loss
    thermal_ocean_coupling: float = 0.080 # HYPOTHETICAL: thermal -> ocean uptake loss

    # ---- Warming feedback into fixation decline ----
    warming_feedback:      float = 0.080  # HYPOTHETICAL: CO2 pressure -> fixation loss


# -----------------------------------------------------------------
# 4.  Scenario colours / styles
# -----------------------------------------------------------------

SCENARIO_COLORS = {
    "1. Baseline":                          "#C0392B",
    "2. Decarbonization Only":              "#E67E22",
    "3. Natural Sink Restoration Only":     "#2980B9",
    "4. Direct Cooling Technologies Only":  "#8E44AD",
    "5. Full Integrated":                   "#27AE60",
}
SCENARIO_STYLES = {
    "1. Baseline":                          "-",
    "2. Decarbonization Only":              "--",
    "3. Natural Sink Restoration Only":     "-.",
    "4. Direct Cooling Technologies Only":  ":",
    "5. Full Integrated":                   "-",
}
SCENARIO_WIDTHS = {
    "1. Baseline":                          1.5,
    "2. Decarbonization Only":              1.5,
    "3. Natural Sink Restoration Only":     1.5,
    "4. Direct Cooling Technologies Only":  2.0,
    "5. Full Integrated":                   2.8,
}


# -----------------------------------------------------------------
# 5.  Intervention engine
# -----------------------------------------------------------------

class InterventionEngine:
    """
    Projects the climate system forward under five intervention scenarios.
    All dynamics are HYPOTHETICAL and conceptual.
    Technology effects are scaled by scale_factor [0-1]; 1.0 = planetary.
    """

    def __init__(self, start: TechStartingState, params: TechParameters):
        self.start  = start
        self.params = params

    # ---- Internal helpers ----

    def _co2_delta(
        self,
        emission: float,
        terr: float,
        soil: float,
        ocean: float,
        new_veg: float,
        p: TechParameters,
    ) -> float:
        """
        HYPOTHETICAL CO2 balance.
        Positive = net accumulation; negative = net drawdown.
        No max(0, ...) floor -- drawdown is allowed when restored fixation
        exceeds emissions (see scenario_examples.py v2 for rationale).
        Desert greening (new_veg) contributes additional terrestrial fixation.
        """
        effective_terr = terr + new_veg * p.dgs_fixation_boost   # unbounded above 1.0 OK
        fixation_removal = (
            p.terr_co2_weight  * effective_terr +
            p.soil_co2_weight  * soil +
            p.ocean_co2_weight * ocean
        )
        degradation_input = p.degrad_co2_weight * max(
            0.0, (0.90 - terr + 0.92 - soil) * 0.5
        )
        return (emission - fixation_removal * 0.85 + degradation_input) * 0.012

    def _eco_recovery(
        self,
        terr: float,
        soil: float,
        ocean: float,
        thermal: float,
        new_veg: float,
    ) -> float:
        """
        HYPOTHETICAL composite ecosystem recovery index [0-1].
        Weighted combination of all five state dimensions.
        """
        p = self.params
        nv_norm = np.clip(new_veg / p.dgs_max_new_area, 0.0, 1.0)
        return float(np.clip(
            terr   * 0.30 +
            soil   * 0.20 +
            ocean  * 0.25 +
            (1.0 - thermal) * 0.15 +
            nv_norm * 0.10,
            0.0, 1.0,
        ))

    # ---- Single scenario ----

    def run_scenario(
        self,
        name: str,
        reduce_emissions:  bool,
        restore_natural:   bool,
        deploy_obs:        bool,
        deploy_otu:        bool,
        deploy_umc:        bool,
        deploy_hrs:        bool,
        deploy_dgs:        bool,
        scale_factor:      float = 1.0,
    ) -> Dict:
        """
        Run a single scenario for projection_years timesteps.

        Parameters
        ----------
        reduce_emissions : apply decarbonization trajectory
        restore_natural  : apply natural forest / soil / ocean restoration
        deploy_obs       : Ocean Breathing System   (scaled)
        deploy_otu       : Ocean Thermal/Upwelling Unit  (scaled)
        deploy_umc       : Ultrasonic Mist Cooling  (scaled)
        deploy_hrs       : Humus Recycling System   (scaled)
        deploy_dgs       : Desert Greening Support  (scaled)
        scale_factor     : technology deployment scale [0-1]; 1.0 = planetary
        """
        T  = self.params.projection_years
        p  = self.params
        s  = self.start
        sf = float(np.clip(scale_factor, 0.0, 1.0))

        years        = np.arange(s.year, s.year + T)
        emission     = np.zeros(T)
        terr         = np.zeros(T)
        soil         = np.zeros(T)
        ocean        = np.zeros(T)
        thermal      = np.zeros(T)
        new_veg      = np.zeros(T)
        co2_pressure = np.zeros(T)
        eco_recovery = np.zeros(T)

        # t = 0  (starting state)
        emission[0]     = s.emission_rate
        terr[0]         = s.terrestrial_fixation
        soil[0]         = s.soil_microbial_health
        ocean[0]        = s.ocean_uptake_capacity
        thermal[0]      = s.thermal_stress
        new_veg[0]      = s.new_vegetation_area
        co2_pressure[0] = s.co2_pressure
        eco_recovery[0] = self._eco_recovery(
            terr[0], soil[0], ocean[0], thermal[0], new_veg[0]
        )

        for t in range(1, T):
            prev_co2 = co2_pressure[t - 1]
            prev_th  = thermal[t - 1]

            # 1. Emission trajectory
            if reduce_emissions:
                emission[t] = max(0.02, emission[t - 1] - p.emission_reduction_rate)
            else:
                emission[t] = min(1.0,  emission[t - 1] + p.bau_emission_growth)

            # 2. Thermal stress
            #    BAU: grows with CO2 pressure feedback
            #    UMC: actively reduces thermal stress at scale
            th_delta = p.thermal_bau_growth + p.thermal_co2_feedback * prev_co2
            if deploy_umc:
                th_delta -= p.umc_thermal_rate * sf
            thermal[t] = float(np.clip(thermal[t - 1] + th_delta * 0.3, 0.0, 1.0))

            # 3. Combined warming/thermal pressure on fixation systems
            combined_p = p.warming_feedback * prev_co2 + p.thermal_land_coupling * prev_th

            # 4. Terrestrial fixation
            #    Passive decline amplified by warming/thermal pressure
            #    Natural restoration + HRS soil boost + UMC indirect benefit
            t_delta = -(p.passive_terr_decline + combined_p * 0.3)
            if restore_natural:
                t_delta += p.terrestrial_restoration_rate
            if deploy_hrs:
                t_delta += (p.hrs_soil_rate + p.hrs_terr_boost) * sf * 0.5
            if deploy_umc:
                t_delta += p.umc_land_benefit * sf
            terr[t] = float(np.clip(terr[t - 1] + t_delta * 0.3, 0.0, 1.0))

            # 5. Soil microbial health
            s_delta = -(p.passive_soil_decline + combined_p * 0.2)
            if restore_natural:
                s_delta += p.soil_restoration_rate
            if deploy_hrs:
                s_delta += p.hrs_soil_rate * sf
            soil[t] = float(np.clip(soil[t - 1] + s_delta * 0.3, 0.0, 1.0))

            # 6. Ocean carbon uptake
            #    Passive decline + thermal stratification + warming feedback
            #    Natural restoration + OBS (oxygenation/plankton) + OTU (upwelling)
            ocean_loss = (
                p.passive_ocean_decline +
                p.thermal_ocean_coupling * prev_th * 0.3 +
                p.warming_feedback * prev_co2 * 0.2
            )
            o_delta = -ocean_loss
            if restore_natural:
                o_delta += p.ocean_restoration_rate
            if deploy_obs:
                obs_effect = (
                    p.obs_ocean_health_rate +
                    p.obs_plankton_recovery +
                    p.obs_uptake_boost
                ) * sf / 3.0          # average of three OBS pathways
                o_delta += obs_effect
            if deploy_otu:
                otu_effect = (p.otu_upwelling_rate + p.otu_recovery_rate) * sf * 0.5
                o_delta += otu_effect
            ocean[t] = float(np.clip(ocean[t - 1] + o_delta * 0.3, 0.0, 1.0))

            # 7. Desert greening: new vegetation area (linear until max)
            if deploy_dgs:
                nv_delta = p.dgs_greening_rate * sf
                new_veg[t] = float(
                    np.clip(new_veg[t - 1] + nv_delta, 0.0, p.dgs_max_new_area)
                )
            else:
                new_veg[t] = new_veg[t - 1]

            # 8. CO2 pressure (unbounded)
            delta = self._co2_delta(
                emission[t], terr[t], soil[t], ocean[t], new_veg[t], p
            )
            co2_pressure[t] = co2_pressure[t - 1] + delta

            # 9. Ecosystem recovery composite
            eco_recovery[t] = self._eco_recovery(
                terr[t], soil[t], ocean[t], thermal[t], new_veg[t]
            )

        return {
            "name":          name,
            "years":         years,
            "emission":      emission,
            "terr":          terr,
            "soil":          soil,
            "ocean":         ocean,
            "thermal":       thermal,
            "new_veg":       new_veg,
            "co2_pressure":  co2_pressure,
            "eco_recovery":  eco_recovery,
            "scale_factor":  sf,
        }

    # ---- Five standard scenarios ----

    def run_all_scenarios(self, scale_factor: float = 1.0) -> List[Dict]:
        """Run the five standard scenarios at the given technology scale factor."""
        return [
            self.run_scenario(
                "1. Baseline",
                reduce_emissions=False, restore_natural=False,
                deploy_obs=False, deploy_otu=False, deploy_umc=False,
                deploy_hrs=False, deploy_dgs=False,
                scale_factor=scale_factor,
            ),
            self.run_scenario(
                "2. Decarbonization Only",
                reduce_emissions=True, restore_natural=False,
                deploy_obs=False, deploy_otu=False, deploy_umc=False,
                deploy_hrs=False, deploy_dgs=False,
                scale_factor=scale_factor,
            ),
            self.run_scenario(
                "3. Natural Sink Restoration Only",
                reduce_emissions=False, restore_natural=True,
                deploy_obs=False, deploy_otu=False, deploy_umc=False,
                deploy_hrs=False, deploy_dgs=False,
                scale_factor=scale_factor,
            ),
            self.run_scenario(
                "4. Direct Cooling Technologies Only",
                reduce_emissions=False, restore_natural=False,
                deploy_obs=True, deploy_otu=True, deploy_umc=True,
                deploy_hrs=True, deploy_dgs=True,
                scale_factor=scale_factor,
            ),
            self.run_scenario(
                "5. Full Integrated",
                reduce_emissions=True, restore_natural=True,
                deploy_obs=True, deploy_otu=True, deploy_umc=True,
                deploy_hrs=True, deploy_dgs=True,
                scale_factor=scale_factor,
            ),
        ]

    # ---- Scale factor sweep ----

    def run_scale_sweep(self) -> Dict:
        """
        Sweep scale_factor from local (0.001) to planetary (1.0) on a log scale.
        Records CO2 pressure at 2099 for tech-enabled scenarios 4 and 5.
        Non-tech scenarios 1-3 are scale-independent and shown as constants.
        """
        sweep_values = np.logspace(-3, 0, 40)
        tech_co2   = np.zeros(len(sweep_values))
        integ_co2  = np.zeros(len(sweep_values))

        for i, sf in enumerate(sweep_values):
            sc4 = self.run_scenario(
                "4. Direct Cooling Technologies Only",
                reduce_emissions=False, restore_natural=False,
                deploy_obs=True, deploy_otu=True, deploy_umc=True,
                deploy_hrs=True, deploy_dgs=True,
                scale_factor=sf,
            )
            sc5 = self.run_scenario(
                "5. Full Integrated",
                reduce_emissions=True, restore_natural=True,
                deploy_obs=True, deploy_otu=True, deploy_umc=True,
                deploy_hrs=True, deploy_dgs=True,
                scale_factor=sf,
            )
            tech_co2[i]  = sc4["co2_pressure"][-1]
            integ_co2[i] = sc5["co2_pressure"][-1]

        return {
            "sweep_values": sweep_values,
            "tech_co2":     tech_co2,
            "integ_co2":    integ_co2,
        }


# -----------------------------------------------------------------
# 6.  Console summary
# -----------------------------------------------------------------

def print_scenario_summary(scenarios: List[Dict]) -> None:
    checkpoints = [2025, 2050, 2075, 2099]
    hdr = (f"  {'Scenario':<42}  {'Year':>4}  "
           f"{'CO2-P':>7}  {'Terr':>6}  {'Ocean':>6}  "
           f"{'Therm':>6}  {'EcoRec':>7}")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for sc in scenarios:
        years_list = list(sc["years"])
        for chk in checkpoints:
            if chk in years_list:
                idx = years_list.index(chk)
                print(
                    f"  {sc['name'][:42]:<42}  {chk:>4}  "
                    f"{sc['co2_pressure'][idx]:>7.3f}  "
                    f"{sc['terr'][idx]:>6.3f}  "
                    f"{sc['ocean'][idx]:>6.3f}  "
                    f"{sc['thermal'][idx]:>6.3f}  "
                    f"{sc['eco_recovery'][idx]:>7.3f}"
                )
        print()


# -----------------------------------------------------------------
# 7.  Visualization
# -----------------------------------------------------------------

def plot_results(scenarios: List[Dict], sweep: Dict) -> None:
    os.makedirs("figures", exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(
        "Technology-Intervention Scenario Comparison (2025–2099)  |  Planetary Scale Deployment\n"
        "OBS  |  OTU  |  UMC  |  Humus Recycling System  |  Desert Greening Support\n"
        "⚠  HYPOTHETICAL CONCEPTUAL MODEL — Not validated. Not calibrated. Not for policy use."
        "  See MODEL_LIMITATIONS.md.",
        fontsize=9, fontweight="bold", color="#8B0000",
    )

    # ---- Five time-series panels ----
    time_panels = [
        ("co2_pressure", "CO₂ Pressure\n(Unbounded Accumulation Index)",    "Unbounded index",    axes[0, 0]),
        ("terr",         "Land Carbon Fixation Capacity",                          "Normalized [0–1]",  axes[0, 1]),
        ("ocean",        "Ocean CO₂ Uptake Capacity",                         "Normalized [0–1]",  axes[0, 2]),
        ("thermal",      "Thermal Stress Index\n(lower = better)",                 "Stress [0–1]",      axes[1, 0]),
        ("eco_recovery", "Ecosystem Recovery Index\n(composite, higher = better)", "Composite [0–1]",   axes[1, 1]),
    ]

    for key, title, ylabel, ax in time_panels:
        for sc in scenarios:
            ax.plot(
                sc["years"], sc[key],
                color=SCENARIO_COLORS[sc["name"]],
                linestyle=SCENARIO_STYLES[sc["name"]],
                linewidth=SCENARIO_WIDTHS[sc["name"]],
                label=sc["name"],
            )
        ax.set_title(title, fontsize=8.5)
        ax.set_xlabel("Year", fontsize=8)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.grid(alpha=0.25)
        ax.tick_params(labelsize=7)
        ax.legend(fontsize=6.2, loc="best")
        if key in ("terr", "ocean", "eco_recovery"):
            ax.set_ylim(0.0, 1.05)
            ax.axhline(0.5, color="#bbb", linewidth=0.5, linestyle=":")
        elif key == "thermal":
            ax.set_ylim(0.0, 1.05)
            ax.axhline(0.5, color="#bbb", linewidth=0.5, linestyle=":")

    # ---- Scale factor sweep panel ----
    ax_sw = axes[1, 2]
    sv = sweep["sweep_values"]

    ax_sw.semilogx(
        sv, sweep["tech_co2"],
        color=SCENARIO_COLORS["4. Direct Cooling Technologies Only"],
        linewidth=2.0, linestyle=":", label="4. Direct Tech Only",
    )
    ax_sw.semilogx(
        sv, sweep["integ_co2"],
        color=SCENARIO_COLORS["5. Full Integrated"],
        linewidth=2.5, label="5. Full Integrated",
    )

    # Constant reference lines for non-tech scenarios
    refs = [
        ("1. Baseline",                      "-"),
        ("2. Decarbonization Only",           "--"),
        ("3. Natural Sink Restoration Only",  "-."),
    ]
    for sc in scenarios:
        for ref_name, ls in refs:
            if sc["name"] == ref_name:
                lbl = f"{ref_name} ({sc['co2_pressure'][-1]:.3f})"
                ax_sw.axhline(
                    sc["co2_pressure"][-1],
                    color=SCENARIO_COLORS[ref_name],
                    linestyle=ls, linewidth=1.2, alpha=0.80,
                    label=lbl,
                )

    # 2025 starting CO2 reference
    ax_sw.axhline(
        0.55, color="#888", linewidth=0.8, linestyle="--", alpha=0.55,
        label="2025 start (0.550)",
    )

    # Named scale ticks on log x-axis
    ax_sw.set_xticks([0.001, 0.01, 0.05, 0.20, 1.0])
    ax_sw.set_xticklabels(
        ["local\n.001", "city\n.01", "regional\n.05", "continental\n.20", "planetary\n1.0"],
        fontsize=6.5,
    )

    ax_sw.set_title(
        "Relative Intervention Scale Requirement\n(CO₂ Pressure at 2099 vs. Deployment Scale)",
        fontsize=8.5,
    )
    ax_sw.set_xlabel("Deployment scale factor (log)", fontsize=8)
    ax_sw.set_ylabel("CO₂ pressure at 2099", fontsize=8)
    ax_sw.grid(alpha=0.25)
    ax_sw.tick_params(axis="y", labelsize=7)
    ax_sw.legend(fontsize=5.8, loc="upper right")

    plt.tight_layout()
    out_path = "figures/intervention_technology_model_output.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"  -> Saved: {out_path}")
    plt.show()


# -----------------------------------------------------------------
# 8.  Main
# -----------------------------------------------------------------

def main() -> None:
    print("=" * 72)
    print("  Intervention Technology Model (2025-2099)")
    print("  Technologies: OBS | OTU | UMC | Humus Recycling | Desert Greening")
    print("  Scale: planetary (1.0) for main run; scale sweep 0.001 -> 1.0")
    print("  WARNING: HYPOTHETICAL CONCEPTUAL MODEL -- See MODEL_LIMITATIONS.md")
    print("=" * 72)

    start  = TechStartingState()
    params = TechParameters()
    engine = InterventionEngine(start, params)

    print("\n  Running 5 scenarios at planetary scale (scale_factor = 1.0)...\n")
    scenarios = engine.run_all_scenarios(scale_factor=1.0)
    print_scenario_summary(scenarios)

    print("  CO2 pressure at 2099 summary:")
    for sc in scenarios:
        print(
            f"    {sc['name']:<44}  CO2-P: {sc['co2_pressure'][-1]:.3f}"
            f"  Thermal: {sc['thermal'][-1]:.3f}"
            f"  EcoRec: {sc['eco_recovery'][-1]:.3f}"
        )

    print("\n  Running scale factor sweep (40 points, log-spaced 0.001 to 1.0)...")
    sweep = engine.run_scale_sweep()

    print("\n  CO2 pressure at 2099 by deployment scale:")
    print(f"  {'Scale':<14}  {'Factor':>7}  {'Tech-Only':>10}  {'Full Integ':>10}")
    print("  " + "-" * 46)
    for name, sf in SCALE_FACTORS.items():
        idx = int(np.argmin(np.abs(sweep["sweep_values"] - sf)))
        print(
            f"  {name:<14}  {sf:>7.3f}  "
            f"{sweep['tech_co2'][idx]:>10.3f}  "
            f"{sweep['integ_co2'][idx]:>10.3f}"
        )

    print()
    print("  Key conceptual conclusions (HYPOTHETICAL -- illustrative only):")
    print("  - OBS + OTU enhance ocean carbon uptake capacity.")
    print("    At local/city scale the planetary effect is negligible.")
    print("    Significant effect requires continental-to-planetary deployment.")
    print("  - UMC reduces thermal stress, slowing the warming feedback loop")
    print("    that degrades land and ocean fixation systems.")
    print("  - HRS improves soil microbial health and terrestrial fixation.")
    print("  - DGS adds new carbon fixation area in previously degraded land.")
    print("  - Direct Cooling Technologies alone cannot stop CO2 accumulation")
    print("    if emissions continue: emission reduction remains necessary.")
    print("  - Only the Full Integrated approach addresses all pathways:")
    print("    emission reduction + natural restoration + direct technologies.")
    print("  - Ecosystem Recovery Index is highest in the Full Integrated")
    print("    scenario and lowest in BAU, illustrating the compound benefit.")
    print()
    print("  WARNING: All values are HYPOTHETICAL. Field validation, ecological")
    print("  risk assessment, and scale testing are required for all technologies.")
    print("  See MODEL_LIMITATIONS.md.")
    print("=" * 72)

    plot_results(scenarios, sweep)


if __name__ == "__main__":
    main()
