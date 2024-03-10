import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import utils
from joblib import load
import numpy as np
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 30)
plt.style.use('ggplot')

def generate_report(y_test, y_pred, title):
    acc_score = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average=None)
    precision = precision_score(y_test, y_pred, average=None)
    recall = recall_score(y_test, y_pred, average=None)

    print(f"{title}")
    print(f"Accuracy: {acc_score:.2%}\n\
    F1 Score: {dict(zip([0, 1, 2], map(lambda x: f'{x:.2%}', f1)))}\n\
    Precision Score: {dict(zip([0, 1, 2], map(lambda x: f'{x:.2%}', precision)))}\n\
    Recall Score: {dict(zip([0, 1, 2], map(lambda x: f'{x:.2%}', recall)))}\n\
    ")

def main(model_type):
    X_test, y_test = utils.load_dataset("dataset/test.csv")
    X_test, _ = utils.scale_data(X_test, X_test)

    if model_type == "avg":
        model = load('model/model_fedavg.joblib')
    elif model_type == "trim":
        model = load('model/model_fedtrimmedavg.joblib')
    elif model_type == "krum":
        model = load('model/model_krum.joblib')
    else:
        print("Invalid model type.")
        return

    y_pred = model.predict(X_test)
    generate_report(y_test, y_pred, model_type.capitalize())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Specify the model type: avg, trim, or krum")
    args = parser.parse_args()

    if args.model:
        main(args.model)
    else:
        main("avg")