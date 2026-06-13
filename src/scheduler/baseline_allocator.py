from __future__ import annotations

from src.scheduler.resource_allocator import AllocationDecision, ResourceAllocator
from src.simulation.process import Process
from src.utils.constants import MIN_CPU_ALLOCATION, MIN_MEMORY_ALLOCATION


class BaselineAllocator(ResourceAllocator):
    """Priority-based allocator without ML prediction."""

    def allocate(
        self,
        waiting_processes: list[Process],
        available_cpu: float,
        available_memory: float,
    ) -> list[AllocationDecision]:
        decisions: list[AllocationDecision] = []
        remaining_cpu = available_cpu
        remaining_memory = available_memory

        for process in sorted(waiting_processes, key=lambda item: (item.priority, item.arrival_time, item.process_id)):
            requested_cpu = max(MIN_CPU_ALLOCATION, min(process.required_cpu, self.total_cpu * 0.4))
            requested_memory = max(MIN_MEMORY_ALLOCATION, min(process.required_memory, self.total_memory * 0.4))

            if requested_cpu <= remaining_cpu and requested_memory <= remaining_memory:
                remaining_cpu -= requested_cpu
                remaining_memory -= requested_memory
                decisions.append(
                    AllocationDecision(
                        process_id=process.process_id,
                        cpu=requested_cpu,
                        memory=requested_memory,
                        accepted=True,
                        reason="priority-fit",
                    )
                )
            else:
                decisions.append(
                    AllocationDecision(
                        process_id=process.process_id,
                        cpu=0.0,
                        memory=0.0,
                        accepted=False,
                        reason="insufficient-resource",
                    )
                )

        return decisions
