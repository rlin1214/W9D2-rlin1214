from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

import joblib
import numpy as np
import os
import time

from sklearn.linear_model import LogisticRegression

app = FastAPI(title="Model Serving API")

MODEL_PATH = "app/model.pkl"


# -------------------------------------------------
# Load existing model or create one
# -------------------------------------------------
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [2, 2],
        [2, 1],
        [3, 2],
        [3, 3],
    ])

    y = np.array([
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
    ])

    model = LogisticRegression()

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return model


model = load_model()


# -------------------------------------------------
# Metrics
# -------------------------------------------------

REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

REQUEST_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction latency"
)


# -------------------------------------------------
# Pydantic Models
# -------------------------------------------------

class PredictionRequest(BaseModel):
    x1: float
    x2: float


class PredictionResponse(BaseModel):
    score: float
    model_version: str


# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    REQUEST_COUNT.inc()

    start = time.time()

    features = np.array([[request.x1, request.x2]])

    probability = model.predict_proba(features)[0][1]

    REQUEST_LATENCY.observe(time.time() - start)

    return PredictionResponse(
        score=round(float(probability), 2),
        model_version="v1.0"
    )


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )