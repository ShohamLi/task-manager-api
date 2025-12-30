# Task Manager API (FastAPI + SQLite)

A simple REST API for managing tasks, built with FastAPI and persisted with SQLite.

## Features
- CRUD endpoints for tasks
- SQLite persistence (`tasks.db`)
- Automatic Swagger docs at `/docs`

## Tech Stack
- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Run locally
```bash
# create & activate venv (example)
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --reload
