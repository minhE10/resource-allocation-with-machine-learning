from __future__ import annotations

from src.ml.predictor import ResourcePredictor
from src.scheduler.resource_allocator import AllocationDecision, ResourceAllocator
from src.simulation.process import Process
from src.utils.constants import MIN_CPU_ALLOCATION, MIN_MEMORY_ALLOCATION


class MLAllocator(ResourceAllocator):
    """Allocator that uses predicted CPU and memory demand."""

    def __init__(self, total_cpu: float, total_memory: float, predictor: ResourcePredictor) -> None:
        super().__init__(total_cpu, total_memory)
        self.predictor = predictor
        self._prediction_cache: dict[int, tuple[float, float, str]] = {}

    def allocate(
        self,
        waiting_processes: list[Process],
        available_cpu: float,
        available_memory: float,
    ) -> list[AllocationDecision]:
        decisions: list[AllocationDecision] = []
        remaining_cpu = available_cpu
        remaining_memory = available_memory

        ranked_processes = sorted(
            waiting_processes,
            key=lambda process: (process.priority, -process.waiting_time, process.arrival_time, process.process_id),
        )
        missing_predictions = [
            process for process in ranked_processes if process.process_id not in self._prediction_cache
        ]
        if missing_predictions:
            prediction_frame = self.predictor.predict_many(missing_predictions)
            for row in prediction_frame.itertuples(index=False):
                self._prediction_cache[int(row.process_id)] = (
                    float(row.predicted_cpu),
                    float(row.predicted_memory),
                    str(row.load_level),
                )

        for process in ranked_processes:
            predicted_cpu, predicted_memory, load_level = self._prediction_cache[process.process_id]
            process.predicted_cpu = predicted_cpu
            process.predicted_memory = predicted_memory

            requested_cpu = max(MIN_CPU_ALLOCATION, min(predicted_cpu, self.total_cpu * 0.5))
            requested_memory = max(MIN_MEMORY_ALLOCATION, min(predicted_memory, self.total_memory * 0.5))

            if requested_cpu <= remaining_cpu and requested_memory <= remaining_memory:
                remaining_cpu -= requested_cpu
                remaining_memory -= requested_memory
                decisions.append(
                    AllocationDecision(
                        process_id=process.process_id,
                        cpu=requested_cpu,
                        memory=requested_memory,
                        accepted=True,
                        reason=f"predicted-{load_level}",
                    )
                )
            else:
                decisions.append(
                    AllocationDecision(
                        process_id=process.process_id,
                        cpu=0.0,
                        memory=0.0,
                        accepted=False,
                        reason="insufficient-predicted-resource",
                    )
                )

        return decisions
