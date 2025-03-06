# Neo4j DB API

A FastAPI-based REST API for interacting with Neo4j database.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Run the application:
```bash
poetry run uvicorn src.app.main:app --reload
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI Schema: http://localhost:8000/api/openapi.json

## Health Check

The health check endpoint is available at:
- http://localhost:8000/health 