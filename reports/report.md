# Resource Allocation with Machine Learning

## 1. Introduction

Resource allocation is a core responsibility of an operating system. The OS must
decide how CPU time, memory, and other resources are distributed among running
processes. Static allocation policies are simple but may perform poorly when the
workload changes over time.

This project aims to build a simulation system that uses machine learning to
predict the CPU and memory demand of processes, then dynamically allocates
resources based on those predictions.

## 2. Main Content

### Chosen Solution

The project compares two resource allocation strategies:

- Baseline allocator: priority-based allocation without machine learning.
- ML allocator: allocation based on predicted CPU and memory demand.

The ML model is a Random Forest regressor trained on synthetic workload data.
It predicts CPU and memory requirements from process attributes and historical
usage features.

### Program Description

Input data:

- Process ID
- Arrival time
- Burst time
- Priority
- Process type
- CPU usage history summary
- Memory usage history summary
- I/O usage

Output data:

- Predicted CPU demand
- Predicted memory demand
- Simulation metrics
- Resource usage charts

Main modules:

- `src/data`: generate, load, and preprocess workload data.
- `src/ml`: train and use the prediction model.
- `src/scheduler`: implement baseline and ML allocators.
- `src/simulation`: simulate process execution and compute metrics.
- `src/visualization`: create charts and dashboard.

## 3. Program Interface

The program supports a command-line interface:

```bash
python main.py
```

It also supports an optional Streamlit dashboard:

```bash
streamlit run src/visualization/dashboard.py
```

## 4. Teamwork

See `docs/team_contribution.md`.

## 5. References

- Silberschatz, Galvin, and Gagne, Operating System Concepts.
- scikit-learn documentation: RandomForestRegressor.
- pandas documentation.
- Streamlit documentation.
