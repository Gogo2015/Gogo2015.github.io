---
layout: default
title: Earthquake Analysis Web App
---

# Earthquake Analysis Web App  
**Repository:** [EarthquakeAnalyzer](https://github.com/Gogo2015/EarthquakeAnalyzer)

## Project Overview  
A containerized Flask API for ingesting, querying, and analyzing real-time earthquake data from the USGS. The system stores earthquake records in Redis, exposes a RESTful API with filtering and search capabilities, and processes analysis jobs asynchronously through a Redis-backed worker queue. The full stack is deployed to Kubernetes with separate test and production environments.

## My Contributions
- Designed and implemented the **Flask REST API** with 12 endpoints covering CRUD operations, parameterized filtering (by place, magnitude range, date range), and asynchronous job management.
- Built a **multi-database Redis architecture** using 4 separate Redis databases: raw earthquake data (DB 0), job queue (DB 1), job metadata (DB 2), and analysis results with generated images (DB 3).
- Implemented an **asynchronous job processing system** using HotQueue: the API enqueues jobs, a background worker dequeues and processes them, generates matplotlib visualizations, and stores both structured results and PNG images back in Redis.
- Developed two analysis pipelines:
  - **Magnitude binning**: Groups earthquakes into magnitude bins and generates distribution bar charts.
  - **Hemisphere analysis**: Categorizes earthquakes by geographic quadrant with per-hemisphere statistics (count, average magnitude, max magnitude) and visualization.
- Wrote **integration and unit tests** covering API endpoints, job lifecycle, and worker logic.
- Created full **Kubernetes deployment manifests** for both test and production environments: Flask, Redis, and Worker deployments, ClusterIP and NodePort services, PersistentVolumeClaims for Redis data, and Ingress configuration for external access.
- Containerized the application with **Docker and Docker Compose** for local development with multi-service orchestration.

## System Architecture

The application runs as three coordinated services:

- **Flask API** — Handles HTTP requests, manages data in Redis, creates and tracks jobs
- **Redis** — Serves as both the primary data store (earthquake records) and the message broker (job queue + results)
- **Worker** — Consumes jobs from the queue, runs analysis, generates charts, and writes results back to Redis

Jobs follow a lifecycle: `submitted → in progress → complete/error`, with status queryable at any point through the API.

## Key Design Decisions
- **4 separate Redis databases** isolate concerns (data, queue, jobs, results) without needing multiple Redis instances — keeping the deployment simple while maintaining logical separation.
- **HotQueue for job processing** provides a lightweight alternative to Celery, appropriate for the scale of this application while still decoupling API response times from analysis compute.
- **Separate test and production Kubernetes manifests** enable CI-style validation: the test deployment runs pytest on startup before promoting to production.
- **Image storage in Redis** (via `hset` with binary data) keeps the architecture stateless — no shared filesystem needed between API and worker containers.

## Tech Stack
- Python, Flask, Redis (multi-DB)
- HotQueue (async job queue)
- matplotlib (server-side visualization)
- Docker, Docker Compose
- Kubernetes (Deployments, Services, Ingress, PVC)
- pytest (integration + unit tests)
- USGS Earthquake API (GeoJSON)

---

**Link:** [GitHub Repository](https://github.com/Gogo2015/EarthquakeAnalyzer)
