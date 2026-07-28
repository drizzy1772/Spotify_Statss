# Spotify Tracker API

Production-ready asynchronous REST API and data pipeline for tracking, saving, and analyzing Spotify listening history in real-time.

### Stack
* FastAPI
* Apache Kafka (KRaft)
* PostgreSQL
* Redis
* Celery
* SQLAlchemy 2.0 (asyncpg)
* Docker Compose
* Pytest

### Key Features
✅ **Real-time Event Streaming:** Asynchronous Kafka producer and consumer for processing Spotify tracks.
✅ **Robust Data Persistence:** `UPSERT` logic (ON CONFLICT DO UPDATE) handling track metadata in PostgreSQL.
✅ **Background Processing:** Celery integration for asynchronous tasks and scheduled Spotify API polling.
✅ **High Performance:** Redis caching for fast GET requests and analytics retrieval.
✅ **Rate Limiting:** Custom dependency-injected rate limits using Redis.
✅ **Test Coverage:** Comprehensive async testing suite using `pytest` and `unittest.mock.AsyncMock`.
✅ **Fully Dockerized:** Isolated containers for Web, Kafka, Postgres, Redis, and Celery with hot-reload volumes.

### API Scheme
```mermaid
graph LR
    A[Spotify API] -->|Fetch Tracks| B(FastAPI / Celery)
    B -->|Produce Event| C{Kafka Topic: spotify_tracks}
    C -->|Consume Event| D[Async Consumer]
    D -->|Upsert Data| E[(PostgreSQL)]
    F[Client] -->|Request Stats| B
    B -->|Cache / Rate Limit| G[(Redis)]
