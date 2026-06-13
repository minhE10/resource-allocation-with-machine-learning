from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import DEFAULT_MODEL_PATH
from src.data.data_generator import generate_workload
from src.data.data_loader import load_processes_from_csv, save_workload_csv
from src.ml.predictor import ResourcePredictor
from src.ml.train_model import train_and_save_model
from src.scheduler.baseline_allocator import BaselineAllocator
from src.scheduler.ml_allocator import MLAllocator
from src.simulation.simulator import Simulator
from src.visualization.charts import timeline_to_frame


def _run_allocator(processes, allocator, total_cpu: float, total_memory: float):
    return Simulator(allocator=allocator, total_cpu=total_cpu, total_memory=total_memory).run(processes)


def main() -> None:
    st.set_page_config(page_title="ML Resource Allocation", layout="wide")
    st.title("Resource Allocation with Machine Learning")

    with st.sidebar:
        process_count = st.slider("Generated processes", 20, 300, 120, 10)
        total_cpu = st.slider("Total CPU capacity", 20.0, 200.0, 100.0, 5.0)
        total_memory = st.slider("Total memory MB", 1024.0, 32768.0, 16384.0, 512.0)
        run_button = st.button("Run simulation", type="primary")

    if run_button:
        data_path = Path("data/sample/dashboard_workload.csv")
        processes = generate_workload(process_count)
        save_workload_csv(processes, data_path)
        train_and_save_model(processes, DEFAULT_MODEL_PATH)
        loaded_processes = load_processes_from_csv(data_path)
        predictor = ResourcePredictor.load(DEFAULT_MODEL_PATH)

        baseline = _run_allocator(
            loaded_processes,
            BaselineAllocator(total_cpu=total_cpu, total_memory=total_memory),
            total_cpu,
            total_memory,
        )
        ml_result = _run_allocator(
            loaded_processes,
            MLAllocator(total_cpu=total_cpu, total_memory=total_memory, predictor=predictor),
            total_cpu,
            total_memory,
        )

        metrics_frame = pd.DataFrame(
            [
                {"allocator": "Baseline", **baseline.metrics.to_dict()},
                {"allocator": "ML", **ml_result.metrics.to_dict()},
            ]
        )

        st.subheader("Metrics")
        st.dataframe(metrics_frame, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Baseline Timeline")
            st.line_chart(timeline_to_frame(baseline.timeline), x="time_tick", y=["used_cpu", "used_memory"])
        with col2:
            st.subheader("ML Timeline")
            st.line_chart(timeline_to_frame(ml_result.timeline), x="time_tick", y=["used_cpu", "used_memory"])

        st.subheader("Workload")
        st.dataframe(pd.DataFrame([process.to_record() for process in loaded_processes]), use_container_width=True)


if __name__ == "__main__":
    main()
