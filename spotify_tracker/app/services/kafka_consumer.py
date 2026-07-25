


import asyncio
import os
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from sqlalchemy.dialects.postgresql import insert
from app.database import async_session
from app.models_spoti import SpotifyTrack
import json


KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")

TOPIC_NAME = "spotify_tracks"

async def save_track_to_db(session, track_data: dict):
    
    track_id = track_data.get("id") or track_data.get("spotify_id")
    
    if not track_id:
        raise ValueError("Message doesnt have an ID track. Send me a data")
    
    
    stmt = insert(SpotifyTrack).values(
        spotify_id=track_id,
        name=track_data.get('name', "Unknown Name"),
        artist=track_data.get('artist', "Unknown Artist"),
        album=track_data.get('album', 'Unknown Album'),
        duration_ms=track_data.get("duration_ms", 0)
    )
    
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=["spotify_id"],
        set_={
            "name": stmt.excluded.name,
            "artist": stmt.excluded.artist,
            "album": stmt.excluded.album,
            "duration_ms": stmt.excluded.duration_ms
        }
    )
    
    await session.execute(do_update_stmt)
    
async def consume_loop():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_URL,
        group_id="spotify-etl-group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    await consumer.start()
    print(f"Consumer started listening topic {TOPIC_NAME}")
    
    try:
        async for msg in consumer:
            track_data = msg.value
            
            async with async_session() as session:
                try:
                    await save_track_to_db(session, track_data)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print(f"Mistake saving track: {e}")
                    
    finally:
        await consumer.stop()
        
if __name__ == "__main__":
    asyncio.run(consume_loop())