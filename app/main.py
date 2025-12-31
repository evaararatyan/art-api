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

@app.get("/artworks/", response_model=schemas.PaginatedResponse)
def list_artworks(
    page: int = Query(1, description="Номер страницы (начинается с 1)", ge=1),
    size: int = Query(10, description="Количество записей на странице", ge=1, le=100),
    sort_by: str = Query("id", description="Поле для сортировки: id, year, title, created_at"),
    sort_order: str = Query("asc", description="Направление: asc или desc"),
    db: Session = Depends(get_db)
):
    """
    📄 Получить список произведений с пагинацией и сортировкой
    """
    # Рассчитываем offset для пагинации
    offset = (page - 1) * size
    
    # Получаем отсортированные данные с учетом пагинации
    if sort_by == "year":
        order_field = models.Artwork.year_created
    elif sort_by == "title":
        order_field = models.Artwork.title
    elif sort_by == "created_at":
        order_field = models.Artwork.created_at
    else:
        order_field = models.Artwork.id
    
    if sort_order.lower() == "desc":
        order_field = order_field.desc()
    else:
        order_field = order_field.asc()
    
    # Получаем данные для текущей страницы
    artworks = db.query(models.Artwork).order_by(order_field).offset(offset).limit(size).all()
    
    # Получаем общее количество записей
    total = db.query(models.Artwork).count()
    
    # Рассчитываем общее количество страниц
    total_pages = (total + size - 1) // size
    
    # Проверяем наличие следующей и предыдущей страницы
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "has_next": has_next,
        "has_prev": has_prev,
        "data": artworks
    }

@app.get("/artworks/paginated/", response_model=schemas.PaginatedResponse)
def get_paginated_artworks(
    page: int = Query(1, description="Номер страницы (начинается с 1)", ge=1),
    size: int = Query(10, description="Количество записей на странице", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    📄 Получить произведения с пагинацией
    """
    return crud.get_artworks_paginated(db, page=page, size=size)

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

# ========== ПОЛНОТЕКСТОВЫЙ ПОИСК ПО JSON (ПУНКТ 6) ==========
@app.get("/artworks/search/metadata/", response_model=schemas.PaginatedResponse)
def search_in_metadata(
    pattern: str = Query(..., description="""Регулярное выражение для поиска в JSON поле metadata_json.
    
    Примеры:
    - 'oil' - найдет все произведения, где в metadata_json есть слово 'oil'
    - '.*1000000.*' - найдет произведения с оценкой 1000000
    - '.*true.*' - найдет произведения, где есть булево значение true
    - 'watercolor|acrylic' - найдет произведения с техникой watercolor ИЛИ acrylic
    """),
    page: int = Query(1, description="Номер страницы", ge=1),
    size: int = Query(10, description="Количество на странице", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    🔍 Поиск по JSON полю с пагинацией
    """
    try:
        if not pattern or pattern.strip() == "":
            raise HTTPException(
                status_code=400, 
                detail="Pattern cannot be empty"
            )
        
        # Рассчитываем offset
        offset = (page - 1) * size
        
        # Используем raw SQL для поиска
        from sqlalchemy import text
        query = text("""
            SELECT * FROM artworks 
            WHERE metadata_json::text ~ :pattern
            ORDER BY id
            LIMIT :limit OFFSET :offset
        """)
        
        result = db.execute(query, {
            "pattern": pattern.strip(),
            "limit": size,
            "offset": offset
        })
        
        # Получаем данные
        artworks_data = [dict(row) for row in result]
        
        # Получаем ОБЩЕЕ количество найденных записей (без пагинации)
        count_query = text("""
            SELECT COUNT(*) FROM artworks 
            WHERE metadata_json::text ~ :pattern
        """)
        
        total_result = db.execute(count_query, {"pattern": pattern.strip()})
        total = total_result.scalar()  # Получаем число
        
        # Рассчитываем страницы
        total_pages = (total + size - 1) // size if total > 0 else 0
        has_next = page < total_pages
        has_prev = page > 1
        
        # Преобразуем словари в объекты Artwork
        from app import models
        artworks = []
        for item in artworks_data:
            artwork = models.Artwork(**item)
            artworks.append(artwork)
        
        return {
            "total": total,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
            "data": artworks
        }
        
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Search failed: {str(e)}"
        )