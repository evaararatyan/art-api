from pydantic import BaseModel
from typing import Optional, Dict

# ---------------- ARTIST ----------------
class ArtistBase(BaseModel):
    name: str
    country: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- GENRE ----------------
class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- MUSEUM ----------------
class MuseumBase(BaseModel):
    name: str
    city: Optional[str] = None
    country: Optional[str] = None

class MuseumCreate(MuseumBase):
    pass

class Museum(MuseumBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- ARTWORK ----------------
class ArtworkBase(BaseModel):
    title: str
    artist_id: int
    genre_id: int
    museum_id: int
    year_created: Optional[int] = None
    description: Optional[str] = None
    metadata_json: Optional[Dict] = None

class ArtworkCreate(ArtworkBase):
    pass

class Artwork(ArtworkBase):
    id: int
    class Config:
        orm_mode = True
