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

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /login | Redirects to Spotify authorization page |
| GET | /callback | Handles Spotify OAuth callback, saves tokens |
| POST | /listen/{track_id} | Records a listening event for a track |
| GET | /analytics/tracks/{track_id}/stats | Get analytics for a specific track |
| POST | /test_task | Trigger a test Celery task |

## Project Structure
```bash
spotify_tracker/
├── app/
│ ├── main.py # Routes & app entry point
│ ├── models/ # SQLAlchemy models (SpotifyToken, etc.)
│ ├── database.py # Async DB engine & session
│ ├── redis_client.py # Redis client & token caching
│ ├── spotify_auth.py # Access token retrieval/refresh logic
│ ├── kafka_producer.py # Publishes track events to Kafka
│ ├── kafka_consumer.py # Consumes events, UPSERTs into Postgres
│ └── tasks.py # Celery tasks
├── alembic/
│ ├── versions/
│ └── env.py
├── tests/
├── .github/
│ └── workflows/
│ └── tests.yml
├── .env
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
## Project Structure with IMAGE:
<img width="744" height="448" alt="SpotifyStats" src="https://github.com/user-attachments/assets/10f9e4dc-b847-4b5f-99d2-8d5dfb8c7e7d" />

## Swagger UI Image:
<img width="1363" height="643" alt="spotifystats" src="https://github.com/user-attachments/assets/cbb06451-f40a-4f13-805d-0df28157a002" />


## API Docs

Swagger UI available at: http://localhost:8000/docs

## Testing
```bash
docker compose exec web pytest
```


1. **Clone the repository**
```bash
git clone [https://github.com/Drizzy1772/spotify-tracker](https://github.com/Drizzy1772/spotify-tracker)
cd spotify-tracker
```

2. **Setup environment variables**
```bash

cp .env.example .env
```


3. **Run infrastructure via Docker**
```bash

docker compose up -d
```


4. **Install dependencies (for local development)**

```bash
pip install -r requirements.txt
```

5. **Apply database migrations**
```bash

alembic upgrade head
```

6. **Start Kafka consumer and launch the app**
```bash
docker compose exec -d web python -m app.services.kafka_consumer
uvicorn app.main:app --reload
```
**Edit .env**
```bash
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback

POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=your-password
POSTGRES_DB=spotify_tracker

REDIS_HOST=redis
REDIS_PORT=6379

KAFKA_BROKER_URL=kafka:9092
```
## Author

This project is developed by Drizzy1772.

## License

This project is licensed under MIT License.
