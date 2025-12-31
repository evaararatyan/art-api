from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, crud

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Art API")

# Зависимость для сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# ARTIST ROUTES
# -------------------------
@app.get("/artists/")
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_artists(db, skip=skip, limit=limit)

@app.post("/artists/")
def add_artist(name: str, country: str, birth_year: int = None, death_year: int = None, db: Session = Depends(get_db)):
    return crud.create_artist(db, name, country, birth_year, death_year)

# -------------------------
# GENRE ROUTES
# -------------------------
@app.get("/genres/")
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_genres(db, skip=skip, limit=limit)

@app.post("/genres/")
def add_genre(name: str, description: str = None, db: Session = Depends(get_db)):
    return crud.create_genre(db, name, description)

# -------------------------
# MUSEUM ROUTES
# -------------------------
@app.get("/museums/")
def read_museums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_museums(db, skip=skip, limit=limit)

@app.post("/museums/")
def add_museum(name: str, city: str = None, country: str = None, db: Session = Depends(get_db)):
    return crud.create_museum(db, name, city, country)

# -------------------------
# ARTWORK ROUTES
# -------------------------
@app.get("/artworks/")
def read_artworks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_artworks(db, skip=skip, limit=limit)

@app.post("/artworks/")
def add_artwork(title: str, artist_id: int, genre_id: int, museum_id: int, year_created: int = None, description: str = None, metadata: dict = None, db: Session = Depends(get_db)):
    return crud.create_artwork(db, title, artist_id, genre_id, museum_id, year_created, description, metadata)
