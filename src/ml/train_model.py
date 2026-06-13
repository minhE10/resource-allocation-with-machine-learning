from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import RANDOM_SEED
from src.data.preprocessing import prepare_training_data
from src.simulation.process import Process


@dataclass(frozen=True, slots=True)
class TrainingResult:
    cpu_mae: float
    memory_mae: float
    sample_count: int


def build_model() -> Pipeline:
    regressor = RandomForestRegressor(
        n_estimators=180,
        random_state=RANDOM_SEED,
        min_samples_leaf=2,
        n_jobs=-1,
    )
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("regressor", MultiOutputRegressor(regressor)),
        ]
    )


def train_model(processes: list[Process]) -> tuple[Pipeline, TrainingResult]:
    features, targets = prepare_training_data(processes)
    test_size = 0.2 if len(processes) >= 20 else 0.3
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        targets,
        test_size=test_size,
        random_state=RANDOM_SEED,
    )

    model = build_model()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    cpu_mae = mean_absolute_error(y_test["required_cpu"], predictions[:, 0])
    memory_mae = mean_absolute_error(y_test["required_memory"], predictions[:, 1])

    return model, TrainingResult(
        cpu_mae=float(cpu_mae),
        memory_mae=float(memory_mae),
        sample_count=len(processes),
    )


def train_and_save_model(processes: list[Process], model_path: Path) -> TrainingResult:
    model, result = train_model(processes)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return result
