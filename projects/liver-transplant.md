---
layout: default
title: Liver Transplant Outcome Prediction
---

# Liver Transplant Outcome Prediction
**Repository:** [liver-transplant-ml](https://github.com/Gogo2015/liver-transplant-ml)
**Course:** CS 7641 — Machine Learning (Georgia Tech) · **Best Project Award**
**Team:** Anushka Bajpai · Madhavan Balasubramaniam · Sanjay Gorur · Ameel Jani · Gaurav Mitra
**Clinical Advisor:** Dr. Marwan Kazimi

## Project Overview
The MELD score effectively measures how sick a patient is before transplant, but it does not predict whether a given donor-recipient pair will result in a functioning graft. We built a full ML pipeline on the OPTN/SRTR national liver transplant registry (2007-2024) to predict graft failure from features available at the time of transplant, across both classification and survival-analysis formulations.

**Dataset:** ~87,000 adult transplants after filtering, 416 raw columns reduced to 113 predictors.
Chronological train/test split: 2007-2020 (train) / 2021-2024 (test) to prevent temporal leakage.

> Raw data is not publicly redistributable under the SRTR Data Use Agreement.

## My Contributions
- Designed and implemented the full preprocessing pipeline: sentinel-code replacement (UNOS codes 997/998/999), structural imputation strategy (N/U/0 fills for absent flags and untested serology), mode imputation for nominal clinical codes, median imputation for right-skewed labs, and KNN imputation for correlated lab groups — all fit exclusively on the training set.
- Built two encoding pipelines: one-hot encoding for Cox PH, Random Forest, and XGBoost; label encoding for tree-based survival models (RSF and GBST), avoiding the memory and sparsity issues of OHE expansion for scikit-survival models.
- Implemented the XGBoost horizon-based classifiers (1-year, 3-year, 5-year graft failure) with winner-takes-all threshold selection, class-weight balancing, and early stopping against a held-out validation split.
- Ran the K-Means clustering and PCA analysis: identified k=40 as optimal by silhouette analysis, discovered clinically interpretable patient subgroups including a high-risk cohort of critically ill recipients paired with older donors.
- Contributed to the Cox PH implementation with forest plot, Kaplan-Meier stratification by risk quartile, and Schoenfeld residual diagnostics.

## Models and Results

| Model | Type | Metric | Value |
|---|---|---|---|
| Cox Proportional Hazards | Survival | C-index (test) | 0.5823 |
| Random Forest | Classification | AUROC (test) | ~0.62 |
| Random Survival Forest | Survival | C-index (test) | 0.6122 |
| Gradient Boosted Survival Trees | Survival | C-index (test) | &gt;0.61 |
| XGBoost (1-year horizon) | Classification | AUROC (test) | ~0.61 |
| XGBoost (3-year horizon) | Classification | AUROC (test) | ~0.64 |
| K-Means (k=40, 90 PCs) | Unsupervised | Silhouette | 0.127 |

RSF and GBST were tuned in two phases using two-phase grid search on Georgia Tech's PACE HPC cluster (SLURM array jobs). RSF Phase 1 best config: `n_estimators=100`, `min_samples_leaf=20`, `max_features='sqrt'` (OOB C-index: 0.6055).

C-index is Harrell's concordance index: 0.5 = random, 1.0 = perfect ranking of patient risk.

## Key Findings

**Temporal leakage is the critical correctness concern.** A random train/test split would allow transplants from 2021 to appear in training, and the model learns patterns from future medical practice. Chronological splitting revealed that test-set event rates differ substantially (recent cohort has shorter follow-up, so fewer graft failures are recorded yet), which is expected and clinically meaningful.

**Sentinel codes are not missing data.** UNOS uses codes like 998 ("unknown") that are not NaN but should not be treated as valid numeric values. Imputing them as-is would introduce misleading correlations.

**Censored outcomes require survival models.** XGBoost with a fixed horizon excludes patients censored before the threshold, which biases the training distribution. Cox PH, RSF, and GBST handle censoring by construction. The 5-year XGBoost result is unreliable on the 2021-2024 test cohort because few patients have reached five-year follow-up.

**Clustering revealed what the models struggled with.** The subgroup that concentrated the worst graft outcomes — critically ill recipients (`MED_COND_TRR=1`, `LIFE_SUP_TRR=1`) paired with older donors — is also the group where clinical judgment has the least quantitative guidance.

## Tech Stack
- Python, scikit-learn, scikit-survival, lifelines, XGBoost
- pandas, numpy (preprocessing pipeline)
- KNNImputer, VarianceThreshold, OneHotEncoder
- RandomSurvivalForest, GradientBoostingSurvivalAnalysis (sksurv)
- CoxPHFitter (lifelines) with L2 regularization
- PCA + KMeans (unsupervised phenotyping)
- SLURM / PACE HPC cluster (RSF and GBST Phase 2 tuning)
- matplotlib, seaborn (forest plots, KM curves, Schoenfeld residuals)

---

**Link:** [GitHub Repository](https://github.com/Gogo2015/liver-transplant-ml)