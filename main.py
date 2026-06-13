from __future__ import annotations

import argparse
from pathlib import Path

from src.config import DEFAULT_MODEL_PATH, DEFAULT_SAMPLE_DATA_PATH
from src.data.data_generator import generate_workload
from src.data.data_loader import load_processes_from_csv, save_workload_csv
from src.ml.predictor import ResourcePredictor
from src.ml.train_model import train_and_save_model
from src.scheduler.baseline_allocator import BaselineAllocator
from src.scheduler.ml_allocator import MLAllocator
from src.simulation.simulator import Simulator
from src.visualization.charts import save_comparison_chart, save_resource_usage_chart


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulate OS resource allocation using baseline and ML-based allocators."
    )
    parser.add_argument("--generate-data", action="store_true", help="Generate a sample workload CSV.")
    parser.add_argument("--train", action="store_true", help="Train and save the ML resource predictor.")
    parser.add_argument("--simulate", action="store_true", help="Run baseline and ML simulations.")
    parser.add_argument("--data", type=Path, default=DEFAULT_SAMPLE_DATA_PATH, help="Path to workload CSV.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH, help="Path to saved ML model.")
    parser.add_argument("--processes", type=int, default=120, help="Number of generated processes.")
    parser.add_argument("--cpu", type=float, default=100.0, help="Total CPU capacity.")
    parser.add_argument("--memory", type=float, default=16_384.0, help="Total memory capacity in MB.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/figures"), help="Chart output folder.")
    return parser


def run_generate_data(path: Path, process_count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workload = generate_workload(process_count)
    save_workload_csv(workload, path)
    print(f"Generated {len(workload)} processes at {path}")


def run_train(data_path: Path, model_path: Path) -> None:
    processes = load_processes_from_csv(data_path)
    result = train_and_save_model(processes, model_path)
    print(f"Saved model to {model_path}")
    print(f"CPU MAE: {result.cpu_mae:.2f}")
    print(f"Memory MAE: {result.memory_mae:.2f} MB")


def run_simulation(data_path: Path, model_path: Path, total_cpu: float, total_memory: float, output_dir: Path) -> None:
    processes = load_processes_from_csv(data_path)

    baseline_result = Simulator(
        allocator=BaselineAllocator(total_cpu=total_cpu, total_memory=total_memory),
        total_cpu=total_cpu,
        total_memory=total_memory,
    ).run(processes)

    predictor = ResourcePredictor.load(model_path)
    ml_result = Simulator(
        allocator=MLAllocator(total_cpu=total_cpu, total_memory=total_memory, predictor=predictor),
        total_cpu=total_cpu,
        total_memory=total_memory,
    ).run(processes)

    output_dir.mkdir(parents=True, exist_ok=True)
    save_resource_usage_chart(baseline_result.timeline, output_dir / "baseline_resource_usage.png", "Baseline Allocator")
    save_resource_usage_chart(ml_result.timeline, output_dir / "ml_resource_usage.png", "ML Allocator")
    save_comparison_chart(
        {"Baseline": baseline_result.metrics, "ML": ml_result.metrics},
        output_dir / "allocator_comparison.png",
    )

    print("Baseline metrics:")
    print(baseline_result.metrics.to_text())
    print()
    print("ML metrics:")
    print(ml_result.metrics.to_text())
    print(f"Charts saved to {output_dir}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not any([args.generate_data, args.train, args.simulate]):
        args.generate_data = True
        args.train = True
        args.simulate = True

    if args.generate_data:
        run_generate_data(args.data, args.processes)
    if args.train:
        run_train(args.data, args.model)
    if args.simulate:
        run_simulation(args.data, args.model, args.cpu, args.memory, args.output_dir)


if __name__ == "__main__":
    main()
