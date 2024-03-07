import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
from flwr.common import NDArrays
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def get_model_parameters(model: LogisticRegression) -> NDArrays:
    """Returns the parameters of a sklearn LogisticRegression model."""
    if model.fit_intercept:
        params = [
            model.coef_,
            model.intercept_,
        ]
    else:
        params = [
            model.coef_,
        ]
    return params


def set_model_params(model: LogisticRegression, params: NDArrays) -> LogisticRegression:
    """Sets the parameters of a sklean LogisticRegression model."""
    model.coef_ = params[0]
    if model.fit_intercept:
        model.intercept_ = params[1]
    return model


def set_initial_params(model: LogisticRegression):
    """Sets initial parameters as zeros Required since model params are uninitialized
    until model.fit is called.

    But server asks for initial parameters from clients at launch. Refer to
    sklearn.linear_model.LogisticRegression documentation for more information.
    """
    n_classes = 3  # has 3 classes
    n_features = 54  # Number of features in dataset
    model.classes_ = np.array([i for i in range(10)])

    model.coef_ = np.zeros((n_classes, n_features))
    if model.fit_intercept:
        model.intercept_ = np.zeros((n_classes,))


NUM_CLIENTS = 3


def load_dataset_for_client(client_id: int, dataset_path: str):
    df = pd.read_csv(dataset_path)
    X = df.drop("Credit_Score", axis=1)
    y = df["Credit_Score"]

    # Ensure even dataset splitting
    np.random.seed(42)
    if len(X) % NUM_CLIENTS != 0:
        drop_indices = np.random.choice(X.index, (len(X) % NUM_CLIENTS), replace=False)
        X = X.drop(drop_indices)
        y = y.drop(drop_indices)

    # Split for clients
    X_splits = np.split(X, NUM_CLIENTS)
    y_splits = np.split(y, NUM_CLIENTS)

    # Train/test split for the selected client
    X_train, X_test, y_train, y_test = train_test_split(
        X_splits[client_id], y_splits[client_id], train_size=0.8, random_state=42
    )

    return X_train, X_test, y_train, y_test


def load_dataset(dataset_path: str):
    df = pd.read_csv(dataset_path)

    X = df.drop("Credit_Score", axis=1)
    y = df["Credit_Score"]

    return X, y


def scale_data(X_train, X_test):
    """Scales the data using StandardScaler."""
    scaler = StandardScaler()
    features = X_train.columns
    X_train = scaler.fit_transform(X_train)
    X_train = pd.DataFrame(X_train, columns=features)
    X_test = scaler.transform(X_test)
    X_test = pd.DataFrame(X_test, columns=features)

    return X_train, X_test
