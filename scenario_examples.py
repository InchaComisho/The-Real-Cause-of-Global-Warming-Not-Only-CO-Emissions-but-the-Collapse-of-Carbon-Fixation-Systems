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
      (~net zero by ~2050). Optimistic policy assumption.
      No active restoration of carbon fixation systems.
      NOT a realistic global prediction — treats all nations as meeting targets.
      Accumulated ocean heat, thermal inertia, and locked-in baseline warming
      mean thermal stress cannot return to pre-industrial levels without
      direct cooling technology.

  Scenario 2b — Realistic Global Decarbonization Only:
      Developed-country emission cuts are MORE THAN OFFSET by:
        - developing-country industrialization and energy demand growth
        - population-driven demand growth
        - ongoing energy infrastructure buildout in emerging economies
      Net global emissions GROW slightly (net_global_decarbonization_rate < 0).
      Land carbon fixation does not recover.
      Ocean carbon uptake does not recover.
      Soil microbial health remains degraded.
      Degradation release continues.
      Legacy warming pressure continues.
      Carbon sink deficit remains unresolved.
      Thermal inertia and ocean heat content continue driving warming.
      Recurring heat shocks damage sinks faster than they can recover.
      Recovery time deficit accumulates — ecosystems never catch up.
      No direct cooling technology is present.
      Result: CO2 accumulation continues AND thermal stress stays in danger zone.
      2099 CO2 pressure still above 1.0; thermal stress above 0.70.
      This is NOT a recovery pathway — only a marginally slower BAU.

  Scenario 3 — Fixation Restoration Only:
      Active restoration of forests, soils, and marine ecosystems.
      No change in emission trajectory (emissions continue growing at BAU pace).
      Fixation capacity recovers gradually, but warming feedback from continuing
      high emissions counteracts restoration gains.
      Thermal stress remains high because emission-driven warming continues.

  Scenario 4 — Integrated Nature-Complementary Approach:
      Aggressive emission reduction (announced decarbonization pace).
      Active restoration of terrestrial and marine carbon fixation systems.
      Both pathways addressed simultaneously.
      Best achievable outcome WITHOUT direct thermal cooling technology.
      Thermal stress cannot fall below the locked-in baseline warming floor
      (baseline_temperature_rise) without UMC/OBS/OTU-type interventions —
      direct planetary cooling is required to go further.

Purpose: To illustrate that (1) the multi-cause hypothesis implies
different policy priorities than the single-cause (emissions-only) model,
and (2) "decarbonization only" is not a single physical process but a
policy assumption whose real-world effectiveness depends on whether global
total emissions actually decline — which has not been structurally achieved
as of the model's publication date — and (3) emissions reduction alone does
not remove accumulated ocean heat, thermal inertia, recurring heat shocks,
or degraded carbon sink deficits.

COVID-19 note:
  Global emissions temporarily declined in 2020 due to pandemic-related
  activity reductions. This is treated as a temporary external shock, not
  as evidence of sustained structural decarbonization.

Change log (v2):
  - Removed max(0.0, ...) floor from _co2_delta to allow CO2 drawdown.
  - Added co2_pressure (unbounded) alongside co2 (clipped [0,1]).

Change log (v3):
  - Split "Decarbonization Only" into 2a (announced) and 2b (realistic).
  - Added realistic decomposition parameters.
  - run_scenario gains `realistic_decarb` flag.
  - "Integrated Approach" renamed to "Integrated Nature-Complementary Approach".

Change log (v4):
  - Revised Realistic Global Decarbonization Only (2b) to model a world
    where developing-world growth EXCEEDS developed-world cuts:
      net_global_decarbonization_rate = -0.002 / yr  (net emission GROWTH)
  - emission block now uses np.clip(..., floor, 1.0) to correctly cap growth.
  - 2b at 2099 now ~1.02-1.06 (above 1.0).

Change log (v5):
  - Added six thermal-inertia / recovery-deficit parameters to
    ScenarioParameters (all HYPOTHETICAL):
      baseline_temperature_rise    — locked-in warming floor; thermal stress
                                     cannot fall below this without direct cooling
      ocean_heat_inertia           — per-year upward pressure from ocean heat content
      recurring_heat_shock         — thermal stress spike per heat shock event
      sink_degradation_frequency   — frequency of major heat shock events
      recovery_time_deficit_rate   — per-year deficit accumulation rate
      direct_cooling_absence_penalty — per-year residual thermal pressure without
                                     UMC/OBS/OTU-type direct cooling technology
    Also added three HYPOTHETICAL pre-degradation baseline capacity parameters:
      baseline_terrestrial_capacity, baseline_soil_capacity,
      baseline_ocean_capacity
  - StartingState gains `thermal_stress` initial value (HYPOTHETICAL: 0.42).
  - run_scenario now tracks four new state arrays (all HYPOTHETICAL):
      thermal_stress_index     — proxy for atmospheric/oceanic thermal state
      carbon_sink_deficit      — how far sinks have fallen below pre-degradation baseline
      recovery_time_deficit    — cumulative gap between heat shock frequency and
                                 ecosystem recovery time
      ecosystem_recovery_index — composite health indicator (terr, soil, ocean, thermal)
  - Structural constraint (2b danger zone): thermal_stress_index cannot fall
    below baseline_temperature_rise in scenarios without direct cooling.
    Result: 2b thermal stress stays in danger zone (>0.70) through 2099.
    This is NOT a recovery pathway.
  - Plots updated from 2×2 to 2×3 (six panels), adding thermal stress index
    and ecosystem recovery index panels; carbon sink deficit shown as third panel.
  - Summary tables updated: Table 1 shows CO2/emission/terr/ocean;
    Table 2 shows thermal stress / sink deficit / recovery deficit / eco recovery.
  - run_scenario gains optional `has_direct_cooling` parameter (default False
    for all scenarios in this module; used by intervention_technology_model.py).

⚠️  IMPORTANT LIMITATIONS
    All parameters, rates, and trajectories are HYPOTHETICAL.
    These scenarios are conceptual illustrations, not climate projections.
    They are NOT calibrated against real data and should NOT be used
    for policy decisions, scientific claims, or quantitative comparison
    with IPCC or other validated model outputs.
    See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Cruz, Real, Lola
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
    # v5: locked-in thermal stress at 2025 (HYPOTHETICAL)
    # Reflects accumulated warming already committed by past emissions.
    thermal_stress:        float = 0.42


# ─────────────────────────────────────────────────────────────────
# 2. Scenario Parameters
# ─────────────────────────────────────────────────────────────────

@dataclass
class ScenarioParameters:
    """
    Parameters controlling the 75-year forward simulation.
    All rates are HYPOTHETICAL and per-year unless otherwise noted.
    """
    projection_years: int = 75

    # ── Emission trajectories ─────────────────────────────────────
    # HYPOTHETICAL: announced decarbonization rate (policy-target pace; ~net zero by 2050)
    emission_reduction_rate: float = 0.018
    # HYPOTHETICAL: annual emission growth in BAU
    bau_emission_growth: float = 0.004

    # ── Realistic global decarbonization decomposition (v3/v4) ───
    # HYPOTHETICAL: rate at which developed-nation blocs cut annual emissions
    developed_country_reduction_rate:    float = 0.018
    # HYPOTHETICAL: annual emission expansion from developing-nation industrialization
    # (v4: raised to 0.010 — aggressive emerging-economy buildout)
    developing_country_emissions_growth: float = 0.010
    # HYPOTHETICAL: additional demand from global population increase
    # (v4: raised to 0.004)
    population_energy_demand_growth:     float = 0.004
    # HYPOTHETICAL: ongoing industrialization pressure (energy infrastructure buildout)
    # (v4: raised to 0.006)
    industrialization_pressure:          float = 0.006
    # HYPOTHETICAL: net global effective rate
    #   = developed_country_reduction_rate
    #     - developing_country_emissions_growth
    #     - population_energy_demand_growth
    #     - industrialization_pressure
    #   = 0.018 - 0.010 - 0.004 - 0.006 = -0.002 / yr
    #
    # SIGN CONVENTION:
    #   positive  = net global emission DECLINE (developed cuts exceed developing growth)
    #   negative  = net global emission GROWTH  (developing growth exceeds developed cuts)
    #
    # v4 uses -0.002: developing-world growth MORE THAN OFFSETS developed-world cuts.
    # This is NOT a recovery pathway. CO2 pressure rises through 2099.
    net_global_decarbonization_rate:     float = -0.002
    # HYPOTHETICAL: emission floor (lower bound for any decline scenario)
    realistic_emission_floor:            float = 0.10

    # ── Fixation restoration rates ────────────────────────────────
    # HYPOTHETICAL: annual improvement in terrestrial fixation under active restoration
    terrestrial_restoration_rate: float = 0.008
    # HYPOTHETICAL: annual improvement in soil health under regenerative agriculture
    soil_restoration_rate:        float = 0.006
    # HYPOTHETICAL: annual improvement in ocean uptake under marine ecosystem recovery
    ocean_restoration_rate:       float = 0.005

    # ── Passive degradation rates (without intervention) ─────────
    # HYPOTHETICAL: continued passive decline even without new pressure
    passive_terr_decline:  float = 0.003
    passive_soil_decline:  float = 0.002
    passive_ocean_decline: float = 0.002

    # ── CO₂ balance sensitivity ───────────────────────────────────
    # HYPOTHETICAL: weights for how each system contributes to CO₂ balance
    terr_co2_weight:   float = 0.35
    soil_co2_weight:   float = 0.25
    ocean_co2_weight:  float = 0.30
    degrad_co2_weight: float = 0.10

    # HYPOTHETICAL: warming feedback into continued fixation decline
    warming_feedback_strength: float = 0.08

    # ── v5: Thermal inertia and heat shock parameters ─────────────
    # All of the following are HYPOTHETICAL.

    # HYPOTHETICAL: locked-in baseline warming floor from past emission accumulation.
    # Even if emissions decline to zero, this floor persists without direct cooling
    # technology (e.g., UMC, OBS, OTU-type interventions). Thermal stress cannot fall
    # below this threshold in scenarios that lack direct planetary cooling.
    baseline_temperature_rise: float = 0.42

    # HYPOTHETICAL: per-year upward thermal pressure from accumulated ocean heat content.
    # Ocean heat content cannot be rapidly discharged; it continues driving surface warming
    # independent of current emission levels.
    ocean_heat_inertia: float = 0.006

    # HYPOTHETICAL: thermal stress added to the system per recurring heat shock event
    # (heat waves, marine heat waves, compound droughts). Such events are expected to
    # recur more frequently as baseline temperature rises.
    recurring_heat_shock: float = 0.06

    # HYPOTHETICAL: frequency parameter controlling how often major heat shock events
    # occur. Default 0.10 → one event per int(1/0.10) = 10 years.
    # Also proxies the rate at which heat damages sink capacity between events.
    sink_degradation_frequency: float = 0.10

    # HYPOTHETICAL: per-year recovery time deficit accumulation rate.
    # Represents the gap between how soon the next heat shock arrives and how much
    # time ecosystems need to recover from the previous one.
    # Accumulates faster under heat shocks; decreases slowly under active restoration.
    recovery_time_deficit_rate: float = 0.012

    # HYPOTHETICAL: per-year residual thermal stress penalty for absence of direct
    # cooling technology (UMC, OBS, OTU-type interventions). Without these,
    # thermal stress cannot return to pre-industrial baseline even after full
    # emission cuts, because ocean heat and atmospheric inertia persist.
    direct_cooling_absence_penalty: float = 0.008

    # ── v5: Pre-degradation baseline sink capacities ──────────────
    # Used to compute carbon_sink_deficit (how far below pre-degradation baseline
    # the current sinks have fallen). All HYPOTHETICAL.
    baseline_terrestrial_capacity: float = 0.90
    baseline_soil_capacity:        float = 0.85
    baseline_ocean_capacity:       float = 0.85


# ─────────────────────────────────────────────────────────────────
# 3. Scenario Engine
# ─────────────────────────────────────────────────────────────────

class ScenarioEngine:
    """
    Projects climate system state forward under five scenarios.
    All dynamics are HYPOTHETICAL and conceptual.
    """

    def __init__(self, start: StartingState, params: ScenarioParameters):
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
        drawdown. The clipped `co2` variable is still clamped in
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
        has_direct_cooling:  bool = False,
    ) -> Dict[str, np.ndarray]:
        """
        Run a single scenario for projection_years timesteps.

        Parameters
        ----------
        reduce_emissions     : apply a decarbonization trajectory
        restore_terrestrial  : apply soil and forest restoration
        restore_ocean        : apply marine ecosystem restoration
        realistic_decarb     : when reduce_emissions=True, use net_global_decarbonization_rate
                               instead of emission_reduction_rate.
                               A negative net rate means net global emission GROWTH
                               (developing-world growth exceeds developed-world cuts).
        has_direct_cooling   : whether UMC/OBS/OTU-type direct cooling technology is active.
                               If False (default for all scenarios in this module),
                               thermal stress cannot fall below baseline_temperature_rise.
                               Used by intervention_technology_model.py for tech scenarios.
        """
        T = self.params.projection_years
        p = self.params
        s = self.start

        years        = np.arange(s.year, s.year + T)
        emission     = np.zeros(T)
        terr         = np.zeros(T)
        soil         = np.zeros(T)
        ocean        = np.zeros(T)
        co2          = np.zeros(T)   # clipped [0,1] — kept for backward compatibility
        co2_pressure = np.zeros(T)   # unbounded — used for comparison plots

        # v5: new state arrays (all HYPOTHETICAL)
        thermal_stress_index     = np.zeros(T)
        carbon_sink_deficit      = np.zeros(T)
        recovery_time_deficit    = np.zeros(T)
        ecosystem_recovery_index = np.zeros(T)

        # ── Initial values ─────────────────────────────────────────
        emission[0]     = s.emission_rate
        terr[0]         = s.terrestrial_fixation
        soil[0]         = s.soil_microbial_health
        ocean[0]        = s.ocean_uptake_capacity
        co2[0]          = s.co2_index
        co2_pressure[0] = s.co2_index

        thermal_stress_index[0] = s.thermal_stress

        # Initial carbon sink deficit: how far below pre-degradation baseline (HYPOTHETICAL)
        carbon_sink_deficit[0] = max(0.0,
            p.terr_co2_weight  * max(0.0, p.baseline_terrestrial_capacity - s.terrestrial_fixation) +
            p.soil_co2_weight  * max(0.0, p.baseline_soil_capacity         - s.soil_microbial_health) +
            p.ocean_co2_weight * max(0.0, p.baseline_ocean_capacity        - s.ocean_uptake_capacity)
        )
        # HYPOTHETICAL initial deficit at 2025:
        # 0.35*(0.90-0.62) + 0.25*(0.85-0.52) + 0.30*(0.85-0.68) ≈ 0.23

        # HYPOTHETICAL: pre-existing recovery time deficit at 2025
        recovery_time_deficit[0] = 0.15

        ecosystem_recovery_index[0] = (
            s.terrestrial_fixation  * 0.30 +
            s.soil_microbial_health * 0.25 +
            s.ocean_uptake_capacity * 0.25 +
            (1.0 - s.thermal_stress) * 0.20
        )

        # HYPOTHETICAL: heat shock recurrence interval (years)
        shock_interval = max(1, int(1.0 / p.sink_degradation_frequency))  # default = 10

        for t in range(1, T):

            # ── Emission trajectory ────────────────────────────────
            if reduce_emissions:
                if realistic_decarb:
                    # HYPOTHETICAL: net global emission change per year.
                    # positive net_global_decarbonization_rate → emission declines
                    # negative net_global_decarbonization_rate → emission grows
                    # np.clip ensures floor ≤ emission ≤ 1.0 in both directions.
                    raw = emission[t - 1] - p.net_global_decarbonization_rate
                    emission[t] = float(np.clip(raw, p.realistic_emission_floor, 1.0))
                else:
                    # HYPOTHETICAL: announced policy-target pace (~net zero by 2050)
                    emission[t] = max(0.02, emission[t - 1] - p.emission_reduction_rate)
            else:
                emission[t] = min(1.0, emission[t - 1] + p.bau_emission_growth)

            # ── Warming feedback (CO₂ → continued fixation decline) ─
            warming_pressure = p.warming_feedback_strength * co2[t - 1]

            # ── Terrestrial fixation ───────────────────────────────
            if restore_terrestrial:
                terr_change = p.terrestrial_restoration_rate - warming_pressure * 0.5
            else:
                terr_change = -(p.passive_terr_decline + warming_pressure * 0.3)
            terr[t] = max(0.0, min(1.0, terr[t - 1] + terr_change * 0.3))

            # ── Soil carbon fixation ───────────────────────────────
            if restore_terrestrial:
                soil_change = p.soil_restoration_rate - warming_pressure * 0.3
            else:
                soil_change = -(p.passive_soil_decline + warming_pressure * 0.2)
            soil[t] = max(0.0, min(1.0, soil[t - 1] + soil_change * 0.3))

            # ── Ocean uptake ───────────────────────────────────────
            if restore_ocean:
                ocean_change = p.ocean_restoration_rate - warming_pressure * 0.2
            else:
                ocean_change = -(p.passive_ocean_decline + warming_pressure * 0.2)
            ocean[t] = max(0.0, min(1.0, ocean[t - 1] + ocean_change * 0.3))

            # ── CO₂ accumulation ───────────────────────────────────
            delta = self._co2_delta(emission[t], terr[t], soil[t], ocean[t], p)
            co2[t]          = max(0.0, min(1.0, co2[t - 1] + delta))
            co2_pressure[t] = co2_pressure[t - 1] + delta   # unbounded

            # ── v5: Heat shock event flag ──────────────────────────
            # HYPOTHETICAL: major heat shock event occurs every shock_interval years.
            heat_shock_this_year = (t % shock_interval == 0)

            # ── v5: Thermal stress index ───────────────────────────
            # Warming drivers: ocean heat inertia + emission-driven warming +
            #   accumulated CO₂ pressure + penalty for no direct cooling technology.
            # Cooling drivers: active fixation + ocean uptake + lower emissions.
            # HYPOTHETICAL — see MODEL_LIMITATIONS.md.
            warming_driver = (
                p.ocean_heat_inertia          +   # stored ocean heat (always upward)
                emission[t]  * 0.06           +   # current emission → new warming
                co2_pressure[t - 1] * 0.025       # accumulated CO₂ → continued warming
            )
            if not has_direct_cooling:
                # HYPOTHETICAL: residual thermal pressure without active cooling tech
                warming_driver += p.direct_cooling_absence_penalty

            cooling_driver = (
                terr[t]  * 0.030 +   # land fixation helps remove CO₂ → less warming
                ocean[t] * 0.020 +   # ocean uptake similarly
                (1.0 - emission[t]) * 0.010   # lower emissions → less new heat added
            )

            delta_thermal = (warming_driver - cooling_driver) * 0.08

            # HYPOTHETICAL: thermal spike from recurring heat shock event
            if heat_shock_this_year:
                delta_thermal += p.recurring_heat_shock * 0.08

            # Floor: locked-in baseline warming (irreducible without direct cooling).
            # HYPOTHETICAL: represents committed warming from past emission accumulation.
            thermal_floor = 0.10 if has_direct_cooling else p.baseline_temperature_rise
            thermal_stress_index[t] = float(np.clip(
                thermal_stress_index[t - 1] + delta_thermal,
                thermal_floor, 1.0
            ))

            # ── v5: Carbon sink deficit ────────────────────────────
            # How far below pre-degradation capacity the sinks currently are (HYPOTHETICAL).
            # Zero = fully recovered to pre-degradation baseline.
            # High = sinks deeply compromised relative to baseline.
            carbon_sink_deficit[t] = max(0.0,
                p.terr_co2_weight  * max(0.0, p.baseline_terrestrial_capacity - terr[t])  +
                p.soil_co2_weight  * max(0.0, p.baseline_soil_capacity         - soil[t]) +
                p.ocean_co2_weight * max(0.0, p.baseline_ocean_capacity        - ocean[t])
            )

            # ── v5: Recovery time deficit ──────────────────────────
            # Accumulates when heat shocks recur faster than ecosystem recovery (HYPOTHETICAL).
            # Heat shock year: large addition (ecosystem damaged before recovery complete).
            # Active restoration: slow recovery of the deficit.
            # No restoration: slow passive accumulation (not fully recovering between events).
            if heat_shock_this_year:
                rtd_delta = p.recovery_time_deficit_rate * 3.0   # shock → large deficit spike
            elif restore_terrestrial:
                rtd_delta = -0.003   # active restoration → partial time-deficit recovery
            else:
                rtd_delta = p.recovery_time_deficit_rate * 0.5   # slow passive accumulation
            recovery_time_deficit[t] = float(np.clip(
                recovery_time_deficit[t - 1] + rtd_delta, 0.0, 1.0
            ))

            # ── v5: Ecosystem recovery index ───────────────────────
            # Composite indicator of overall ecosystem health (HYPOTHETICAL).
            # Higher = healthier system, lower = more degraded.
            ecosystem_recovery_index[t] = (
                terr[t]  * 0.30 +
                soil[t]  * 0.25 +
                ocean[t] * 0.25 +
                (1.0 - thermal_stress_index[t]) * 0.20
            )

        return {
            "name":                     name,
            "years":                    years,
            "emission":                 emission,
            "terr":                     terr,
            "soil":                     soil,
            "ocean":                    ocean,
            "co2":                      co2,
            "co2_pressure":             co2_pressure,
            # v5 additions
            "thermal_stress_index":     thermal_stress_index,
            "carbon_sink_deficit":      carbon_sink_deficit,
            "recovery_time_deficit":    recovery_time_deficit,
            "ecosystem_recovery_index": ecosystem_recovery_index,
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
    "1. Business as Usual":                       "#C0392B",   # red
    "2a. Announced Decarbonization Only":          "#F0B27A",   # light orange (optimistic)
    "2b. Realistic Global Decarbonization Only":   "#E67E22",   # dark orange  (realistic)
    "3. Fixation Restoration Only":                "#2980B9",   # blue
    "4. Integrated Nature-Complementary Approach": "#27AE60",   # green
}
SCENARIO_STYLES = {
    "1. Business as Usual":                       "-",
    "2a. Announced Decarbonization Only":          "--",
    "2b. Realistic Global Decarbonization Only":   ":",
    "3. Fixation Restoration Only":                "-.",
    "4. Integrated Nature-Complementary Approach": "-",
}
SCENARIO_WIDTHS = {
    "1. Business as Usual":                       1.5,
    "2a. Announced Decarbonization Only":          1.5,
    "2b. Realistic Global Decarbonization Only":   1.5,
    "3. Fixation Restoration Only":                1.5,
    "4. Integrated Nature-Complementary Approach": 2.2,
}


def plot_scenario_comparison(scenarios: List[Dict]) -> None:
    import os
    os.makedirs("figures", exist_ok=True)

    # v5: 2×3 layout (six panels) — adds thermal stress and ecosystem recovery
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(
        "Scenario Comparison: Five Climate Intervention Strategies (2025–2099)\n"
        "2a = Announced Decarb (optimistic policy)   |   "
        "2b = Realistic Global Decarb (net emission growth -- NOT a recovery pathway)\n"
        "WARNING: HYPOTHETICAL CONCEPTUAL VALUES -- Not climate projections. Not calibrated against real data.",
        fontsize=9, fontweight="bold", color="#8B0000",
    )

    panels = [
        # (key,                       title,                                    ax)
        ("co2_pressure",             "CO₂ Pressure (Unbounded)",               axes[0, 0]),
        ("thermal_stress_index",     "Thermal Stress Index (v5, HYPOTHETICAL)", axes[0, 1]),
        ("carbon_sink_deficit",      "Carbon Sink Deficit (v5, HYPOTHETICAL)",  axes[0, 2]),
        ("emission",                 "Emission Rate",                           axes[1, 0]),
        ("terr",                     "Terrestrial Fixation Capacity",           axes[1, 1]),
        ("ecosystem_recovery_index", "Ecosystem Recovery Index (v5)",           axes[1, 2]),
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
        ax.legend(fontsize=6.5, loc="best")
        ax.tick_params(labelsize=7)

        # Panel-specific axes and reference lines
        if key == "co2_pressure":
            ax.set_ylabel("Unbounded accumulation index", fontsize=8)
            ax.axhline(0.55, color="#999", linewidth=0.6, linestyle=":",
                       label="2025 start (0.55)")
            ax.axhline(1.0, color="#C0392B", linewidth=0.8, linestyle="--",
                       label="Danger threshold (1.0)")

        elif key == "thermal_stress_index":
            ax.set_ylabel("Normalized [0–1]", fontsize=8)
            ax.set_ylim(0, 1.05)
            ax.axhline(0.70, color="#E67E22", linewidth=0.8, linestyle="--",
                       label="Danger zone threshold (0.70)")
            ax.axhline(0.42, color="#999", linewidth=0.6, linestyle=":",
                       label="Baseline warming floor (0.42)")

        elif key == "carbon_sink_deficit":
            ax.set_ylabel("Weighted normalized deficit [0–1]", fontsize=8)
            ax.set_ylim(0, 0.65)
            ax.axhline(0.23, color="#999", linewidth=0.6, linestyle=":",
                       label="2025 deficit (~0.23)")

        elif key == "emission":
            ax.set_ylabel("Normalized [0–1]", fontsize=8)
            ax.set_ylim(0, 1.05)
            ax.axhline(0.50, color="#999", linewidth=0.6, linestyle=":")

        elif key == "terr":
            ax.set_ylabel("Normalized [0–1]", fontsize=8)
            ax.set_ylim(0, 1.05)
            ax.axhline(0.50, color="#999", linewidth=0.6, linestyle=":")

        elif key == "ecosystem_recovery_index":
            ax.set_ylabel("Normalized composite [0–1]", fontsize=8)
            ax.set_ylim(0, 1.05)
            ax.axhline(0.60, color="#2980B9", linewidth=0.8, linestyle="--",
                       label="Recovery threshold (0.60)")

    plt.tight_layout()
    plt.savefig("figures/scenario_comparison_output.png", dpi=150, bbox_inches="tight")
    print("  -> Saved: figures/scenario_comparison_output.png")
    plt.show()


def print_scenario_summary(scenarios: List[Dict]) -> None:
    checkpoints = [2025, 2035, 2050, 2075, 2099]
    W = 44

    # ── Table 1: CO₂, emission, terrestrial fixation, ocean uptake ──
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

    # ── Table 2: v5 thermal / ecosystem indicators ────────────────
    print(f"\n  {'Scenario':<{W}}  {'Year':>4}  {'ThrStrs':>7}  {'SinkDef':>7}  {'RcvDef':>7}  {'EcoRcv':>7}")
    print("  (v5 HYPOTHETICAL indicators: ThrStrs=thermal stress, SinkDef=carbon sink deficit,")
    print("   RcvDef=recovery time deficit, EcoRcv=ecosystem recovery index)")
    print("  " + "-" * (W + 42))
    for sc in scenarios:
        years = sc["years"]
        for chk in checkpoints:
            if chk in years:
                idx = list(years).index(chk)
                print(
                    f"  {sc['name'][:W]:<{W}}  {chk:>4}  "
                    f"{sc['thermal_stress_index'][idx]:>7.3f}  "
                    f"{sc['carbon_sink_deficit'][idx]:>7.3f}  "
                    f"{sc['recovery_time_deficit'][idx]:>7.3f}  "
                    f"{sc['ecosystem_recovery_index'][idx]:>7.3f}"
                )
        print()


# ─────────────────────────────────────────────────────────────────
# 5. Main
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("  Scenario Comparison (2025-2099)  [v5]")
    print("  1. BAU  |  2a. Announced Decarb  |  2b. Realistic Global Decarb")
    print("  3. Fixation Restoration  |  4. Integrated Nature-Complementary")
    print("  v5: +thermal stress index, +carbon sink deficit,")
    print("      +recovery time deficit, +ecosystem recovery index")
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
        print(f"    {sc['name']:<50}  {sc['co2_pressure'][-1]:.3f}")

    print("\n  Thermal stress index at 2099 (HYPOTHETICAL):")
    for sc in scenarios:
        ts = sc["thermal_stress_index"][-1]
        zone = "DANGER ZONE" if ts >= 0.70 else ("elevated" if ts >= 0.50 else "reduced")
        print(f"    {sc['name']:<50}  {ts:.3f}  [{zone}]")

    gap_co2 = sc_real["co2_pressure"][-1] - sc_ann["co2_pressure"][-1]
    gap_ts  = sc_real["thermal_stress_index"][-1] - sc_ann["thermal_stress_index"][-1]
    print(
        f"\n  Decarbonization realism gap at 2099 (2b minus 2a):"
        f"\n    CO2 pressure:       {gap_co2:+.3f}"
        f"\n    Thermal stress:     {gap_ts:+.3f}"
        "\n  (HYPOTHETICAL -- depends entirely on assumed offset rates)"
    )

    print(
        "\n  Key conceptual conclusions (HYPOTHETICAL -- illustrative only):"
        "\n"
        "\n  - 2b (Realistic) CO2 pressure stays ABOVE 1.0 at 2099."
        "\n    Realistic decarbonization is NOT a recovery pathway."
        "\n    It only marginally slows accumulation relative to BAU."
        "\n"
        "\n  - 2b (Realistic) thermal stress stays IN THE DANGER ZONE (>0.70) at 2099."
        "\n    Emissions reduction alone does not remove:"
        "\n      * accumulated ocean heat content"
        "\n      * thermal inertia (locked-in baseline warming)"
        "\n      * recurring heat shocks and their sink damage"
        "\n      * recovery time deficit (ecosystems cannot recover between events)"
        "\n    Direct cooling technology (UMC/OBS/OTU) would be required to go further."
        "\n"
        "\n  - Without restoring carbon fixation and absorption systems,"
        "\n    atmospheric CO2 pressure does not meaningfully decline."
        "\n    Land fixation, ocean uptake, and soil health remain degraded."
        "\n    Carbon sink deficit and degradation release continue unresolved."
        "\n"
        "\n  - 2a (Announced) reflects an optimistic policy assumption (0.47 CO2-P),"
        "\n    not an observed global structural trend."
        "\n    Even 2a cannot bring thermal stress below the locked-in baseline floor"
        f"   ({params.baseline_temperature_rise:.2f}) without direct cooling technology."
        "\n"
        "\n  - Fixation restoration alone (3) cannot compensate for continuing emissions."
        "\n    High emission-driven warming feedback counteracts restoration gains."
        "\n"
        "\n  - Only Integrated Nature-Complementary (4) addresses both pathways."
        "\n    It reaches the thermal floor but cannot go below it -- direct planetary"
        "\n    cooling is required to move from mitigation to full recovery."
        "\n"
        "\n  - COVID-19 (2020) was a temporary shock, not structural decarbonization."
    )
    print("\n  WARNING: All values are HYPOTHETICAL. See MODEL_LIMITATIONS.md.")
    print("=" * 72)

    plot_scenario_comparison(scenarios)


if __name__ == "__main__":
    main()
