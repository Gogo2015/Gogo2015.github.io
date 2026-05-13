---
layout: default
title: GNN Molecular Property Prediction
---

# GNN Molecular Property Prediction
**Course:** CS 7643 — Deep Learning (Georgia Tech) · Final Project
**Team:** Net-Runners (Kapil Meena, Gaurav Mitra, Archith K. Iyer)

## Project Overview

Predicting the HOMO-LUMO energy gap of molecules from 2D graph structure. The HOMO-LUMO gap is a quantum-chemical property used in materials and drug discovery, normally computed by Density Functional Theory at a cost of hours per molecule. A learned model can predict the same scalar in milliseconds, which is the scale needed for screening millions of candidates.

The project compares a deep edge-aware message-passing GNN against the same backbone augmented with a Virtual Node — a single global node connected to every atom, intended to address the over-squashing bottleneck on larger molecular graphs.

## My Contributions

- Built the custom GNN architecture from scratch in PyTorch Geometric: GINE convolution stack with residual connections, BatchNorm, dropout, and jumping-knowledge readout.
- Implemented the Virtual Node variant — per-layer broadcast addition into atom embeddings and the post-layer VN update MLP.
- Wrote the full training loop: PCQM4Mv2 data pipeline via `smiles2graph`, batched message passing, validation, checkpointing.
- Contributed to the technical report.

## Architecture

Both models use a 7-layer GINE backbone with hidden dimension 256:

1. Atom features (9 categoricals: atomic number, chirality, degree, formal charge, hydrogen count, hybridization, aromaticity, ring membership, radical electrons) and bond features (3 categoricals: bond type, stereo, conjugation) embedded via learned per-feature lookups.
2. 7 GINE layers — each one applies the convolution, BatchNorm, ReLU, dropout, and a residual.
3. Mean-pool atom embeddings to graph level at every layer; sum across layers (jumping knowledge).
4. 2-layer MLP regression head produces the predicted gap in eV.

GINE update rule:

$$h_v^{(l+1)} = \text{MLP}^{(l)}\!\left((1+\epsilon^{(l)})\, h_v^{(l)} + \sum_{u \in N(v)} \text{ReLU}(h_u^{(l)} + e_{vu}^{(l)})\right)$$

The Virtual Node variant adds one global node per graph; before each layer it is broadcast into every atom embedding, and after each layer it is refreshed from the sum of atom embeddings. This gives any two atoms in the molecule a constant-hop communication path.

## Results

Trained on the full PCQM4Mv2 split (3.38M molecules) for 5 epochs on an H100. The official metric is mean absolute error (MAE) in eV on the 73,545-molecule validation split.

| Model              | Validation MAE (eV) |
|--------------------|---------------------|
| Baseline GINE      | **0.1421**          |
| Virtual Node GINE  | 0.1487              |

The Virtual Node did not improve aggregate MAE — somewhat against the original hypothesis. A size-bucket breakdown gave a more interesting result:

| Size Bucket (# atoms) | Baseline GINE | VN GINE    |
|-----------------------|---------------|------------|
| 0–10                  | **0.1590**    | 0.1601     |
| 11–20                 | **0.1337**    | 0.1422     |
| 21–30                 | 0.2314        | **0.2133** |
| 31–40                 | 0.5078        | **0.4761** |

The Virtual Node helps on medium-to-large molecules (21–40 atoms) where long-range information flow matters more, and slightly hurts on small molecules where the baseline already has short paths between all atoms. This is consistent with the over-squashing motivation, but not with the simpler "VN is always helpful" claim.

## Key Findings

- **Depth mattered more than width.** Hyperparameter search on a 200k subset showed that going from 5 to 7 GINE layers gave the biggest improvement; narrowing hidden dimension or lowering learning rate both hurt.
- **A bigger model is not automatically a better model.** The Virtual Node added ~30% more parameters and a global communication channel, but didn't help in aggregate against a deep, edge-aware baseline trained on a large dataset.
- **Aggregate metrics can hide where a method actually helps.** Slicing validation error by molecule size revealed the regime (medium-to-large graphs) where the Virtual Node's design assumption holds up.

## Limitations

- 2D only. The dataset ships with 3D conformer coordinates that we didn't use; HOMO-LUMO gaps depend on spatial and electronic structure that 2D connectivity can't fully capture.
- 5 epochs per final run (~3 hours/epoch on an H100). Neither model showed overfitting at epoch 5, so both could have improved with more compute.
- Single seed for the final comparison. The 0.0066 eV gap should be read as suggestive.

## Tech Stack

- PyTorch, PyTorch Geometric (custom GINE conv + Virtual Node module)
- RDKit (SMILES → molecular graph)
- OGB (PCQM4Mv2 dataset loader, official evaluator)
- NumPy, pandas, matplotlib (analysis and plots)
- H100 GPU on a cloud platform for final training

---

**Repository:** [GitHub link](https://github.com/Gogo2015/GNN-HOMO-LUMO)
**Report:** [Final_Report.pdf](../assets/gnn-homo-lumo/Final_Report.pdf)