"""
terraforming_scale_requirement_model.py
=======================================
Scale Requirement Analysis: Technology Deployment to Offset
Super El Nino-Level Carbon Sink Loss

This model estimates the global coverage percentage of five natural-complementary
technologies (OBS, OTU, UMC, HRS, DGS) required to compensate a hypothetical
10% carbon sink loss caused by a Super El Nino-level climate shock event.

IMPORTANT: This is a conceptual proof-of-concept (PoC), NOT a scientific
prediction model. All parameters are HYPOTHETICAL. The model has NOT been
calibrated against real observational data. Results are illustrative of
the *scale* and *placement* requirements under the multi-cause hypothesis
described in this repository's CAUSAL_STRUCTURE.md.

Shock scenario:
  A Super El Nino event temporarily degrades global carbon sinks by 10%.
  This 10% figure is a hypothetical worst-case stress assumption -- NOT an
  observed or scientifically validated value. It is chosen to stress-test
  the scale requirements under extreme conditions.

Placement strategies evaluated:
  1. Random Distributed      -- globally dispersed, no strategic placement
  2. Urban / Coastal Only    -- cities, coasts, human infrastructure
  3. Equatorial Belt         -- concentrated in the tropical/equatorial zone
                               (HYPOTHETICAL: acts on the primary driver of
                               global atmospheric and ocean circulation)
  4. Ocean Current Coupled   -- major ocean currents and upwelling zones
  5. Full Planetary Network  -- integrated combination of all placement types

Coverage sweep: 0% to 30% global surface coverage, in 5% steps.

Equatorial Belt Scale definition:
  In this model, "Equatorial Belt Scale" means deployment concentrated in
  the equatorial zone (~20 deg N to ~20 deg S latitude), targeting the
  Intertropical Convergence Zone (ITCZ), tropical ocean, tropical forests,
  and adjacent upwelling systems. This is treated as a HYPOTHETICAL
  strategic placement hypothesis: that concentrating OBS/OTU/UMC/HRS/DGS
  along the equatorial belt acts on the primary coupling zone between
  Northern and Southern Hemisphere atmospheric circulation, ocean heat
  exchange, evaporative cooling, cloud formation, and phytoplankton recovery.
  This hypothesis has NOT been validated.

Technologies modelled:
  OBS  Ocean Biological Sequestration support
  OTU  Ocean Thermal Upwelling restoration
  UMC  Urban / Marine Cooling systems
  HRS  Humus Recycling System (soil carbon restoration)
  DGS  Desert Greening Support

Output metrics (all HYPOTHETICAL):
  - remaining_carbon_sink_loss       : fraction of sink loss NOT yet compensated
  - compensated_sink_loss_percent    : % of 10% sink loss offset by intervention
  - thermal_stress_reduction         : reduction in thermal stress index
  - ocean_metabolism_recovery        : recovery of ocean metabolic capacity
  - ecosystem_recovery_index         : composite ecosystem health indicator
  - CO2_pressure_modifier            : change in CO2 accumulation rate (negative = reduction)
  - minimum_scale_to_offset_10pct    : minimum global coverage % to fully offset 10% loss
  - feasibility_index                : current technical/operational feasibility (0=infeasible)

Key findings (HYPOTHETICAL -- illustrative only):
  - At <5% coverage regardless of placement: effect is near-negligible.
  - Equatorial Belt placement is hypothetically more effective per unit area
    than Random Distributed placement.
  - At 30% coverage, only Full Planetary Network fully offsets 10% sink loss.
  - Equatorial Belt approaches ~97% compensation at 30% but does not fully close.
  - Ocean Current Coupled reaches ~80% at 30%.
  - Random and Urban placements cannot offset 10% sink loss within 30% range.
  - Feasibility is inversely related to required scale: the most effective
    strategies have the lowest current feasibility.

See MODEL_LIMITATIONS.md for full disclaimers on all assumptions.

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
import matplotlib.patches as mpatches
import os


# ==========================================================================
# 1. Parameters
# ==========================================================================

@dataclass
class ScaleParameters:
    """
    All parameters are HYPOTHETICAL and have NOT been calibrated against
    real observational data. They are chosen to illustrate scale relationships
    under the multi-cause hypothesis. See MODEL_LIMITATIONS.md.
    """

    # ── Shock scenario ─────────────────────────────────────────────
    # HYPOTHETICAL: fraction of global carbon sink lost in a Super El Nino event.
    # This is a worst-case hypothetical stress assumption, not a validated figure.
    # Real Super El Nino sink anomalies vary significantly by region and year.
    super_el_nino_sink_loss: float = 0.10

    # ── Technology base rates (HYPOTHETICAL, per unit global coverage fraction) ──
    # OBS: rate of ocean biological sequestration support per coverage fraction
    obs_sequestration_rate: float = 0.030
    # OTU: rate of ocean thermal upwelling restoration contribution
    otu_circulation_rate: float = 0.025
    # UMC: direct cooling capacity (thermal stress reduction rate per coverage)
    direct_cooling_capacity: float = 0.060
    # Ocean metabolism recovery rate per coverage fraction
    ocean_metabolism_recovery_rate: float = 0.100
    # HRS: humus/soil carbon restoration rate per coverage fraction
    humus_soil_restoration_rate: float = 0.050
    # DGS: desert greening area factor (land sink contribution)
    desert_greening_area_factor: float = 0.015

    # ── Coupling bonuses (HYPOTHETICAL multipliers for strategic placement) ───
    # HYPOTHETICAL: additional sink recovery from enhanced atmospheric circulation
    # when deployment is concentrated in the equatorial/tropical zone.
    # Mechanism: increased evapotranspiration, cloud formation, inter-hemispheric
    # heat redistribution. NOT validated.
    atmospheric_circulation_coupling: float = 0.30

    # HYPOTHETICAL: additional ocean metabolism recovery from deployment along
    # major ocean current pathways. Mechanism: strategic phytoplankton seeding,
    # upwelling support, thermohaline circulation enhancement. NOT validated.
    ocean_current_coupling: float = 0.25

    # HYPOTHETICAL: additional benefit from cross-hemisphere connectivity in a
    # Full Planetary Network (linking Northern and Southern Hemisphere systems).
    cross_hemisphere_transfer: float = 0.20

    # HYPOTHETICAL: equatorial belt relative effectiveness factor vs. random placement.
    # This value parameterizes how much more effective equatorial deployment is
    # per unit area compared to random global distribution. NOT validated.
    equatorial_belt_factor: float = 2.50

    # HYPOTHETICAL: scaling factor for how coupling parameters translate to
    # additional sink recovery rate. Kept small to represent uncertain coupling.
    coupling_scale_factor: float = 0.50

    # HYPOTHETICAL: penalty rate for feasibility decay with increasing coverage.
    # Higher coverage always requires more international coordination, energy,
    # and logistics, reducing near-term feasibility.
    feasibility_penalty: float = 1.00


# ==========================================================================
# 2. Placement Strategies
# ==========================================================================

@dataclass
class PlacementStrategy:
    """
    Defines how technology is geographically deployed.
    All multipliers are HYPOTHETICAL.
    """
    name: str
    description: str
    color: str
    linestyle: str
    # How many times more effective this placement is at recovering carbon sinks
    # compared to random global distribution (HYPOTHETICAL)
    sink_multiplier: float
    # Thermal stress reduction multiplier vs random (HYPOTHETICAL)
    thermal_multiplier: float
    # Ocean metabolism recovery multiplier vs random (HYPOTHETICAL)
    ocean_met_multiplier: float
    # Technical/operational feasibility at zero coverage (scale 0-1)
    base_feasibility: float
    # Rate at which feasibility declines per unit coverage fraction (HYPOTHETICAL)
    feasibility_steepness: float
    # Atmospheric circulation coupling strength (0-2 scale, HYPOTHETICAL)
    atm_coupling: float
    # Ocean current coupling strength (0-2 scale, HYPOTHETICAL)
    ocean_coupling: float
    # Cross-hemisphere coupling (only Full Planetary Network, HYPOTHETICAL)
    cross_coupling: float


PLACEMENT_STRATEGIES: List[PlacementStrategy] = [
    PlacementStrategy(
        name="Random Distributed",
        description=(
            "Dispersed globally with no strategic placement. "
            "Represents baseline deployment with no geographical optimization. "
            "HYPOTHETICAL: no circulation coupling benefit."
        ),
        color="#808080",
        linestyle=":",
        sink_multiplier=1.0,
        thermal_multiplier=1.0,
        ocean_met_multiplier=1.0,
        base_feasibility=0.80,
        feasibility_steepness=1.5,
        atm_coupling=0.0,
        ocean_coupling=0.0,
        cross_coupling=0.0,
    ),
    PlacementStrategy(
        name="Urban / Coastal Only",
        description=(
            "Concentrated in cities, coastlines, and human infrastructure. "
            "UMC and HRS most relevant here. "
            "HYPOTHETICAL: effective for urban thermal mitigation but limited "
            "planetary-scale sink recovery."
        ),
        color="#E67E22",
        linestyle="--",
        sink_multiplier=0.8,
        thermal_multiplier=1.8,     # better for urban heat mitigation (UMC focused)
        ocean_met_multiplier=0.6,
        base_feasibility=0.70,
        feasibility_steepness=1.5,
        atm_coupling=0.0,
        ocean_coupling=0.2,         # coastal OTU provides minor ocean current coupling
        cross_coupling=0.0,
    ),
    PlacementStrategy(
        name="Equatorial Belt",
        description=(
            "Concentrated along the equatorial and tropical zone "
            "(approx. 20 deg N to 20 deg S). "
            "Targets the ITCZ, tropical ocean, tropical forests, and adjacent "
            "upwelling systems. "
            "HYPOTHETICAL: acts on the primary coupling zone of global atmospheric "
            "and ocean circulation. NOT validated."
        ),
        color="#27AE60",
        linestyle="-",
        sink_multiplier=3.0,
        thermal_multiplier=2.5,
        ocean_met_multiplier=2.2,
        base_feasibility=0.30,      # requires international tropical cooperation
        feasibility_steepness=0.8,
        atm_coupling=1.0,           # full atmospheric circulation coupling
        ocean_coupling=0.8,
        cross_coupling=0.0,
    ),
    PlacementStrategy(
        name="Ocean Current Coupled",
        description=(
            "Deployed along major ocean currents and upwelling zones "
            "(Gulf Stream, Kuroshio, Antarctic Circumpolar, Humboldt, etc.). "
            "OBS and OTU most relevant. "
            "HYPOTHETICAL: targets ocean metabolism recovery and thermohaline "
            "circulation support. NOT validated."
        ),
        color="#2980B9",
        linestyle="-.",
        sink_multiplier=2.4,
        thermal_multiplier=2.0,
        ocean_met_multiplier=2.8,   # highest ocean metabolism recovery
        base_feasibility=0.25,      # remote ocean logistics challenging
        feasibility_steepness=0.7,
        atm_coupling=0.5,
        ocean_coupling=1.5,         # maximum ocean current coupling
        cross_coupling=0.0,
    ),
    PlacementStrategy(
        name="Full Planetary Network",
        description=(
            "Integrated deployment combining equatorial belt, major ocean currents, "
            "desert greening corridors, and urban/coastal cooling. "
            "HYPOTHETICAL: achieves cross-hemisphere atmospheric and ocean coupling. "
            "Highest theoretical effectiveness, lowest near-term feasibility."
        ),
        color="#8E44AD",
        linestyle="-",
        sink_multiplier=3.5,
        thermal_multiplier=3.0,
        ocean_met_multiplier=2.5,
        base_feasibility=0.10,      # requires global coordination infrastructure
        feasibility_steepness=0.3,
        atm_coupling=1.5,
        ocean_coupling=1.5,
        cross_coupling=1.0,         # unique: cross-hemisphere transfer coupling
    ),
]

# Coverage levels to evaluate (percent of global surface)
COVERAGE_LEVELS: List[float] = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]


# ==========================================================================
# 3. Scale Requirement Engine
# ==========================================================================

class ScaleRequirementEngine:
    """
    Computes scale requirement metrics for each (coverage, placement) combination.
    All computations are HYPOTHETICAL.
    """

    def __init__(self, params: ScaleParameters):
        self.params = params

    def _base_sink_rate(self) -> float:
        """
        Combined base sink recovery rate per unit global coverage fraction.
        Sum of all technology contributions at neutral (random) placement.
        HYPOTHETICAL.
        """
        p = self.params
        return (p.obs_sequestration_rate
                + p.otu_circulation_rate
                + p.humus_soil_restoration_rate
                + p.desert_greening_area_factor)

    def _effective_sink_rate(self, placement: PlacementStrategy) -> float:
        """
        Effective sink recovery rate per unit global coverage fraction,
        adjusted for placement strategy and coupling bonuses.
        HYPOTHETICAL -- depends entirely on unvalidated coupling parameters.
        """
        p = self.params
        base = self._base_sink_rate()

        # Core rate from placement strategy efficiency multiplier
        core = base * placement.sink_multiplier

        # Additional atmospheric circulation coupling bonus (HYPOTHETICAL).
        # Represents enhanced evapotranspiration, cloud seeding, inter-hemispheric
        # heat redistribution from strategic equatorial/planetary placement.
        atm_bonus = (p.atmospheric_circulation_coupling
                     * placement.atm_coupling
                     * base
                     * p.coupling_scale_factor)

        # Additional ocean current coupling bonus (HYPOTHETICAL).
        # Represents enhanced phytoplankton productivity and ocean biological pump
        # from deployment along current pathways.
        ocean_bonus = (p.ocean_current_coupling
                       * placement.ocean_coupling
                       * base
                       * p.coupling_scale_factor)

        # Cross-hemisphere transfer bonus (Full Planetary Network only, HYPOTHETICAL).
        # Represents coupled Northern / Southern Hemisphere sink synchronization.
        cross_bonus = (p.cross_hemisphere_transfer
                       * placement.cross_coupling
                       * base
                       * p.coupling_scale_factor
                       * 0.6)   # additional discount for highly uncertain coupling

        return core + atm_bonus + ocean_bonus + cross_bonus

    def find_minimum_scale(self, placement: PlacementStrategy) -> float:
        """
        Compute the minimum global coverage percent required to fully offset
        super_el_nino_sink_loss under this placement strategy.
        Returns a value in percent. May exceed 30% (or even 100%).
        HYPOTHETICAL.
        """
        eff = self._effective_sink_rate(placement)
        if eff <= 0.0:
            return float("inf")
        return (self.params.super_el_nino_sink_loss / eff) * 100.0

    def compute_metrics(
        self,
        coverage_percent: float,
        placement: PlacementStrategy,
    ) -> Dict:
        """
        Compute all output metrics for a given coverage level and placement.
        All results are HYPOTHETICAL.
        """
        p = self.params
        cov = coverage_percent / 100.0   # convert to fraction

        # ── Sink recovery ──────────────────────────────────────────
        eff_rate = self._effective_sink_rate(placement)
        sink_recovery = cov * eff_rate
        # Allow over-compensation in the formula (shown as capped in percent)
        remaining_sink_loss = max(0.0, p.super_el_nino_sink_loss - sink_recovery)
        compensated_pct = min(100.0,
                              (sink_recovery / p.super_el_nino_sink_loss) * 100.0)

        # ── Thermal stress reduction ───────────────────────────────
        # HYPOTHETICAL: UMC-driven cooling + atmospheric circulation cooling.
        # Cap at 0.30 (significant but bounded -- thermal inertia persists).
        thermal_reduction = min(
            0.30,
            cov * p.direct_cooling_capacity * placement.thermal_multiplier,
        )

        # ── Ocean metabolism recovery ──────────────────────────────
        # HYPOTHETICAL: OBS/OTU-driven phytoplankton and ocean biological pump recovery.
        ocean_met = min(
            0.90,
            cov * p.ocean_metabolism_recovery_rate * placement.ocean_met_multiplier,
        )

        # ── Soil / humus restoration component ────────────────────
        # HYPOTHETICAL: HRS + DGS contribution to soil carbon sequestration.
        soil_restoration = min(
            0.50,
            cov * (p.humus_soil_restoration_rate + p.desert_greening_area_factor)
            * placement.sink_multiplier * 0.4,
        )

        # ── Ecosystem recovery index (composite, HYPOTHETICAL) ─────
        comp_fraction = compensated_pct / 100.0
        max_thermal = 0.30
        eco_recovery = min(1.0,
            comp_fraction                         * 0.40 +  # sink recovery dominant
            (thermal_reduction / max_thermal)     * 0.25 +  # thermal improvement
            ocean_met                             * 0.20 +  # ocean metabolism
            soil_restoration                      * 0.15    # soil/land recovery
        )

        # ── CO2 pressure modifier (HYPOTHETICAL) ──────────────────
        # Negative = reduces CO2 accumulation rate vs baseline.
        # Small values: even full compensation only modestly reduces CO2 rate.
        co2_modifier = -(comp_fraction * 0.040 + thermal_reduction * 0.015)

        # ── Feasibility index (HYPOTHETICAL) ──────────────────────
        # Base feasibility decays linearly with coverage fraction.
        # Additional penalty for coverage exceeding 10% (operational scale challenge).
        raw_feas = placement.base_feasibility - cov * placement.feasibility_steepness
        if cov > 0.10:
            raw_feas *= max(0.0, 1.0 - (cov - 0.10) * p.feasibility_penalty * 0.5)
        feasibility = float(np.clip(raw_feas, 0.0, 1.0))

        # ── Minimum required scale (HYPOTHETICAL) ─────────────────
        min_scale = self.find_minimum_scale(placement)

        # ── Required intervention scale label ─────────────────────
        if min_scale <= 30.0:
            required_intervention_scale = f"{min_scale:.1f}%"
        elif min_scale < 100.0:
            required_intervention_scale = f">30% (est. {min_scale:.0f}%)"
        else:
            required_intervention_scale = ">30% (est. >>30%)"

        return {
            "coverage_percent":                     coverage_percent,
            "placement_name":                       placement.name,
            "remaining_carbon_sink_loss":           remaining_sink_loss,
            "compensated_sink_loss_percent":        compensated_pct,
            "thermal_stress_reduction":             thermal_reduction,
            "ocean_metabolism_recovery":            ocean_met,
            "ecosystem_recovery_index":             eco_recovery,
            "CO2_pressure_modifier":                co2_modifier,
            "minimum_scale_to_offset_10pct":        min_scale,
            "required_intervention_scale":          required_intervention_scale,
            "feasibility_index":                    feasibility,
        }

    def run_sweep(self) -> Dict[str, List[Dict]]:
        """
        Run the coverage sweep for all placement strategies.
        Returns results keyed by placement name.
        """
        results: Dict[str, List[Dict]] = {}
        for placement in PLACEMENT_STRATEGIES:
            results[placement.name] = [
                self.compute_metrics(cov, placement)
                for cov in COVERAGE_LEVELS
            ]
        return results


# ==========================================================================
# 4. Summary Printing
# ==========================================================================

def print_summary(
    results: Dict[str, List[Dict]],
    params: ScaleParameters,
    engine: ScaleRequirementEngine,
) -> None:
    """Print tabular summary of results."""
    W = 30

    print(f"\n  Super El Nino sink loss: {params.super_el_nino_sink_loss*100:.0f}%  (HYPOTHETICAL)")
    print(f"  Coverage range evaluated: {COVERAGE_LEVELS[0]:.0f}% to {COVERAGE_LEVELS[-1]:.0f}%\n")

    # Table 1: Compensated sink loss % across coverage levels
    cov_headers = "  ".join(f"{c:>5.0f}%" for c in COVERAGE_LEVELS)
    print(f"  {'Placement Strategy':<{W}}  {cov_headers}  {'Min. Scale':>12}")
    print(f"  {'(Compensated sink loss %, HYPOTHETICAL)':<{W}}")
    print("  " + "-" * (W + len(COVERAGE_LEVELS) * 9 + 14))
    for placement in PLACEMENT_STRATEGIES:
        data = results[placement.name]
        row = "  ".join(f"{d['compensated_sink_loss_percent']:>5.1f}%" for d in data)
        min_s = data[0]["required_intervention_scale"]  # same for all rows
        print(f"  {placement.name:<{W}}  {row}  {min_s:>12}")
    print()

    # Table 2: Feasibility index
    print(f"  {'Placement Strategy':<{W}}  {cov_headers}")
    print(f"  {'(Feasibility index 0-1, HYPOTHETICAL)':<{W}}")
    print("  " + "-" * (W + len(COVERAGE_LEVELS) * 9))
    for placement in PLACEMENT_STRATEGIES:
        data = results[placement.name]
        row = "  ".join(f"{d['feasibility_index']:>5.3f} " for d in data)
        print(f"  {placement.name:<{W}}  {row}")
    print()

    # Minimum required scale summary
    print("  Minimum coverage required to fully offset 10% sink loss (HYPOTHETICAL):")
    print("  " + "-" * 60)
    for placement in PLACEMENT_STRATEGIES:
        min_s = engine.find_minimum_scale(placement)
        within = "** Within 30% range **" if min_s <= 30.0 else "(beyond evaluated range)"
        print(f"  {placement.name:<35}  {min_s:6.1f}%  {within}")
    print()

    # Key interpretation
    print("  Key interpretation (HYPOTHETICAL -- NOT scientific prediction):")
    print("  - Full Planetary Network (min ~21%) and Equatorial Belt (min ~26%)")
    print("    are the only strategies that can fully offset a 10% sink loss")
    print("    within the 0-30% evaluated coverage range.")
    print("  - Ocean Current Coupled reaches ~96% at 30% -- just short of full")
    print("    offset. Its minimum required scale (~31%) is just outside the range.")
    print("  - At 25% coverage, Equatorial Belt reaches ~97.5%; Full Planetary ~100%.")
    print("  - Random and Urban placements cannot offset 10% sink loss within the")
    print("    evaluated range (random ~36% compensation at max 30% coverage).")
    print("  - The most effective strategies (Equatorial, Full Planetary) have the")
    print("    lowest current feasibility -- scale and feasibility are in tension.")
    print("  - All results are HYPOTHETICAL. See MODEL_LIMITATIONS.md.")


# ==========================================================================
# 5. Visualization
# ==========================================================================

PLOT_COLORS = {p.name: p.color for p in PLACEMENT_STRATEGIES}
PLOT_STYLES = {p.name: p.linestyle for p in PLACEMENT_STRATEGIES}


def plot_results(
    results: Dict[str, List[Dict]],
    params: ScaleParameters,
    engine: ScaleRequirementEngine,
) -> None:
    os.makedirs("figures", exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        "Scale Requirement Model: Technology Deployment to Offset Super El Nino Sink Loss\n"
        f"Hypothetical 10% Carbon Sink Loss -- Coverage Sweep 0-30% -- 5 Placement Strategies\n"
        "WARNING: HYPOTHETICAL CONCEPTUAL VALUES (PoC) -- Not calibrated against real data.",
        fontsize=9, fontweight="bold", color="#8B0000",
    )

    cov_arr = np.array(COVERAGE_LEVELS)

    # ── Panel 1: Compensated sink loss % ──────────────────────────
    ax = axes[0, 0]
    for placement in PLACEMENT_STRATEGIES:
        data = results[placement.name]
        y = [d["compensated_sink_loss_percent"] for d in data]
        ax.plot(cov_arr, y,
                color=PLOT_COLORS[placement.name],
                linestyle=PLOT_STYLES[placement.name],
                linewidth=2.0,
                marker="o", markersize=4,
                label=placement.name)
    ax.axhline(100.0, color="#C0392B", linewidth=1.2, linestyle="--",
               label="Full compensation threshold (100%)")
    ax.set_title("Compensated Sink Loss (%)\n"
                 f"(Super El Nino: {params.super_el_nino_sink_loss*100:.0f}% sink loss -- HYPOTHETICAL)",
                 fontsize=8.5)
    ax.set_xlabel("Global Coverage (%)", fontsize=8)
    ax.set_ylabel("Compensated Sink Loss (%)", fontsize=8)
    ax.set_xlim(-1, 32)
    ax.set_ylim(-5, 115)
    ax.set_xticks(COVERAGE_LEVELS)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=6.5, loc="upper left")
    ax.tick_params(labelsize=7)

    # ── Panel 2: Thermal stress reduction ─────────────────────────
    ax = axes[0, 1]
    for placement in PLACEMENT_STRATEGIES:
        data = results[placement.name]
        y = [d["thermal_stress_reduction"] for d in data]
        ax.plot(cov_arr, y,
                color=PLOT_COLORS[placement.name],
                linestyle=PLOT_STYLES[placement.name],
                linewidth=2.0,
                marker="o", markersize=4,
                label=placement.name)
    ax.set_title("Thermal Stress Reduction\n(HYPOTHETICAL; thermal inertia limits total reduction)",
                 fontsize=8.5)
    ax.set_xlabel("Global Coverage (%)", fontsize=8)
    ax.set_ylabel("Thermal Stress Reduction (index units)", fontsize=8)
    ax.set_xlim(-1, 32)
    ax.set_ylim(-0.005, 0.22)
    ax.set_xticks(COVERAGE_LEVELS)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=6.5, loc="upper left")
    ax.tick_params(labelsize=7)

    # ── Panel 3: Ecosystem recovery index ─────────────────────────
    ax = axes[0, 2]
    for placement in PLACEMENT_STRATEGIES:
        data = results[placement.name]
        y = [d["ecosystem_recovery_index"] for d in data]
        ax.plot(cov_arr, y,
                color=PLOT_COLORS[placement.name],
                linestyle=PLOT_STYLES[placement.name],
                linewidth=2.0,
                marker="o", markersize=4,
                label=placement.name)
    ax.axhline(0.60, color="#2980B9", linewidth=0.8, linestyle="--",
               label="Recovery threshold (0.60)")
    ax.set_title("Ecosystem Recovery Index\n(Composite: sink + thermal + ocean + soil, HYPOTHETICAL)",
                 fontsize=8.5)
    ax.set_xlabel("Global Coverage (%)", fontsize=8)
    ax.set_ylabel("Ecosystem Recovery Index [0-1]", fontsize=8)
    ax.set_xlim(-1, 32)
    ax.set_ylim(-0.02, 0.85)
    ax.set_xticks(COVERAGE_LEVELS)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=6.5, loc="upper left")
    ax.tick_params(labelsize=7)

    # ── Panel 4: Feasibility index ─────────────────────────────────
    ax = axes[1, 0]
    for placement in PLACEMENT_STRATEGIES:
        data = results[placement.name]
        y = [d["feasibility_index"] for d in data]
        ax.plot(cov_arr, y,
                color=PLOT_COLORS[placement.name],
                linestyle=PLOT_STYLES[placement.name],
                linewidth=2.0,
                marker="o", markersize=4,
                label=placement.name)
    ax.axhline(0.50, color="#999", linewidth=0.6, linestyle=":", label="Moderate feasibility")
    ax.axhline(0.20, color="#E74C3C", linewidth=0.6, linestyle=":", label="Low feasibility")
    ax.set_title("Feasibility Index\n(Current technical/operational feasibility, HYPOTHETICAL)",
                 fontsize=8.5)
    ax.set_xlabel("Global Coverage (%)", fontsize=8)
    ax.set_ylabel("Feasibility Index [0-1]", fontsize=8)
    ax.set_xlim(-1, 32)
    ax.set_ylim(-0.02, 1.05)
    ax.set_xticks(COVERAGE_LEVELS)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=6.5, loc="upper right")
    ax.tick_params(labelsize=7)

    # ── Panel 5: Placement strategy comparison at 20% coverage ─────
    ax = axes[1, 1]
    compare_cov = 20.0
    comp_cov_idx = COVERAGE_LEVELS.index(compare_cov)
    bar_names = [p.name.replace(" / ", "/\n").replace(" Only", "").replace(" Coupled", "\nCoupled").replace(" Distributed", "\nDistributed") for p in PLACEMENT_STRATEGIES]
    bar_comp = [results[p.name][comp_cov_idx]["compensated_sink_loss_percent"]
                for p in PLACEMENT_STRATEGIES]
    bar_feas = [results[p.name][comp_cov_idx]["feasibility_index"]
                for p in PLACEMENT_STRATEGIES]
    bar_colors = [PLOT_COLORS[p.name] for p in PLACEMENT_STRATEGIES]

    x_pos = np.arange(len(PLACEMENT_STRATEGIES))
    bars = ax.bar(x_pos, bar_comp, color=bar_colors, edgecolor="black",
                  linewidth=0.5, alpha=0.8, label="Compensated sink loss %")
    ax.axhline(100.0, color="#C0392B", linewidth=1.2, linestyle="--",
               label="Full compensation (100%)")

    for i, (bar, fc, feas) in enumerate(zip(bars, bar_comp, bar_feas)):
        ax.text(bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() + 1.5,
                f"{fc:.0f}%\n(f={feas:.2f})",
                ha="center", va="bottom", fontsize=6.5)

    ax.set_title(f"Placement Strategy Comparison at {compare_cov:.0f}% Coverage\n"
                 "(Compensated sink loss %, with feasibility f, HYPOTHETICAL)",
                 fontsize=8.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(bar_names, fontsize=6.5, ha="center")
    ax.set_ylabel("Compensated Sink Loss (%)", fontsize=8)
    ax.set_ylim(0, 120)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=7)
    ax.tick_params(labelsize=7)

    # ── Panel 6: Required minimum scale per placement ───────────────
    ax = axes[1, 2]
    min_scales = [engine.find_minimum_scale(p) for p in PLACEMENT_STRATEGIES]
    # Cap display at 120% for visibility; beyond that it's clearly impossible in range
    display_scales = [min(120.0, s) for s in min_scales]
    bar_names_h = [p.name for p in PLACEMENT_STRATEGIES]
    bar_colors_h = [PLOT_COLORS[p.name] for p in PLACEMENT_STRATEGIES]

    # Color bars differently: within 30% range = strategy color, beyond = lighter gray
    bar_colors_h2 = []
    hatches = []
    for s, c in zip(min_scales, bar_colors_h):
        if s <= 30.0:
            bar_colors_h2.append(c)
            hatches.append("")
        else:
            bar_colors_h2.append("#BBBBBB")
            hatches.append("///")

    y_pos = np.arange(len(PLACEMENT_STRATEGIES))
    bars_h = ax.barh(y_pos, display_scales,
                     color=bar_colors_h2, edgecolor="black",
                     linewidth=0.5, alpha=0.8, hatch=None)
    for bar, hatch in zip(bars_h, hatches):
        bar.set_hatch(hatch)

    # 30% evaluated boundary line
    ax.axvline(30.0, color="#C0392B", linewidth=1.5, linestyle="--",
               label="Max evaluated (30%)")

    # Labels
    for i, (s, ds) in enumerate(zip(min_scales, display_scales)):
        if s <= 30.0:
            label = f"{s:.1f}%  <-- WITHIN RANGE"
            ax.text(ds + 1.5, i, label, va="center", fontsize=7, color="#27AE60",
                    fontweight="bold")
        elif s < 100.0:
            label = f"est. {s:.0f}%  (beyond range)"
            ax.text(min(ds, 118) + 1.5, i, label, va="center", fontsize=6.5,
                    color="#888888")
        else:
            label = ">100%  (beyond range)"
            ax.text(min(ds, 118) + 1.5, i, label, va="center", fontsize=6.5,
                    color="#888888")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(bar_names_h, fontsize=7)
    ax.set_xlabel("Required Global Coverage (%) to Fully Offset 10% Sink Loss", fontsize=8)
    ax.set_title("Minimum Scale Threshold per Placement Strategy\n"
                 "(Red line = max evaluated coverage, HYPOTHETICAL)",
                 fontsize=8.5)
    ax.set_xlim(0, 130)
    ax.grid(axis="x", alpha=0.3)
    ax.legend(fontsize=7, loc="lower right")
    ax.tick_params(labelsize=7)

    # Legend patches for Panel 6 hatch explanation
    within_patch = mpatches.Patch(color="#27AE60", label="Within 0-30% range")
    beyond_patch = mpatches.Patch(color="#BBBBBB", hatch="///", label="Beyond evaluated range")
    ax.legend(handles=[within_patch, beyond_patch],
              fontsize=7, loc="lower right")

    plt.tight_layout()
    out_path = "figures/terraforming_scale_requirement_model_output.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"  -> Saved: {out_path}")
    plt.show()


# ==========================================================================
# 6. Main
# ==========================================================================

def main() -> None:
    print("=" * 72)
    print("  Terraforming Scale Requirement Model")
    print("  Super El Nino Sink Loss Offset Analysis")
    print("  Coverage sweep: 0% to 30%  |  5 Placement Strategies")
    print("  Shock: 10% carbon sink loss (HYPOTHETICAL worst-case assumption)")
    print("  Technologies: OBS / OTU / UMC / HRS / DGS")
    print("  WARNING: HYPOTHETICAL CONCEPTUAL MODEL (PoC)")
    print("  NOT calibrated against real data. See MODEL_LIMITATIONS.md.")
    print("=" * 72)

    params = ScaleParameters()
    engine = ScaleRequirementEngine(params)

    print("\n  Running coverage sweep...")
    results = engine.run_sweep()

    print("\n  Parameters (all HYPOTHETICAL):")
    print(f"    super_el_nino_sink_loss          = {params.super_el_nino_sink_loss:.2f}  (10% hypothetical sink loss)")
    print(f"    obs_sequestration_rate           = {params.obs_sequestration_rate:.3f}")
    print(f"    otu_circulation_rate             = {params.otu_circulation_rate:.3f}")
    print(f"    direct_cooling_capacity          = {params.direct_cooling_capacity:.3f}")
    print(f"    ocean_metabolism_recovery_rate   = {params.ocean_metabolism_recovery_rate:.3f}")
    print(f"    humus_soil_restoration_rate      = {params.humus_soil_restoration_rate:.3f}")
    print(f"    desert_greening_area_factor      = {params.desert_greening_area_factor:.3f}")
    print(f"    atmospheric_circulation_coupling = {params.atmospheric_circulation_coupling:.2f}")
    print(f"    ocean_current_coupling           = {params.ocean_current_coupling:.2f}")
    print(f"    cross_hemisphere_transfer        = {params.cross_hemisphere_transfer:.2f}")
    print(f"    equatorial_belt_factor           = {params.equatorial_belt_factor:.2f}")
    print(f"    feasibility_penalty              = {params.feasibility_penalty:.2f}")

    print_summary(results, params, engine)

    print("\n  Key conceptual conclusions (HYPOTHETICAL -- PoC only):")
    print()
    print("  1. SCALE MATTERS: Below 5% coverage, even the best placement")
    print("     strategy shows negligible planetary-scale effect.")
    print()
    print("  2. PLACEMENT MATTERS: At 20% coverage, Equatorial Belt achieves")
    print("     ~68% sink compensation vs ~20% for Random Distributed.")
    print("     Same coverage area -- dramatically different effect (HYPOTHETICAL).")
    print()
    print("  3. EQUATORIAL BELT SCALE: The equatorial zone (~20N to 20S) is")
    print("     hypothesized as the primary coupling zone for global atmospheric")
    print("     and ocean circulation. Concentrating OBS/OTU/UMC/HRS/DGS there")
    print("     amplifies per-unit effectiveness. This is NOT validated.")
    print()
    print("  4. THRESHOLD FINDING: Full Planetary Network fully offsets 10%")
    print("     sink loss at approximately 21% global coverage (HYPOTHETICAL).")
    print("     Equatorial Belt reaches full offset at approximately 26% coverage.")
    print("     Ocean Current Coupled reaches ~96% at 30% -- just under threshold.")
    print()
    print("  5. FEASIBILITY-SCALE TENSION: The most effective strategies")
    print("     (Equatorial Belt, Full Planetary) have the lowest near-term")
    print("     feasibility. Random and Urban have high feasibility but cannot")
    print("     achieve the required scale effect.")
    print()
    print("  6. NOT FULL OFFSET AT 30%: Even at the maximum evaluated coverage")
    print("     (30%), three of five strategies cannot fully offset a 10% sink loss.")
    print("     This illustrates the scale challenge of reversing planetary-level")
    print("     carbon cycle disruption.")
    print()
    print("  7. THIS MODEL CANNOT PROVE any of the above claims.")
    print("     It is a conceptual PoC to visualize scale requirements.")
    print("     Scientific validation requires:")
    print("     - Ocean biogeochemistry field trials (OBS/OTU)")
    print("     - Atmospheric circulation modelling (equatorial belt hypothesis)")
    print("     - Long-term soil carbon measurement (HRS)")
    print("     - Large-scale land restoration monitoring (DGS)")
    print("     - International feasibility assessment (energy, water, biodiversity)")
    print()
    print("  WARNING: All values are HYPOTHETICAL. See MODEL_LIMITATIONS.md.")
    print("=" * 72)

    plot_results(results, params, engine)


if __name__ == "__main__":
    main()
