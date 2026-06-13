# Resource Allocation with Machine Learning

Project topic 21 for Operating Systems: dynamically allocate CPU and memory to
running processes using machine-learning predictions.

## Features

- Generate synthetic process workloads.
- Train a Random Forest model to predict CPU and memory demand.
- Simulate an ML-based allocator.
- Compare against a baseline priority-based allocator when needed.
- Compare CPU utilization, memory utilization, waiting time, turnaround time,
  throughput, and delayed processes.
- Export charts for the report.
- Optional Streamlit dashboard.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run CLI

Run the full pipeline: generate data, train model, and simulate the ML allocator.

```bash
python main.py
```

Run individual steps:

```bash
python main.py --generate-data --processes 150
python main.py --train --data data/sample/sample_workload.csv
python main.py --simulate --data data/sample/sample_workload.csv
```

Run a report-oriented comparison between baseline and ML:

```bash
python main.py --compare --data data/sample/sample_workload.csv
```

## Run Dashboard

```bash
python -m streamlit run src/visualization/dashboard.py
```

## Project Structure

```text
data/                 Workload CSV files
models/               Saved ML model
reports/              Report markdown and generated figures
src/data/             Data generation, loading, preprocessing
src/ml/               Training, prediction, evaluation
src/scheduler/        Baseline and ML allocation algorithms
src/simulation/       Process model, simulator, metrics
src/visualization/    Charts and Streamlit dashboard
tests/                Unit tests
docs/                 Algorithm and project documentation
```
