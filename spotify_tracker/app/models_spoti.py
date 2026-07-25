



from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class SpotifyTrack(Base):
    __tablename__ = "spotify_tracks"

    id = Column(Integer, primary_key=True, index=True)
    
    spotify_id = Column(String, unique=True, index=True, nullable=False)
    
    name = Column(String, nullable=False)
    
    artist = Column(String, nullable=False)
    album = Column(String, nullable=False)
    duration_ms = Column(Integer, nullable=False)