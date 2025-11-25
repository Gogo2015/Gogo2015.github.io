# Waymo Motion Forecasting Baseline  
**Repository:** [WaymoMotionEstimator](https://github.com/Gogo2015/WaymoMotionEstimator)  
**Technical Report:** [Conv MLP Paper](https://github.com/Gogo2015/WaymoMotionEstimator/blob/main/ConvMLPPaper.pdf)

## Project Overview  
This project implements a trajectory‐prediction model on the Waymo Open Motion Dataset. The model uses past agent motion (e.g., 10­step history) to forecast future positions (~80 steps ahead), helping autonomous agents anticipate motion for planning and safety.

## My Contributions  
- Designed and implemented a **Conv-MLP architecture**:  
  - Convolutional encoder extracts temporal motion features from past trajectory sequences.  
  - MLP decoder outputs the future trajectory coordinates.  
- Built the data pipeline:  
  - Reading Waymo TFRecords, transforming coordinate frame so last heading aligns with +x axis.  
  - Creating training/validation splits.  
- Training & evaluation:  
  - Employed metrics such as Average Displacement Error (ADE) and Final Displacement Error (FDE).  
  - Incorporated predictive visualization comparing actual vs predicted trajectories.

## Insights & Visualization
- Key insight: Without map or social context, models tend to default to simple continuation of past motion, limiting performance in curve/branching scenarios.  
- Reflection: Gained stronger understanding of deep learning pipeline for motion forecasting and WOMD data, and learned how simplifying assumptions (no map context) affect real-world viability.

![Trajectory comparison](https://raw.githubusercontent.com/Gogo2015/WaymoMotionEstimator/main/gifs/ConvMLP/test_agent_4.gif)  
*Example GIF: predicted vs actual trajectory for a test agent.*

## Tech Stack  
- Python, Tensorflow/Keras
- Conv1D + MLP layers  
- TFRecord ingestion & preprocessing  
- Visualization (trajectory plots / GIFs)  
- Docker + reproducible environment

## Future Work  
- Integrate map / road-graph context and neighboring agents.  
- Extend model to multi-agent, multi-modal predictions.  
- Experiment with Transformer or Graph Neural Network architectures for improved generalization.

---

**Link:** [GitHub Repository](https://github.com/Gogo2015/WaymoMotionEstimator)  
