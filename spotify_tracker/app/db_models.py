


from datetime import date
from sqlalchemy import Integer, Date, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, Date, DateTime, func

class Base(DeclarativeBase):
    pass

class TrackDailyStats(Base):
    __tablename__ = "track_daily_stats"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    event_date: Mapped[date] = mapped_column(Date)
    listen_count: Mapped[int] = mapped_column(Integer, default=0)
    
    __table_args__ = (UniqueConstraint("track_id", "event_date",
    name="uq_track_event_date"
    ),)