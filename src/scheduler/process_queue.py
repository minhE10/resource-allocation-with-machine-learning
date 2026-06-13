from __future__ import annotations

from src.simulation.process import Process


class ProcessQueue:
    def __init__(self) -> None:
        self._items: list[Process] = []

    def add_arrivals(self, processes: list[Process], time_tick: int) -> None:
        self._items.extend(process for process in processes if process.arrival_time == time_tick)
        self._items.sort(key=lambda process: (process.priority, process.arrival_time, process.process_id))

    def remove(self, process: Process) -> None:
        self._items.remove(process)

    def increment_waiting_time(self) -> None:
        for process in self._items:
            process.waiting_time += 1

    def as_list(self) -> list[Process]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)
