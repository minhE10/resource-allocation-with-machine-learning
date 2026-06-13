from __future__ import annotations

from dataclasses import dataclass

from sklearn.metrics import mean_absolute_error, r2_score


@dataclass(frozen=True, slots=True)
class RegressionReport:
    cpu_mae: float
    memory_mae: float
    cpu_r2: float
    memory_r2: float

    def to_text(self) -> str:
        return (
            f"CPU MAE: {self.cpu_mae:.2f}\n"
            f"Memory MAE: {self.memory_mae:.2f} MB\n"
            f"CPU R2: {self.cpu_r2:.3f}\n"
            f"Memory R2: {self.memory_r2:.3f}"
        )


def evaluate_regression(y_true, y_pred) -> RegressionReport:
    return RegressionReport(
        cpu_mae=float(mean_absolute_error(y_true["required_cpu"], y_pred[:, 0])),
        memory_mae=float(mean_absolute_error(y_true["required_memory"], y_pred[:, 1])),
        cpu_r2=float(r2_score(y_true["required_cpu"], y_pred[:, 0])),
        memory_r2=float(r2_score(y_true["required_memory"], y_pred[:, 1])),
    )
