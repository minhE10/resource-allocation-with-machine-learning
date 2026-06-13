from src.scheduler.baseline_allocator import BaselineAllocator
from src.simulation.process import Process


def test_baseline_allocator_accepts_process_when_resources_fit():
    process = Process(
        process_id=1,
        arrival_time=0,
        burst_time=4,
        priority=1,
        process_type="cpu_bound",
        cpu_usage_avg=30,
        cpu_usage_peak=50,
        memory_usage_avg=512,
        memory_usage_peak=1024,
        io_usage=10,
        required_cpu=40,
        required_memory=1024,
    )

    allocator = BaselineAllocator(total_cpu=100, total_memory=4096)
    decisions = allocator.allocate([process], available_cpu=100, available_memory=4096)

    assert decisions[0].accepted is True
    assert decisions[0].cpu > 0
    assert decisions[0].memory > 0
