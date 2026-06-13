from __future__ import annotations

import pandas as pd

from src.config import FEATURE_COLUMNS, PROCESS_TYPES, TARGET_COLUMNS
from src.simulation.process import Process


def processes_to_frame(processes: list[Process]) -> pd.DataFrame:
    return pd.DataFrame([process.to_record() for process in processes])


def prepare_feature_frame(processes: list[Process]) -> pd.DataFrame:
    frame = processes_to_frame(processes)
    if "process_type_code" not in frame.columns:
        frame["process_type_code"] = frame["process_type"].map(PROCESS_TYPES)
    return frame[FEATURE_COLUMNS]


def prepare_training_data(processes: list[Process]) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = processes_to_frame(processes)
    frame["process_type_code"] = frame["process_type"].map(PROCESS_TYPES)
    return frame[FEATURE_COLUMNS], frame[TARGET_COLUMNS]
