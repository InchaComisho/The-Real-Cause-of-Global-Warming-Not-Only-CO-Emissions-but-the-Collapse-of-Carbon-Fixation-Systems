"""
sensitivity_analysis.py
========================
One-at-a-time parameter sensitivity analysis for scenario_examples.py

For each of five key parameters, this script sweeps a range of values and
records the unbounded CO2 pressure (co2_pressure) at year 2099 for two
contrasting scenarios:

  Scenario 2 — Decarbonization Only (emissions cut, no fixation restoration)
  Scenario 4 — Integrated Approach  (emissions cut + full fixation restoration)

The gap between the two lines reveals how much fixation restoration contributes
*relative to decarbonization alone* as each parameter varies.

Parameters swept (one at a time, all others held at default):
  1. emission_reduction_rate        — speed of decarbonization
  2. terrestrial_restoration_rate   — speed of land/soil recovery
  3. ocean_restoration_rate         — speed of marine ecosystem recovery
  4. degrad_co2_weight              — sensitivity of CO2 balance to degradation release
  5. warming_feedback_strength      — CO2 → continued fixation decline feedback gain

⚠️  IMPORTANT LIMITATIONS
    All parameters and sweep ranges are HYPOTHETICAL.
    Results are conceptual illustrations only, not climate projections.
    They are NOT calibrated against real data.
    See MODEL_LIMITATIONS.md for full disclosure.

Author: Master (inchacomisho / inchacomusho)
AI Collaborators: G, Copi, Mini, Cruz, Real, Lola
Published: May 2026
License: CC BY-SA 4.0
"""

from __future__ import annotations

import os
import copy
from dataclasses import replace

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from scenario_examples import StartingState, ScenarioParameters, ScenarioEngine


# ─────────────────────────────────────────────────────────────────
# 1. Sweep specification
# ─────────────────────────────────────────────────────────────────

SWEEP_SPECS = [
    {
        "label":   "emission_reduction_rate",
        "display": "Emission Reduction Rate\n(decarbonization speed)",
        "attr":    "emission_reduction_rate",
        "default": ScenarioParameters().emission_reduction_rate,
        "values":  np.linspace(0.005, 0.035, 25),
    },
    {
        "label":   "terrestrial_restoration_rate",
        "display": "Terrestrial Restoration Rate\n(forest + soil recovery speed)",
        "attr":    "terrestrial_restoration_rate",
        "default": ScenarioParameters().terrestrial_restoration_rate,
        "values":  np.linspace(0.002, 0.022, 25),
    },
    {
        "label":   "ocean_restoration_rate",
        "display": "Ocean Restoration Rate\n(marine ecosystem recovery speed)",
        "attr":    "ocean_restoration_rate",
        "default": ScenarioParameters().ocean_restoration_rate,
        "values":  np.linspace(0.001, 0.015, 25),
    },
    {
        "label":   "degrad_co2_weight",
        "display": "Degradation CO2 Weight\n(sensitivity to ecosystem release)",
        "attr":    "degrad_co2_weight",
        "default": ScenarioParameters().degrad_co2_weight,
        "values":  np.linspace(0.02, 0.35, 25),
    },
    {
        "label":   "warming_feedback_strength",
        "display": "Warming Feedback Strength\n(CO2 → continued fixation decline)",
        "attr":    "warming_feedback_strength",
        "default": ScenarioParameters().warming_feedback_strength,
        "values":  np.linspace(0.01, 0.25, 25),
    },
]

SCENARIO_COLORS = {
    "2. Decarbonization Only": "#E67E22",
    "4. Integrated Approach":  "#27AE60",
}


# ─────────────────────────────────────────────────────────────────
# 2. Engine helper
# ─────────────────────────────────────────────────────────────────

def _run_pair(params: ScenarioParameters) -> tuple[float, float]:
    """
    Run Scenario 2 (Decarbonisation Only) and Scenario 4 (Integrated)
    with the given ScenarioParameters.
    Returns (co2_pressure_decarb_2099, co2_pressure_integrated_2099).
    """
    start  = StartingState()
    engine = ScenarioEngine(start, params)

    sc_dc  = engine.run_scenario(
        "2. Decarbonization Only",
        reduce_emissions=True,  restore_terrestrial=False, restore_ocean=False,
    )
    sc_int = engine.run_scenario(
        "4. Integrated Approach",
        reduce_emissions=True,  restore_terrestrial=True,  restore_ocean=True,
    )

    return float(sc_dc["co2_pressure"][-1]), float(sc_int["co2_pressure"][-1])


# ─────────────────────────────────────────────────────────────────
# 3. Sweep runner
# ─────────────────────────────────────────────────────────────────

def run_sensitivity() -> list[dict]:
    """
    For each sweep spec, vary the target parameter over its value range
    while holding all other parameters at their defaults.
    Returns a list of result dicts, one per sweep spec.
    """
    base_params = ScenarioParameters()
    results = []

    for spec in SWEEP_SPECS:
        attr   = spec["attr"]
        values = spec["values"]
        dc_out  = np.zeros(len(values))
        int_out = np.zeros(len(values))

        for i, v in enumerate(values):
            # Build a modified ScenarioParameters with one field changed
            p = replace(base_params, **{attr: float(v)})
            dc_out[i], int_out[i] = _run_pair(p)

        results.append({
            "label":   spec["label"],
            "display": spec["display"],
            "default": spec["default"],
            "values":  values,
            "decarb":  dc_out,
            "integrated": int_out,
        })
        print(f"  Swept: {attr:40s}  "
              f"Decarb 2099 range [{dc_out.min():.3f}, {dc_out.max():.3f}]  "
              f"Integrated 2099 range [{int_out.min():.3f}, {int_out.max():.3f}]")

    return results


# ─────────────────────────────────────────────────────────────────
# 4. Visualization
# ─────────────────────────────────────────────────────────────────

def plot_sensitivity(results: list[dict]) -> None:
    os.makedirs("figures", exist_ok=True)

    n = len(results)
    cols = 3
    rows = (n + cols - 1) // cols   # ceiling division  => 2 rows for 5 panels

    fig, axes = plt.subplots(rows, cols, figsize=(14, 8))
    axes_flat = axes.flatten()

    fig.suptitle(
        "Sensitivity Analysis: CO₂ Pressure at 2099 vs. Key Parameters\n"
        "Comparing Decarbonization Only vs. Integrated Approach (Decarb + Restoration)\n"
        "⚠ HYPOTHETICAL CONCEPTUAL VALUES — Not climate projections.",
        fontsize=9, fontweight="bold", color="#8B0000",
    )

    for ax, res in zip(axes_flat, results):
        v   = res["values"]
        dc  = res["decarb"]
        ing = res["integrated"]
        gap = dc - ing                 # positive gap = integrated is better

        ax.plot(v, dc,  color=SCENARIO_COLORS["2. Decarbonization Only"],
                linewidth=2.0, label="Decarb Only")
        ax.plot(v, ing, color=SCENARIO_COLORS["4. Integrated Approach"],
                linewidth=2.0, label="Integrated")
        ax.fill_between(v, ing, dc, alpha=0.12, color="#27AE60",
                        label="Benefit of restoration")

        # Mark the default parameter value
        ax.axvline(res["default"], color="#555", linewidth=1.0,
                   linestyle="--", label=f"Default ({res['default']:.3f})")

        ax.set_title(res["display"], fontsize=8.5)
        ax.set_xlabel("Parameter value", fontsize=8)
        ax.set_ylabel("CO₂ pressure (unbounded)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7, loc="best")

    # Hide any unused axes (last panel if n < rows*cols)
    for ax in axes_flat[len(results):]:
        ax.set_visible(False)

    plt.tight_layout()
    out_path = "figures/sensitivity_analysis_output.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"  -> Saved: {out_path}")
    plt.show()


# ─────────────────────────────────────────────────────────────────
# 5. Main
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("  Sensitivity Analysis (2025-2099)")
    print("  One-at-a-time parameter sweeps")
    print("  Decarbonization Only  vs.  Integrated Approach")
    print("  Metric: unbounded CO2 pressure at 2099")
    print("  WARNING: HYPOTHETICAL CONCEPTUAL MODEL -- See MODEL_LIMITATIONS.md")
    print("=" * 70)

    results = run_sensitivity()
    plot_sensitivity(results)

    print()
    print("  Interpretation notes (HYPOTHETICAL -- illustrative only):")
    print("  - A larger gap between the two lines means that fixation")
    print("    restoration matters more *relative to* decarbonisation alone")
    print("    at that parameter value.")
    print("  - When the gap narrows, decarbonisation alone is nearly as")
    print("    effective as the integrated approach under those assumptions.")
    print("  - These results depend entirely on hypothetical parameter values.")
    print("    Calibration against observed data is required before drawing")
    print("    any policy conclusions.")
    print("=" * 70)


if __name__ == "__main__":
    main()
