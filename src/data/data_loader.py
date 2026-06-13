from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.simulation.process import Process


def save_workload_csv(processes: list[Process], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([process.to_record() for process in processes]).to_csv(path, index=False)


def load_workload_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Workload file not found: {path}")
    return pd.read_csv(path)


def load_processes_from_csv(path: Path) -> list[Process]:
    frame = load_workload_frame(path)
    required_columns = {
        "process_id",
        "arrival_time",
        "burst_time",
        "priority",
        "process_type",
        "cpu_usage_avg",
        "cpu_usage_peak",
        "memory_usage_avg",
        "memory_usage_peak",
        "io_usage",
        "required_cpu",
        "required_memory",
    }
    missing = required_columns.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing workload columns: {', '.join(sorted(missing))}")

    return [
        Process(
            process_id=int(row.process_id),
            arrival_time=int(row.arrival_time),
            burst_time=int(row.burst_time),
            priority=int(row.priority),
            process_type=str(row.process_type),
            cpu_usage_avg=float(row.cpu_usage_avg),
            cpu_usage_peak=float(row.cpu_usage_peak),
            memory_usage_avg=float(row.memory_usage_avg),
            memory_usage_peak=float(row.memory_usage_peak),
            io_usage=float(row.io_usage),
            required_cpu=float(row.required_cpu),
            required_memory=float(row.required_memory),
        )
        for row in frame.itertuples(index=False)
    ]
