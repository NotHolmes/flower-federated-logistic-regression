import argparse
import warnings

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
import pandas as pd
import numpy as np

import flwr as fl
import utils
import requests
import os

if __name__ == "__main__":

    PUBLIC_IP = os.environ.get(
        "PUBLIC_IP"
    )  # run PUBLIC_IP=$(curl -s ifconfig.co) on GCP VM on startup to set the public IP
    N_CLIENTS = 3

    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--client-id",
        type=int,
        choices=range(0, N_CLIENTS),
        required=True,
        help="Specifies the artificial data partition",
    )
    args = parser.parse_args()
    client_id = args.client_id

    X_train, X_test, y_train, y_test = utils.load_dataset_for_client(
        client_id=client_id, dataset_path="dataset/train.csv"
    )
    X_train, X_test = utils.scale_data(X_train, X_test)

    # Print the label distribution
    unique, counts = np.unique(y_train, return_counts=True)
    train_counts = dict(zip(unique, counts))
    print(f"Client {client_id} Label distribution in the training set: {train_counts}")
    unique, counts = np.unique(y_test, return_counts=True)
    test_counts = dict(zip(unique, counts))
    print(f"Client {client_id} Label distribution in the testing set: {test_counts}")

    # Create LogisticRegression Model
    model = LogisticRegression(
        penalty="l2",
        max_iter=1,  # local epoch
        warm_start=True,  # prevent refreshing weights when fitting
    )

    # Setting initial parameters, akin to model.compile for keras models
    utils.set_initial_params(model)

    # Define Flower client
    class FlowerClient(fl.client.NumPyClient):
        def get_parameters(self, config):  # type: ignore
            return utils.get_model_parameters(model)

        def fit(self, parameters, config):  # type: ignore
            utils.set_model_params(model, parameters)
            # Ignore convergence failure due to low local epochs
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model.fit(X_train, y_train)
            print(f"Training finished for round {config['server_round']}")
            return utils.get_model_parameters(model), len(X_train), {}

        def evaluate(self, parameters, config):  # type: ignore
            utils.set_model_params(model, parameters)
            loss = log_loss(y_test, model.predict_proba(X_test))
            accuracy = model.score(X_test, y_test)
            return loss, len(X_test), {"accuracy": accuracy}

    # Start Flower client
    fl.client.start_client(
        server_address="{PUBLIC_IP}:8080", client=FlowerClient().to_client()
    )
