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
