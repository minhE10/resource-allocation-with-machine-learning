from src.data.data_generator import generate_workload
from src.ml.train_model import train_model


def test_train_model_returns_metrics():
    processes = generate_workload(40)
    model, result = train_model(processes)

    assert model is not None
    assert result.sample_count == 40
    assert result.cpu_mae >= 0
    assert result.memory_mae >= 0
