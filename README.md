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
API Endpoints
Method	Path	Description
GET	/analytics/tracks/{track_id}/stats	Get detailed analytics and cached metadata for a specific track
GET	/analytics/tracks/batch	Fetch statistics for a batch of track IDs
GET	/users/{user_id}/history	Retrieve user's listening history and top tracks
POST	/sync/trigger	Manually trigger Celery task to fetch latest Spotify data
Quick Start
Bash

# Clone the repository
git clone [https://github.com/Drizzy1772/spotify-tracker](https://github.com/Drizzy1772/spotify-tracker)
cd spotify-tracker

# Setup environment variables
cp .env.example .env

# Build and start all services (FastAPI, Kafka, Postgres, Redis, Celery)
docker compose up -d --build

# Run database migrations (or init script)
docker compose exec web alembic upgrade head

# Start the Kafka consumer in the background
docker compose exec -d web python -m app.services.kafka_consumer

Structure of Project
Plaintext

spotify_tracker/
├── app/
│   ├── database.py          # SQLAlchemy engine and session makers
│   ├── models_spoti.py      # Database models
│   ├── routers/             # FastAPI endpoints (analytics, dependencies)
│   └── services/            # Business logic, Kafka consumer/producer, Spotify client
├── tests/                   # Pytest async test suite
├── docker-compose.yml       # Infrastructure orchestration
├── requirements.txt         # Python dependencies
└── .env.example             # Environment template

API Docs

Swagger UI available at: http://localhost:8000/docs
ReDoc available at: http://localhost:8000/redoc
Author

This project is developed by Drizzy1772.
License

This project is licensed under the MIT License.
