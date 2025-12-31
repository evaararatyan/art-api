from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String)
    birth_year = Column(Integer)
    death_year = Column(Integer, nullable=True)

    artworks = relationship("Artwork", back_populates="artist")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

    artworks = relationship("Artwork", back_populates="genre")

class Museum(Base):
    __tablename__ = "museums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String)
    country = Column(String)

    artworks = relationship("Artwork", back_populates="museum")

class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year_created = Column(Integer)
    description = Column(String)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    artist_id = Column(Integer, ForeignKey("artists.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    museum_id = Column(Integer, ForeignKey("museums.id"))

    artist = relationship("Artist", back_populates="artworks")
    genre = relationship("Genre", back_populates="artworks")
    museum = relationship("Museum", back_populates="artworks")