from __future__ import annotations

import random

import numpy as np

from src.config import PROCESS_TYPES, RANDOM_SEED
from src.simulation.process import Process


def _bounded(value: float, lower: float, upper: float) -> float:
    return round(max(lower, min(upper, value)), 2)


def generate_workload(process_count: int = 120, seed: int = RANDOM_SEED) -> list[Process]:
    random.seed(seed)
    np.random.seed(seed)

    processes: list[Process] = []
    process_types = list(PROCESS_TYPES.keys())

    for process_id in range(1, process_count + 1):
        process_type = random.choices(
            process_types,
            weights=[0.25, 0.30, 0.20, 0.25],
            k=1,
        )[0]
        arrival_time = int(np.random.poisson(lam=process_id / 4))
        burst_time = int(np.random.randint(2, 16))
        priority = int(np.random.randint(1, 6))

        if process_type == "cpu_bound":
            cpu_avg = np.random.normal(55, 12)
            memory_avg = np.random.normal(850, 250)
            io_usage = np.random.normal(20, 8)
        elif process_type == "io_bound":
            cpu_avg = np.random.normal(24, 8)
            memory_avg = np.random.normal(650, 180)
            io_usage = np.random.normal(72, 12)
        elif process_type == "interactive":
            cpu_avg = np.random.normal(34, 10)
            memory_avg = np.random.normal(1_100, 260)
            io_usage = np.random.normal(46, 15)
        else:
            cpu_avg = np.random.normal(42, 14)
            memory_avg = np.random.normal(1_600, 420)
            io_usage = np.random.normal(34, 12)

        cpu_usage_avg = _bounded(cpu_avg, 4, 90)
        cpu_usage_peak = _bounded(cpu_usage_avg + np.random.normal(14, 8), cpu_usage_avg, 100)
        memory_usage_avg = _bounded(memory_avg, 128, 6_144)
        memory_usage_peak = _bounded(memory_usage_avg + np.random.normal(380, 180), memory_usage_avg, 8_192)
        io_usage = _bounded(io_usage, 0, 100)

        urgency_factor = 1 + (6 - priority) * 0.025
        required_cpu = _bounded((0.45 * cpu_usage_avg + 0.55 * cpu_usage_peak) * urgency_factor, 1, 100)
        required_memory = _bounded(0.35 * memory_usage_avg + 0.65 * memory_usage_peak, 64, 8_192)

        processes.append(
            Process(
                process_id=process_id,
                arrival_time=arrival_time,
                burst_time=burst_time,
                priority=priority,
                process_type=process_type,
                cpu_usage_avg=cpu_usage_avg,
                cpu_usage_peak=cpu_usage_peak,
                memory_usage_avg=memory_usage_avg,
                memory_usage_peak=memory_usage_peak,
                io_usage=io_usage,
                required_cpu=required_cpu,
                required_memory=required_memory,
            )
        )

    return sorted(processes, key=lambda process: (process.arrival_time, process.priority, process.process_id))
