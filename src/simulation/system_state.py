from __future__ import annotations

from dataclasses import dataclass

from src.simulation.process import Process


@dataclass(frozen=True, slots=True)
class SystemState:
    time_tick: int
    running_processes: tuple[int, ...]
    waiting_processes: tuple[int, ...]
    used_cpu: float
    used_memory: float
    available_cpu: float
    available_memory: float
    completed_count: int

    @classmethod
    def from_processes(
        cls,
        time_tick: int,
        running: list[Process],
        waiting: list[Process],
        total_cpu: float,
        total_memory: float,
        completed_count: int,
    ) -> "SystemState":
        used_cpu = sum(process.allocated_cpu for process in running)
        used_memory = sum(process.allocated_memory for process in running)
        return cls(
            time_tick=time_tick,
            running_processes=tuple(process.process_id for process in running),
            waiting_processes=tuple(process.process_id for process in waiting),
            used_cpu=used_cpu,
            used_memory=used_memory,
            available_cpu=max(0.0, total_cpu - used_cpu),
            available_memory=max(0.0, total_memory - used_memory),
            completed_count=completed_count,
        )
