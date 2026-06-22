#!/usr/bin/env python3
import mlflow
from sklearn.ensemble import RandomForestClassifier

def train_model(X_train, y_train):
    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        mlflow.sklearn.log_model(model, "model")
        return model
