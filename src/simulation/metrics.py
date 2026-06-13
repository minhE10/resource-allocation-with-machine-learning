from __future__ import annotations

from dataclasses import dataclass

from src.simulation.process import Process
from src.simulation.system_state import SystemState


@dataclass(frozen=True, slots=True)
class SimulationMetrics:
    average_cpu_utilization: float
    average_memory_utilization: float
    average_waiting_time: float
    average_turnaround_time: float
    throughput: float
    delayed_processes: int
    completed_processes: int
    total_time: int

    def to_dict(self) -> dict[str, float | int]:
        return {
            "average_cpu_utilization": self.average_cpu_utilization,
            "average_memory_utilization": self.average_memory_utilization,
            "average_waiting_time": self.average_waiting_time,
            "average_turnaround_time": self.average_turnaround_time,
            "throughput": self.throughput,
            "delayed_processes": self.delayed_processes,
            "completed_processes": self.completed_processes,
            "total_time": self.total_time,
        }

    def to_text(self) -> str:
        return (
            f"Average CPU utilization: {self.average_cpu_utilization:.2f}%\n"
            f"Average memory utilization: {self.average_memory_utilization:.2f}%\n"
            f"Average waiting time: {self.average_waiting_time:.2f} ticks\n"
            f"Average turnaround time: {self.average_turnaround_time:.2f} ticks\n"
            f"Throughput: {self.throughput:.3f} processes/tick\n"
            f"Delayed processes: {self.delayed_processes}\n"
            f"Completed processes: {self.completed_processes}\n"
            f"Total time: {self.total_time} ticks"
        )


def calculate_metrics(
    completed_processes: list[Process],
    timeline: list[SystemState],
    total_cpu: float,
    total_memory: float,
) -> SimulationMetrics:
    if not completed_processes:
        return SimulationMetrics(0, 0, 0, 0, 0, 0, 0, len(timeline))

    total_time = max(1, timeline[-1].time_tick + 1 if timeline else 1)
    average_cpu = sum(state.used_cpu / total_cpu for state in timeline) / max(1, len(timeline)) * 100
    average_memory = sum(state.used_memory / total_memory for state in timeline) / max(1, len(timeline)) * 100
    average_waiting = sum(process.waiting_time for process in completed_processes) / len(completed_processes)
    average_turnaround = (
        sum((process.finish_time or 0) - process.arrival_time for process in completed_processes)
        / len(completed_processes)
    )
    delayed_processes = sum(1 for process in completed_processes if process.waiting_time > 0)

    return SimulationMetrics(
        average_cpu_utilization=float(average_cpu),
        average_memory_utilization=float(average_memory),
        average_waiting_time=float(average_waiting),
        average_turnaround_time=float(average_turnaround),
        throughput=float(len(completed_processes) / total_time),
        delayed_processes=delayed_processes,
        completed_processes=len(completed_processes),
        total_time=total_time,
    )
