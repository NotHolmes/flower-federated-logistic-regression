import flwr as fl
import utils
from sklearn.metrics import log_loss
from sklearn.linear_model import LogisticRegression
from typing import Dict
from joblib import dump


def fit_round(server_round: int) -> Dict:
    """Send round number to client."""
    return {"server_round": server_round}


def get_evaluate_fn(model: LogisticRegression):
    """Return an evaluation function for server-side evaluation."""

    X_test, y_test = utils.load_dataset("dataset/validation.csv")
    X_test, _ = utils.scale_data(X_test, X_test)

    # The `evaluate` function will be called after every round
    def evaluate(server_round, parameters: fl.common.NDArrays, config):
        # Update model with the latest parameters
        utils.set_model_params(model, parameters)
        loss = log_loss(y_test, model.predict_proba(X_test.values))
        accuracy = model.score(X_test.values, y_test)
        return loss, {"accuracy": accuracy}

    return evaluate


# Start Flower server for five rounds of federated learning
if __name__ == "__main__":
    model = LogisticRegression(random_state=42)
    utils.set_initial_params(model)
    strategy = fl.server.strategy.FedMedian(
        min_available_clients=3,
        evaluate_fn=get_evaluate_fn(model),
        on_fit_config_fn=fit_round,
    )
    fl.common.logger.configure(identifier="FedMedian Server", filename="fedmedian_log.txt")
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        strategy=strategy,
        config=fl.server.ServerConfig(num_rounds=100),
    )
    dump(model, "model/model_fedmedian.joblib")
