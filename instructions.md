# W9D2-rlin1214
for homework

Assignment Submission Guidelines

Follow these instructions

After-Class Assignment: Model Serving with REST API and Batch Inference

Estimated Time: 1 hour

Overview
Build a minimal model serving system that demonstrates both online (REST API) and batch inference capabilities with basic monitoring.

What You'll Build
A FastAPI application that serves predictions via REST endpoint
A batch inference script that processes CSV files
Prometheus metrics for monitoring
A Docker container to package everything
Requirements
Part 1: REST API (25 minutes)
Create a FastAPI application with the following endpoints:

Required Endpoints:

GET /health - Returns {"status": "ok"}
POST /predict - Accepts input features and returns prediction
GET /metrics - Exposes Prometheus metrics
Predict Endpoint Specification:

Input (JSON):

{
  "x1": 1.5,
  "x2": 2.3
}
Output (JSON):

{
  "score": 0.85,
  "model_version": "v1.0"
}
Implementation Notes:

Use Pydantic for request/response validation
Load your W9D1 baseline model (or create a simple LogisticRegression if needed)
Track request count and latency using Prometheus Counter and Histogram
Part 2: Batch Inference (20 minutes)
Create batch_infer.py that:

Reads an input CSV file with feature columns
Loads your trained model
Generates predictions for all rows
Writes output CSV with original data plus a prediction column
Prints processing statistics (rows processed, time taken)
Usage:

python batch_infer.py data/input.csv data/predictions.csv
Part 3: Docker Packaging (15 minutes)
Create a Dockerfile that:

Uses python:3.11-slim as base image
Installs dependencies from requirements.txt
Copies application code
Exposes port 8000
Runs Uvicorn server
Build and run commands should work:

docker build -t model-server:v1 .
docker run -p 8000:8000 model-server:v1
Deliverables
Submit a GitHub repository containing:

your-repo/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── metrics.py       # Prometheus instrumentation (optional separate file)
├── data/
│   ├── input.csv        # Sample input (5-10 rows minimum)
│   └── predictions.csv  # Sample output from batch script
├── models/
│   └── baseline.joblib  # Your trained model (or training script)
├── batch_infer.py       # Batch inference script
├── requirements.txt     # All dependencies
├── Dockerfile
├── README.md           # Setup and usage instructions
└── screenshots/
    └── metrics.png      # Screenshot of /metrics endpoint response
README Requirements
Your README.md must include:

Setup Instructions

How to install dependencies
How to run the application locally
API Usage Examples

Example curl commands for each endpoint
Expected responses
Batch Inference Usage

Command to run batch script
Input/output format description
Docker Instructions

Build command
Run command
How to test the containerized app
Testing Your Work
Before submission, verify:

[ ] uvicorn app.main:app --reload starts without errors
[ ] curl http://localhost:8000/health returns 200
[ ] curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"x1":1.0,"x2":2.0}' returns valid prediction
[ ] curl http://localhost:8000/metrics shows prometheus metrics
[ ] python batch_infer.py data/input.csv data/predictions.csv creates output file
[ ] Docker container builds and runs successfully
[ ] All endpoints accessible from container on http://localhost:8000
Grading Rubric (10 points)
Component	Points	Criteria
REST API	3	/predict endpoint works with proper schema, returns score and version
Batch Inference	3	Script successfully processes CSV and generates predictions
Monitoring	2	/metrics endpoint exposes Counter and Histogram metrics
Docker	1	Container builds and runs, app accessible on port 8000
Documentation	1	README includes clear setup and usage instructions
Hints
Start with the in-class examples and modify them incrementally
Test each endpoint individually before moving to the next part
Use joblib.dump() and joblib.load() for model persistence
Keep your model simple - a LogisticRegression on 2 features is sufficient
If you get stuck on Docker, ensure the app works locally first
Common Issues
Port already in use: Change to a different port like 8001
Module not found: Check that app/__init__.py exists
Docker connection refused: Use --host 0.0.0.0 in CMD, not 127.0.0.1
Metrics not showing: Import prometheus_client and call counter.inc() before returning