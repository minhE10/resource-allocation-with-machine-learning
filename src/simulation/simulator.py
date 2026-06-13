from __future__ import annotations

from dataclasses import dataclass

from src.scheduler.process_queue import ProcessQueue
from src.scheduler.resource_allocator import ResourceAllocator
from src.simulation.metrics import SimulationMetrics, calculate_metrics
from src.simulation.process import Process
from src.simulation.system_state import SystemState


@dataclass(frozen=True, slots=True)
class SimulationResult:
    metrics: SimulationMetrics
    timeline: list[SystemState]
    completed_processes: list[Process]


class Simulator:
    def __init__(
        self,
        allocator: ResourceAllocator,
        total_cpu: float = 100.0,
        total_memory: float = 16_384.0,
        max_ticks: int = 10_000,
    ) -> None:
        self.allocator = allocator
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.max_ticks = max_ticks

    def run(self, processes: list[Process]) -> SimulationResult:
        pending = sorted([process.clone() for process in processes], key=lambda item: item.arrival_time)
        queue = ProcessQueue()
        running: list[Process] = []
        completed: list[Process] = []
        timeline: list[SystemState] = []
        time_tick = 0

        while len(completed) < len(pending) and time_tick < self.max_ticks:
            queue.add_arrivals(pending, time_tick)

            available_cpu = self.total_cpu - sum(process.allocated_cpu for process in running)
            available_memory = self.total_memory - sum(process.allocated_memory for process in running)
            decisions = self.allocator.allocate(queue.as_list(), available_cpu, available_memory)
            accepted = {decision.process_id: decision for decision in decisions if decision.accepted}

            for process in queue.as_list():
                decision = accepted.get(process.process_id)
                if decision is None:
                    continue
                process.allocated_cpu = decision.cpu
                process.allocated_memory = decision.memory
                process.start_time = time_tick
                running.append(process)
                queue.remove(process)

            queue.increment_waiting_time()

            for process in list(running):
                if process.remaining_time is None:
                    process.remaining_time = process.burst_time
                progress = max(1, round(process.allocated_cpu / max(1.0, process.required_cpu)))
                process.remaining_time -= progress
                if process.remaining_time <= 0:
                    process.finish_time = time_tick + 1
                    completed.append(process)
                    running.remove(process)

            timeline.append(
                SystemState.from_processes(
                    time_tick=time_tick,
                    running=running,
                    waiting=queue.as_list(),
                    total_cpu=self.total_cpu,
                    total_memory=self.total_memory,
                    completed_count=len(completed),
                )
            )
            time_tick += 1

        metrics = calculate_metrics(completed, timeline, self.total_cpu, self.total_memory)
        return SimulationResult(metrics=metrics, timeline=timeline, completed_processes=completed)
