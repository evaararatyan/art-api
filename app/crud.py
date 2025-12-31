from sqlalchemy.orm import Session
from app import models, schemas

# ---------------- ARTIST ----------------
def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()

# ---------------- GENRE ----------------
def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

# ---------------- MUSEUM ----------------
def create_museum(db: Session, museum: schemas.MuseumCreate):
    db_museum = models.Museum(**museum.dict())
    db.add(db_museum)
    db.commit()
    db.refresh(db_museum)
    return db_museum

def get_museums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Museum).offset(skip).limit(limit).all()

# ---------------- ARTWORK ----------------
def create_artwork(db: Session, artwork: schemas.ArtworkCreate):
    db_artwork = models.Artwork(**artwork.dict())
    db.add(db_artwork)
    db.commit()
    db.refresh(db_artwork)
    return db_artwork

def get_artworks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artwork).offset(skip).limit(limit).all()
