from __future__ import annotations

from dataclasses import dataclass, field

from src.config import PROCESS_TYPES


@dataclass(slots=True)
class Process:
    process_id: int
    arrival_time: int
    burst_time: int
    priority: int
    process_type: str
    cpu_usage_avg: float
    cpu_usage_peak: float
    memory_usage_avg: float
    memory_usage_peak: float
    io_usage: float
    required_cpu: float
    required_memory: float
    remaining_time: int | None = None
    start_time: int | None = None
    finish_time: int | None = None
    allocated_cpu: float = 0.0
    allocated_memory: float = 0.0
    waiting_time: int = 0
    predicted_cpu: float | None = None
    predicted_memory: float | None = None
    metadata: dict[str, float | str | int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.remaining_time is None:
            self.remaining_time = self.burst_time
        if self.process_type not in PROCESS_TYPES:
            raise ValueError(f"Unknown process type: {self.process_type}")

    @property
    def process_type_code(self) -> int:
        return PROCESS_TYPES[self.process_type]

    @property
    def is_finished(self) -> bool:
        return self.remaining_time is not None and self.remaining_time <= 0

    def clone(self) -> "Process":
        return Process(
            process_id=self.process_id,
            arrival_time=self.arrival_time,
            burst_time=self.burst_time,
            priority=self.priority,
            process_type=self.process_type,
            cpu_usage_avg=self.cpu_usage_avg,
            cpu_usage_peak=self.cpu_usage_peak,
            memory_usage_avg=self.memory_usage_avg,
            memory_usage_peak=self.memory_usage_peak,
            io_usage=self.io_usage,
            required_cpu=self.required_cpu,
            required_memory=self.required_memory,
            remaining_time=self.burst_time,
            metadata=dict(self.metadata),
        )

    def to_record(self) -> dict[str, float | int | str]:
        return {
            "process_id": self.process_id,
            "arrival_time": self.arrival_time,
            "burst_time": self.burst_time,
            "priority": self.priority,
            "process_type": self.process_type,
            "process_type_code": self.process_type_code,
            "cpu_usage_avg": self.cpu_usage_avg,
            "cpu_usage_peak": self.cpu_usage_peak,
            "memory_usage_avg": self.memory_usage_avg,
            "memory_usage_peak": self.memory_usage_peak,
            "io_usage": self.io_usage,
            "required_cpu": self.required_cpu,
            "required_memory": self.required_memory,
        }
