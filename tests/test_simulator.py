from src.data.data_generator import generate_workload
from src.scheduler.baseline_allocator import BaselineAllocator
from src.simulation.simulator import Simulator


def test_simulator_completes_generated_workload():
    processes = generate_workload(20)
    simulator = Simulator(
        allocator=BaselineAllocator(total_cpu=100, total_memory=8192),
        total_cpu=100,
        total_memory=8192,
    )

    result = simulator.run(processes)

    assert result.metrics.completed_processes == 20
    assert result.metrics.total_time > 0
    assert len(result.timeline) > 0
