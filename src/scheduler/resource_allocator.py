from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.simulation.process import Process


@dataclass(frozen=True, slots=True)
class AllocationDecision:
    process_id: int
    cpu: float
    memory: float
    accepted: bool
    reason: str


class ResourceAllocator(ABC):
    def __init__(self, total_cpu: float, total_memory: float) -> None:
        self.total_cpu = total_cpu
        self.total_memory = total_memory

    @abstractmethod
    def allocate(
        self,
        waiting_processes: list[Process],
        available_cpu: float,
        available_memory: float,
    ) -> list[AllocationDecision]:
        """Return allocation decisions for the current simulation tick."""
