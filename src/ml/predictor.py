from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from src.data.preprocessing import prepare_feature_frame
from src.simulation.process import Process
from src.utils.constants import LOW_LOAD_THRESHOLD, MEDIUM_LOAD_THRESHOLD


@dataclass(frozen=True, slots=True)
class ResourcePrediction:
    cpu: float
    memory: float
    load_level: str


class ResourcePredictor:
    def __init__(self, model: object) -> None:
        self.model = model

    @classmethod
    def load(cls, model_path: Path) -> "ResourcePredictor":
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        return cls(joblib.load(model_path))

    def predict_one(self, process: Process) -> ResourcePrediction:
        features = prepare_feature_frame([process])
        prediction = self.model.predict(features)[0]
        cpu = max(1.0, float(prediction[0]))
        memory = max(64.0, float(prediction[1]))
        load_ratio = min(1.0, (cpu / 100.0 + memory / 8_192.0) / 2)
        return ResourcePrediction(cpu=cpu, memory=memory, load_level=_load_level(load_ratio))

    def predict_many(self, processes: list[Process]) -> pd.DataFrame:
        features = prepare_feature_frame(processes)
        predictions = self.model.predict(features)
        rows = []
        for process, prediction in zip(processes, predictions, strict=True):
            cpu = max(1.0, float(prediction[0]))
            memory = max(64.0, float(prediction[1]))
            load_ratio = min(1.0, (cpu / 100.0 + memory / 8_192.0) / 2)
            rows.append(
                {
                    "process_id": process.process_id,
                    "predicted_cpu": cpu,
                    "predicted_memory": memory,
                    "load_level": _load_level(load_ratio),
                }
            )
        return pd.DataFrame(rows)


def _load_level(load_ratio: float) -> str:
    if load_ratio < LOW_LOAD_THRESHOLD:
        return "low"
    if load_ratio < MEDIUM_LOAD_THRESHOLD:
        return "medium"
    return "high"
