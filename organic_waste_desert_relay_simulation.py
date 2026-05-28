"""
organic_waste_desert_relay_simulation.py
==========================================
Conceptual Proof-of-Concept Simulation:
Organic Waste -> Humus Recycling System (HRS) ->
Desert Greening Support (DGS) -> Stepwise Food Transition Relay

This is a CONCEPTUAL PROOF-OF-CONCEPT MODEL derived from the framework in:
  ORGANIC_WASTE_HUMUS_AND_DESERT_REGENERATION_MODEL.md
  (Natural-Complementary-Science repository)

Connected framework:
  Natural Complementary Science (philosophical foundation)
  -> HRS / DGS (practical circulation layer)
  -> New Civilizational Genesis Plan (civilizational implementation)

ALL parameters, rates, and indices are HYPOTHETICAL and NORMALIZED.
This model does NOT represent measured or validated real-world data.
Results are illustrative of structural logic only.
Independent scientific, sanitary, ecological, agricultural, and
engineering verification is required before any practical application.

Organic waste categories modelled (relative units, not real tonnage):
  food_loss, kitchen_waste, fallen_leaves, branches,
  paper_cardboard, agricultural_residues

Preprocessing pipeline:
  source separation -> drying -> sanitation -> pulverization -> transport
  NOTE: residual_biosecurity_risk is NEVER zero.
  Pathogen elimination is never guaranteed; only reduction is modelled.

HRS -- Humus Recycling System:
  organic matter -> decomposition pool -> humus ->
  soil_carbon, microbial_habitat, water_retention

DGS -- Desert Greening Support:
  humus-amended soil -> dryland_soil_recovery,
  surface_temperature_moderation, vegetation_establishment

Stepwise Food Transition (conceptual cultivation succession hypothesis):
  Phase 1 (yr 1-5  after activation): Tuber -- ground cover, soil loosening
  Phase 2 (yr 6-15 after activation): Legume -- nitrogen fixation, fertility
  Phase 3 (yr 16+  after activation): Herb/Mixed -- biodiversity, stability

Four scenarios (2026-2075, T=50 years):
  1. Baseline Desert          -- no organic input
  2. Organic Waste Only       -- raw/minimally processed (high risk, low yield)
  3. HRS + DGS                -- fully processed organic relay
  4. HRS + DGS + Food Relay   -- full stepwise system

Seven output indices (all hypothetical, normalized [0-1]):
  soil_carbon_index, water_retention_index, microbial_diversity_index,
  vegetation_cover_index, food_production_potential,
  carbon_fixation_potential, residual_risk_index

WARNING: All parameter values and trajectories are HYPOTHETICAL.
Real-world outcomes depend on site-specific climate, hydrology,
soil chemistry, species selection, sanitation standards, regulatory
context, water availability, and many other factors not captured here.

Figures saved to: figures/
  organic_waste_desert_relay_main.png
  organic_waste_preprocessing_pipeline.png
  organic_waste_food_transition_relay.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Optional

# ─────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────
T_YEARS = 50
START_YEAR = 2026
YEARS = np.arange(START_YEAR, START_YEAR + T_YEARS)
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

DISCLAIMER = ('CONCEPTUAL MODEL -- All values are hypothetical, not measured. '
              'Requires independent validation.')


# ─────────────────────────────────────────────────────────────────
# Parameter Dataclasses
# ─────────────────────────────────────────────────────────────────

@dataclass
class WasteStream:
    """
    Annual organic waste generation profile.
    Values are HYPOTHETICAL relative units (not real tonnage).
    Represents a developed-region baseline.
    """
    food_loss:              float = 3.5
    kitchen_waste:          float = 2.8
    fallen_leaves:          float = 2.0
    branches:               float = 1.5
    paper_cardboard:        float = 1.8
    agricultural_residues:  float = 2.5

    def total(self) -> float:
        return (self.food_loss + self.kitchen_waste + self.fallen_leaves +
                self.branches + self.paper_cardboard + self.agricultural_residues)


@dataclass
class PreprocessingParams:
    """
    HRS preprocessing pipeline parameters.
    All values are HYPOTHETICAL fractions.

    IMPORTANT: residual_biosecurity_risk is NEVER zero.
    Even best-practice processing (thermal treatment, UV, freeze-dry)
    retains a non-negligible residual pathogen risk.
    This floor is enforced throughout all scenarios with organic input.
    """
    source_separation_rate:    float = 0.70   # fraction of waste successfully separated
    drying_factor:             float = 0.75   # mass fraction retained after drying
    sanitation_efficiency:     float = 0.80   # fraction of pathogens eliminated (realistic max ~0.92)
    residual_biosecurity_risk: float = 0.05   # minimum risk floor even after best processing
    pulverization_factor:      float = 0.90   # surface-area utilization enhancement
    transport_burden_index:    float = 0.15   # fraction of benefit lost to logistics

    def effective_yield(self, waste_total: float) -> float:
        """Net processed organic matter available after all pipeline losses."""
        return (waste_total
                * self.source_separation_rate
                * self.drying_factor
                * self.sanitation_efficiency
                * self.pulverization_factor
                * (1.0 - self.transport_burden_index))

    def residual_risk(self) -> float:
        """
        Residual biosecurity risk index.
        Always >= residual_biosecurity_risk floor.
        """
        contamination_contribution = (1.0 - self.sanitation_efficiency) * 0.20
        return self.residual_biosecurity_risk + contamination_contribution


@dataclass
class HRSParams:
    """
    Humus Recycling System dynamics.
    All values are HYPOTHETICAL.
    """
    decomposition_rate:          float = 0.15   # fraction of organic input entering decomp pool / yr
    humus_conversion_rate:       float = 0.45   # fraction of decomposed material -> humus
    humus_pool_decay:            float = 0.08   # humus pool annual turnover fraction
    soil_carbon_per_pool:        float = 0.002  # soil carbon gain per unit of humus pool
    microbial_per_pool:          float = 0.002  # microbial diversity gain per unit of humus pool
    water_retention_per_pool:    float = 0.003  # water retention gain per unit of humus pool
    contamination_penalty:       float = 0.15   # risk-proportional reduction in conversion quality


@dataclass
class DGSParams:
    """
    Desert Greening Support parameters.
    All values are HYPOTHETICAL.
    Water availability is the primary real-world constraint --
    modelled here as water_stress_factor < 1.0.
    """
    vegetation_threshold:           float = 0.12   # minimum water_retention for vegetation establishment
    vegetation_growth_coeff:        float = 0.15   # vegetation growth rate when threshold met
    soil_recovery_coupling:         float = 0.06   # soil recovery rate from DGS per year
    temp_moderation_per_cover:      float = 0.025  # surface temp moderation per vegetation unit
    carbon_fixation_per_cover:      float = 0.008  # carbon fixation per vegetation cover unit
    water_stress_factor:            float = 0.60   # dryland water constraint [0=severe, 1=none]
    veg_water_feedback:             float = 0.005  # vegetation -> soil moisture feedback


@dataclass
class FoodTransitionParams:
    """
    Stepwise Food Transition Model parameters.
    Conceptual cultivation succession hypothesis only.
    Phase boundaries are relative to food relay activation year.
    Actual timing depends on DGS deployment and vegetation establishment.
    """
    activation_vc_threshold:     float = 0.10   # vegetation cover needed to start relay
    phase2_start_yr:             int   = 5      # years after activation
    phase3_start_yr:             int   = 15     # years after activation

    # Phase 1: Tuber (potatoes, sweet potatoes, root crops)
    tuber_cover_rate:            float = 0.045  # additional vc gain / yr
    tuber_soil_looseness:        float = 0.003  # soil carbon benefit / yr from root action
    tuber_food_target:           float = 0.020  # food production target for phase 1
    tuber_food_approach:         float = 0.15   # convergence rate to target

    # Phase 2: Legume (beans, nitrogen-fixing crops)
    legume_nitrogen_rate:        float = 0.020  # microbial diversity gain / yr
    legume_fertility_rate:       float = 0.003  # soil carbon gain / yr
    legume_wr_rate:              float = 0.002  # water retention gain / yr (improved structure)
    legume_food_target:          float = 0.035
    legume_food_approach:        float = 0.18

    # Phase 3: Herb / Mixed vegetation
    herb_biodiversity_rate:      float = 0.015  # microbial diversity gain / yr
    herb_soil_rate:              float = 0.003  # soil carbon gain / yr
    herb_carbon_fixation_rate:   float = 0.006  # carbon fixation gain / yr
    herb_vc_rate:                float = 0.020  # vegetation diversification rate
    herb_food_target:            float = 0.030  # stable diverse food production
    herb_food_approach:          float = 0.08


# ─────────────────────────────────────────────────────────────────
# Initial State
# ─────────────────────────────────────────────────────────────────

def baseline_state() -> Dict[str, float]:
    """
    Severely degraded dryland / desert initial conditions.
    All values are HYPOTHETICAL normalized indices.
    """
    return {
        'soil_carbon':          0.05,
        'water_retention':      0.03,
        'microbial_diversity':  0.05,
        'vegetation_cover':     0.02,
        'food_production':      0.01,
        'carbon_fixation':      0.02,
        'residual_risk':        0.00,
    }


# ─────────────────────────────────────────────────────────────────
# Scenario Simulation
# ─────────────────────────────────────────────────────────────────

def run_scenario(
    name:            str,
    use_hrs:         bool,
    use_dgs:         bool,
    use_food_relay:  bool,
    raw_waste_only:  bool,
    waste:           WasteStream,
    pre:             PreprocessingParams,
    hrs:             HRSParams,
    dgs:             DGSParams,
    ft:              FoodTransitionParams,
) -> Dict:
    """
    Simulate one scenario over T_YEARS.
    Returns dict with arrays of shape (T_YEARS,) for each index.

    HYPOTHETICAL dynamics only. Not validated against real data.
    """
    # State arrays
    soil_carbon          = np.zeros(T_YEARS)
    water_retention      = np.zeros(T_YEARS)
    microbial_diversity  = np.zeros(T_YEARS)
    vegetation_cover     = np.zeros(T_YEARS)
    food_production      = np.zeros(T_YEARS)
    carbon_fixation      = np.zeros(T_YEARS)
    residual_risk        = np.zeros(T_YEARS)
    humus_pool           = np.zeros(T_YEARS)

    # Initialise from baseline
    s = baseline_state()
    soil_carbon[0]         = s['soil_carbon']
    water_retention[0]     = s['water_retention']
    microbial_diversity[0] = s['microbial_diversity']
    vegetation_cover[0]    = s['vegetation_cover']
    food_production[0]     = s['food_production']
    carbon_fixation[0]     = s['carbon_fixation']
    residual_risk[0]       = s['residual_risk']
    humus_pool[0]          = 0.0

    # Phase tracking
    dgs_active_since:      Optional[int] = None   # year index when DGS vegetation began
    relay_active_since:    Optional[int] = None   # year index when food relay began

    waste_total = waste.total()

    for t in range(1, T_YEARS):
        sc  = soil_carbon[t-1]
        wr  = water_retention[t-1]
        md  = microbial_diversity[t-1]
        vc  = vegetation_cover[t-1]
        fp  = food_production[t-1]
        cf  = carbon_fixation[t-1]
        rr  = residual_risk[t-1]
        hp  = humus_pool[t-1]

        # -- Natural baseline processes (slow degradation without intervention)
        d_sc = -0.002 * sc
        d_wr = -0.001 * wr
        d_md = -0.003 * md
        d_vc = -0.003 * vc
        d_fp = -0.002 * fp
        d_cf = -0.002 * cf
        d_rr =  0.0
        d_hp =  0.0

        # ── Scenario: Raw / Minimally Processed Organic Waste
        if raw_waste_only:
            # Low source separation, poor sanitation, rough handling
            organic_frac = 0.40 * waste_total   # ~40% source separation
            # Humus pool: grows slowly (poor decomposition quality); decays faster
            new_hp = organic_frac * 0.008       # much lower than HRS
            d_hp += new_hp - hp * 0.12          # faster decay (unstable raw material)
            # Soil benefits: limited by contamination and incomplete decomposition
            d_sc += hp * 0.0005                 # ~4x lower than HRS
            d_wr += hp * 0.0008
            d_md += hp * 0.0001 - 0.002         # pathogen disruption penalty on microbial
            # Risk: builds toward a high floor
            target_risk = 0.15
            d_rr = (target_risk - rr) * 0.08

        # ── Scenario: HRS -- Full Processing Pipeline
        if use_hrs and not raw_waste_only:
            organic_input = pre.effective_yield(waste_total)
            current_risk  = pre.residual_risk()    # always > 0

            # Humus pool: new input - natural turnover
            quality_factor = 1.0 - hrs.contamination_penalty * current_risk
            new_hp = (organic_input
                      * hrs.decomposition_rate
                      * hrs.humus_conversion_rate
                      * quality_factor)
            d_hp += new_hp - hp * hrs.humus_pool_decay

            # Soil improvements from humus pool
            d_sc += hp * hrs.soil_carbon_per_pool
            d_md += hp * hrs.microbial_per_pool
            d_wr += hp * hrs.water_retention_per_pool

            # Residual risk: stabilises at HRS floor (never zero)
            target_risk = current_risk
            d_rr = (target_risk - rr) * 0.10

        # ── Scenario: DGS -- Desert Greening Support
        if use_dgs and not raw_waste_only:
            # Vegetation only establishes when water retention meets threshold
            if wr >= dgs.vegetation_threshold:
                if dgs_active_since is None:
                    dgs_active_since = t
                # Vegetation growth (logistic: slows as vc -> 1.0)
                d_vc += ((1.0 - vc)
                          * dgs.vegetation_growth_coeff
                          * dgs.water_stress_factor
                          * 0.20)
                # Soil carbon recovery accelerates with vegetation cover
                d_sc += sc * dgs.soil_recovery_coupling * dgs.water_stress_factor * 0.08
                # Vegetation -> water retention feedback
                d_wr += vc * dgs.veg_water_feedback

            # Surface temperature moderation from any vegetation
            temp_mod = vc * dgs.temp_moderation_per_cover
            d_sc += temp_mod * 0.002   # reduced thermal stress slows soil carbon loss

            # Carbon fixation from vegetation
            d_cf += vc * dgs.carbon_fixation_per_cover

        # ── Scenario: Stepwise Food Transition Relay
        if use_food_relay and not raw_waste_only:
            # Relay activates when vegetation cover reaches threshold
            if relay_active_since is None and vc >= ft.activation_vc_threshold:
                relay_active_since = t

            if relay_active_since is not None:
                yr_in_relay = t - relay_active_since

                if yr_in_relay < ft.phase2_start_yr:
                    # Phase 1: Tuber -- ground cover, soil loosening
                    d_vc += (1.0 - vc) * ft.tuber_cover_rate * 0.40
                    d_sc += ft.tuber_soil_looseness
                    d_fp += (ft.tuber_food_target - fp) * ft.tuber_food_approach
                    d_md += 0.003   # root exudate benefit to microbiome

                elif yr_in_relay < ft.phase3_start_yr:
                    # Phase 2: Legume -- nitrogen fixation, fertility
                    d_md += ft.legume_nitrogen_rate * (1.0 - md)
                    d_sc += ft.legume_fertility_rate
                    d_wr += ft.legume_wr_rate
                    d_fp += (ft.legume_food_target - fp) * ft.legume_food_approach

                else:
                    # Phase 3: Herb / Mixed -- biodiversity, stability
                    d_md += ft.herb_biodiversity_rate * (1.0 - md)
                    d_sc += ft.herb_soil_rate
                    d_cf += ft.herb_carbon_fixation_rate * (1.0 - cf)
                    d_vc += (1.0 - vc) * ft.herb_vc_rate * 0.15
                    d_fp += (ft.herb_food_target - fp) * ft.herb_food_approach

        # -- Apply deltas with clipping
        soil_carbon[t]         = float(np.clip(sc + d_sc, 0.0, 1.0))
        water_retention[t]     = float(np.clip(wr + d_wr, 0.0, 1.0))
        microbial_diversity[t] = float(np.clip(md + d_md, 0.0, 1.0))
        vegetation_cover[t]    = float(np.clip(vc + d_vc, 0.0, 1.0))
        food_production[t]     = float(np.clip(fp + d_fp, 0.0, 1.0))
        carbon_fixation[t]     = float(np.clip(cf + d_cf, 0.0, 1.0))
        residual_risk[t]       = float(np.clip(rr + d_rr, 0.0, 1.0))
        humus_pool[t]          = float(np.clip(hp + d_hp, 0.0, 6.0))

    return {
        'name':               name,
        'dgs_active_since':   dgs_active_since,
        'relay_active_since': relay_active_since,
        'soil_carbon':        soil_carbon,
        'water_retention':    water_retention,
        'microbial_diversity': microbial_diversity,
        'vegetation_cover':   vegetation_cover,
        'food_production':    food_production,
        'carbon_fixation':    carbon_fixation,
        'residual_risk':      residual_risk,
        'humus_pool':         humus_pool,
    }


# ─────────────────────────────────────────────────────────────────
# Plot styles
# ─────────────────────────────────────────────────────────────────

SCENARIO_STYLES = [
    {'color': '#888888', 'ls': '-',  'lw': 1.5,
     'label': '1. Baseline Desert (no intervention)'},
    {'color': '#cc4400', 'ls': '--', 'lw': 1.8,
     'label': '2. Organic Waste Only (minimal processing, high risk)'},
    {'color': '#0055bb', 'ls': '-',  'lw': 2.2,
     'label': '3. HRS + DGS (fully processed)'},
    {'color': '#007733', 'ls': '-',  'lw': 2.5,
     'label': '4. HRS + DGS + Food Relay (full system)'},
]


# ─────────────────────────────────────────────────────────────────
# Figure 1: Main indices over time
# ─────────────────────────────────────────────────────────────────

def plot_main_indices(scenarios: List[Dict], years: np.ndarray) -> str:
    """
    4x2 layout: 7 scenario indices + humus pool.
    Outputs to figures/organic_waste_desert_relay_main.png
    """
    panels = [
        ('soil_carbon',          'Soil Carbon Index',          'Hypothetical [0-1]'),
        ('water_retention',      'Water Retention Index',      'Hypothetical [0-1]'),
        ('microbial_diversity',  'Microbial Diversity Index',  'Hypothetical [0-1]'),
        ('vegetation_cover',     'Vegetation Cover Index',     'Hypothetical [0-1]'),
        ('food_production',      'Food Production Potential',  'Hypothetical [0-1]'),
        ('carbon_fixation',      'Carbon Fixation Potential',  'Hypothetical [0-1]'),
        ('residual_risk',        'Residual Biosecurity Risk',  'Hypothetical [0-1]'),
        ('humus_pool',           'Cumulative Humus Pool',      'Hypothetical [rel. units]'),
    ]

    fig, axes = plt.subplots(4, 2, figsize=(14, 18))
    axes = axes.flatten()

    for i, (key, title, ylabel) in enumerate(panels):
        ax = axes[i]
        for j, sc in enumerate(scenarios):
            sty = SCENARIO_STYLES[j]
            ax.plot(years, sc[key],
                    color=sty['color'], linestyle=sty['ls'],
                    linewidth=sty['lw'], label=sty['label'])
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlabel('Year', fontsize=8)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.set_xlim(years[0], years[-1])
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.3)
        if i == 0:
            ax.legend(fontsize=7, loc='upper left')
        # Risk panel annotation
        if key == 'residual_risk':
            ax.axhline(0.0, color='k', linewidth=0.5, linestyle=':')
            ax.text(years[0] + 1, 0.003,
                    'Zero risk is not achievable in this model',
                    fontsize=6, color='#880000', style='italic')

    fig.suptitle('Organic Waste -> HRS -> DGS -> Food Relay: Scenario Comparison\n'
                 + DISCLAIMER,
                 fontsize=9, y=0.998)
    plt.tight_layout(rect=[0, 0, 1, 0.997])
    out = os.path.join(FIGURES_DIR, 'organic_waste_desert_relay_main.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─────────────────────────────────────────────────────────────────
# Figure 2: Preprocessing pipeline analysis
# ─────────────────────────────────────────────────────────────────

def plot_preprocessing_pipeline(waste: WasteStream) -> str:
    """
    2-panel figure:
      Left:  organic waste generation profile by type
      Right: effective yield vs residual risk across 3 processing levels
    """
    waste_labels = ['food\nloss', 'kitchen\nwaste', 'fallen\nleaves',
                    'branches', 'paper/\ncardboard', 'agri.\nresidues']
    generation   = np.array([waste.food_loss, waste.kitchen_waste,
                              waste.fallen_leaves, waste.branches,
                              waste.paper_cardboard, waste.agricultural_residues])
    bar_colors   = ['#cc4400', '#dd7700', '#558833',
                    '#336622', '#886644', '#aa9933']

    # Three processing levels
    proc_levels  = ['No\nProcessing', 'Minimal\nProcessing', 'HRS Full\nProcessing']
    proc_params  = [
        PreprocessingParams(source_separation_rate=0.10, drying_factor=1.00,
                            sanitation_efficiency=0.00, residual_biosecurity_risk=0.25,
                            pulverization_factor=1.00, transport_burden_index=0.00),
        PreprocessingParams(source_separation_rate=0.40, drying_factor=0.50,
                            sanitation_efficiency=0.30, residual_biosecurity_risk=0.12,
                            pulverization_factor=0.60, transport_burden_index=0.25),
        PreprocessingParams(source_separation_rate=0.70, drying_factor=0.75,
                            sanitation_efficiency=0.80, residual_biosecurity_risk=0.05,
                            pulverization_factor=0.90, transport_burden_index=0.15),
    ]
    waste_total   = waste.total()
    eff_yields    = [p.effective_yield(waste_total) for p in proc_params]
    risks         = [p.residual_risk() for p in proc_params]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: waste type profile
    bars = ax1.bar(range(len(waste_labels)), generation, color=bar_colors, alpha=0.85,
                   edgecolor='white', linewidth=0.5)
    ax1.set_xticks(range(len(waste_labels)))
    ax1.set_xticklabels(waste_labels, fontsize=9)
    ax1.set_ylabel('Relative Annual Generation\n(hypothetical units, not real tonnage)', fontsize=9)
    ax1.set_title('Organic Waste Generation Profile by Type\n(HYPOTHETICAL relative units)',
                  fontsize=10, fontweight='bold')
    ax1.grid(True, axis='y', alpha=0.3)
    for bar, val in zip(bars, generation):
        ax1.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 0.05,
                 f'{val:.1f}', ha='center', va='bottom', fontsize=9)

    # Panel B: processing level comparison
    x     = np.arange(len(proc_levels))
    width = 0.30
    bars1 = ax2.bar(x - width / 2, eff_yields, width,
                    label='Effective Yield (hypothetical)',
                    color='#0055bb', alpha=0.85, edgecolor='white')
    ax2b  = ax2.twinx()
    bars2 = ax2b.bar(x + width / 2, risks, width,
                     label='Residual Risk (hypothetical)',
                     color='#cc4400', alpha=0.85, edgecolor='white')

    ax2.set_xticks(x)
    ax2.set_xticklabels(proc_levels, fontsize=10)
    ax2.set_ylabel('Effective Organic Yield (hypothetical)', fontsize=9, color='#0055bb')
    ax2b.set_ylabel('Residual Biosecurity Risk (hypothetical)', fontsize=9, color='#cc4400')
    ax2.set_title('Processing Level: Yield vs Residual Risk\n'
                  '(Risk is NEVER zero -- even best processing retains residual)',
                  fontsize=10, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#0055bb')
    ax2b.tick_params(axis='y', labelcolor='#cc4400')
    ax2.legend(loc='upper left',  fontsize=8)
    ax2b.legend(loc='upper right', fontsize=8)
    # Annotate risk values
    for xi, rv in zip(x, risks):
        ax2b.text(xi + width / 2, rv + 0.003,
                  f'{rv:.3f}', ha='center', va='bottom', fontsize=9, color='#880000')

    fig.suptitle('Preprocessing Pipeline Analysis\n' + DISCLAIMER, fontsize=9)
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, 'organic_waste_preprocessing_pipeline.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─────────────────────────────────────────────────────────────────
# Figure 3: Food transition relay phases
# ─────────────────────────────────────────────────────────────────

def plot_food_transition_relay(sc_full: Dict, sc_hrs: Dict,
                               years: np.ndarray, ft: FoodTransitionParams) -> str:
    """
    2x2 panel comparing HRS+DGS vs Full Relay on 4 key metrics,
    with phase-zone annotations where relay is active.
    """
    relay_yr = sc_full.get('relay_active_since')

    panels = [
        ('vegetation_cover',    'Vegetation Cover Index',   '#007733'),
        ('food_production',     'Food Production Potential','#cc7700'),
        ('microbial_diversity', 'Microbial Diversity Index','#884499'),
        ('carbon_fixation',     'Carbon Fixation Potential','#0055bb'),
    ]

    phase_colors = ['#ffe8a0', '#c8e8ff', '#c8ffcc']
    phase_labels = ['Phase 1\nTuber', 'Phase 2\nLegume', 'Phase 3\nHerb/Mixed']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, (key, title, color) in enumerate(panels):
        ax = axes[i]
        # HRS + DGS baseline (no relay)
        ax.plot(years, sc_hrs[key],
                color='#0055bb', linestyle='--', linewidth=1.8,
                label='HRS + DGS (no relay)', alpha=0.7)
        # Full relay
        ax.plot(years, sc_full[key],
                color=color, linestyle='-', linewidth=2.5,
                label='HRS + DGS + Food Relay')
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlabel('Year', fontsize=9)
        ax.set_ylabel('Hypothetical Index [0-1]', fontsize=9)
        ax.set_xlim(years[0], years[-1])
        ax.set_ylim(-0.02, 1.05)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

        # Phase zone annotations (only if relay activated)
        if relay_yr is not None:
            yr_p1_start = START_YEAR + relay_yr
            yr_p2_start = START_YEAR + relay_yr + ft.phase2_start_yr
            yr_p3_start = START_YEAR + relay_yr + ft.phase3_start_yr
            yr_end      = years[-1]
            spans = [
                (yr_p1_start, min(yr_p2_start, yr_end)),
                (yr_p2_start, min(yr_p3_start, yr_end)),
                (yr_p3_start, yr_end),
            ]
            for (ps, pe), pc, pl in zip(spans, phase_colors, phase_labels):
                if ps < yr_end:
                    ax.axvspan(ps, pe, alpha=0.15, color=pc, zorder=0)
                    mid = (ps + min(pe, yr_end)) / 2.0
                    ax.text(mid, 0.97, pl, ha='center', va='top',
                            fontsize=6, color='#555555', style='italic')

    relay_note = (f'Food relay activated ~{START_YEAR + relay_yr}'
                  if relay_yr is not None else 'Food relay did not activate')
    fig.suptitle('Food Transition Relay Phases -- HRS + DGS + Food Relay vs HRS + DGS\n'
                 f'({relay_note}; phase boundaries are approximate)\n' + DISCLAIMER,
                 fontsize=9)
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, 'organic_waste_food_transition_relay.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─────────────────────────────────────────────────────────────────
# Summary print
# ─────────────────────────────────────────────────────────────────

def print_summary(scenarios: List[Dict]) -> None:
    print()
    print('=' * 80)
    print('ORGANIC WASTE -> HRS -> DGS -> FOOD RELAY: YEAR 2075 SUMMARY')
    print('CONCEPTUAL MODEL -- All values are HYPOTHETICAL, not real measurements.')
    print('=' * 80)
    hdr = ('Scenario', 'SoilC', 'WaterR', 'MicDiv',
           'VegCov', 'FoodProd', 'CarbFix', 'Risk')
    print('{:<40} {:>6} {:>6} {:>6} {:>6} {:>8} {:>7} {:>6}'.format(*hdr))
    print('-' * 95)
    for sc in scenarios:
        print(('{:<40} {:>6.3f} {:>6.3f} {:>6.3f} '
               '{:>6.3f} {:>8.3f} {:>7.3f} {:>6.3f}').format(
            sc['name'][:39],
            sc['soil_carbon'][-1],
            sc['water_retention'][-1],
            sc['microbial_diversity'][-1],
            sc['vegetation_cover'][-1],
            sc['food_production'][-1],
            sc['carbon_fixation'][-1],
            sc['residual_risk'][-1],
        ))
    print('-' * 95)
    print()
    print('Phase activation (Scenario 4):')
    s4 = scenarios[3]
    dgs_yr  = s4.get('dgs_active_since')
    rly_yr  = s4.get('relay_active_since')
    print('  DGS vegetation start : year {} (water retention threshold met)'.format(
        START_YEAR + dgs_yr if dgs_yr else 'not reached'))
    print('  Food relay activation: year {} (vegetation cover threshold met)'.format(
        START_YEAR + rly_yr if rly_yr else 'not reached'))
    print()
    print('KEY OBSERVATIONS (conceptual only):')
    print('  1. Baseline Desert shows slow continued degradation without intervention.')
    print('  2. Organic Waste Only provides modest soil gain but elevated residual risk.')
    print('  3. HRS + DGS achieves meaningful soil and vegetation recovery at lower risk.')
    print('  4. Full Relay adds food production, biodiversity, and carbon fixation gains.')
    print('  5. Residual risk > 0 in ALL scenarios with organic input. Zero is not modelled.')
    print()
    print('ALL values require independent scientific, sanitary, and engineering validation.')
    print('Water availability (modelled as stress factor 0.60) is the primary constraint.')
    print('=' * 80)


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

def main():
    waste = WasteStream()
    pre   = PreprocessingParams()
    hrs   = HRSParams()
    dgs   = DGSParams()
    ft    = FoodTransitionParams()

    # -- Scenario 1: Baseline Desert (no intervention)
    s1 = run_scenario('1. Baseline Desert',
                      use_hrs=False, use_dgs=False,
                      use_food_relay=False, raw_waste_only=False,
                      waste=waste, pre=pre, hrs=hrs, dgs=dgs, ft=ft)

    # -- Scenario 2: Organic Waste Only (raw / minimal processing)
    s2 = run_scenario('2. Organic Waste Only (minimal)',
                      use_hrs=False, use_dgs=False,
                      use_food_relay=False, raw_waste_only=True,
                      waste=waste, pre=pre, hrs=hrs, dgs=dgs, ft=ft)

    # -- Scenario 3: HRS + DGS (fully processed, no food relay)
    s3 = run_scenario('3. HRS + DGS (processed)',
                      use_hrs=True, use_dgs=True,
                      use_food_relay=False, raw_waste_only=False,
                      waste=waste, pre=pre, hrs=hrs, dgs=dgs, ft=ft)

    # -- Scenario 4: HRS + DGS + Food Transition Relay (full system)
    s4 = run_scenario('4. HRS + DGS + Food Relay (full)',
                      use_hrs=True, use_dgs=True,
                      use_food_relay=True, raw_waste_only=False,
                      waste=waste, pre=pre, hrs=hrs, dgs=dgs, ft=ft)

    scenarios = [s1, s2, s3, s4]

    print_summary(scenarios)

    print('Generating figures...')
    out1 = plot_main_indices(scenarios, YEARS)
    out2 = plot_preprocessing_pipeline(waste)
    out3 = plot_food_transition_relay(s4, s3, YEARS, ft)
    print('Saved: ' + out1)
    print('Saved: ' + out2)
    print('Saved: ' + out3)
    print('All figures saved to: ' + FIGURES_DIR)


if __name__ == '__main__':
    main()
