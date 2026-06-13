from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.simulation.metrics import SimulationMetrics
from src.simulation.system_state import SystemState


def timeline_to_frame(timeline: list[SystemState]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "time_tick": state.time_tick,
                "used_cpu": state.used_cpu,
                "used_memory": state.used_memory,
                "waiting_count": len(state.waiting_processes),
                "running_count": len(state.running_processes),
                "completed_count": state.completed_count,
            }
            for state in timeline
        ]
    )


def save_resource_usage_chart(timeline: list[SystemState], output_path: Path, title: str) -> None:
    frame = timeline_to_frame(timeline)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    axes[0].plot(frame["time_tick"], frame["used_cpu"], color="#2563eb", linewidth=2)
    axes[0].set_ylabel("CPU")
    axes[0].set_title(title)
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(frame["time_tick"], frame["used_memory"], color="#16a34a", linewidth=2)
    axes[1].set_xlabel("Time tick")
    axes[1].set_ylabel("Memory MB")
    axes[1].grid(True, alpha=0.25)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def save_comparison_chart(results: dict[str, SimulationMetrics], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(
        [
            {
                "allocator": name,
                "cpu_utilization": metrics.average_cpu_utilization,
                "memory_utilization": metrics.average_memory_utilization,
                "waiting_time": metrics.average_waiting_time,
                "turnaround_time": metrics.average_turnaround_time,
            }
            for name, metrics in results.items()
        ]
    )

    metrics = ["cpu_utilization", "memory_utilization", "waiting_time", "turnaround_time"]
    allocators = list(frame["allocator"])
    x_positions = list(range(len(metrics)))
    width = 0.35

    fig, ax = plt.subplots(figsize=(11, 6))
    for index, allocator in enumerate(allocators):
        values = [float(frame.loc[frame["allocator"] == allocator, metric].iloc[0]) for metric in metrics]
        offsets = [position + (index - (len(allocators) - 1) / 2) * width for position in x_positions]
        ax.bar(offsets, values, width=width, label=allocator)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(metrics, rotation=20)
    ax.set_xlabel("Metric")
    ax.set_ylabel("Value")
    ax.set_title("Allocator Comparison")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
