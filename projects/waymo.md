---
layout: default
title: Waymo Motion Forecasting
---

# Waymo Motion Forecasting Baseline  
**Repository:** [WaymoMotionEstimator](https://github.com/Gogo2015/WaymoMotionEstimator)  
**Technical Report:** [Conv MLP Paper](https://github.com/Gogo2015/WaymoMotionEstimator/blob/main/ConvMLPPaper.pdf)

## Project Overview  
This project implements a trajectory‐prediction model on the Waymo Open Motion Dataset. The model uses past agent motion (e.g., 10­step history) to forecast future positions (~80 steps ahead), helping autonomous agents anticipate motion for planning and safety.

## My Contributions
- Designed and implemented a **Conv-MLP baseline architecture**:
  - Convolutional encoder extracts temporal motion features from past trajectory sequences.
  - MLP decoder outputs the future trajectory coordinates.
- Extended to **Multi-Modal prediction system**:
  - Implemented MultiModalConvMLP predicting 6 possible future trajectories with confidence scores.
  - Developed winner-takes-all loss combining regression (control) and classification (intent) objectives.
  - Addressed inherent uncertainty in motion prediction by modeling multiple plausible futures.
- Built the data pipeline:
  - Reading Waymo TFRecords, transforming coordinate frame so last heading aligns with +x axis.
  - Creating training/validation splits.
- Established config-based experiment management system with YAML configuration files for reproducible research.
- Training & evaluation:
  - Employed metrics such as Average Displacement Error (ADE) and Final Displacement Error (FDE).
  - Incorporated predictive visualization comparing actual vs predicted trajectories.

## Insights & Visualization
- Key insight: Without map or social context, models tend to default to simple continuation of past motion, limiting performance in curve/branching scenarios.
- Multi-modal prediction captures uncertainty better: predicting multiple plausible trajectories with confidence scores proves more robust than single-trajectory forecasting.
- Reflection: Gained stronger understanding of deep learning pipeline for motion forecasting and WOMD data. Learned how simplifying assumptions (no map context) affect real-world viability, and how modeling uncertainty through multi-modal outputs improves prediction reliability.

**Single-Mode Baseline:**
![Trajectory comparison](https://raw.githubusercontent.com/Gogo2015/WaymoMotionEstimator/main/gifs/ConvMLP/test_agent_4.gif)
*Single trajectory prediction vs ground truth*

**Multi-Modal Predictions:**
![Multimodal Predictions](https://raw.githubusercontent.com/Gogo2015/WaymoMotionEstimator/main/gifs/MultiModalConvMLP/test_agent_0.gif)
![Multimodal Predictions](https://raw.githubusercontent.com/Gogo2015/WaymoMotionEstimator/main/gifs/MultiModalConvMLP/test_agent_2.gif)
*Multiple trajectory modes with confidence scores for better uncertainty modeling*

## Tech Stack
- Python, TensorFlow/Keras
- Conv1D + MLP layers
- Multi-modal architecture with winner-takes-all loss
- YAML-based configuration management
- TFRecord ingestion & preprocessing
- Visualization (trajectory plots / GIFs)
- Docker + reproducible environment

## Recent Improvements
**Multi-modal predictions** - Implemented 6-mode trajectory prediction with confidence scoring
**Config-based experiment management** - YAML configuration system for reproducible research
**Winner-takes-all loss** - Combined control and intent objectives for better multi-modal training

## Future Work
- Integrate map / road-graph context and neighboring agents for scene-aware predictions.
- Extend to multi-agent interaction modeling with social context.
- Experiment with Transformer or Graph Neural Network architectures for improved generalization.
- Attention mechanisms for dynamic mode selection.
- Scale to full dataset using cloud compute resources (Google Compute Engine).

---

**Link:** [GitHub Repository](https://github.com/Gogo2015/WaymoMotionEstimator)  
