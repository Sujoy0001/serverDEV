# Server

This project runs a FastAPI application behind nginx using Docker Compose.

## Run locally

```bash
docker compose up --build
```

Then open:

- http://localhost/
- http://localhost/docs

## Services

- FastAPI app: http://app:8000 inside Docker
- nginx: http://localhost/ from the host
