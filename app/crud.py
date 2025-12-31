from sqlalchemy.orm import Session
from app import models

# -------------------------
# ARTIST
# -------------------------
def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()

def create_artist(db: Session, name: str, country: str, birth_year: int = None, death_year: int = None):
    db_artist = models.Artist(name=name, country=country, birth_year=birth_year, death_year=death_year)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

# -------------------------
# GENRE
# -------------------------
def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

def create_genre(db: Session, name: str, description: str = None):
    db_genre = models.Genre(name=name, description=description)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

# -------------------------
# MUSEUM
# -------------------------
def get_museums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Museum).offset(skip).limit(limit).all()

def create_museum(db: Session, name: str, city: str = None, country: str = None):
    db_museum = models.Museum(name=name, city=city, country=country)
    db.add(db_museum)
    db.commit()
    db.refresh(db_museum)
    return db_museum

# -------------------------
# ARTWORK
# -------------------------
def get_artworks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artwork).offset(skip).limit(limit).all()

def create_artwork(db: Session, title: str, artist_id: int, genre_id: int, museum_id: int, year_created: int = None, description: str = None, metadata: dict = None):
    db_artwork = models.Artwork(
        title=title,
        artist_id=artist_id,
        genre_id=genre_id,
        museum_id=museum_id,
        year_created=year_created,
        description=description,
        metadata=metadata
    )
    db.add(db_artwork)
    db.commit()
    db.refresh(db_artwork)
    return db_artwork
