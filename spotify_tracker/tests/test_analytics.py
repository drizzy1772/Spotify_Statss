







import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.database import get_db



client = TestClient(app)


def override_get_db():
    try:
        db = MagicMock()
        mock_stat = MagicMock()
        mock_stat.track_id = 123
        mock_stat.play_count = 50
        mock_stat.date = "2026-07-22"
        db.query().filter().all.return_value = [mock_stat]
        yield db
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

@patch('app.routers.analytics.get_track_metadata')
def test_get_track_analytics(mock_get_track_metadata):
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