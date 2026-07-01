# W9D2 Model Serving

## Overview

This project implements a minimal machine learning model serving system using FastAPI. It provides:

* REST API for online inference
* Batch inference using CSV files
* Prometheus metrics for monitoring
* Docker support for containerized deployment

---

# Setup Instructions

## Prerequisites

* Python 3.11.9
* pip
* Docker Desktop (optional, for Part 3)

## Create and Activate a Virtual Environment

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application Locally

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Usage Examples

## Health Check

### Request

```bash
curl http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "ok"
}
```

---

## Predict

### Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
-H "Content-Type: application/json" ^
-d "{\"x1\":1.5,\"x2\":2.3}"
```

### Request Body

```json
{
  "x1": 1.5,
  "x2": 2.3
}
```

### Example Response

```json
{
  "score": 0.85,
  "model_version": "v1.0"
}
```

> **Note:** The score may vary depending on the trained Logistic Regression model.

---

## Metrics

### Request

```bash
curl http://127.0.0.1:8000/metrics
```

### Example Response

```text
prediction_requests_total 5
prediction_latency_seconds_count 5
prediction_latency_seconds_sum 0.004
```

---

# Batch Inference Usage

Run the batch inference script:

```bash
python batch_infer.py data/input.csv data/predictions.csv
```

## Input Format

The input CSV must contain the following columns:

```csv
x1,x2
1.5,2.3
0.2,0.8
2.1,1.7
3.0,3.2
```

## Output Format

The output CSV contains the original data with an additional prediction column.

Example:

```csv
x1,x2,prediction
1.5,2.3,0.85
0.2,0.8,0.13
2.1,1.7,0.91
3.0,3.2,0.99
```

The script also prints processing statistics, including:

* Number of rows processed
* Processing time
* Output file location

---

# Docker Instructions

## Build the Docker Image

```bash
docker build -t w9d2-model-serving .
```

## Run the Container

```bash
docker run -p 8000:8000 w9d2-model-serving
```

The API will be available at:

```
http://127.0.0.1:8000
```

## Test the Containerized Application

Health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Prediction endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
-H "Content-Type: application/json" ^
-d "{\"x1\":1.5,\"x2\":2.3}"
```

Metrics endpoint:

```bash
curl http://127.0.0.1:8000/metrics
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```
