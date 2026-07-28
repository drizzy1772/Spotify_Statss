







import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app
from app.database import get_db



client = TestClient(app)


def override_get_db_empty():
    db = MagicMock()
    db.query().filter().all.return_value = []
    yield db

def override_get_db_success():
    db = MagicMock()
    mock_stat = MagicMock()
    mock_stat.track_id = "123"
    db.query().filter().all.return_value = [mock_stat]
    yield db

@patch('app.routers.dependencies.redis_client')
def test_get_track_analytics_not_found(mock_redis_client):
    
    app.dependency_overrides[get_db] = override_get_db_empty
    
    mock_redis_client.get = AsyncMock(return_value="1")
    mock_redis_client.incr = AsyncMock(return_value=2)
    
    response = client.get("/analytics/tracks/999/stats")
    
    print("FASTAPI ERROR:", response.json())
    
    assert response.status_code == 404

@patch('app.routers.dependencies.redis_client')
@patch('app.routers.analytics.get_cached_spotify_track')
def test_get_track_analytics_success(mock_get_track_metadata, mock_redis_client):
    
    app.dependency_overrides[get_db] = override_get_db_success
    
    mock_redis_client.get = AsyncMock(return_value="1")
    mock_redis_client.incr = AsyncMock(return_value=2)
    
    mock_get_track_metadata.return_value = {
        "name": "Test Song",
        "artist": "Test Artist",
        "album_cover": "http://test.com/cover.jpg"
    }

    response = client.get(
        "/analytics/tracks/123/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["info"]["name"] == "Test Song"