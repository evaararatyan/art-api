from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, crud, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Art API",
    description="REST API для управления произведениями искусства",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Art API работает! Перейди на /docs для документации"}

# ---------------- ARTIST ----------------
@app.post("/artists/", response_model=schemas.Artist)
def add_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    return crud.create_artist(db, artist)

@app.get("/artists/", response_model=List[schemas.Artist])
def list_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_artists(db, skip=skip, limit=limit)

# ---------------- GENRE ----------------
@app.post("/genres/", response_model=schemas.Genre)
def add_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    return crud.create_genre(db, genre)

@app.get("/genres/", response_model=List[schemas.Genre])
def list_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_genres(db, skip=skip, limit=limit)

# ---------------- MUSEUM ----------------
@app.post("/museums/", response_model=schemas.Museum)
def add_museum(museum: schemas.MuseumCreate, db: Session = Depends(get_db)):
    return crud.create_museum(db, museum)

@app.get("/museums/", response_model=List[schemas.Museum])
def list_museums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_museums(db, skip=skip, limit=limit)

# ---------------- ARTWORK ----------------
@app.post("/artworks/", response_model=schemas.Artwork)
def add_artwork(artwork: schemas.ArtworkCreate, db: Session = Depends(get_db)):
    return crud.create_artwork(db, artwork)

@app.get("/artworks/", response_model=List[schemas.Artwork])
def list_artworks(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = Query("id", description="Поле для сортировки: id, year, title, created_at"),
    sort_order: str = Query("asc", description="Направление: asc или desc"),
    db: Session = Depends(get_db)
):
    return crud.get_artworks_sorted(
        db, skip=skip, limit=limit,
        sort_by=sort_by, sort_order=sort_order
    )

# ========== СЛОЖНЫЕ ЗАПРОСЫ ==========
@app.get("/artworks/filter/", response_model=List[schemas.Artwork])
def filter_artworks(
    min_year: int = Query(None, description="Минимальный год создания"),
    max_year: int = Query(None, description="Максимальный год создания"),
    artist_id: int = Query(None, description="ID художника"),
    museum_id: int = Query(None, description="ID музея"),
    genre_id: int = Query(None, description="ID жанра"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_artworks_filtered(
        db, skip=skip, limit=limit,
        min_year=min_year, max_year=max_year,
        artist_id=artist_id, museum_id=museum_id,
        genre_id=genre_id
    )

@app.get("/artworks/with-details/", response_model=List[schemas.ArtworkWithDetails])
def get_artworks_details(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_artworks_with_details(db, skip=skip, limit=limit)

@app.put("/artworks/apply-discount/")
def apply_discount_to_expensive(
    discount_percent: float = Query(10.0, description="Процент скидки"),
    db: Session = Depends(get_db)
):
    updated = crud.update_expensive_artworks_discount(db, discount_percent)
    return {
        "message": f"Скидка {discount_percent}% применена к {updated} произведениям",
        "updated_count": updated
    }

@app.get("/stats/by-country/", response_model=List[schemas.StatsByCountry])
def get_stats_by_country(db: Session = Depends(get_db)):
    return crud.get_stats_by_country(db)


@app.get("/artworks/search/metadata/", response_model=list[schemas.Artwork])
def search_in_metadata(
    pattern: str = Query(..., description="""Регулярное выражение для поиска в JSON поле metadata_json.
    
    Примеры:
    - 'oil' - найдет все произведения, где в metadata_json есть слово 'oil'
    - '.*1000000.*' - найдет произведения с оценкой 1000000
    - '.*true.*' - найдет произведения, где есть булево значение true
    - 'watercolor|acrylic' - найдет произведения с техникой watercolor ИЛИ acrylic
    """),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    🔍 Полнотекстовый поиск по JSON полю metadata_json
    
    Использует регулярные выражения PostgreSQL (оператор ~) и работает 
    с созданным GIN индексом для ускорения поиска.
    
    📌 Примеры запросов:
    - GET /artworks/search/metadata/?pattern=oil
    - GET /artworks/search/metadata/?pattern=.*1000000.*
    - GET /artworks/search/metadata/?pattern=watercolor|acrylic
    """
    try:
        # Проверяем, что pattern не пустой
        if not pattern or pattern.strip() == "":
            raise HTTPException(
                status_code=400, 
                detail="Pattern cannot be empty. Please provide a search pattern."
            )
        
        # Вызываем функцию поиска
        results = crud.search_artworks_by_metadata(
            db, 
            pattern=pattern.strip(),
            skip=skip, 
            limit=limit
        )
        
        # Если ничего не найдено
        if not results:
            return []
        
        # Преобразуем словари в объекты Artwork для Pydantic
        # Это нужно, потому что наша функция возвращает словари, а не объекты SQLAlchemy
        from app import models
        
        artwork_objects = []
        for item in results:
            # Создаем объект Artwork из словаря
            artwork = models.Artwork(**item)
            artwork_objects.append(artwork)
        
        return artwork_objects
        
    except Exception as e:
        # Логируем ошибку для отладки
        import traceback
        print(f"Search error: {e}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500, 
            detail=f"Search failed: {str(e)}"
        )