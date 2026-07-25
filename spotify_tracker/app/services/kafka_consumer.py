


import asyncio
import os
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import sqlalchemy
from app.database import AsyncSessionLocal
from app.models import SpotifyTrack


KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")

TOPIC_NAME = "spotify_tracks"

async def save_track_to_db(session, track_data: dict):
    columns = ", ".join(track_data.keys())
    placeholders = ", ".join([":" + k for k in track_data.keys()])