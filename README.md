# Spotify Tracker API
Production-ready asynchronous REST API for tracking, saving, and analyzing Spotify listening history in real-time.

## Stack
* FastAPI
* PostgreSQL
* Redis
* Apache Kafka
* Celery
* SQLAlchemy 2.0
* Docker Compose

## Key Features
✅ Asynchronous Kafka consumer and producer for processing Spotify tracks

✅ Data persistence with UPSERT logic in PostgreSQL

✅ Background task processing and scheduling with Celery

✅ Rate limiting on critical endpoints

✅ Redis caching for GET requests

✅ Global error handling

✅ Test coverage (pytest)

✅ Fully containerized infrastructure

## API Scheme
*(Здесь позже сможешь добавить ссылку на картинку со схемой)*

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /analytics/tracks/{track_id}/stats | Get detailed analytics for a track |
| GET | /analytics/tracks/batch | Fetch statistics for a batch of tracks |
| GET | /users/{user_id}/history | Retrieve user's listening history |
| POST | /sync/trigger | Manually trigger Spotify data sync |

## Quick Start
```bash
Clone the repository**
```bash
git clone [https://github.com/Drizzy1772/spotify-tracker](https://github.com/Drizzy1772/spotify-tracker)
cd spotify-tracker

2. Setup environment variables
Bash

cp .env.example .env

3. Run infrastructure via Docker
Bash

docker compose up -d

4. Install dependencies (for local development)
Bash

pip install -r requirements.txt

5. Apply database migrations
Bash

alembic upgrade head

6. Start Kafka consumer and launch the app
Bash

docker compose exec -d web python -m app.services.kafka_consumer
uvicorn app.main:app --reload
