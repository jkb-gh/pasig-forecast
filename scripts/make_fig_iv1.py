"""Figure IV.1 (Chapter IV A): system architecture of the forecasting pipeline.

    python scripts/make_fig_iv1.py   ->  reports/figures/fig_IV-1_system_architecture.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "reports" / "figures" / "fig_IV-1_system_architecture.png"
C_IN, C_MOD, C_GATE, C_OUT, C_EDGE = "#dbe7f3", "#e3f1e0", "#f6e7c8", "#fbe1dc", "#444444"


def box(ax, x, y, w, h, title, body, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.012",
                                fc=color, ec=C_EDGE, lw=1))
    ax.text(x + w / 2, y + h - 0.012, title, ha="center", va="top", fontsize=8.6, weight="bold")
    ax.text(x + w / 2, y + h - 0.036, body, ha="center", va="top", fontsize=7.1, linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10, lw=1,
                                 color=C_EDGE, linestyle=ls))


def main():
    fig, ax = plt.subplots(figsize=(10, 11.2))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # external inputs
    box(ax, 0.02, 0.885, 0.30, 0.095, "MMDA EFCOS water levels",
        "hourly, 2018–2024; Pandacan (target),\nSto. Niño, Fort Santiago and others", C_IN)
    box(ax, 0.35, 0.885, 0.30, 0.095, "MMDA Aviles and Quiapo logs",
        "hourly pumps running, gate status,\ninside and outside levels (to mid-July 2024)", C_IN)
    box(ax, 0.68, 0.885, 0.30, 0.095, "PAGASA Science Garden",
        "6-hourly rainfall; daily relative humidity,\npressure and mean temperature", C_IN)

    # module 1
    box(ax, 0.17, 0.745, 0.66, 0.105, "Module 1. Data ingestion and quality control (Notebook 01)",
        "file manifest and checksums; parsers; time alignment (PHT, rain usable 1 h after its period);\n"
        "QC flags; gaps ≤ 3 h filled; coverage rule; one hourly table; chronological split;\n"
        "fixed evaluation hours", C_MOD)
    for x in (0.17, 0.50, 0.83):
        arrow(ax, x, 0.885, 0.5 if x == 0.50 else (0.30 if x < 0.5 else 0.70), 0.852)

    # modules 2-4
    box(ax, 0.02, 0.585, 0.30, 0.125, "Module 2. Link analysis and\nalert levels (Notebook 02)",
        "\n\nlogistic regression of drainage\nstress on Pandacan level and rain (H1);\n"
        "high-water 11.69 m, flood-risk 12.00 m", C_MOD)
    box(ax, 0.35, 0.585, 0.30, 0.125, "Module 3. Tide and feature\nbuilder (Notebook 03)",
        "\n\nharmonic tide fit (2018–2022);\n24-hour windows; tabular features;\nmin-max scalers", C_MOD)
    box(ax, 0.68, 0.585, 0.30, 0.125, "Module 4. Granger input\nselection (Notebook 04)",
        "\n\nde-tided level; ADF; BIC lags;\nBonferroni F-tests (H2);\nselected: rainfall, pressure", C_MOD)
    arrow(ax, 0.30, 0.745, 0.17, 0.712)
    arrow(ax, 0.50, 0.745, 0.50, 0.712)
    arrow(ax, 0.70, 0.745, 0.83, 0.712)
    arrow(ax, 0.65, 0.645, 0.68, 0.645, style="<|-|>")

    # module 5
    box(ax, 0.17, 0.425, 0.66, 0.125, "Module 5. Model training and tuning (Notebook 05)",
        "\nhybrid LSTM-GRU + tabular network (two-stage grid, 5 seeds); standalone LSTM;\n"
        "persistence, tide-only, tide + residual, ridge, KNN; Logistic Regression and KNN classifiers;\n"
        "trigger offsets and thresholds tuned on 2023; checks G11–G16, G19", C_MOD)
    arrow(ax, 0.17, 0.585, 0.30, 0.552)
    arrow(ax, 0.50, 0.585, 0.50, 0.552)
    arrow(ax, 0.83, 0.585, 0.70, 0.552)

    # freeze gate
    box(ax, 0.30, 0.335, 0.40, 0.06, "Settings frozen (G17)",
        "SHA-256 manifest of every setting and model; git tag", C_GATE)
    arrow(ax, 0.50, 0.425, 0.50, 0.397)

    # modules 6-7
    box(ax, 0.02, 0.17, 0.46, 0.13, "Module 6. Test evaluation (Notebook 06)",
        "\nG18 opens 2024 once; predictions of every model;\nRMSE, MAE, R², skill; alerts, PR-AUC, equal recall;\n"
        "events; Diebold–Mariano + Holm; bootstrap CIs (H3, H4)", C_MOD)
    box(ax, 0.52, 0.17, 0.46, 0.13, "Module 7. Robustness (Notebook 07)",
        "\nwalk-forward folds (2021, 2022, 2023);\nsix ablations incl. weighted loss;\n"
        "case study of 2024 flood-risk events; Aviles check", C_MOD)
    arrow(ax, 0.42, 0.335, 0.25, 0.302)
    arrow(ax, 0.58, 0.335, 0.75, 0.302)

    # module 8 + outputs
    box(ax, 0.17, 0.065, 0.66, 0.075, "Module 8. Report assembler (make report)",
        "every Chapter IV table and figure, verdicts, measured run time", C_MOD)
    arrow(ax, 0.25, 0.17, 0.35, 0.142)
    arrow(ax, 0.75, 0.17, 0.65, 0.142)
    ax.text(0.5, 0.03, "Outputs: 1–6 h forecasts of the Pandacan level · high-water and flood-risk alerts · "
            "model comparison · river–drainage evidence", ha="center", va="center", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.4", fc=C_OUT, ec=C_EDGE, lw=1))
    arrow(ax, 0.5, 0.065, 0.5, 0.045)

    # cross-cutting control
    ax.text(0.5, 0.0, "Gates G0–G20, automated tests and the transparency log check every module",
            ha="center", va="center", fontsize=7.5, style="italic", color="#555555")
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(OUT)


if __name__ == "__main__":
    main()
