# Model Limitations and Disclaimers

*A full disclosure of the hypothetical nature, unverified assumptions, and calibration requirements of all Python simulation models in this repository.*

---

## Purpose of This Document

This repository contains six Python simulation models:

- `causal_carbon_model.py`
- `historical_phase_model.py`
- `feedback_loop_simulation.py`
- `scenario_examples.py`
- `sensitivity_analysis.py`
- `intervention_technology_model.py`

These models were designed to **illustrate the conceptual framework** described in `README.md` and `CAUSAL_STRUCTURE.md` — specifically, the hypothesis that global warming is driven by both CO₂ emissions and the degradation of carbon fixation systems.

**This document discloses what these models are, and what they are not.**

---

## What These Models Are

- **Conceptual illustration tools.** They translate the causal structure described in the text documents into a runnable form, allowing the relationships between pressures, fixation decline, and CO₂ accumulation to be visualized dynamically.

- **Hypothesis generators.** By adjusting parameters, researchers can explore what kinds of outcomes the multi-cause hypothesis predicts — as a starting point for designing empirical tests.

- **Structural consistency checks.** The models help verify that the causal logic described in `CAUSAL_STRUCTURE.md` is internally consistent when implemented as a dynamic simulation.

---

## What These Models Are Not

- **Scientific predictions.** These models do not generate predictions about real-world atmospheric CO₂ levels, temperature trajectories, or ecosystem states.

- **Validated earth system models.** They are not comparable to IPCC-class earth system models (CMIP6, etc.), which are calibrated against decades of observational data.

- **Policy tools.** No policy decision, investment, regulation, or scientific claim should be based on the outputs of these models without independent verification and calibration against real data.

- **Published or peer-reviewed science.** These models have not been reviewed by climate scientists, ecologists, soil scientists, or oceanographers.

---

## Hypothetical Values: Full Inventory

The following tables document all hardcoded numerical values across the four models, their role in the model, and their calibration status.

---

### `causal_carbon_model.py`

| Parameter | Value | Role | Calibration Status |
|---|---|---|---|
| `emission_start` | 0.10 | Initial normalized emission rate | 🔴 Hypothetical |
| `emission_end` | 0.65 | Final normalized emission rate | 🔴 Hypothetical |
| `land_fixation_initial` | 0.90 | Initial terrestrial fixation capacity | 🔴 Hypothetical |
| `land_fixation_decline_rate` | 0.003/yr | Rate of fixation decline | 🔴 Hypothetical |
| `ocean_uptake_initial` | 0.85 | Initial ocean uptake capacity | 🔴 Hypothetical |
| `ocean_uptake_decline_rate` | 0.001/yr | Rate of ocean uptake decline | 🔴 Hypothetical |
| `degradation_release_base` | 0.02 | Baseline ecosystem carbon release | 🔴 Hypothetical |
| `degradation_release_growth` | 0.002/yr | Growth rate of degradation release | 🔴 Hypothetical |
| `land_fixation_weight` | 0.45 | CO₂ balance weight for land | 🔴 Hypothetical |
| `ocean_uptake_weight` | 0.35 | CO₂ balance weight for ocean | 🔴 Hypothetical |
| `degradation_weight` | 0.20 | CO₂ balance weight for degradation | 🔴 Hypothetical |

---

### `historical_phase_model.py`

All phase pressure growth rates are HYPOTHETICAL. They represent the author's conceptual judgment about relative magnitudes and are not derived from historical data.

| Phase | Parameter | Value | Calibration Status |
|---|---|---|---|
| Phase 1 (1760–1945) | `deforestation_rate` | 0.0008/yr | 🔴 Hypothetical |
| Phase 1 | `urbanization_rate` | 0.0005/yr | 🔴 Hypothetical |
| Phase 1 | `agricultural_rate` | 0.0010/yr | 🔴 Hypothetical |
| Phase 2 (1945–1990) | `synth_fertilizer_rate` | 0.0120/yr | 🔴 Hypothetical |
| Phase 2 | `pesticide_rate` | 0.0090/yr | 🔴 Hypothetical |
| Phase 2 | `monoculture_rate` | 0.0100/yr | 🔴 Hypothetical |
| Phase 2 | `nutrient_runoff_rate` | 0.0080/yr | 🔴 Hypothetical |
| Phase 3 (1990–2025) | `forest_fire_rate` | 0.0150/yr | 🔴 Hypothetical |
| Phase 3 | `amazon_loss_rate` | 0.0120/yr | 🔴 Hypothetical |
| Phase 3 | `marine_deadzone_rate` | 0.0080/yr | 🔴 Hypothetical |
| All phases | `COUPLING` coefficients | 0.10–0.40 | 🔴 Hypothetical |
| All phases | System health initial values | 0.90–0.95 | 🔴 Hypothetical |
| All phases | Phase boundary years (1760, 1945, 1990, 2025) | Fixed | ⚪ Definitional |

The emission milestones {1760: 0.01, 1945: 0.15, 1990: 0.45, 2025: 0.75} are HYPOTHETICAL normalized values. They are not calibrated against Mauna Loa CO₂ data, Global Carbon Project data, or any other emission dataset.

---

### `feedback_loop_simulation.py`

All coupling coefficients and gain parameters are HYPOTHETICAL. They were chosen to produce qualitatively plausible behavior (positive feedback amplification) rather than to reproduce any measured real-world feedback magnitudes.

| Parameter | Value | Role | Calibration Status |
|---|---|---|---|
| `warming_to_forest_stress` | 0.30 | Coupling: warming → forest stress | 🔴 Hypothetical |
| `forest_loss_to_co2` | 0.25 | Coupling: forest loss → CO₂ | 🔴 Hypothetical |
| `warming_to_soil_resp` | 0.25 | Coupling: warming → soil respiration | 🔴 Hypothetical |
| `resp_acceleration` | 0.015 | Respiration increase rate | 🔴 Hypothetical |
| `soil_loss_to_co2` | 0.20 | Coupling: soil carbon loss → CO₂ | 🔴 Hypothetical |
| `warming_to_stratification` | 0.20 | Coupling: warming → stratification | 🔴 Hypothetical |
| `strat_to_phyto_loss` | 0.30 | Coupling: stratification → phyto | 🔴 Hypothetical |
| `phyto_to_ocean_co2` | 0.22 | Coupling: phyto loss → CO₂ | 🔴 Hypothetical |
| `global_co2_warming_sensitivity` | 0.15 | CO₂ → warming feedback gain | 🔴 Hypothetical |
| All initial state values | various | Starting conditions | 🔴 Hypothetical |
| All scaling multipliers (0.004–0.015) | various | Numerical stability factors | 🔴 Hypothetical |

---

### `scenario_examples.py`

| Parameter | Value | Role | Calibration Status |
|---|---|---|---|
| All `StartingState` values (2025 conditions) | 0.52–0.75 | Initial conditions from historical model | 🔴 Hypothetical (inherited) |
| `emission_reduction_rate` | 0.018/yr | Decarbonization speed | 🔴 Hypothetical |
| `bau_emission_growth` | 0.004/yr | BAU emission growth | 🔴 Hypothetical |
| `terrestrial_restoration_rate` | 0.008/yr | Active restoration speed | 🔴 Hypothetical |
| `soil_restoration_rate` | 0.006/yr | Soil restoration speed | 🔴 Hypothetical |
| `ocean_restoration_rate` | 0.005/yr | Ocean restoration speed | 🔴 Hypothetical |
| `passive_terr_decline` | 0.003/yr | Decline without intervention | 🔴 Hypothetical |
| `warming_feedback_strength` | 0.08 | Feedback gain from CO₂ | 🔴 Hypothetical |
| All CO₂ balance weights | 0.25–0.35 | Relative system contributions | 🔴 Hypothetical |

---

## Structural Limitations

Beyond parameter values, the model structure itself involves simplifications that may not represent real-world dynamics.

### 1. Linear coupling

Most relationships in these models are linear (pressure × coefficient = change in health). Real-world carbon cycle dynamics are nonlinear, involve threshold effects, and vary substantially by region, climate regime, and ecosystem type.

### 2. Timescale conflation

The models aggregate processes that operate on very different timescales — from seasonal (phytoplankton blooms) to decadal (soil carbon stabilization) to millennial (deep ocean circulation). This conflation is a known limitation.

### 3. No spatial resolution

The models operate as globally aggregated indices. Regional dynamics (Amazon vs. boreal forest; tropical ocean vs. polar) are not captured.

### 4. No carbon chemistry

The CO₂ index used in these models is a simplified accumulation counter, not a physically correct representation of atmospheric CO₂ in ppm, ocean pCO₂, or carbonate chemistry. The relationship between CO₂ index and temperature is not physically derived.

### 5. No economic or political dynamics

Restoration and decarbonization are modeled as simple rate changes applied uniformly over time. Real-world policy implementation involves political, economic, and social constraints not captured here.

### 6. No tipping points

The models do not include explicit tipping point mechanisms (e.g., Amazon dieback threshold, AMOC collapse threshold). This may underestimate the risk of abrupt transitions.

---

## What Calibration Would Require

To convert these models from conceptual illustrations into scientifically valid tools, the following calibration steps would be required:

1. **Pressure variable calibration:** Each pressure variable (deforestation rate, fertilizer use, etc.) should be replaced with normalized historical data from FAO, FAOSTAT, Global Forest Watch, USGS, or equivalent sources.

2. **Fixation capacity calibration:** Each fixation health variable should be calibrated against observed data — net biome production from FLUXNET, soil carbon from ISRIC, ocean productivity from SeaWiFS/MODIS, etc.

3. **CO₂ index calibration:** The CO₂ index should be replaced by or calibrated against actual atmospheric CO₂ concentration data (Mauna Loa, ice core records) in units of ppm.

4. **Coupling coefficient estimation:** Statistical regression or sensitivity analysis should be used to estimate coupling coefficients from observational data rather than setting them by author judgment.

5. **Model validation:** The calibrated model should be validated against held-out data (e.g., hindcast the 1990–2025 period against known observations) before being used for projection.

6. **Uncertainty quantification:** Probability distributions should replace point estimates for all parameters. Ensemble runs should be used to characterize model uncertainty.

---

## Relationship to Existing Science

The causal mechanisms illustrated by these models are grounded in established scientific literature:

| Mechanism | Scientific Basis |
|---|---|
| Terrestrial carbon sink variability | Global Carbon Project annual budgets |
| Forest carbon source (Amazon) | Gatti et al. (2021), *Science* |
| Soil carbon loss under warming | Crowther et al. (2016), *Nature* |
| Phytoplankton biomass trends | Boyce et al. (2010), *Nature* |
| Ocean stratification increase | IPCC AR6 WGI, Chapter 9 |
| Soil carbon under agriculture | Lal (2004), *Science*; Poeplau & Don (2015) |
| Natural climate solutions potential | Griscom et al. (2017), *PNAS* |

However, these models do not reproduce or validate against any of the above studies. They use these studies only as qualitative support for the direction of the causal relationships, not for the magnitude of the parameter values.

---

## Summary: What Readers Should Conclude

| Claim | Valid? |
|---|---|
| The causal structure (nodes and relationships) is logically consistent | ✅ Yes — within the model's simplifications |
| The parameter values represent real-world magnitudes | ❌ No — all hypothetical |
| The model outputs can be compared to IPCC projections | ❌ No — incompatible scale and structure |
| The scenario comparison shows which policy is most effective | ❌ No — illustrative only |
| The models support the general plausibility of the multi-cause hypothesis | ✅ Tentatively — but require empirical validation |
| The models are a valid starting point for designing verification studies | ✅ Yes — as a structural scaffold |

---

---

## Appendix: Decarbonization as a Policy Assumption, Not a Physical Process

### Core limitation

In `scenario_examples.py`, the "Announced Decarbonization Only" scenario assumes that global total CO₂ emissions decline at a rate of approximately 0.018 normalized units per year, corresponding to net-zero by around 2050 from a 2025 baseline. This represents the optimistic case where announced national and international policy targets are met globally.

**This is a policy assumption, not an observed physical outcome.**

### Why Announced Decarbonization is an optimistic scenario

As of the model's publication date (May 2026), global CO₂ emissions have not entered a structurally sustained year-over-year decline at the scale implied by the Announced scenario. Key structural barriers include:

- **Developing-nation industrialization.** Nations in South and Southeast Asia, Africa, and Latin America are actively expanding energy infrastructure, industrial capacity, and transportation networks. This drives aggregate emission growth that may offset cuts made in developed economies.
- **Population growth.** Global population increase, particularly in regions with lower per-capita energy access, is associated with rising total energy demand even at constant per-capita efficiency levels.
- **Electricity demand growth.** Electrification of transport, heating, and industry (which is itself part of decarbonization in developed countries) increases total electricity demand, which in many developing regions is still supplied largely from fossil sources.
- **COVID-19 as a temporary shock.** Global CO₂ emissions temporarily declined in 2020 due to pandemic-related reductions in transport, industry, and economic activity. This decline reversed rapidly in 2021–2022. It should be treated as a temporary external shock to the system, not as evidence of structural decarbonization. This model does not simulate temporary shocks.

### How the realistic scenario is modelled (HYPOTHETICAL)

`scenario_examples.py` (v3) introduces a second decarbonization scenario:

**2b. Realistic Global Decarbonization Only**

The emission trajectory is governed by:

```
net_global_decarbonization_rate  
  = developed_country_reduction_rate         (0.018 / yr)
  - developing_country_emissions_growth      (0.008 / yr)
  - population_energy_demand_growth          (0.003 / yr)
  - industrialization_pressure               (0.004 / yr)
  = 0.003 / yr  (net)
```

All four component rates are **HYPOTHETICAL**. They do not reproduce any specific historical dataset. They are chosen to illustrate the structural logic that offset pressures can substantially slow the effective global emission trajectory.

| Component | Default value | Calibration |
|---|---|---|
| `developed_country_reduction_rate` | 0.018 / yr | 🔴 Hypothetical |
| `developing_country_emissions_growth` | 0.008 / yr | 🔴 Hypothetical |
| `population_energy_demand_growth` | 0.003 / yr | 🔴 Hypothetical |
| `industrialization_pressure` | 0.004 / yr | 🔴 Hypothetical |
| `net_global_decarbonization_rate` | 0.003 / yr | 🔴 Hypothetical (derived) |
| `realistic_emission_floor` | 0.10 | 🔴 Hypothetical |

### What these two scenarios can and cannot claim

| Claim | Valid? |
|---|---|
| Announced Decarb (2a) represents a coherent optimistic policy trajectory | ✅ Yes — as a structural assumption |
| Realistic Decarb (2b) represents an observed real-world trajectory | ❌ No — it is a hypothetical illustration |
| The gap between 2a and 2b (CO₂ pressure at 2099: 0.388 units) is quantitatively accurate | ❌ No — depends entirely on hypothetical rates |
| The gap illustrates the structural logic that offset pressures matter | ✅ Yes — as a directional illustration |
| Either scenario should be used for policy conclusions | ❌ No — calibration against real emission databases required |

### What calibration would require

To make these scenarios empirically grounded:
- Replace `developed_country_reduction_rate` with observed emission trends from IEA, Global Carbon Project, or UNFCCC national inventory data for OECD nations.
- Replace `developing_country_emissions_growth` with observed trends for non-OECD nations (IEA World Energy Outlook, BP Statistical Review).
- Replace `population_energy_demand_growth` with UN World Population Prospects × IEA per-capita energy intensity trends.
- Replace `industrialization_pressure` with industrial sector CO₂ growth in emerging markets (IEA Industrial Transitions, OECD Economic Outlook).

---

## Appendix: CO₂ Index Scaling and the Near-Identical Scenario Problem

### What the problem was

In the initial version of `scenario_examples.py`, the CO₂ delta function contained the expression:

```python
return max(0.0, emission - fixation_removal * 0.85 + degradation_input) * 0.012
```

The `max(0.0, ...)` floor meant that any scenario in which restored fixation capacity exceeded emissions would produce **zero delta** rather than **negative delta (CO₂ drawdown)**. This is physically incorrect: a sufficiently healthy carbon cycle should be able to draw CO₂ down, not merely stop accumulating it.

Additionally, the `co2` variable was clipped to `[0.0, 1.0]`. In scenarios with high accumulated CO₂, both "Decarbonization Only" and "Integrated Approach" could be pressed against the ceiling, making them visually indistinguishable.

### What was changed (v2)

1. **Floor removed.** `_co2_delta` now returns `(emission - fixation_removal * 0.85 + degradation_input) * 0.012` without a lower bound, allowing genuine drawdown when restored fixation capacity is strong enough.

2. **Unbounded `co2_pressure` variable added.** `run_scenario` now tracks both:
   - `co2` — clipped to `[0, 1]`, kept for backward compatibility.
   - `co2_pressure` — unbounded float accumulator, used in all comparison plots and summary tables.

3. **New `sensitivity_analysis.py`** sweeps five key parameters to show how the gap between "Decarbonization Only" and "Integrated Approach" changes as parameter assumptions change.

### What calibration would be required to resolve this structurally

The near-identical scenario result was a symptom of two deeper problems:

| Problem | Required fix |
|---|---|
| Scaling mismatch: the 0.012 multiplier and the 0.85 fixation efficiency factor were chosen arbitrarily | Calibrate against observed net primary production, ocean uptake flux, and atmospheric CO₂ growth rates (e.g., from Global Carbon Project) |
| Fixation and degradation weights (0.10–0.35) are not grounded in observational data | Derive from FLUXNET biome carbon flux data, ISRIC soil carbon maps, and SeaWiFS/MODIS ocean productivity records |
| `warming_feedback_strength` (0.08) is hypothetical | Estimate from observed correlations between CO₂ anomalies and land/ocean sink efficiency (e.g., Le Quéré et al., Global Carbon Budget annual updates) |

Until these calibration steps are completed, **no quantitative comparison between scenarios should be treated as a prediction or used as a basis for policy decisions**. The scenario outputs are illustrative of structural logic only.

---

## Appendix: `intervention_technology_model.py` — Technology Limitations

### What this model does

`intervention_technology_model.py` extends the scenario framework to include five proposed natural-complementary technologies: OBS (Ocean Breathing System), OTU (Ocean Thermal / Upwelling Unit), UMC (Ultrasonic Mist Cooling), HRS (Humus Recycling System), and DGS (Desert Greening Support). It also introduces a **thermal stress index** as a new state variable, driven by CO₂ pressure feedback and reduced by UMC deployment.

### Technology effect parameters (all HYPOTHETICAL)

| Technology | Parameter | Value | Role | Calibration Status |
|---|---|---|---|---|
| OBS | `obs_ocean_health_rate` | 0.008/yr | Deep-O₂ → ocean health | 🔴 Hypothetical |
| OBS | `obs_plankton_recovery` | 0.005/yr | Plankton productivity | 🔴 Hypothetical |
| OBS | `obs_uptake_boost` | 0.004/yr | Direct CO₂ uptake boost | 🔴 Hypothetical |
| OTU | `otu_upwelling_rate` | 0.006/yr | Nutrient upwelling | 🔴 Hypothetical |
| OTU | `otu_recovery_rate` | 0.004/yr | Ocean metabolic recovery | 🔴 Hypothetical |
| UMC | `umc_thermal_rate` | 0.012/yr | Thermal stress reduction | 🔴 Hypothetical |
| UMC | `umc_land_benefit` | 0.003/yr | Indirect land fixation gain | 🔴 Hypothetical |
| HRS | `hrs_soil_rate` | 0.010/yr | Soil microbial recovery | 🔴 Hypothetical |
| HRS | `hrs_terr_boost` | 0.005/yr | Land fixation improvement | 🔴 Hypothetical |
| DGS | `dgs_greening_rate` | 0.005/yr | New vegetation area/yr | 🔴 Hypothetical |
| DGS | `dgs_max_new_area` | 0.300 | Max restorable fraction | 🔴 Hypothetical |
| DGS | `dgs_fixation_boost` | 0.300 | Max add. fixation at full area | 🔴 Hypothetical |
| All | `thermal_bau_growth` | 0.005/yr | BAU thermal stress growth | 🔴 Hypothetical |
| All | `thermal_co2_feedback` | 0.006/yr | CO₂ → thermal amplification | 🔴 Hypothetical |
| All | `thermal_land_coupling` | 0.120 | Thermal → land fixation loss | 🔴 Hypothetical |
| All | `thermal_ocean_coupling` | 0.080 | Thermal → ocean uptake loss | 🔴 Hypothetical |

### What field validation would require

**OBS (Ocean Breathing System):**
- Controlled mesocosm studies measuring O₂ injection effects on plankton productivity and carbon export flux.
- Assessment of nutrient balance disruption, dead-zone recovery rates, and potential for unintended ecological effects (e.g., altered food-web dynamics, invasive species vectors).
- Scaling studies: single-unit pilot → regional array → open-ocean deployment.
- Monitoring protocols for ocean acidification interaction effects.

**OTU (Ocean Thermal / Upwelling Unit):**
- Pilot upwelling experiments measuring nutrient flux, surface productivity, and net CO₂ exchange.
- Risk assessment for disruption of natural thermal stratification, AMOC interaction, and deep-water current patterns.
- Studies of potential negative outcomes: upwelling of deep CO₂-rich water offsetting biological pump gains.
- Coastal vs. open-ocean siting constraints.

**UMC (Ultrasonic Mist Cooling):**
- Field trials measuring effective thermal reduction radius, water consumption rates, and energy requirements.
- Studies of interaction effects with local precipitation patterns, humidity, and urban heat island dynamics.
- Assessment at regional scale: cumulative water use vs. local water cycle capacity.
- Indirect ecological effects of altered local microclimate on surrounding vegetation.

**HRS (Humus Recycling System):**
- Field trials measuring actual humus formation rates from food waste, fallen leaves, and organic biomass inputs.
- Soil carbon stabilization studies: distinguishing labile from stable carbon fractions.
- Microbial community recovery timescales under regenerative input regimes.
- Contamination risk assessment for urban organic waste streams.

**DGS (Desert Greening Support):**
- Regional pilots measuring soil formation rates under humus import + vegetation establishment.
- Long-term carbon fixation monitoring (FLUXNET-style eddy covariance) on restored sites.
- Hydrological studies: vegetation water demand vs. local groundwater and precipitation availability.
- Biodiversity risk assessment: native species compatibility, invasive species control.

### Structural limitations specific to this model

1. **Technology effects are additive and linear.** Real-world interactions between OBS, OTU, UMC, HRS, and DGS may be synergistic, antagonistic, or subject to diminishing returns not captured here.

2. **Scale factor is a global uniform multiplier.** Real deployment would be geographically uneven, with local saturation effects, transport costs, and site-specific constraints not modelled.

3. **Thermal stress is a single global index.** Regional variation (Arctic amplification, tropical wet-bulb limits, monsoon disruption) is not captured.

4. **No energy budget or resource constraint.** Operating OBS, OTU, and UMC requires energy and materials. The model does not account for the energy-carbon footprint of technology deployment.

5. **No ecological risk feedback.** If OBS or OTU deployment has negative side effects (e.g., deep CO₂ upwelling, habitat disruption), those feedbacks are not modelled.

### What this model can and cannot claim

| Claim | Valid? |
|---|---|
| Technologies are correctly defined as a separate intervention pathway | ✅ Yes — structurally appropriate |
| The direction of effects (OBS improves ocean uptake, UMC reduces thermal stress) is consistent with proposed mechanisms | ✅ Tentatively — as directional hypotheses |
| The magnitude of technology effects represents real-world impact | ❌ No — all hypothetical |
| The scale sweep correctly shows that local-scale deployment has negligible planetary effect | ✅ Yes — follows from the scale_factor multiplier structure |
| The model proves OBS/OTU/UMC would work as described | ❌ No — field validation required |
| The model supports OBS/OTU/UMC as worthy of further research and pilot testing | ✅ Tentatively — as a structural rationale |

---

## Author

Master
inchacomisho / inchacomusho

AI Collaborators: G (ChatGPT), Copi (Microsoft Copilot), Mini (Google Gemini), Clus (Anthropic Claude), Real (Perplexity AI), Lora (Dola)

Published: May 2026

License: CC BY-SA 4.0
https://creativecommons.org/licenses/by-sa/4.0/
