from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

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
        from_attributes = True

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    class Config:
        from_attributes = True

class MuseumBase(BaseModel):
    name: str
    city: Optional[str] = None
    country: Optional[str] = None

class MuseumCreate(MuseumBase):
    pass

class Museum(MuseumBase):
    id: int
    class Config:
        from_attributes = True

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
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ArtworkWithDetails(BaseModel):
    id: int
    title: str
    year_created: Optional[int]
    description: Optional[str]
    artist_name: str
    genre_name: str
    museum_name: str
    museum_country: str
    
    class Config:
        from_attributes = True

class StatsByCountry(BaseModel):
    country: str
    artwork_count: int
    avg_year: Optional[float]
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    """
    схема для пагинированного ответа
    """
    total: int              # Общее количество записей
    page: int               # Текущая страница
    size: int               # Количество записей на странице
    total_pages: int        # Общее количество страниц
    has_next: bool          # Есть ли следующая страница
    has_prev: bool          # Есть ли предыдущая страница
    data: List[Artwork]     # Сами данные
    
    class Config:
        from_attributes = True