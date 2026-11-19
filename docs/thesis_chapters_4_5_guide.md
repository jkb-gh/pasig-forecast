# Chapters IV and V — writing guide with paste-ready text

For: the three proponents, writing Chapters IV and V of the thesis.
Follows the CICS *Thesis Template.pdf* (Chapter IV sections A–E, Chapter V sections A–C) and stays consistent with
Chapters I–III of *Revised_Copy_of_Thesis.pdf*, including the Chapter III revisions agreed on 14 Nov 2026.
Every number below comes from the committed results of the laptop run (`reports/chapter4/chapter4.md` and the
CSV files beside it, `gates/*.json`, `reports/tables/*`). All citations are already in your References list, so
no new reference entries are needed.

---

## 0. Before you paste

**Formatting (template rules).**
- Body: Times New Roman 12 pt.
- Paragraphs: first line indented 0.5 in, ragged right, two spaces between sentences. The text below uses one
  space; after pasting, run a find-and-replace from ". " to ".  " and check it.
- Table and figure labels: Arial 10 pt bold. Table captions go **above** the table, as in your Table III.1.
  Figure captions go **below** the figure, as in your Figure III.1.
- Numbering: keep your Chapter III style, "Table IV.1" and "Figure IV.1".
- Tense: past tense, as in Chapters I–III.

**Where the files are** (in the repository):

| Item | File |
|---|---|
| Figure IV.1 System architecture | `reports/figures/fig_IV-1_system_architecture.png` (made by `scripts/make_fig_iv1.py`) |
| Figure IV.2 Test RMSE by lead | `reports/figures/test_rmse_by_lead.png` |
| Figure IV.3 2024 season, 3-hour forecasts | `reports/figures/test_series_lead3.png` |
| Figure IV.4 Carina event | `reports/figures/case_event_02.png` |
| Figure IV.5 Walk-forward RMSE | `reports/chapter4/fig_walkforward_rmse.png` |
| Figure IV.6 Ablations | `reports/chapter4/fig_ablation_rmse_diff.png` |
| Full-precision numbers for every table | `reports/chapter4/table_IV-NN_*.csv` |

**Tables.** They are written as Markdown tables. The easiest way to get real tables into Word or Google Docs is
to open the HTML version of this guide (`docs/thesis_chapters_4_5_guide.html`) in a browser and copy from there.

**Add to the List of Figures and List of Tables:** Figures IV.1–IV.6 and Tables IV.1–IV.18, with the captions
given below.

---

# CHAPTER IV — Presentation and Analysis of Data

## A. System Architecture

**What this part does.** The template asks for a diagram of the system's modules and how data flows between
them, with the external entities that supply the inputs and receive the outputs, plus a short high-level
narrative. Section B then describes each module in detail.

**Paste this:**

> **Chapter IV Presentation and Analysis of Data**
>
> **A. System Architecture**
>
> The researchers implemented the study as a forecasting pipeline of eight modules, shown in Figure IV.1. The pipeline received its inputs from two external entities: the Metropolitan Manila Development Authority (MMDA), which supplied the EFCOS hourly water levels and the Aviles and Quiapo pumping-station logs, and PAGASA, which supplied the Science Garden 6-hourly and daily weather records. Its outputs were the 1- to 6-hour forecasts of the Pandacan level, the high-water and flood-risk alerts derived from them, the comparison of the proposed model with the baselines, and the evidence on how the river level relates to drainage stress in Sampaloc. These outputs were consumed by the researchers and reported in this chapter; no live warning service was built.
>
> Data flowed in one direction. Module 1 turned the raw files into one checked hourly table. Modules 2, 3 and 4 used only the training and validation seasons to set the alert levels, build the model inputs and select the weather predictors. Module 5 trained and tuned every model. After Module 5, every setting and trained model was frozen and recorded with a checksum, and only then did Module 6 open the 2024 test season, once, to evaluate all models. Module 7 checked the robustness of the results, and Module 8 assembled the tables and figures of this chapter. Each module ended with automated checks (gates and tests) that had to pass before the next module could start, so that no later module could run on missing or faulty inputs.
>
> *(Insert Figure IV.1 here.)*
>
> **Figure IV.1: System Architecture of the Forecasting Pipeline**

**Possible panel questions**
- *"Is this a system or just an experiment? Where is the user?"* — It is an offline research pipeline, as Scope
  and Limitations states. The external entities are the data providers (MMDA, PAGASA) and the consumers of the
  outputs (the researchers and, potentially, MMDA or the Manila DRRMO). No live service was in scope.
- *"How do you know the test season was not used during development?"* — The settings were frozen with SHA-256
  checksums and a git tag before Module 6 ran. Module 6 refuses to open 2024 unless every checksum matches, and
  it records each opening. 2024 was opened once, on 11 November 2026. A test also shows that adding 5 m to every
  2024 value leaves every fitted setting unchanged.
- *"Why eight modules but five phases in Chapter III?"* — Phase 3 of Chapter III spans Modules 3 and 4 (features,
  then Granger selection), and Phase 5 spans Modules 6–8 (test evaluation, robustness, reporting).

**Learn this**
- The map from Chapter III phases to modules: Phase 1 → M1; Phase 2 → M2; Phase 3 → M3 + M4; Phase 4 → M5;
  Phase 5 → M6 + M7 + M8.
- What a gate is (a recorded pass/fail check with its rule and evidence), and why freezing settings before the
  test prevents leakage (Chapter I definition of *Data Leakage*).

**Watch out**
- The figure says "Notebook 01 … 07". If the panel asks to see them, they are in the repository's `notebooks/`
  folder.
- Keep "eight modules" consistent with Section B.

---

## B. Description of the Modules and Interfaces

**What this part does.** The template asks you to describe each module in processing order: what it receives and
from whom, what it does, and what it outputs and to whom.

**Paste this:**

> **B. Description of the Modules and Interfaces**
>
> **Module 1: Data ingestion and quality control.** *Input:* the 465 raw MMDA and PAGASA files, received from the two agencies. *Process:* each file was checked against a manifest of SHA-256 checksums and read by a parser written for its layout. Readings were converted to Philippine Standard Time; each PAGASA 6-hour rainfall total was made available one hour after its period ended, and each daily value from 09:00 PHT on the day after its label. Implausible readings were flagged by range, spike and stuck-sensor rules; gaps of three hours or less were filled and flagged; and the 80% coverage rule was applied to the candidate stations. The module then built one hourly table, split it into training (2018–2022), validation (2023) and test (2024) seasons, and fixed the hours on which every model would be scored. *Output:* the hourly master table, the evaluation hours and Table III.6, used by Modules 2 to 7.
>
> **Module 2: Link analysis and alert levels.** *Input:* the hourly table and the Aviles and Quiapo pumping-station logs for the training seasons. *Process:* the status codes were checked against the water levels; the Pandacan level was compared with the river-side level at Aviles; and logistic regression estimated how the odds of drainage stress (two or more Aviles pumps running) changed with the Pandacan level, with and without Science Garden rainfall (H1). The two alert levels were derived by the rules in Chapter III, with a sensitivity analysis. *Output:* the high-water level of 11.69 m and the flood-risk level of 12.00 m, used by Modules 5 to 7 to define alerts.
>
> **Module 3: Tide and feature builder.** *Input:* the hourly table for the training and validation seasons. *Process:* a harmonic tide model was fitted to each water-level series on the training years. For every forecast hour t, the module built a 24-hour sequence (the Pandacan level, its hourly change and the latest Science Garden 6-hour rainfall) and a tabular vector (calendar terms at t and t+1 to t+6, the predicted tide at t+1 to t+6 and its change, rainfall totals, hours since the last rainfall report, and the previous day's weather). Min-max scalers were fitted on the training seasons. *Output:* the training and validation windows, the scalers and the tide coefficients, used by Modules 4 and 5. The 2024 windows were built later by the same frozen code in Module 6.
>
> **Module 4: Granger input selection.** *Input:* the de-tided Pandacan level and the four Science Garden candidates for the training seasons. *Process:* the module checked stationarity with the Augmented Dickey-Fuller test, chose the lag order with the Bayesian Information Criterion, and ran one pooled F-test per candidate against the Bonferroni-corrected level (H2). *Output:* the list of selected weather inputs (rainfall and pressure), used by Module 5 to decide which features enter the model.
>
> **Module 5: Model training and tuning.** *Input:* the windows, scalers and selected inputs. *Process:* the module benchmarked the laptop and chose the training device and number of seeds; compared the tide and output alternatives (G11, G12); ran the two-stage grid search for the proposed model and the grid for the standalone LSTM; trained the final configurations with five seeds; fitted the baselines and classifiers; tuned the trigger offsets and decision thresholds on 2023; and checked that every model beat persistence (G16). *Output:* the trained models, the offsets and thresholds, and the validation results. All of these were frozen and recorded with checksums before Module 6.
>
> **Module 6: Test evaluation.** *Input:* the frozen settings and models, and the 2024 test season, opened once after the checksums were verified. *Process:* the module built the 2024 windows, predicted the level with every model and seed, issued alerts with the frozen offsets and thresholds, and computed the error measures, alert measures, equal-recall comparison, event detection, Diebold–Mariano tests with Holm adjustment and bootstrap confidence intervals, and the H3 and H4 verdicts. *Output:* the test results in Section D, used by Modules 7 and 8.
>
> **Module 7: Robustness.** *Input:* the hourly table (2018–2023 for the walk-forward), the frozen settings and the 2024 test hours. *Process:* walk-forward validation in three folds, six ablation variants, a case study of every 2024 flood-risk event, and the descriptive comparison of the alert levels with the Aviles records from June to mid-July 2024. *Output:* the robustness results in Section D.
>
> **Module 8: Report assembler.** *Input:* the result files of Modules 2 to 7. *Process:* it read the finished results, without retraining or re-scoring anything, and formatted every table and figure. *Output:* the tables and figures of this chapter and the measured run time reported in Chapter III.

**Possible panel questions**
- *"Did the classifiers get the same information as your model?"* — Yes. Each classifier was trained twice: on
  current-hour inputs (the snapshot use) and on the same 24-hour window plus tabular features. H4 used the input
  set with the higher 2023 F1, which was the 24-hour window for both Logistic Regression and KNN.
- *"Why are the pumping logs not model inputs?"* — They end in mid-July 2024 and reflect operator decisions.
  They served only as Sampaloc-side evidence for H1 and the flood-risk level (Chapter I, Figure I.2).
- *"Where is the predicted tide at t+h coming from — isn't that the future?"* — It is computed from the date and
  time alone, like a tide table, so it is known in advance (Table III.2).

**Learn this**
- The input lists in Table III.2, and why calendar and tide terms at t+h are allowed while measured inputs stop
  at t.
- Min-max scaling, and why the scalers are fitted on training data only.
- The idea of "add-back": the network predicts the change in level, and the current level is added back.

**Watch out**
- "465 raw files" is the full manifest (458 used, 7 excluded). If asked: the 7 excluded are the Taguig files
  and the duplicate Quiapo copy.
- The previous day's weather in the final model is **pressure only** (rainfall enters through the rainfall
  features). Don't write "humidity and temperature" as inputs.

---

## C. Sample System Simulation of Test Data

**What this part does.** The template asks you to take one small, representative test input and show how it
flows through the modules to the output. We use one real forecast hour from the 2024 test season: **05:00 PHT on
24 July 2024**, during the Carina event. It shows every module's role, and it is the hour of the proposed model's
earliest 3-hour flood-risk alert for that event.

**Paste this:**

> **C. Sample System Simulation of Test Data**
>
> To show how one forecast moves through the system, this section follows a single test case: the forecast issued at 05:00 PHT on 24 July 2024, the morning the southwest monsoon enhanced by Typhoon Carina flooded Metro Manila.
>
> **Module 1** supplied the last 24 hours of the Pandacan level (06:00 PHT on 23 July to 05:00 PHT on 24 July): 23 observed hours and one short gap (15:00 on 23 July) filled with the previous reading. The level had fallen to about 11.0 m overnight and was rising fast: 11.20 m at 03:00, 11.49 m at 04:00 and 11.97 m at 05:00. The latest Science Garden 6-hour total that had been available for at least one hour was 3.4 mm, the 24-hour total was 75.7 mm and the 72-hour total was 150.4 mm, so the hour counted as a rainy hour. The latest usable daily pressure was 1001.5 hPa.
>
> **Module 3** turned these values into the model inputs. It added the calendar terms and the predicted astronomical tide for 06:00 to 11:00: 11.07, 11.19, 11.32, 11.44, 11.55 and 11.62 m. The tide was therefore rising throughout the six hours ahead, and the observed level already stood about 1 m above it. All inputs were scaled with the training-season scalers.
>
> **Module 5** supplied the frozen proposed model, and **Module 6** produced its forecasts (Table IV.1). For the seed with the median validation RMSE, the forecast level rose from 11.92 m at 06:00 to 12.30 m at 11:00. Across the five seeds, the 3-hour forecast ranged from 11.96 to 12.10 m. With the frozen trigger offset of 0.02 m, a high-water alert was issued when the forecast reached 11.67 m and a flood-risk alert when it reached 11.98 m. The forecast therefore issued high-water alerts for all six hours ahead and flood-risk alerts for 08:00 to 11:00 (lead times 3 to 6 hours).
>
> **Table IV.1: Forecasts Issued at 05:00 PHT on 24 July 2024 (Pandacan Level, m)**
>
> *(Table IV.1 — see the table below this block.)*
>
> The observed level first reached the flood-risk level at 07:00 (12.11 m). The 3-hour alert issued at 05:00 targeted 08:00, within two hours of that first exceedance, so Module 6 counted the event as detected at the 3-hour lead time with 2 hours of warning. The flood-risk alerts were correct for every scored hour (08:00, 09:00 and 11:00). The readings at 06:00 and 10:00 were gap-filled and therefore not scored. In this case the tide plus persisted residual forecast came closer to the rising level than the proposed model did, and persistence, which repeats 11.97 m, stayed just below the 11.98 m trigger and issued no flood-risk alert. The level peaked at 12.98 m at 15:00. The proposed model's 1-hour forecast for that hour was 12.74 m, 0.24 m too low: an example of the under-forecasting of peaks discussed in Section E.

Insert as Table IV.1 (lead = hours after 05:00):

| Lead (target hour) | Observed | Proposed model (median seed) | Standalone LSTM | Ridge | Tide + persisted residual | Persistence | Flood-risk alert by proposed model |
|---|---|---|---|---|---|---|---|
| 1 h (06:00) | gap-filled, not scored | 11.92 | 11.93 | 11.91 | 12.06 | 11.97 | no |
| 2 h (07:00) | 12.11 | 11.95 | 11.95 | 11.95 | 12.18 | 11.97 | no |
| 3 h (08:00) | 12.25 | 12.03 | 12.00 | 12.00 | 12.31 | 11.97 | yes |
| 4 h (09:00) | 12.38 | 12.17 | 12.09 | 12.08 | 12.43 | 11.97 | yes |
| 5 h (10:00) | gap-filled, not scored | 12.24 | 12.18 | 12.16 | 12.54 | 11.97 | yes |
| 6 h (11:00) | 12.59 | 12.30 | 12.24 | 12.20 | 12.62 | 11.97 | yes |

**Possible panel questions**
- *"Why show an hour where a baseline did better?"* — Chapter III promised to report results whichever way they
  fell. Over the whole season the proposed model had a lower RMSE than tide plus persisted residual at every
  lead (Table IV.6). A single hour is an illustration, not evidence.
- *"What does 'median seed' mean?"* — Of the five training seeds, the one whose 2023 validation RMSE was the
  median. It is used wherever a single model is needed (DM test, H4, case study), so that one ordinary run
  represents the model (Chapter III F.8).
- *"Why is the alert at 11.98 m and not 12.00 m?"* — The trigger offset of 0.02 m was tuned on 2023 to maximise
  F1 (Chapter III, Phase 4). An alert is issued when the forecast reaches the level minus the offset.

**Learn this**
- How the ±2 h event-detection window and the warning time are computed (Chapter III, Phase 5).
- Why gap-filled hours are never scored (Chapter III, Phase 1).

**Watch out**
- All numbers in Table IV.1 come from `reports/tables/preds_test.parquet` (hybrid seed 1 = median seed;
  LSTM seed 0).
- "Observed level first reached 12.00 m at 07:00": the case-study table lists this event as starting at 07:00.
- Don't call 06:00 "missing"; it was a **filled** hour (the 05:00 value repeated), so it is excluded from scoring.

---

## D. Test Results

**What this part does.** The template asks you to group the test data by the categories from Chapter III,
measure the results per category and overall with the Chapter III statistics, and show tables and graphs. Our
categories are: hypothesis (H1–H4); lead time (1–6 h); alert level (high water, flood risk); and hour type (all,
rainy, dry). The verdicts are given here; the interpretation is in Section E.

### D.1 River level and drainage stress (H1) and the alert levels

**Paste this:**

> **D. Test Results**
>
> **1. River level and drainage stress (H1) and the alert levels**
>
> The Pandacan level and the river-side level recorded at the Aviles pumping station moved together. Over 17,588 training hours their correlation was 0.934, and the correlation of their hourly changes was 0.706. The Aviles reading was on average 0.22 m higher, consistent with the two gauges using different reference levels. Over the 954 hours at or above 11.69 m, the correlation was lower (0.598). This supported the first assumption of the study: the Pandacan gauge reflected the outlet condition of the Aviles–Sampaloc drainage area.
>
> Table IV.2 shows the logistic regression of drainage stress on the training seasons (17,132 hours on 840 days, 448 of them hours of drainage stress). With rainfall in the model, each 0.1-m rise in the Pandacan level multiplied the odds of drainage stress by 1.207 (95% CI 1.143 to 1.275), and adding the level to the rainfall-only model improved the fit (likelihood-ratio χ² = 162.6, p < 0.001). The interaction between level and rainfall was also significant: a high river mattered more when it rained. On the 2023 validation season, however, adding the river level raised the area under the ROC curve only from 0.824 to 0.829, a gain of 0.004 whose 95% confidence interval (−0.022 to 0.027) included zero. The Quiapo station gave the same direction with a weaker effect (odds ratio 1.067 per 0.1 m). By the rule set in Chapter III, H1 was **partly supported**.
>
> **Table IV.2: Association between the Pandacan Level and Drainage Stress (Training Seasons 2018–2022)**

| Measure | Result |
|---|---|
| Training hours / days / drainage-stress hours | 17,132 / 840 / 448 |
| Odds ratio per 0.1 m of Pandacan level, with rainfall in the model | 1.207 (95% CI 1.143–1.275), p < 0.001 |
| Odds ratio per unit of ln(1 + 24-h rainfall), with level in the model | 2.155 (95% CI 1.842–2.521) |
| Likelihood-ratio test, rainfall only vs rainfall + level | χ² = 162.6, df = 1, p < 0.001 |
| Interaction model: odds ratio per 0.1 m at mean rainfall; interaction odds ratio | 1.117 (1.031–1.210); 1.534 (1.066–2.206) |
| 2023 ROC-AUC, rainfall only → rainfall + level (gain, 95% CI by resampling days) | 0.824 → 0.829 (0.004, −0.022 to 0.027) |
| Quiapo check, odds ratio per 0.1 m (≥ 2 Quiapo pumps), without / with 2021 | 1.067 (1.046–1.088) / 1.066 (1.046–1.086) |
| Pandacan vs Aviles river-side level: correlation (all training hours / hours ≥ 11.69 m) | 0.934 / 0.598 |
| H1 verdict | Partly supported (odds ratio CI excludes 1; AUC gain CI includes 0) |

> The high-water level, the 95th percentile of training-season levels, was 11.69 m. The share of training hours under drainage stress rose with the level: 34.9% of the 172 hours at or above 11.90 m, 42.3% of the 123 hours at or above 11.95 m, and 55.0% of the 80 hours at or above 12.00 m. The flood-risk level was therefore 12.00 m, the lowest level at which at least half of the hours were hours of stress. Table IV.3 shows how this level would change under other definitions. On the 2023 season, which did not affect the levels, 4.2% of hours were at or above 11.69 m and 0.3% (13 hours) at or above 12.00 m.
>
> **Table IV.3: Flood-Risk Level under Other Definitions of Drainage Stress (Training Seasons)**

| Stress definition | Cut-off 40% | Cut-off 50% | Cut-off 60% |
|---|---|---|---|
| ≥ 1 Aviles pump running | 11.70 m | 11.85 m | 11.90 m |
| ≥ 2 Aviles pumps running (chosen) | 11.95 m | **12.00 m** | 12.05 m |
| ≥ 3 Aviles pumps running | 12.10 m | 12.20 m | 12.25 m |

### D.2 Granger-causal predictors (H2)

> **2. Granger-causal predictors (H2)**
>
> Table IV.4 shows the Granger tests on the de-tided Pandacan level for the training seasons. Rainfall and pressure passed the Bonferroni-corrected level of 0.0125; relative humidity and mean temperature did not. H2 was therefore **supported**, and rainfall and pressure entered the model. Their contribution to forecast skill was small: each improved the 2023 validation RMSE of a ridge model by less than 0.3 mm. The two upstream stations, tested only descriptively because they failed the coverage rule, also showed Granger-causal precedence at a 23-hour lag, but adding them made the ridge validation RMSE worse (by 0.27 mm for Sto. Niño and 2.0 mm for Fort Santiago).
>
> **Table IV.4: Granger Causality Tests on the De-tided Pandacan Level (Training Seasons)**

| Candidate | Time step | Lags (BIC) | F | p-value | Selected (α′ = 0.0125) | Ridge validation RMSE gain (mm) |
|---|---|---|---|---|---|---|
| Rainfall | 6-hourly | 4 | 58.96 | 6.1 × 10⁻⁴⁸ | Yes | +0.22 |
| Pressure | daily | 3 | 9.88 | 2.2 × 10⁻⁶ | Yes | +0.26 |
| Relative humidity | daily | 3 | 0.42 | 0.74 | No | −0.01 |
| Mean temperature | daily | 3 | 1.25 | 0.29 | No | +0.004 |

### D.3 Model design and settings chosen on the validation season

> **3. Model design and settings chosen on the 2023 season**
>
> Table IV.5 lists the settings fixed on the 2023 validation season before the test season was opened. The tide alternative and the direct-level alternative were both rejected: the constituent-pair version had a slightly lower mean validation RMSE (0.0664 m against 0.0688 m) but not by more than one standard deviation of the default's seeds (0.0031 m), and the direct-level version was worse (0.0732 m). Training ran on the laptop's GPU with deterministic operations, which gave identical results on repeated runs. Because the projected run time with five seeds (11.11 hours) exceeded the 10-hour limit, the walk-forward folds and ablation variants used three seeds. Every model beat persistence on the validation season at lead times of 2 hours or more, and the automated error checklist found no fault. The best grid setting lay at the edge of its range for seven of the eight searched settings; the ranges were not widened.
>
> On the validation season, the proposed model averaged an RMSE of 0.0678 ± 0.0013 m over the six lead times and five seeds, the standalone LSTM 0.0681 ± 0.0017 m, ridge regression 0.0711 m, and the tide plus persisted residual model 0.0956 m, which made the latter the strongest simple baseline for the skill scores.
>
> **Table IV.5: Settings Chosen on the 2023 Validation Season**

| Setting | Result |
|---|---|
| Tide input (G11) | Predicted tide kept (constituent pairs 0.0664 m vs 0.0688 ± 0.0031 m; not better by > 1 SD) |
| Output form (G12) | Change in level with add-back kept (direct level 0.0732 m) |
| Device and determinism (G13, G14) | GPU; repeated runs identical (projected 11.11 h vs 17.54 h on CPU) |
| Seeds (G15) | 5 for final models; 3 for walk-forward and ablations |
| Proposed model | 2 LSTM layers × 64 units; GRU 64 units; tabular path 1 layer × 16 units; head 32 units; dropout 0.2; learning rate 0.001; batch 64 |
| Standalone LSTM | 1 layer × 128 units; dropout 0.2; learning rate 0.0001; batch 64 |
| Trigger offsets, proposed model | +0.02 m at both levels (alerts at 11.67 m and 11.98 m) |
| Persistence check (G16) | Every model beat persistence at leads ≥ 2 h; checklist passed |
| Strongest simple baseline | Tide plus persisted residual (2023 RMSE 0.0956 m) |

### D.4 Forecast error on the 2024 test season (H3)

> **4. Forecast error on the 2024 test season (H3)**
>
> Table IV.6 and Figure IV.2 show the RMSE of every model on the 3,729 to 3,692 test cases per lead time. The proposed model had the lowest RMSE at every lead time, from 0.052 m at 1 hour to 0.095 m at 6 hours, with a seed-to-seed standard deviation of 0.001 to 0.002 m. The standalone LSTM was within 0.003 m of it at every lead time. Ridge regression followed at 0.057 to 0.110 m and tide plus persisted residual at 0.062 to 0.144 m. Persistence was competitive only at 1 hour (0.102 m) and degraded to 0.401 m at 6 hours as the tide moved on. Tide-only stayed near 0.19 m at every lead, and the K-Nearest Neighbors regressor near 0.13 m.
>
> **Table IV.6: Test RMSE (m) by Lead Time, All Hours, 2024 (Neural Models: Mean ± SD over Five Seeds)**

| Model | 1 h | 2 h | 3 h | 4 h | 5 h | 6 h |
|---|---|---|---|---|---|---|
| Proposed model | 0.0516 ± 0.0011 | 0.0646 ± 0.0008 | 0.0727 ± 0.0014 | 0.0800 ± 0.0013 | 0.0869 ± 0.0017 | 0.0949 ± 0.0022 |
| Standalone LSTM | 0.0529 ± 0.0011 | 0.0662 ± 0.0023 | 0.0748 ± 0.0031 | 0.0828 ± 0.0035 | 0.0895 ± 0.0032 | 0.0957 ± 0.0032 |
| Ridge regression | 0.0572 | 0.0754 | 0.0879 | 0.0975 | 0.1046 | 0.1103 |
| KNN regressor | 0.1242 | 0.1266 | 0.1292 | 0.1308 | 0.1327 | 0.1348 |
| Tide + persisted residual | 0.0615 | 0.0842 | 0.1025 | 0.1187 | 0.1315 | 0.1436 |
| Tide only | 0.1896 | 0.1893 | 0.1891 | 0.1889 | 0.1888 | 0.1887 |
| Persistence | 0.1015 | 0.1744 | 0.2428 | 0.3042 | 0.3566 | 0.4006 |

> *(Insert Figure IV.2 here.)*
>
> **Figure IV.2: Test RMSE by Lead Time, 2024**

> Errors were larger in rainy hours (Table IV.7). The proposed model's RMSE in the 1,328 rainy hours rose from 0.056 m at 1 hour to 0.123 m at 6 hours, against 0.049 to 0.075 m in the 2,401 dry hours. Its advantage over ridge regression and the tide-based models was larger in rainy hours, while in dry hours at 5 and 6 hours the standalone LSTM was slightly better.
>
> **Table IV.7: Test RMSE (m) in Rainy and Dry Hours at 1, 3 and 6 Hours, 2024**

| Model | Rainy 1 h | Rainy 3 h | Rainy 6 h | Dry 1 h | Dry 3 h | Dry 6 h |
|---|---|---|---|---|---|---|
| Proposed model | 0.0562 | 0.0884 | 0.1233 | 0.0489 | 0.0623 | 0.0747 |
| Standalone LSTM | 0.0573 | 0.0924 | 0.1283 | 0.0503 | 0.0630 | 0.0717 |
| Ridge regression | 0.0665 | 0.1145 | 0.1526 | 0.0514 | 0.0691 | 0.0778 |
| Tide + persisted residual | 0.0655 | 0.1169 | 0.1701 | 0.0592 | 0.0936 | 0.1267 |
| Persistence | 0.1054 | 0.2486 | 0.4090 | 0.0993 | 0.2395 | 0.3960 |
| KNN regressor | 0.1646 | 0.1752 | 0.1878 | 0.0947 | 0.0947 | 0.0937 |
| Tide only | 0.2505 | 0.2502 | 0.2489 | 0.1453 | 0.1447 | 0.1452 |

> Table IV.8 gives the MAE, R² and skill. The proposed model explained 97.5% of the variance of the level at 1 hour and 91.5% at 6 hours. Its skill against persistence rose from 0.49 at 1 hour to 0.76 at 6 hours, and its skill against the strongest simple baseline from 0.16 to 0.34. The bootstrap confidence intervals for the RMSE difference against tide plus persisted residual excluded zero at every lead time, from −0.010 m (95% CI −0.012 to −0.007) at 1 hour to −0.049 m (−0.057 to −0.042) at 6 hours.
>
> **Table IV.8: Test MAE (m), R² and Skill at 1, 3 and 6 Hours, All Hours, 2024**

| Model | MAE 1 h | MAE 3 h | MAE 6 h | R² 1 h | R² 3 h | R² 6 h | Skill vs persistence 1 / 3 / 6 h | Skill vs tide + residual 1 / 3 / 6 h |
|---|---|---|---|---|---|---|---|---|
| Proposed model | 0.0281 | 0.0444 | 0.0606 | 0.975 | 0.950 | 0.915 | 0.49 / 0.70 / 0.76 | 0.16 / 0.29 / 0.34 |
| Standalone LSTM | 0.0285 | 0.0450 | 0.0577 | 0.974 | 0.947 | 0.914 | 0.48 / 0.69 / 0.76 | 0.14 / 0.27 / 0.33 |
| Ridge regression | 0.0317 | 0.0540 | 0.0658 | 0.969 | 0.927 | 0.885 | 0.44 / 0.64 / 0.73 | 0.07 / 0.14 / 0.23 |
| Tide + persisted residual | 0.0342 | 0.0700 | 0.1025 | 0.964 | 0.901 | 0.806 | 0.39 / 0.58 / 0.64 | 0 / 0 / 0 |
| KNN regressor | 0.0817 | 0.0824 | 0.0815 | 0.855 | 0.843 | 0.829 | −0.22 / 0.47 / 0.66 | −1.02 / −0.26 / 0.06 |
| Tide only | 0.1281 | 0.1278 | 0.1274 | 0.662 | 0.664 | 0.665 | — | — |
| Persistence | 0.0744 | 0.1952 | 0.3295 | 0.903 | 0.446 | −0.511 | 0 / 0 / 0 | — |

> Table IV.9 shows the Diebold–Mariano tests after Holm adjustment over all 72 tests. Over all hours, the proposed model was significantly more accurate than persistence, tide-only and tide plus persisted residual at all six lead times, and than the K-Nearest Neighbors regressor at 1 and 2 hours: 20 of the 36 baseline–lead pairs. It was not significantly different from ridge regression (adjusted p from 0.13 to 1.00) or from the standalone LSTM (adjusted p = 1.00) at any lead time, and no baseline was significantly more accurate than the proposed model anywhere. Over rainy hours, it remained significantly more accurate than persistence and tide plus persisted residual at every lead time (12 pairs). By the rule set in Chapter III, H3 was **partly supported**.
>
> **Table IV.9: Diebold–Mariano Tests, Proposed Model vs Each Baseline (Holm-Adjusted p-Values; All Hours / Rainy Hours)**

| Baseline | 1 h | 2 h | 3 h | 4 h | 5 h | 6 h |
|---|---|---|---|---|---|---|
| Standalone LSTM | 1.000 / 1.000 | 1.000 / 1.000 | 1.000 / 1.000 | 1.000 / 1.000 | 1.000 / 1.000 | 1.000 / 1.000 |
| Ridge regression | 0.145 / 0.423 | 0.145 / 0.563 | 0.131 / 0.563 | 0.248 / 0.714 | 0.623 / 1.000 | 1.000 / 1.000 |
| KNN regressor | **0.003** / 0.161 | **0.021** / 0.304 | 0.058 / 0.452 | 0.145 / 0.621 | 0.304 / 0.833 | 0.471 / 1.000 |
| Tide + persisted residual | **<0.001** / **0.009** | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **0.003** |
| Tide only | **<0.001** / 0.116 | **<0.001** / 0.137 | **0.001** / 0.145 | **0.001** / 0.149 | **0.001** / 0.176 | **0.002** / 0.202 |
| Persistence | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **<0.001** | **<0.001** / **<0.001** |

*Note under Table IV.9:* Bold = proposed model significantly more accurate (adjusted p < 0.05). No baseline was significantly more accurate than the proposed model. Neural models are represented by their median-validation seed.

> *(Insert Figure IV.3 here.)*
>
> **Figure IV.3: Observed Pandacan Level and 3-Hour Forecasts of the Proposed Model and the Tide Plus Persisted Residual Model, 2024 Wet Season**

### D.5 High-water and flood-risk alerts (H4)

> **5. Alerts at the high-water and flood-risk levels (H4)**
>
> Table IV.10 shows the hourly alerts at the high-water level with the frozen offsets and thresholds (392 alert hours at 1 hour). The proposed model's F1-Score fell from 0.92 at 1 hour to 0.86 at 6 hours, with Recall from 0.95 to 0.85. The standalone LSTM, ridge regression and Logistic Regression on the 24-hour window performed almost the same. The K-Nearest Neighbors classifiers missed many more alert hours, and persistence lost almost all skill beyond 2 hours.
>
> **Table IV.10: Hourly High-Water Alerts, All Hours, 2024: F1-Score (Precision, Recall; False Alarms, Missed Alerts)**

| Model | 1 h | 3 h | 6 h |
|---|---|---|---|
| Proposed model | 0.92 (0.90, 0.95; 40, 21) | 0.88 (0.89, 0.87; 41, 50) | 0.86 (0.87, 0.85; 48, 58) |
| Standalone LSTM | 0.93 (0.90, 0.95; 40, 19) | 0.89 (0.91, 0.87; 32, 50) | 0.86 (0.90, 0.82; 35, 72) |
| Ridge regression | 0.92 (0.89, 0.96; 46, 17) | 0.87 (0.87, 0.87; 51, 51) | 0.84 (0.84, 0.83; 61, 67) |
| Tide + persisted residual | 0.92 (0.93, 0.92; 28, 31) | 0.85 (0.86, 0.85; 55, 58) | 0.80 (0.85, 0.75; 52, 98) |
| KNN regressor | 0.84 (0.92, 0.77; 27, 91) | 0.81 (0.88, 0.75; 38, 99) | 0.82 (0.86, 0.78; 49, 85) |
| Tide only | 0.56 (0.95, 0.39; 8, 238) | 0.56 (0.95, 0.39; 8, 237) | 0.56 (0.95, 0.39; 8, 237) |
| Persistence | 0.76 (0.74, 0.78; 105, 86) | 0.40 (0.39, 0.40; 250, 233) | 0.11 (0.11, 0.12; 358, 346) |
| Logistic Regression, 24-h window | 0.93 (0.91, 0.95; 36, 19) | 0.88 (0.90, 0.86; 36, 56) | 0.84 (0.87, 0.81; 48, 73) |
| Logistic Regression, current hour | 0.91 (0.93, 0.90; 25, 41) | 0.84 (0.95, 0.76; 17, 93) | 0.83 (0.87, 0.80; 46, 80) |
| KNN classifier, 24-h window | 0.78 (0.89, 0.69; 35, 120) | 0.78 (0.83, 0.74; 61, 102) | 0.76 (0.85, 0.69; 49, 123) |
| KNN classifier, current hour | 0.64 (0.89, 0.50; 25, 196) | 0.66 (0.88, 0.53; 28, 183) | 0.57 (0.86, 0.42; 27, 226) |

*Note:* Neural models are the mean over five seeds (counts are seed means, rounded).

> Table IV.11 shows the H4 comparison at equal Recall. Against the K-Nearest Neighbors classifier, the proposed model raised far fewer false alarms at Recall 0.90 (for example 18 against 200 at 1 hour) and reached a higher PR-AUC, with both confidence intervals on the winning side at 1 to 5 hours; at 6 hours the PR-AUC interval included zero. Against Logistic Regression, the two were statistically indistinguishable at every lead time: the PR-AUC values were nearly equal (0.971 against 0.972 at 1 hour) and every false-alarm interval included zero, although the proposed model raised fewer false alarms at longer lead times (79 against 107 at 6 hours). The proposed model won 5 of the 12 family–lead pairs, so H4 was **partly supported**. At Recall 0.80 and 0.95, which did not affect the verdict, the pattern was similar, except that at Recall 0.95 Logistic Regression raised fewer false alarms than the proposed model at 1 and 2 hours (36 against 66 and 74 against 80).
>
> **Table IV.11: High-Water Alerts at Equal Recall (H4), 2024**

| Classifier | Lead | False alarms at Recall ≥ 0.90 (proposed / classifier) | 95% CI of difference | PR-AUC (proposed / classifier) | 95% CI of difference | Proposed model wins |
|---|---|---|---|---|---|---|
| Logistic Regression | 1 h | 18 / 18 | −13 to 18 | 0.971 / 0.972 | −0.012 to 0.009 | No |
| Logistic Regression | 2 h | 34 / 35 | −14 to 20 | 0.959 / 0.958 | −0.010 to 0.014 | No |
| Logistic Regression | 3 h | 55 / 61 | −38 to 16 | 0.950 / 0.943 | −0.005 to 0.020 | No |
| Logistic Regression | 4 h | 60 / 71 | −41 to 10 | 0.933 / 0.924 | −0.010 to 0.032 | No |
| Logistic Regression | 5 h | 63 / 84 | −68 to 1 | 0.908 / 0.900 | −0.017 to 0.042 | No |
| Logistic Regression | 6 h | 79 / 107 | −89 to 4 | 0.890 / 0.882 | −0.025 to 0.055 | No |
| KNN classifier | 1 h | 18 / 200 | −280 to −96 | 0.971 / 0.856 | 0.066 to 0.164 | Yes |
| KNN classifier | 2 h | 34 / 225 | −279 to −103 | 0.959 / 0.848 | 0.066 to 0.157 | Yes |
| KNN classifier | 3 h | 55 / 190 | −211 to −82 | 0.950 / 0.869 | 0.050 to 0.113 | Yes |
| KNN classifier | 4 h | 60 / 200 | −292 to −67 | 0.933 / 0.864 | 0.041 to 0.098 | Yes |
| KNN classifier | 5 h | 63 / 213 | −302 to −64 | 0.908 / 0.861 | 0.009 to 0.084 | Yes |
| KNN classifier | 6 h | 79 / 210 | −327 to −64 | 0.890 / 0.855 | −0.007 to 0.079 | No |

*Note:* Both classifiers used the 24-hour window input set, which had the higher 2023 F1-Score. Share of alert hours (the PR-AUC of a random guess): about 0.105.

> Alerts at the flood-risk level, reported descriptively, were weaker. With only 42 alert hours in the scored test cases, the proposed model's hourly F1-Score fell from 0.76 at 1 hour to 0.44 at 6 hours. The corresponding values were 0.80 and 0.46 for tide plus persisted residual, 0.72 and 0.30 for ridge regression, and 0.72 and 0.27 for Logistic Regression on the 24-hour window.

### D.6 Event detection

> **6. Event detection**
>
> Table IV.12 counts the events detected (an alert within two hours of the first exceedance) out of the 95 high-water and 11 flood-risk events that could be scored. The proposed model detected 95% of high-water events at 1 hour and 88% at 6 hours, with a median warning time equal to the lead time. Flood-risk events were harder: the proposed model detected about 8 of 11 at 1 hour, but only about 4 at 3 hours and 3 at 6 hours. Ridge regression and tide plus persisted residual detected 5 of 11 at 6 hours. Persistence detected all 11 at 1 hour, but with a median warning time of 0 hours, because an alert repeated from the current hour only confirms that the level is already high.
>
> **Table IV.12: Events Detected at 1, 3 and 6 Hours, 2024 (Detected / Events; Neural Models: Mean over Seeds)**

| Model | High water 1 h | High water 3 h | High water 6 h | Flood risk 1 h | Flood risk 3 h | Flood risk 6 h |
|---|---|---|---|---|---|---|
| Proposed model | 90.2 / 95 (95%) | 87.6 / 95 (92%) | 83.2 / 95 (88%) | 8.4 / 11 (76%) | 4.2 / 11 (38%) | 2.6 / 11 (24%) |
| Standalone LSTM | 90.0 / 95 (95%) | 86.8 / 95 (91%) | 83.6 / 95 (88%) | 9.0 / 11 (82%) | 4.6 / 11 (42%) | 2.2 / 11 (20%) |
| Ridge regression | 90 / 95 (95%) | 87 / 95 (92%) | 84 / 95 (88%) | 10 / 11 (91%) | 6 / 11 (55%) | 5 / 11 (45%) |
| Tide + persisted residual | 92 / 95 (97%) | 87 / 95 (92%) | 74 / 95 (78%) | 10 / 11 (91%) | 4 / 11 (36%) | 5 / 11 (45%) |
| Persistence | 94 / 95 (99%) | 10 / 95 (11%) | 1 / 95 (1%) | 11 / 11 (100%) | 3 / 11 (27%) | 0 / 11 (0%) |
| Logistic Regression, 24-h window | 91 / 95 (96%) | 85 / 95 (89%) | 81 / 95 (85%) | 7 / 11 (64%) | 7 / 11 (64%) | 1 / 11 (9%) |
| KNN classifier, 24-h window | 71 / 95 (75%) | 75 / 95 (79%) | 72 / 95 (76%) | 5 / 11 (45%) | 5 / 11 (45%) | 4 / 11 (36%) |

### D.7 Walk-forward validation

> **7. Walk-forward validation**
>
> Table IV.13 and Figure IV.5 show the walk-forward results with three seeds per fold. In every fold, the proposed model was significantly more accurate than persistence, tide-only and tide plus persisted residual at all six lead times. Against ridge regression the result changed. In the two independent folds, the proposed model was not significantly more accurate than ridge regression at any lead time. Ridge regression had the lower RMSE at almost every lead time in 2021 and at 5 and 6 hours in 2022, and it was significantly more accurate at one lead time in each fold (1 hour in 2021, 6 hours in 2022). In the 2023 fold, which is not independent because the hyperparameters were chosen on 2023, the proposed model was significantly more accurate than ridge regression at 2, 3 and 5 hours.
>
> **Table IV.13: Walk-Forward RMSE (m) at 1, 3 and 6 Hours (Proposed Model: Mean ± SD over Three Seeds)**

| Fold (evaluated year) | Model | 1 h | 3 h | 6 h | DM vs proposed model (6 leads) |
|---|---|---|---|---|---|
| 2021 | Proposed model | 0.0610 ± 0.0016 | 0.0778 ± 0.0033 | 0.0905 ± 0.0041 | — |
| 2021 | Ridge regression | 0.0586 | 0.0761 | 0.0854 | ridge better at 1 lead |
| 2021 | Tide + persisted residual | 0.0684 | 0.1056 | 0.1375 | proposed better at 6 |
| 2021 | Persistence | 0.1054 | 0.2420 | 0.3931 | proposed better at 6 |
| 2022 | Proposed model | 0.0515 ± 0.0021 | 0.0732 ± 0.0036 | 0.0907 ± 0.0036 | — |
| 2022 | Ridge regression | 0.0544 | 0.0746 | 0.0857 | ridge better at 1 lead |
| 2022 | Tide + persisted residual | 0.0599 | 0.1005 | 0.1357 | proposed better at 6 |
| 2022 | Persistence | 0.1038 | 0.2533 | 0.4157 | proposed better at 6 |
| 2023 (not independent) | Proposed model | 0.0502 ± 0.0014 | 0.0714 ± 0.0027 | 0.0842 ± 0.0038 | — |
| 2023 (not independent) | Ridge regression | 0.0496 | 0.0742 | 0.0845 | proposed better at 3 |
| 2023 (not independent) | Tide + persisted residual | 0.0547 | 0.0938 | 0.1252 | proposed better at 6 |
| 2023 (not independent) | Persistence | 0.0983 | 0.2462 | 0.4083 | proposed better at 6 |

*Note:* Tide-only (RMSE 0.124–0.142 m) is omitted for space; the proposed model was more accurate at every lead time in every fold. DM tests are Holm-adjusted over 72 tests and descriptive.

> *(Insert Figure IV.5 here.)*
>
> **Figure IV.5: Walk-Forward RMSE by Evaluation Year**

### D.8 Ablation study

> **8. Ablation study**
>
> Table IV.14 and Figure IV.6 show how each change to the proposed model altered its 2024 RMSE, with three seeds each. Removing the tabular path was clearly harmful: the RMSE rose by 0.4 cm at 1 hour and 2.1 cm at 6 hours, and the difference was significant at two lead times. Removing the rainfall features, skipping Granger selection, or replacing it with correlation selection changed the RMSE by at most 0.2 cm, mostly within seed-to-seed variation, with no significant difference at any lead time. Replacing the GRU with a second LSTM made the model slightly worse (significant at one lead time), and so did the weighted loss (significant at three lead times).
>
> **Table IV.14: Ablation Results — Change in Test RMSE (m) against the Proposed Model, 2024**

| Variant | 1 h | 2 h | 3 h | 4 h | 5 h | 6 h | Leads significantly worse (DM, Holm) |
|---|---|---|---|---|---|---|---|
| No Granger selection | +0.0001 | +0.0004* | +0.0002 | +0.0005 | +0.0018* | +0.0020* | 0 |
| Correlation selection | −0.0007 | −0.0002 | +0.0009* | +0.0012* | +0.0011 | +0.0004 | 0 |
| No rainfall | −0.0004 | −0.0005* | −0.0001 | +0.0005 | +0.0008 | +0.0010 | 0 |
| No tabular path | +0.0042* | +0.0085* | +0.0136* | +0.0177* | +0.0202* | +0.0214* | 2 |
| GRU replaced by a second LSTM | +0.0022* | +0.0019* | +0.0019* | +0.0015* | +0.0015 | +0.0011 | 1 |
| Weighted loss (w = 2) | +0.0022* | +0.0024* | +0.0021* | +0.0008 | +0.0024* | +0.0026* | 3 |

*Note:* Positive = worse than the proposed model over the same three seeds (proposed model RMSE: 0.0510, 0.0641, 0.0718, 0.0795, 0.0859, 0.0934 m). * = larger than the proposed model's seed standard deviation. No variant was significantly better at any lead time.

> The weighted-loss variant used w = 2, chosen on 2023 (high-water F1-Score 0.795 for w = 2, 0.790 for w = 5, 0.779 for w = 10). Table IV.15 shows that it did not reduce the under-forecasting of peaks: the mean error at the flood-risk peaks stayed within 0.02 m of the proposed model's, the flood-risk Recall rose slightly (for example from 0.36 to 0.40 at 6 hours), and the high-water Recall fell slightly at most lead times.
>
> **Table IV.15: Weighted-Loss Variant vs Proposed Model, 2024 (Same Three Seeds; Proposed → Weighted)**

| Measure | 1 h | 3 h | 6 h |
|---|---|---|---|
| RMSE (m) | 0.051 → 0.053 | 0.072 → 0.074 | 0.093 → 0.096 |
| RMSE at high-water hours (m) | 0.081 → 0.080 | 0.143 → 0.142 | 0.191 → 0.186 |
| Mean error at flood-risk peaks (m) | −0.158 → −0.157 | −0.288 → −0.284 | −0.352 → −0.347 |
| Recall, high water | 0.937 → 0.921 | 0.885 → 0.870 | 0.840 → 0.847 |
| Recall, flood risk | 0.746 → 0.754 | 0.524 → 0.548 | 0.357 → 0.397 |

> *(Insert Figure IV.6 here.)*
>
> **Figure IV.6: Ablation Results, Change in RMSE against the Proposed Model**

### D.9 Case study of the 2024 flood-risk events

> **9. Case study of the 2024 flood-risk events**
>
> Table IV.16 lists the 11 flood-risk events that could be scored, and Table IV.17 summarizes how each model handled them. Every model forecast the peaks too low. For the proposed model, the mean error at the peak was −0.18 m at 1 hour, −0.30 m at 3 hours and −0.35 m at 6 hours; ridge regression and tide plus persisted residual showed similar errors. The largest event, on 24 July 2024 (Figure IV.4), reached 12.98 m at 15:00. The proposed model detected it at lead times of 1 to 4 hours, with up to 2 hours of warning, but not at 5 or 6 hours, and its forecasts for the peak hour ranged from 12.74 m (1 hour ahead, 0.24 m too low) to 12.16 m (6 hours ahead, 0.82 m too low).
>
> **Table IV.16: Flood-Risk Events (≥ 12.00 m) in the 2024 Test Season That Could Be Scored**

| Event | First hour ≥ 12.00 m | Last hour | Peak (m) | Hours | Note |
|---|---|---|---|---|---|
| 1 | 23 Jul 11:00 | 23 Jul 13:00 | 12.19 | 3 | |
| 2 | 24 Jul 07:00 | 25 Jul 00:00 | 12.98 | 17 | Carina |
| 3 | 25 Jul 12:00 | 25 Jul 12:00 | 12.03 | 1 | |
| 4 | 2 Sep 08:00 | 2 Sep 12:00 | 12.26 | 5 | |
| 5 | 5 Sep 10:00 | 5 Sep 13:00 | 12.12 | 3 | |
| 6 | 15 Sep 22:00 | 15 Sep 22:00 | 12.02 | 1 | |
| 7 | 11 Oct 05:00 | 11 Oct 05:00 | 12.26 | 1 | |
| 8 | 23 Oct 02:00 | 23 Oct 03:00 | 12.00 | 2 | |
| 9 | 6 Nov 22:00 | 7 Nov 01:00 | 12.26 | 4 | |
| 10 | 17 Nov 22:00 | 17 Nov 23:00 | 12.04 | 2 | |
| 11 | 18 Nov 22:00 | 19 Nov 00:00 | 12.05 | 3 | |

*Note:* A twelfth event (24–25 October 2024, peak 12.59 m) could not be scored because 24 Pandacan hours were missing on 23–24 October (Chapter III, Section E). Hours count only scored hours.

> **Table IV.17: Case Study Summary at 1, 3 and 6 Hours: Events Detected out of 11, Median Warning, Mean Error at the Peak**

| Model | 1 h | 3 h | 6 h |
|---|---|---|---|
| Proposed model | 9, 0.0 h, −0.18 m | 4, 2.5 h, −0.30 m | 3, 5.0 h, −0.35 m |
| Standalone LSTM | 9, 0.0 h, −0.16 m | 5, 3.0 h, −0.30 m | 2, 5.5 h, −0.36 m |
| Ridge regression | 10, 1.0 h, −0.17 m | 6, 3.0 h, −0.29 m | 5, 6.0 h, −0.32 m |
| Tide + persisted residual | 10, 0.0 h, −0.13 m | 4, 2.5 h, −0.27 m | 5, 5.0 h, −0.31 m |
| Persistence | 11, 0.0 h, −0.13 m | 3, 1.0 h, −0.38 m | 0, —, −0.69 m |
| KNN regressor | 5, 1.0 h, −0.51 m | 4, 3.0 h, −0.53 m | 4, 6.0 h, −0.52 m |
| Logistic Regression, 24-h window | 7, 0.0 h | 7, 3.0 h | 1, 5.0 h |
| KNN classifier, 24-h window | 5, 0.0 h | 5, 2.0 h | 4, 5.0 h |

*Note:* Neural models use the median-validation seed. Negative error = forecast below the observed peak. Classifiers give no level, so no peak error.

> *(Insert Figure IV.4 here.)*
>
> **Figure IV.4: Observed Level and Forecasts of the Proposed Model at 1, 3 and 6 Hours, 22–26 July 2024 (Carina)**

### D.10 Comparison with the 2024 Aviles records

> **10. Comparison with the 2024 Aviles records**
>
> After the evaluation, the alert levels were compared descriptively with the Aviles records from 1 June to 15 July 2024 (Table IV.18). The Pandacan level reached 11.69 m in 21 hours of this window and never reached 12.00 m, because the window ended before the July floods. In those 21 hours, drainage stress occurred in 4.8% of hours, against 10.8% in the training seasons, and two thirds of them were dry hours. The comparison neither confirmed nor contradicted the flood-risk level, and the levels were not changed.
>
> **Table IV.18: Alert Levels Compared with the Aviles Records, 1 June to 15 July 2024 (Descriptive)**

| Level | Period | Hours at or above | Stress share at or above | Stress share below | Gate-open share at or above | Dry share at or above |
|---|---|---|---|---|---|---|
| High water (11.69 m) | 2024 check | 21 | 4.8% | 0.4% | 0.0% | 66.7% |
| High water (11.69 m) | Training 2018–2022 | 964 | 10.8% | 2.1% | 0.5% | 47.7% |
| Flood risk (12.00 m) | 2024 check | 0 | — | 0.5% | — | — |
| Flood risk (12.00 m) | Training 2018–2022 | 80 | 55.0% | 2.4% | 0.0% | 11.2% |

**Possible panel questions (Section D)**
- *"Your model has the lowest RMSE at every lead. Why do you say it doesn't beat ridge?"* — Lower RMSE in a
  sample is not proof. The DM test asks whether the difference is larger than the hour-to-hour variation of the
  errors would produce by chance, allowing for autocorrelation. After Holm adjustment across the 72 pre-set
  tests, the ridge differences were not significant. The walk-forward then showed ridge matching the model in
  2021 and 2022, and significantly better at one lead time in each.
- *"Without Holm, are the ridge differences significant?"* — Yes: the raw p-values are below 0.05 at 1–5 hours
  (0.004–0.033), but not after Holm adjustment. The adjustment was fixed before the test because 72 tests were
  run. Say this openly; don't hide it.
- *"Why is the rainy-hour DM vs tide-only not significant when the RMSE gap is so large (0.056 vs 0.25 m)?"* —
  In rainy hours there are fewer cases (1,328), and the squared-error differences are very large and strongly
  autocorrelated during storms. That inflates the Newey–West variance, so the test has less power.
- *"Persistence detected 11 of 11 flood-risk events at 1 h. Isn't that the best model?"* — Its median warning
  time is 0 h: at 1 h it alerts only when the river is already at the level. It detects 0 of 11 at 6 h.
- *"Why does KNN at Recall 0.95 have 3,337 false alarms?"* — KNN probabilities move in steps of 1/k. To reach
  0.95 Recall its threshold had to drop to the lowest step, so it alerted almost every hour. That is why D19 uses
  0.90 for the verdict and reports 0.80/0.95 only as a sensitivity check.
- *"Why is H2 'supported' if rainfall barely helps?"* — H2 tests Granger precedence by a pre-set rule, not
  forecast skill. Section F of Chapter III anticipated this: with thousands of rows, tiny effects become
  significant, which is why the ridge gain was reported beside each p-value.

**Learn this (Section D)**
- Odds ratio and its CI; what "per 0.1 m" means (an OR of 1.207 means about 21% higher odds per 0.1 m rise).
- ROC-AUC vs PR-AUC; why PR-AUC is compared with the alert-hour share (Saito & Rehmsmeier, 2015).
- Diebold–Mariano: loss difference, Newey–West variance, HLN correction; Holm adjustment.
- Moving-block bootstrap (Künsch, 1989): why 24-h blocks.
- Skill score, and why skill against persistence looks large but against the tide-based model is modest
  (Pappenberger, Ramos, et al., 2015).
- Equal-recall comparison (D19); trigger offsets.

**Watch out (Section D)**
- **Event counts:** 95 of 103 high-water and 11 of 12 flood-risk events could be scored. Chapter III Table III.6
  shows 103 and 12 (all events). Both are correct; say which you mean.
- **Seeds:** 5 for Tables IV.6–IV.12; 3 for Tables IV.13–IV.15. The ablation "proposed model" RMSE (0.0510 at
  1 h) is the 3-seed mean, which is why it differs slightly from Table IV.6 (0.0516).
- **DM seeds:** proposed model seed 1, standalone LSTM seed 0 (the median-validation seeds).
- **The 2023 walk-forward fold is not independent.** Don't count it as evidence for the proposed model.
- **The likelihood-ratio χ² for H1 is computed without day-clustering**; the odds-ratio CIs are day-clustered. If
  asked, say so.
- **Figure IV.3 draws straight lines across data gaps** (for example late October). Add to its caption: "Straight
  segments are gaps in the record, not forecasts."
- Use "more accurate" or "lower error" for levels. Use "accuracy" only in its alert sense, and only for reference
  (Chapter III F.7).
- Exact numbers: `reports/chapter4/table_IV-*.csv`. If anything in `reports/tables` changes, rerun
  `make report`.

---

## E. Analysis and Interpretation of the Results

**What this part does.** The template asks you to interpret the results, decide on the effectiveness and
efficiency of the system, and say under which conditions it works well or badly. Here you explain *why* the
results came out as they did, and compare them with the studies in Chapter II.

**Paste this:**

> **E. Analysis and Interpretation of the Results**
>
> **River level as a flood-risk indicator (H1).** The training records supported the physical reasoning of Chapter II: when the Pasig River at Pandacan was higher, the Aviles station was more likely to run two or more pumps, and more so when it rained, as the significant interaction showed (JICA, 2005a; Liu et al., 2025; Xi & Hu, 2026). The river level, however, added almost nothing to rainfall in separating stress hours from other hours in 2023. Two reasons are likely. Rainfall and high river levels occur together, so much of the river's information is already carried by the rain. And the stress label reflects operators' decisions as well as water conditions (Chapter I, Scope and Limitations). The Pandacan level is therefore best read as a contributing condition for drainage stress in Sampaloc, not as a sufficient signal on its own. The flood-risk level of 12.00 m rested on 80 training hours and moved between 11.70 and 12.25 m under other reasonable definitions (Table IV.3), so it should be treated as an indicative threshold.
>
> **Granger selection (H2).** Rainfall and pressure passed the Granger test, but neither improved forecasts much, and the ablation without rainfall was within seed noise. This agrees with the warning in Chapter II that Granger precedence is a statement about prediction in a linear model, not about how much a variable will help a given forecaster (Hristopulos et al., 2026; Yadav et al., 2026), and with Le et al. (2023), who found that adding precipitation did not clearly help LSTM and GRU forecasts. Two features of the data likely limited rainfall's value: Science Garden rainfall was available only as 6-hour totals, at least one hour late, and the gauge lies in Quezon City rather than over the Sampaloc drainage area. Granger selection also did not choose better inputs than a simple correlation screen. Unlike Sun et al. (2015), this study found no advantage for causal selection.
>
> **Forecast accuracy (H3).** The proposed model was clearly more accurate than persistence and the two tide-based models at every lead time, and its skill grew with the lead time as persistence fell behind the moving tide (Pappenberger, Ramos, et al., 2015). Its 1-hour RMSE of 0.052 m compares well with the 0.10 to 0.12 m reported by Tran et al. (2022) for LSTMs at Mekong estuary stations, although differences in site and tidal range make this only a reference point. The proposed model did not, however, significantly outperform ridge regression or the standalone LSTM, and in the two independent walk-forward years ridge regression matched it and was significantly more accurate at one lead time in each. The ablations explain much of this. The largest gain came from the tabular path, which carries the predicted tide and the calendar terms. Once a model knows the tide for the next six hours and the current level, most of the remaining signal is close to linear, which a ridge model on the same inputs can capture. The two-path design and the LSTM-GRU stack added little beyond that: the standalone LSTM with the same inputs, and the variant with two LSTM layers, were within a few millimeters. This matches Islam et al. (2025), where a non-sequential model beat LSTM and GRU networks for river stage, and qualifies the advantage of LSTM over linear models reported by Nevo et al. (2022) and of the stacked LSTM-GRU reported by Widiasari and Efendi (2024), neither of which tested significance against a linear model on the same inputs.
>
> **Alerts (H4).** At the high-water level, the proposed model was clearly better than the K-Nearest Neighbors classifier but statistically indistinguishable from Logistic Regression on the same 24-hour window. Logistic Regression with class weights and a tuned threshold avoided the zero-recall failure reported by De Leon et al. (2025) and reached an F1-Score of 0.93 at 1 hour. A simple classifier trained directly on the alert, and given the same inputs, was therefore a strong competitor. The K-Nearest Neighbors models, rated excellent for 1- to 6-hour forecasting in the review of Asif et al. (2025), were the weakest learned models here, likely because distances over a long flattened window are dominated by the tidal pattern rather than by the rare high-water situations.
>
> **Peaks and flood-risk events.** Every model forecast flood-risk peaks too low, by 0.13 to 0.18 m at 1 hour and 0.31 to 0.36 m at 6 hours for the better models, and detection of flood-risk events fell sharply beyond 2 hours. Kardhana et al. (2022) reported the same under-forecasting of extremes at Katulampa. The training seasons contained only 80 flood-risk hours from 22 events, and a model trained on mean squared error is drawn toward typical levels. Giving high-water hours twice the weight in the loss did not change this. The 2024 season was also wetter than the training seasons (11% of hours at or above 11.69 m against 5%), so its extremes lay at the edge of what the models had seen.
>
> **Effectiveness and efficiency.** The system was effective as a high-water forecaster: at 1 to 3 hours it caught 92% to 95% of high-water events with Precision near 0.9, and its errors were small compared with the daily tidal swing. It was not yet effective as a flood-risk warning: beyond 2 hours it detected fewer than half of the flood-risk events and forecast their peaks too low. The proposed model needed about 6.4 hours of GPU time for its grid search and final seeds, while ridge regression, which gave statistically equal accuracy, needs no GPU. On efficiency alone, ridge regression or tide plus persisted residual would be the practical first choice for an operational trial, with the proposed model as a candidate to re-test as more flood seasons accumulate.
>
> **Conditions under which the results were good or bad.** Results were best in dry hours and at short lead times, where the level follows the tide (RMSE 0.049 to 0.075 m in dry hours). They were worse in rainy hours (0.056 to 0.123 m), at longer lead times, and at the highest levels, where the model under-forecast. They also depended on the completeness of the Pandacan record: during the 24–25 October 2024 event, 24 missing hours left no complete input window, and no model could issue a forecast. A model that needs 24 unbroken hours of history cannot warn during a sensor outage, which is when warnings may matter most.

**Possible panel questions (Section E)**
- *"So was the hybrid model worth it?"* — For RMSE against simple and tide baselines, yes. Against ridge and a
  plain LSTM, our evidence says no significant gain. We report that honestly, and Chapter II anticipated it (Islam
  et al., 2025). The contribution is the tested pipeline, the alert levels from local records, and showing which
  inputs matter (the tide and calendar terms).
- *"Why did the hybrid fail at peaks?"* — Few extreme examples in training (22 flood-risk events), MSE training
  pulls toward typical values, and 2024 was wetter than training. Kardhana et al. (2022) saw the same thing.
- *"Is 12.00 m a reliable alert level?"* — Indicative. It rests on 80 training hours, and the 2024 Aviles records
  end before the July floods, so it could not be confirmed against 2024 drainage stress.
- *"Why compare your RMSE with Tran et al. if the sites differ?"* — Only as a reference point, as the text says.
  The significance tests against baselines on the same hours are the real evidence.

**Learn this (Section E)**
- Why linear models do well when the predictable tide is given as an input (most of the variation is explained
  by the tide and the current level).
- Regression toward the mean with MSE loss; why extremes are under-forecast.
- The difference between statistical significance and practical importance.

**Watch out (Section E)**
- **"About 6.4 hours of GPU time"** = the proposed model's grid (stage 1: 1.79 h; stage 2: 4.16 h) plus its five
  final seeds (0.46 h), from `reports/chapter4/compute_runtime.csv`. All networks together took 10.6 h (the
  number in Chapter III). Don't mix the two numbers up.
- The claim that ridge "needs no GPU" is true for its method. We did not measure ridge's training time, so don't
  quote a number.
- Keep comparisons with other studies as reference points only (different sites and data).

---

# CHAPTER V — Summary, Conclusions and Recommendations

## A. Summary

**What this part does.** The template asks you to discuss the findings per hypothesis, compare them with previous
results, and be analytical. Keep it shorter than Chapter IV; give no new numbers beyond the key ones.

**Paste this:**

> **Chapter V Summary, Conclusions and Recommendations**
>
> **A. Summary**
>
> This study developed a Granger-Selected Hybrid LSTM-GRU and Tabular Neural Network that forecasts the hourly level of the Pasig River at the MMDA EFCOS Pandacan station 1 to 6 hours ahead, and it evaluated the model's high-water and flood-risk alerts as indicators of drainage stress in the Aviles–Sampaloc drainage area. It used only MMDA and PAGASA Science Garden records for the wet seasons of 2018 to 2024, set every learned quantity on the 2018–2022 training seasons or the 2023 validation season, and opened the 2024 test season once, after all settings were frozen.
>
> **H1 (river level and drainage stress) was partly supported.** With rainfall accounted for, each 0.1-m rise in the Pandacan level raised the odds of drainage stress at the Aviles station by about 21% (odds ratio 1.207, 95% CI 1.143 to 1.275), and the Quiapo station showed the same direction. Adding the river level to rainfall, however, did not significantly improve the separation of stress hours in 2023 (AUC gain 0.004, 95% CI −0.022 to 0.027). The alert levels were set at 11.69 m (high water) and 12.00 m (flood risk).
>
> **H2 (Granger-causal predictors) was supported.** Science Garden rainfall and pressure Granger-caused the de-tided Pandacan level after Bonferroni correction, while relative humidity and mean temperature did not. Their contribution to forecast accuracy was small, and the ablations without rainfall or without Granger selection stayed within seed-to-seed variation, in line with Le et al. (2023).
>
> **H3 (forecast accuracy) was partly supported.** On the 2024 test season, the proposed model had an RMSE of 0.052 m at 1 hour and 0.095 m at 6 hours, the lowest of all models. It was significantly more accurate than persistence, tide-only and tide plus persisted residual at every lead time, and than the K-Nearest Neighbors regressor at 1 and 2 hours (20 of 36 comparisons), but not than ridge regression or the standalone LSTM. Walk-forward validation confirmed the advantage over the tide-based models and persistence, but ridge regression matched the proposed model in 2021 and 2022 and was significantly more accurate at one lead time in each year. As in Islam et al. (2025), a simpler model matched the recurrent networks once both received the same inputs.
>
> **H4 (alert performance) was partly supported.** At the high-water level and equal Recall of 0.90, the proposed model raised fewer false alarms and reached a higher PR-AUC than the K-Nearest Neighbors classifier at 1 to 5 hours, but it was statistically indistinguishable from Logistic Regression on the same 24-hour window. High-water events were detected well (95% at 1 hour, 88% at 6 hours). Flood-risk events, reported descriptively, were detected less often at longer lead times (about 8 of 11 at 1 hour, 3 of 11 at 6 hours), and every model forecast their peaks too low, as Kardhana et al. (2022) observed for extremes elsewhere.

**Possible panel questions**
- *"Summarize your contribution in one sentence."* — We showed, with agency records and pre-registered tests,
  that the Pasig level at Pandacan is linked to drainage stress in Sampaloc and can be forecast 1–6 h ahead with
  about 5–10 cm error. We also showed that a hybrid deep model does not significantly beat a well-fed ridge
  regression on this task.

**Learn this**
- Each hypothesis's decision rule (Chapter III A) and why its verdict came out as it did.

**Watch out**
- Use the exact verdict words: "supported", "partly supported", "not supported".
- "About 21%" comes from OR 1.207 per 0.1 m. Don't write "21% more likely" (that's probability, not odds).

---

## B. Conclusions

**What this part does.** The template asks: how well do the results support the hypotheses; how well do they
answer the statement of the problem; how well were the objectives accomplished; what are the implications and
significance; and a final judgment.

**Paste this:**

> **B. Conclusions**
>
> The results supported the study's hypotheses in part. They confirmed that the Pasig River level at Pandacan is associated with drainage stress at the Aviles pumping station (H1) and that Science Garden rainfall and pressure carry predictive information about the de-tided river level (H2). They also showed that a forecasting model built on these ideas is far more accurate than persistence and tide-based forecasts (H3) and issues fewer false alarms than a K-Nearest Neighbors classifier (H4). They did not support the stronger claims that the river level adds much to rainfall in identifying drainage stress, or that the hybrid design is more accurate than ridge regression, a standalone LSTM or Logistic Regression on the same inputs.
>
> The study answered each question in its statement of the problem. (1) The Pandacan level is associated with drainage stress after accounting for rainfall (odds ratio 1.207 per 0.1 m), and the alerts were set at 11.69 m and 12.00 m, with a sensitivity analysis showing how the flood-risk level depends on the definition of stress. (2) Rainfall and pressure showed Granger-causal precedence; the upstream stations Sto. Niño and Fort Santiago showed it too, but they failed the coverage rule and made a ridge model worse. (3) A dual-path network with two 64-unit LSTM layers, a 64-unit GRU and a 16-unit tabular path, predicting the change in level for six lead times at once, was designed and trained with five seeds. (4) Compared with the baselines on the 2024 season, the proposed model had the lowest error at every lead time, with significant gains over persistence, the tide-based models and the K-Nearest Neighbors models, and no significant difference from ridge regression, the standalone LSTM or Logistic Regression.
>
> All four objectives were accomplished as planned. Every analysis set out in Chapter III was run and reported, the test season was opened once, and every result was reported whichever way it fell. Two departures from the plan were recorded: the walk-forward and ablation runs used three seeds instead of five because of the run-time limit, and one 2024 flood-risk event could not be scored because of missing Pandacan readings.
>
> These results have practical and methodological implications. For agencies and the University, the Pasig level at Pandacan can serve as an early high-water signal for the Aviles–Sampaloc drainage area: at 1 to 3 hours it caught more than nine in ten high-water events, and even one hour of lead time has value for flood response (National Hydrologic Warning Council, 2002). The flood-risk alert, however, is not yet reliable enough to act on alone, because peaks were forecast too low and most flood-risk events were missed beyond 2 hours. For researchers, the study shows that strong simple baselines and significance tests can change the conclusion: judged by RMSE alone, the hybrid model would appear best, but with ridge regression, a standalone LSTM and Diebold–Mariano tests on the same hours, its advantage was not significant.
>
> In final judgment, the study met its aim of building and fairly testing an hourly Pasig River forecast as a flood-risk indicator for Sampaloc. Its most useful outputs are the locally derived alert levels, the leak-free and reproducible pipeline, and the evidence on which inputs matter. The hybrid deep-learning design itself was not shown to be necessary for this task.

**Possible panel questions**
- *"If ridge is as good, why is your title about the hybrid model?"* — The title names what we proposed and
  tested. The finding that it does not beat ridge significantly is a result, and Chapter II and the hypotheses
  prepared for it ("the study also had to be ready to report a baseline that wins", Chapter II C).
- *"Did you accomplish Objective 4?"* — Yes, as an evaluation objective: every comparison, test, walk-forward,
  ablation and case study was run. Accomplishing it doesn't require the proposed model to win.

**Learn this**
- Distinguish "objective accomplished" (the analysis was done) from "hypothesis supported" (the result came out
  as expected).

**Watch out**
- The conclusions must not add results that are not in Chapter IV.
- "National Hydrologic Warning Council (2002)" is already cited in your Chapter I. Use the same reference.

---

## C. Recommendations

**What this part does.** The template asks for further improvements and extensions, and for newly discovered
problems to be addressed. Tie each recommendation to a finding.

**Paste this:**

> **C. Recommendations**
>
> Based on the findings, the researchers recommend the following.
>
> 1. **Use higher-resolution and closer rainfall data.** Rainfall added little in this study partly because Science Garden rainfall was available only as 6-hour totals from a gauge in Quezon City. Future studies should test hourly or sub-hourly rainfall from gauges within or near the Aviles–Sampaloc drainage area, such as the telemetered rain gauges of the MMDA EFCOS network.
> 2. **Improve the forecasting of peaks.** All models under-forecast flood-risk peaks, and a weighted loss with w = 2 did not help. Future work should try approaches aimed at extremes, such as probabilistic or quantile forecasts that give an upper range, and should retrain as more flood seasons accumulate, since the training record held only 22 flood-risk events.
> 3. **Model the seasonal change of the tide.** The fixed-amplitude tide fit left residual tidal peaks. A tide model whose amplitudes vary with the season and river flow, reflecting the interaction of river discharge and tide (Hoitink & Jay, 2016), may reduce the error the networks had to learn.
> 4. **Make forecasts robust to missing readings.** The 24–25 October 2024 event could not be forecast because of a gap in the Pandacan record. An operational system should handle missing hours, for example with models trained to accept incomplete windows or with a backup gauge, and should monitor gauge outages during storms.
> 5. **Test the alert levels against more drainage records.** The Aviles logs ended in mid-July 2024, before the season's floods. Obtaining later Aviles and Quiapo records would allow the alert levels to be checked against drainage stress during the 2024 events and later seasons, and confirming the elevation datum of the EFCOS readings would allow comparison with the JICA design levels.
> 6. **Start any operational trial with the simplest adequate model.** Because ridge regression and Logistic Regression on the same inputs matched the proposed model, an operational trial with MMDA or the Manila DRRMO could begin with these simpler models and re-test the hybrid model as new seasons provide more test data.
> 7. **Relate the river forecast to street flooding.** The study could not measure flood depth in Sampaloc. Installing water-level sensors on flood-prone streets such as España Boulevard, or collecting verified flood reports, would allow future work to test whether high-water and flood-risk alerts correspond to actual flooding.
> 8. **Evaluate on further test seasons.** Results rested on one test season with 11 scoreable flood-risk events. Repeating the evaluation on 2025 and later seasons, with the same frozen procedure, would give firmer evidence on the flood-risk alerts and the comparison with ridge regression.

**Possible panel questions**
- *"Which recommendation matters most?"* — Peak forecasting (2) and missing-data robustness (4), because those
  are where the system failed for flood-risk warnings.
- *"Why not just add more layers or a Transformer?"* — The ablations show that architecture changes moved the RMSE
  by millimeters. The limits are in the data (rain resolution, few extremes, gaps), so data recommendations come
  first.

**Learn this**
- What a quantile or probabilistic forecast is, and why it helps with peaks (it gives an upper bound, not just a
  mean).

**Watch out**
- Recommendation 1 mentions EFCOS rain gauges. Your Chapter I definition says EFCOS includes "telemetered rain and
  river gauges", so this is consistent. Don't name specific gauges unless you have their data.

---

## Extra: Abstract (required by the template, 50–100 words)

**Paste this:**

> This study developed a Granger-Selected Hybrid LSTM-GRU and Tabular Neural Network that forecasts the hourly Pasig River level at the MMDA EFCOS Pandacan station 1 to 6 hours ahead as a flood-risk indicator for Sampaloc, Manila. Using MMDA and PAGASA records from 2018 to 2024, the river level was linked to drainage stress at the Aviles pumping station, and rainfall and pressure were selected by Granger tests. On the 2024 test season, the model's RMSE was 0.052 to 0.095 m, significantly lower than tide-based and persistence forecasts but not than ridge regression, and it under-forecast flood-risk peaks.

*(Word count: 97.)*

**Watch out:** the template limits the abstract to 50–100 words. Recount if you edit it.

---

## Checklist before submission

- [ ] The two remaining Chapter III edits are done, so Chapter III and Chapter IV use the same seed counts
      (5 / 3) and event counts (11 of 12, 95 of 103).
- [ ] Figures IV.1–IV.6 and Tables IV.1–IV.18 are added to the List of Figures and List of Tables.
- [ ] Every figure has a sentence in the text that refers to it (template rule).
- [ ] Appendix H is added (test scripts list; critical source code in Courier New 8 pt).
- [ ] Two spaces between sentences after pasting.
- [ ] Numbers spot-checked against `reports/chapter4/chapter4.md`.
