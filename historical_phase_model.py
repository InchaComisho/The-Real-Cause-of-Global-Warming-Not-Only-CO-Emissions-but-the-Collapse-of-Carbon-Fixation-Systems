"""
historical_phase_model.py
=========================
Historical Phase Model — Carbon Fixation Decline Since the Industrial Revolution

This model implements a CONCEPTUAL three-phase simulation of how human
activities have progressively degraded carbon fixation and absorption systems
since the Industrial Revolution.

Central hypothesis (not yet empirically validated):
  Global warming has been driven not only by increasing CO₂ emissions,
  but also by the accumulation of damage to natural carbon processing systems
  across three distinct historical phases.

─────────────────────────────────────────────────────────────────────────
  Phase 1: Industrial Expansion (1760–1945)
    - Gradual increase in deforestation, urbanization, agricultural expansion
    - Slow decline in terrestrial carbon fixation capacity
    - Emissions begin rising but remain relatively low

  Phase 2: Post-War Agrochemical Acceleration (1945–1990)
    - Rapid adoption of synthetic fertilizers, pesticides, monoculture
    - Accelerated soil microbial ecosystem degradation
    - Soil carbon fixation capacity declines faster
    - Nutrient runoff begins to stress marine ecosystems

  Phase 3: Modern Feedback Acceleration (1990–2025)
    - Increased forest fire pressure; Amazon forest loss accelerates
    - Marine dead zones expand, weakening ocean carbon uptake
    - Warming feedback begins to amplify ecosystem degradation
    - CO₂ accumulation accelerates beyond what emission rates alone explain
─────────────────────────────────────────────────────────────────────────

⚠️  IMPORTANT LIMITATIONS
    All pressure values, rates, and trajectories are HYPOTHETICAL.
    They are normalized to [0.0, 1.0] for conceptual illustration.
    None of these values have been calibrated against real observational data.
    Phase boundaries and rates reflect the author's conceptual framing.
    See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Cruz, Real, Lola
Published: May 2026
License: CC BY-SA 4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ─────────────────────────────────────────────────────────────────
# 1. Phase Definitions
# ─────────────────────────────────────────────────────────────────

@dataclass
class PhaseDefinition:
    """
    Defines a historical phase and its pressure growth rates.
    All rates are HYPOTHETICAL and normalized.
    """
    name:        str
    year_start:  int
    year_end:    int
    color:       str   # For visualization

    # Pressure growth rates per year within this phase [HYPOTHETICAL]
    deforestation_rate:      float = 0.0
    urbanization_rate:       float = 0.0
    agricultural_rate:       float = 0.0
    synth_fertilizer_rate:   float = 0.0
    pesticide_rate:          float = 0.0
    monoculture_rate:        float = 0.0
    nutrient_runoff_rate:    float = 0.0
    forest_fire_rate:        float = 0.0
    amazon_loss_rate:        float = 0.0
    marine_deadzone_rate:    float = 0.0


# HYPOTHETICAL phase parameter values.
# These represent conceptual trends, not measured rates.
PHASE_1 = PhaseDefinition(
    name="Phase 1: Industrial Expansion",
    year_start=1760,
    year_end=1945,
    color="#F4D03F",
    # HYPOTHETICAL: slow, gradual increase in land pressures
    deforestation_rate=0.0008,    # slow clearing for timber and farmland
    urbanization_rate=0.0005,     # gradual city expansion
    agricultural_rate=0.0010,     # steady expansion of farmland
    synth_fertilizer_rate=0.0,    # not yet widespread
    pesticide_rate=0.0,           # not yet widespread
    monoculture_rate=0.0002,      # early forms of monoculture begin
    nutrient_runoff_rate=0.0003,  # natural fertilizer runoff, low
    forest_fire_rate=0.0003,      # mostly controlled
    amazon_loss_rate=0.0001,      # minimal
    marine_deadzone_rate=0.0001,  # minimal
)

PHASE_2 = PhaseDefinition(
    name="Phase 2: Post-War Agrochemical Acceleration",
    year_start=1945,
    year_end=1990,
    color="#E67E22",
    # HYPOTHETICAL: faster degradation from industrial agriculture
    deforestation_rate=0.0030,    # accelerates with chainsaws and machinery
    urbanization_rate=0.0025,     # post-war urban expansion
    agricultural_rate=0.0020,     # Green Revolution expansion
    synth_fertilizer_rate=0.0120, # rapid adoption (Green Revolution)
    pesticide_rate=0.0090,        # DDT and successors, wide adoption
    monoculture_rate=0.0100,      # industrial-scale monoculture
    nutrient_runoff_rate=0.0080,  # fertilizer runoff increases
    forest_fire_rate=0.0010,      # increases but not dominant yet
    amazon_loss_rate=0.0030,      # Amazon clearing begins
    marine_deadzone_rate=0.0060,  # coastal eutrophication begins
)

PHASE_3 = PhaseDefinition(
    name="Phase 3: Modern Feedback Acceleration",
    year_start=1990,
    year_end=2025,
    color="#C0392B",
    # HYPOTHETICAL: feedback effects amplify all pressures
    deforestation_rate=0.0020,    # continues but some reforestation policies
    urbanization_rate=0.0030,     # rapid urbanization in Global South
    agricultural_rate=0.0010,     # slower expansion, but intensification
    synth_fertilizer_rate=0.0050, # plateaus in some regions, grows in others
    pesticide_rate=0.0040,        # continues globally
    monoculture_rate=0.0050,      # expands in tropical regions
    nutrient_runoff_rate=0.0040,  # persists despite some regulation
    forest_fire_rate=0.0150,      # climate-driven wildfires increase sharply
    amazon_loss_rate=0.0120,      # accelerated Amazon clearing
    marine_deadzone_rate=0.0080,  # continued expansion
)

ALL_PHASES = [PHASE_1, PHASE_2, PHASE_3]


# ─────────────────────────────────────────────────────────────────
# 2. Model State
# ─────────────────────────────────────────────────────────────────

@dataclass
class ModelState:
    """
    State variables for each simulation timestep.
    All values normalized to [0.0, 1.0].
    """
    year: int = 1760

    # Pressure variables (0 = no pressure, 1 = maximum pressure)
    # HYPOTHETICAL initial values
    deforestation_pressure:    float = 0.02
    urbanization_pressure:     float = 0.01
    agricultural_pressure:     float = 0.05
    synth_fertilizer_pressure: float = 0.0
    pesticide_pressure:        float = 0.0
    monoculture_pressure:      float = 0.02
    nutrient_runoff_pressure:  float = 0.02
    forest_fire_pressure:      float = 0.02
    amazon_loss_pressure:      float = 0.01
    marine_deadzone_pressure:  float = 0.01

    # System health variables (1.0 = pristine, 0.0 = collapsed)
    # HYPOTHETICAL initial values (pre-industrial not fully pristine)
    terrestrial_fixation:  float = 0.95  # forests, vegetation
    soil_microbial_health: float = 0.93  # soil microbiome
    soil_carbon_fixation:  float = 0.92  # soil carbon retention
    ocean_uptake_capacity: float = 0.90  # ocean CO2 absorption

    # Derived output
    co2_accumulation_index: float = 0.0   # normalized CO2 accumulation


# ─────────────────────────────────────────────────────────────────
# 3. Historical Phase Simulation Engine
# ─────────────────────────────────────────────────────────────────

class HistoricalPhaseModel:
    """
    Simulates the three-phase decline of carbon fixation systems
    from 1760 to 2025.

    The model is intentionally simple and conceptual.
    The causal relationships and rates are HYPOTHETICAL.
    """

    # HYPOTHETICAL coupling coefficients:
    # How much each pressure unit affects each health variable per year.
    # These are illustrative only and require empirical calibration.
    COUPLING = {
        # Terrestrial fixation damage
        "terr_from_defor":    0.40,  # deforestation is strongest driver
        "terr_from_urban":    0.10,
        "terr_from_agri":     0.15,
        "terr_from_fire":     0.30,
        "terr_from_amazon":   0.25,
        # Soil microbial damage
        "soil_from_synfert":  0.35,
        "soil_from_pest":     0.40,  # pesticides directly kill microbes
        "soil_from_mono":     0.25,
        # Soil carbon (follows soil microbial health with lag)
        "soilc_from_soil":    0.60,
        "soilc_from_agri":    0.10,
        # Ocean uptake damage
        "ocean_from_runoff":  0.20,
        "ocean_from_deadzone":0.35,
        "ocean_from_warming": 0.20,  # warming feedback from CO2 accumulation
    }

    # HYPOTHETICAL: emissions trajectory parameters (normalized)
    EMISSION_PARAMS = {
        1760: 0.01,   # pre-industrial baseline
        1945: 0.15,   # end of Phase 1
        1990: 0.45,   # end of Phase 2
        2025: 0.75,   # end of Phase 3
    }

    def __init__(self):
        self.history: List[Dict] = []

    def _emission_at(self, year: int) -> float:
        """
        HYPOTHETICAL: linear interpolation between milestone emission levels.
        """
        milestones = sorted(self.EMISSION_PARAMS.items())
        for i in range(len(milestones) - 1):
            y0, e0 = milestones[i]
            y1, e1 = milestones[i + 1]
            if y0 <= year <= y1:
                frac = (year - y0) / (y1 - y0)
                return e0 + (e1 - e0) * frac
        return self.EMISSION_PARAMS[2025]

    def _get_phase(self, year: int) -> PhaseDefinition:
        for phase in ALL_PHASES:
            if phase.year_start <= year < phase.year_end:
                return phase
        return ALL_PHASES[-1]

    def _update_pressures(self, s: ModelState, phase: PhaseDefinition) -> None:
        """Increment pressure variables based on the current phase rates."""
        s.deforestation_pressure    = min(1.0, s.deforestation_pressure    + phase.deforestation_rate)
        s.urbanization_pressure     = min(1.0, s.urbanization_pressure     + phase.urbanization_rate)
        s.agricultural_pressure     = min(1.0, s.agricultural_pressure     + phase.agricultural_rate)
        s.synth_fertilizer_pressure = min(1.0, s.synth_fertilizer_pressure + phase.synth_fertilizer_rate)
        s.pesticide_pressure        = min(1.0, s.pesticide_pressure        + phase.pesticide_rate)
        s.monoculture_pressure      = min(1.0, s.monoculture_pressure      + phase.monoculture_rate)
        s.nutrient_runoff_pressure  = min(1.0, s.nutrient_runoff_pressure  + phase.nutrient_runoff_rate)
        s.forest_fire_pressure      = min(1.0, s.forest_fire_pressure      + phase.forest_fire_rate)
        s.amazon_loss_pressure      = min(1.0, s.amazon_loss_pressure      + phase.amazon_loss_rate)
        s.marine_deadzone_pressure  = min(1.0, s.marine_deadzone_pressure  + phase.marine_deadzone_rate)

    def _update_health(self, s: ModelState) -> None:
        """Update system health based on pressures. All coefficients HYPOTHETICAL."""
        C = self.COUPLING

        # Warming feedback: HYPOTHETICAL — proportional to CO2 index
        warming_feedback = min(1.0, s.co2_accumulation_index * 0.80)

        # Terrestrial fixation decline
        terr_loss = (
            C["terr_from_defor"]  * s.deforestation_pressure +
            C["terr_from_urban"]  * s.urbanization_pressure  +
            C["terr_from_agri"]   * s.agricultural_pressure  +
            C["terr_from_fire"]   * s.forest_fire_pressure   +
            C["terr_from_amazon"] * s.amazon_loss_pressure
        ) * 0.002  # HYPOTHETICAL: scaling factor
        s.terrestrial_fixation = max(0.0, s.terrestrial_fixation - terr_loss)

        # Soil microbial health decline
        soil_loss = (
            C["soil_from_synfert"] * s.synth_fertilizer_pressure +
            C["soil_from_pest"]    * s.pesticide_pressure        +
            C["soil_from_mono"]    * s.monoculture_pressure
        ) * 0.003  # HYPOTHETICAL
        s.soil_microbial_health = max(0.0, s.soil_microbial_health - soil_loss)

        # Soil carbon fixation (lags soil microbial health)
        soilc_loss = (
            C["soilc_from_soil"] * (0.93 - s.soil_microbial_health) * 0.002 +
            C["soilc_from_agri"] * s.agricultural_pressure          * 0.001
        )
        s.soil_carbon_fixation = max(0.0, s.soil_carbon_fixation - soilc_loss)

        # Ocean uptake decline
        ocean_loss = (
            C["ocean_from_runoff"]   * s.nutrient_runoff_pressure  +
            C["ocean_from_deadzone"] * s.marine_deadzone_pressure   +
            C["ocean_from_warming"]  * warming_feedback
        ) * 0.002  # HYPOTHETICAL
        s.ocean_uptake_capacity = max(0.0, s.ocean_uptake_capacity - ocean_loss)

    def _update_co2(self, s: ModelState) -> None:
        """
        CO₂ accumulation:
        ΔCO₂ = emissions − fixation_removal + degradation_release

        All weights HYPOTHETICAL.
        """
        emission = self._emission_at(s.year)

        # Total fixation removal (HYPOTHETICAL weights)
        fixation_total = (
            0.40 * s.terrestrial_fixation  +
            0.20 * s.soil_carbon_fixation  +
            0.40 * s.ocean_uptake_capacity
        )

        # Degradation release: rises as health falls (HYPOTHETICAL)
        degradation = (
            0.05 * (0.95 - s.terrestrial_fixation) +
            0.03 * (0.92 - s.soil_carbon_fixation)
        )

        delta = max(0.0, emission - fixation_total * 0.80 + degradation)
        s.co2_accumulation_index = min(1.0, s.co2_accumulation_index + delta * 0.012)

    def simulate(self) -> List[Dict]:
        """Run the full simulation from 1760 to 2025."""
        state = ModelState()
        self.history = []

        year_range = range(
            ALL_PHASES[0].year_start,
            ALL_PHASES[-1].year_end + 1
        )

        for year in year_range:
            state.year = year
            phase = self._get_phase(year)

            # Record state BEFORE update
            self.history.append({
                "year":                    year,
                "phase":                   phase.name,
                "emission":                self._emission_at(year),
                "deforestation_pressure":  state.deforestation_pressure,
                "urbanization_pressure":   state.urbanization_pressure,
                "agricultural_pressure":   state.agricultural_pressure,
                "synth_fertilizer":        state.synth_fertilizer_pressure,
                "pesticide":               state.pesticide_pressure,
                "monoculture":             state.monoculture_pressure,
                "nutrient_runoff":         state.nutrient_runoff_pressure,
                "forest_fire":             state.forest_fire_pressure,
                "amazon_loss":             state.amazon_loss_pressure,
                "marine_deadzone":         state.marine_deadzone_pressure,
                "terrestrial_fixation":    state.terrestrial_fixation,
                "soil_microbial_health":   state.soil_microbial_health,
                "soil_carbon_fixation":    state.soil_carbon_fixation,
                "ocean_uptake_capacity":   state.ocean_uptake_capacity,
                "co2_index":               state.co2_accumulation_index,
            })

            # Update
            self._update_pressures(state, phase)
            self._update_health(state)
            self._update_co2(state)

        return self.history


# ─────────────────────────────────────────────────────────────────
# 4. Visualization
# ─────────────────────────────────────────────────────────────────

def plot_phase_results(history: List[Dict]) -> None:
    years  = np.array([r["year"] for r in history])
    phases = [r["phase"]   for r in history]

    def arr(key: str) -> np.ndarray:
        return np.array([r[key] for r in history])

    fig, axes = plt.subplots(3, 1, figsize=(13, 12))
    fig.suptitle(
        "Historical Phase Model: Carbon Fixation Decline since the Industrial Revolution\n"
        "⚠ HYPOTHETICAL CONCEPTUAL VALUES — Not calibrated against real data",
        fontsize=11, fontweight="bold", color="#8B0000",
    )

    # Phase background shading
    phase_colors = {
        "Phase 1: Industrial Expansion":              "#FEF9E7",
        "Phase 2: Post-War Agrochemical Acceleration":"#FEF0E7",
        "Phase 3: Modern Feedback Acceleration":      "#FDEDEC",
    }
    phase_labels = {p.name: p for p in ALL_PHASES}

    def shade_phases(ax):
        for phase in ALL_PHASES:
            ax.axvspan(phase.year_start, phase.year_end,
                       alpha=0.30,
                       color=phase.color,
                       label=phase.name)
        ax.axvline(1945, color="#666", linewidth=0.8, linestyle=":")
        ax.axvline(1990, color="#666", linewidth=0.8, linestyle=":")

    # ── Panel 1: Pressure Variables ──
    ax1 = axes[0]
    shade_phases(ax1)
    ax1.plot(years, arr("deforestation_pressure"), color="#2E7D32", label="Deforestation")
    ax1.plot(years, arr("agricultural_pressure"),  color="#F9A825", label="Agricultural expansion")
    ax1.plot(years, arr("synth_fertilizer"),        color="#6A1B9A", label="Synthetic fertilizer")
    ax1.plot(years, arr("pesticide"),               color="#AD1457", label="Pesticide")
    ax1.plot(years, arr("forest_fire"),             color="#BF360C", label="Forest fire (Phase 3)")
    ax1.plot(years, arr("amazon_loss"),             color="#1B5E20", linestyle="--", label="Amazon loss")
    ax1.plot(years, arr("marine_deadzone"),         color="#0277BD", linestyle="--", label="Marine dead zone")
    ax1.set_ylabel("Normalized Pressure [0–1]")
    ax1.set_title("Degradation Pressure Variables (HYPOTHETICAL)")
    ax1.legend(fontsize=8, ncol=3)
    ax1.set_xlim(1760, 2025)
    ax1.grid(alpha=0.3)

    # ── Panel 2: System Health ──
    ax2 = axes[1]
    shade_phases(ax2)
    ax2.plot(years, arr("terrestrial_fixation"),  color="#27AE60", linewidth=2,   label="Terrestrial fixation capacity")
    ax2.plot(years, arr("soil_microbial_health"), color="#8B4513", linewidth=2,   label="Soil microbial health")
    ax2.plot(years, arr("soil_carbon_fixation"),  color="#A0522D", linewidth=2,   label="Soil carbon fixation capacity")
    ax2.plot(years, arr("ocean_uptake_capacity"), color="#2980B9", linewidth=2,   label="Ocean CO₂ uptake capacity")
    ax2.set_ylabel("Normalized Health [0–1]")
    ax2.set_title("Carbon Fixation and Uptake System Health (HYPOTHETICAL)")
    ax2.legend(fontsize=9)
    ax2.set_xlim(1760, 2025)
    ax2.set_ylim(0, 1.05)
    ax2.grid(alpha=0.3)

    # ── Panel 3: CO₂ Index + Emissions ──
    ax3 = axes[2]
    shade_phases(ax3)
    ax3_twin = ax3.twinx()
    ax3.plot(years, arr("co2_index"),  color="#C0392B", linewidth=2.5, label="CO₂ accumulation index")
    ax3_twin.plot(years, arr("emission"), color="#7F8C8D", linewidth=1.5,
                  linestyle="--", label="Emission rate (right axis)")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("CO₂ Index [0–1]", color="#C0392B")
    ax3_twin.set_ylabel("Emission Rate [0–1]", color="#7F8C8D")
    ax3.set_title("CO₂ Accumulation Index vs. Emission Rate (HYPOTHETICAL)")
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="upper left")
    ax3.set_xlim(1760, 2025)
    ax3.grid(alpha=0.3)

    # Phase legend
    phase_patches = [
        mpatches.Patch(color=p.color, alpha=0.4, label=p.name)
        for p in ALL_PHASES
    ]
    fig.legend(handles=phase_patches, loc="lower center", ncol=3,
               fontsize=9, bbox_to_anchor=(0.5, -0.01))

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig("historical_phase_model_output.png", dpi=150, bbox_inches="tight")
    print("  → Saved: historical_phase_model_output.png")
    plt.show()


def print_phase_summary(history: List[Dict]) -> None:
    checkpoints = [1760, 1900, 1945, 1970, 1990, 2010, 2024]
    print(f"\n  {'Year':>6}  {'Phase':<38}  {'TF':>6}  {'Soil':>6}  {'Ocean':>6}  {'CO₂':>6}  {'Emit':>6}")
    print(f"  {'─'*6}  {'─'*38}  {'─'*6}  {'─'*6}  {'─'*6}  {'─'*6}  {'─'*6}")
    for r in history:
        if r["year"] in checkpoints:
            ph = r["phase"].split(":")[0].strip()
            print(
                f"  {r['year']:>6}  {ph:<38}  "
                f"{r['terrestrial_fixation']:>6.3f}  "
                f"{r['soil_microbial_health']:>6.3f}  "
                f"{r['ocean_uptake_capacity']:>6.3f}  "
                f"{r['co2_index']:>6.3f}  "
                f"{r['emission']:>6.3f}"
            )
    print("  TF=Terrestrial Fixation, Soil=Soil Microbial Health, Ocean=Ocean Uptake")
    print("  ⚠ All values HYPOTHETICAL. See MODEL_LIMITATIONS.md.")


# ─────────────────────────────────────────────────────────────────
# 5. Main
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("  Historical Phase Model (1760–2025)")
    print("  Three-phase decline of carbon fixation systems")
    print("  ⚠ HYPOTHETICAL CONCEPTUAL MODEL — See MODEL_LIMITATIONS.md")
    print("=" * 70)

    model = HistoricalPhaseModel()
    history = model.simulate()

    print_phase_summary(history)
    plot_phase_results(history)


if __name__ == "__main__":
    main()
