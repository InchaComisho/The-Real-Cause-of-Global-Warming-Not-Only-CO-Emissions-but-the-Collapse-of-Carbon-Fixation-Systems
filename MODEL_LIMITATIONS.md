# Model Limitations and Disclaimers

*A full disclosure of the hypothetical nature, unverified assumptions, and calibration requirements of all Python simulation models in this repository.*

---

## Purpose of This Document

This repository contains four Python simulation models:

- `causal_carbon_model.py`
- `historical_phase_model.py`
- `feedback_loop_simulation.py`
- `scenario_examples.py`

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

## Author

Master
inchacomisho / inchacomusho

AI Collaborators: G (ChatGPT), Copi (Microsoft Copilot), Mini (Google Gemini), Clus (Anthropic Claude), Real (Perplexity AI), Lora (Dola)

Published: May 2026

License: CC BY-SA 4.0
https://creativecommons.org/licenses/by-sa/4.0/
