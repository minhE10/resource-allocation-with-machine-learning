# Algorithms

## Baseline Allocator

The baseline allocator is a priority-based resource allocator. At each
simulation tick, waiting processes are sorted by:

1. Priority
2. Arrival time
3. Process ID

The allocator grants each process a bounded amount of its declared CPU and
memory demand if enough resources are available. Otherwise, the process remains
in the waiting queue.

## ML-Based Allocator

The ML allocator uses a `RandomForestRegressor` wrapped in
`MultiOutputRegressor` to predict two outputs:

- Required CPU
- Required memory

Input features:

- Arrival time
- Burst time
- Priority
- Process type code
- Average CPU usage
- Peak CPU usage
- Average memory usage
- Peak memory usage
- I/O usage

At each simulation tick, the allocator predicts resource demand for every
waiting process, ranks processes by priority and waiting time, then grants CPU
and memory if the predicted demand fits in the remaining capacity.

## Comparison Metrics

- Average CPU utilization
- Average memory utilization
- Average waiting time
- Average turnaround time
- Throughput
- Delayed processes
- Completed processes
