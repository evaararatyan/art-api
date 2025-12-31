from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.database import engine, Base, get_db

# Создаём таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Art API")

# ---------------- ARTIST ----------------
@app.post("/artists/", response_model=schemas.Artist)
def add_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    return crud.create_artist(db, artist)

@app.get("/artists/", response_model=list[schemas.Artist])
def list_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_artists(db, skip, limit)

# ---------------- GENRE ----------------
@app.post("/genres/", response_model=schemas.Genre)
def add_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    return crud.create_genre(db, genre)

@app.get("/genres/", response_model=list[schemas.Genre])
def list_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_genres(db, skip, limit)

# ---------------- MUSEUM ----------------
@app.post("/museums/", response_model=schemas.Museum)
def add_museum(museum: schemas.MuseumCreate, db: Session = Depends(get_db)):
    return crud.create_museum(db, museum)

@app.get("/museums/", response_model=list[schemas.Museum])
def list_museums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_museums(db, skip, limit)

# ---------------- ARTWORK ----------------
@app.post("/artworks/", response_model=schemas.Artwork)
def add_artwork(artwork: schemas.ArtworkCreate, db: Session = Depends(get_db)):
    return crud.create_artwork(db, artwork)

@app.get("/artworks/", response_model=list[schemas.Artwork])
def list_artworks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_artworks(db, skip, limit)
