# sEMG Hand Gesture Recognition

## Overview
A system to capture muscle activation signals (sEMG) and classify hand gestures using machine learning.

## Features
- **sEMG Sensor System**: Custom-built for high-fidelity muscle signal recording.
- **Gesture Classification**: ML model predicts gestures from sEMG data.
- **Data Processing Pipeline**: Filters noise and extracts features for training.

## How It Works
1. **Hardware**:
   - sEMG sensors record muscle activity.
   - Signals are amplified and digitized for analysis.
2. **Data Processing**:
   - Filters applied (20-450 Hz).
   - Extracted features: RMS, MAV, Zero Crossing.
3. **Machine Learning**:
   - Models: SVM, Neural Networks.
   - Performance: X% accuracy.

## Workflow
1. **Data Collection**:
   - Participants perform predefined gestures (e.g., fist, wave).
   - Signals recorded for multiple trials.
2. **Model Training**:
   - Train/test split (80/20).
   - Evaluate accuracy and confusion matrix.
3. **Prediction**:
   - Model predicts gestures based on live sEMG input.

## Tech Stack
- **Hardware**: sEMG sensors, Arduino.
- **Software**: Python, `numpy`, `scikit-learn`, `tensorflow`.
- **Tools**: Signal processing with SciPy, visualization with Matplotlib.

## Quick Start
1. Clone the repo:
   ```bash
   git clone https://github.com/beaukuhn/sEMG_Project.git
