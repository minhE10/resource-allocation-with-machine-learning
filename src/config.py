from __future__ import annotations

from pathlib import Path

RANDOM_SEED = 42

DEFAULT_SAMPLE_DATA_PATH = Path("data/sample/sample_workload.csv")
DEFAULT_MODEL_PATH = Path("models/resource_predictor.pkl")

FEATURE_COLUMNS = [
    "arrival_time",
    "burst_time",
    "priority",
    "process_type_code",
    "cpu_usage_avg",
    "cpu_usage_peak",
    "memory_usage_avg",
    "memory_usage_peak",
    "io_usage",
]

TARGET_COLUMNS = ["required_cpu", "required_memory"]

PROCESS_TYPES = {
    "batch": 0,
    "interactive": 1,
    "io_bound": 2,
    "cpu_bound": 3,
}
