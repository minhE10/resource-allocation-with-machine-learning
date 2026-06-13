# Resource Allocation with Machine Learning

Project topic 21 for Operating Systems: dynamically allocate CPU and memory to
running processes using machine-learning predictions.

## Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux

## Features

- Generate synthetic process workloads.
- Train a Random Forest model to predict CPU and memory demand.
- Simulate an ML-based allocator.
- Compare against a baseline priority-based allocator when needed.
- Compare CPU utilization, memory utilization, waiting time, turnaround time,
  throughput, and delayed processes.
- Export charts for the report.
- Optional Streamlit dashboard.

## Quick Start

```bash
git clone <your-repository-url>
cd resource-allocation-with-machine-learning
python -m venv .venv
```

Activate the virtual environment on Windows CMD:

```bat
.venv\Scripts\activate.bat
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run CLI

Run the full ML pipeline:

```text
generate workload -> train model -> simulate ML allocator -> export charts
```

```bash
python main.py
```

Generated files:

```text
data/sample/sample_workload.csv
models/resource_predictor.pkl
reports/figures/ml_resource_usage.png
```

Run individual steps:

```bash
python main.py --generate-data --processes 150
python main.py --train --data data/sample/sample_workload.csv
python main.py --simulate --data data/sample/sample_workload.csv
```

`--simulate` uses the ML allocator by default. It requires a trained model at
`models/resource_predictor.pkl`.

Run a report-oriented comparison between baseline and ML:

```bash
python main.py --compare --data data/sample/sample_workload.csv
```

This exports:

```text
reports/figures/baseline_resource_usage.png
reports/figures/ml_resource_usage.png
reports/figures/allocator_comparison.png
```

## Run Dashboard

```bash
python -m streamlit run src/visualization/dashboard.py
```

Use `python -m streamlit` instead of `streamlit` so Windows uses the same Python
environment where Streamlit was installed.

## Smoke Test

After installing dependencies, run:

```bash
python -m compileall src tests main.py
python -m pytest -q
python main.py --processes 30
```

Expected result:

```text
3 passed
Generated ... processes
Saved model to models/resource_predictor.pkl
ML metrics:
Charts saved to reports/figures
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

## Common Issues

If `streamlit` is not recognized, run:

```bash
python -m streamlit run src/visualization/dashboard.py
```

If `--simulate` says the model file is missing, train first:

```bash
python main.py --generate-data
python main.py --train
python main.py --simulate
```

If imports fail in tests, run commands from the repository root directory.
