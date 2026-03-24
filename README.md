# testKS

This repository contains a small FastAPI microservice prepared for Docker and Kubernetes, along with a couple of standalone Python practice scripts.

## Project Overview

The main application is a FastAPI service in [app/main.py](/c:/Abhishek/Learning/testKS/testKS/app/main.py). It exposes a single root endpoint:

- `GET /` returns `{"message": "Hello from Kubernetes Microservice"}`

The repo also includes:

- [Dockerfile](/c:/Abhishek/Learning/testKS/testKS/Dockerfile) to containerize the FastAPI app
- Kubernetes manifests in [k8s/deployment.yaml](/c:/Abhishek/Learning/testKS/testKS/k8s/deployment.yaml) and [k8s/service.yaml](/c:/Abhishek/Learning/testKS/testKS/k8s/service.yaml)
- [basic_ML.py](/c:/Abhishek/Learning/testKS/testKS/basic_ML.py), a beginner-friendly linear regression example
- [test.py](/c:/Abhishek/Learning/testKS/testKS/test.py), an Azure Durable Functions practice script

## Repository Structure

```text
testKS/
├── app/
│   ├── main.py
│   └── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── Dockerfile
├── basic_ML.py
├── req.txt
└── test.py
```

## Requirements

For the FastAPI app:

- Python 3.11 or later recommended
- Packages listed in [app/requirements.txt](/c:/Abhishek/Learning/testKS/testKS/app/requirements.txt):
  - `fastapi`
  - `uvicorn`

For the ML example:

- Packages listed in [req.txt](/c:/Abhishek/Learning/testKS/testKS/req.txt):
  - `numpy`
  - `pandas`
  - `scikit-learn`

## Run the FastAPI App Locally

Install the app dependencies:

```powershell
pip install -r app\requirements.txt
```

Start the API server:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open:

- `http://localhost:8000/`
- `http://localhost:8000/docs`

## Run with Docker

Build the image:

```powershell
docker build -t fastapi-microservice .
```

Run the container:

```powershell
docker run -p 8000:8000 fastapi-microservice
```

## Deploy to Kubernetes

Apply the manifests:

```powershell
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check resources:

```powershell
kubectl get pods
kubectl get services
```

Notes:

- The deployment uses 2 replicas
- The container listens on port `8000`
- The service is exposed as `NodePort`
- The image in the manifest is `fastapi-microservice` with `imagePullPolicy: Never`, which is suitable for local cluster setups such as Minikube or Docker Desktop Kubernetes after building the image locally

## Standalone Scripts

### `basic_ML.py`

This script demonstrates a simple machine learning workflow using linear regression:

- creates a sample dataset
- splits data into training and testing sets
- trains a model
- evaluates it with mean squared error
- accepts user input for salary prediction

Run it after installing the ML dependencies:

```powershell
pip install -r req.txt
python basic_ML.py
```

### `test.py`

This file contains Azure Functions Durable Functions sample code for orchestration/activity patterns. It appears to be a practice or experimental script and is not connected to the FastAPI app, Dockerfile, or Kubernetes manifests in this repository.

## Current Focus of the Project

At present, the most complete part of this repository is the FastAPI microservice and its container/Kubernetes setup. The ML and Azure Functions files look like separate learning examples kept in the same repo.
