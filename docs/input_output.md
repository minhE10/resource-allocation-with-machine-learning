# Input and Output

## Input CSV

The program expects a workload CSV with these columns:

```text
process_id
arrival_time
burst_time
priority
process_type
cpu_usage_avg
cpu_usage_peak
memory_usage_avg
memory_usage_peak
io_usage
required_cpu
required_memory
```

`required_cpu` and `required_memory` are used as target labels during model
training. During simulation, the baseline allocator uses them directly while
the ML allocator uses predicted values.

## Output

The CLI prints allocator metrics to the terminal and saves charts to
`reports/figures/`:

```text
baseline_resource_usage.png
ml_resource_usage.png
allocator_comparison.png
```

The Streamlit dashboard displays:

- Generated workload table
- Baseline metrics
- ML allocator metrics
- CPU and memory usage over time
