






import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.spotify import get_tracks_batch_stats
from unittest.mock import MagicMock

pytestmark = pytest.mark.anyio

@patch("app.services.spotify.get_spotify_token", new_callable=AsyncMock)
@patch("app.services.spotify.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_tracks_batch_stats(mock_get, mock_get_token):
    mock_get_token.return_value = "fake_token"
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = MagicMock(return_value={
        "tracks": [
            {"id": "1xK1Gg9SxG8s2cg46sEAIG", "name": "test track"}
        ]
    })
    
    mock_get.return_value = mock_response
        
    track_ids = ["1xK1Gg9SxG8s2cg46sEAIG"]
    
    mock_httpx_client = MagicMock()
    
    result = await get_tracks_batch_stats(track_ids, client=mock_httpx_client)
    
    print(f"\n THATS RESULT: {result}\n")
    
    assert len(result) == 1
    assert result[0]["track_id"] == "1xK1Gg9SxG8s2cg46sEAIG"
    
    mock_get.assert_awaited_once()