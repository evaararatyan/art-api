from sqlalchemy.orm import Session
from sqlalchemy import and_, func, text
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

# ========== СЛОЖНЫЕ ЗАПРОСЫ ==========
def get_artworks_filtered(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_year: int = None,
    max_year: int = None,
    artist_id: int = None,
    museum_id: int = None,
    genre_id: int = None
):
    """SELECT ... WHERE с несколькими условиями"""
    query = db.query(models.Artwork)
    
    filters = []
    if min_year:
        filters.append(models.Artwork.year_created >= min_year)
    if max_year:
        filters.append(models.Artwork.year_created <= max_year)
    if artist_id:
        filters.append(models.Artwork.artist_id == artist_id)
    if museum_id:
        filters.append(models.Artwork.museum_id == museum_id)
    if genre_id:
        filters.append(models.Artwork.genre_id == genre_id)
    
    if filters:
        query = query.filter(and_(*filters))
    
    return query.offset(skip).limit(limit).all()

def get_artworks_with_details(db: Session, skip: int = 0, limit: int = 100):
    """JOIN: Получить artworks с информацией о художнике, жанре и музее"""
    results = db.query(
        models.Artwork,
        models.Artist.name.label("artist_name"),
        models.Genre.name.label("genre_name"),
        models.Museum.name.label("museum_name"),
        models.Museum.country.label("museum_country")
    ).join(
        models.Artist, models.Artwork.artist_id == models.Artist.id
    ).join(
        models.Genre, models.Artwork.genre_id == models.Genre.id
    ).join(
        models.Museum, models.Artwork.museum_id == models.Museum.id
    ).offset(skip).limit(limit).all()
    
    artworks = []
    for artwork, artist_name, genre_name, museum_name, museum_country in results:
        artwork_dict = {
            "id": artwork.id,
            "title": artwork.title,
            "year_created": artwork.year_created,
            "description": artwork.description,
            "artist_name": artist_name,
            "genre_name": genre_name,
            "museum_name": museum_name,
            "museum_country": museum_country
        }
        artworks.append(artwork_dict)
    
    return artworks

def update_expensive_artworks_discount(db: Session, discount_percent: float = 10.0):
    """UPDATE с нетривиальным условием: скидка на дорогие произведения"""
    artworks = db.query(models.Artwork).all()
    updated = 0
    
    for artwork in artworks:
        if (artwork.metadata_json and 
            'estimated_value_usd' in artwork.metadata_json):
            value = artwork.metadata_json['estimated_value_usd']
            if isinstance(value, (int, float)) and value > 1000000:
                new_value = value * (1 - discount_percent/100)
                artwork.metadata_json['estimated_value_usd'] = new_value
                artwork.metadata_json['has_discount'] = True
                artwork.metadata_json['discount_percent'] = discount_percent
                updated += 1
    
    if updated > 0:
        db.commit()
    return updated

def get_stats_by_country(db: Session):
    """GROUP BY: Статистика произведений по странам музеев"""
    stats = db.query(
        models.Museum.country,
        func.count(models.Artwork.id).label("artwork_count"),
        func.avg(models.Artwork.year_created).label("avg_year")
    ).join(
        models.Artwork, models.Museum.id == models.Artwork.museum_id
    ).group_by(
        models.Museum.country
    ).all()
    
    return [{"country": s[0], "artwork_count": s[1], "avg_year": float(s[2]) if s[2] else None} for s in stats]

def get_artworks_sorted(db: Session, skip: int = 0, limit: int = 100, sort_by: str = "id", sort_order: str = "asc"):
    """Получить произведения с сортировкой"""
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
    
    return db.query(models.Artwork).order_by(order_field).offset(skip).limit(limit).all()

def search_artworks_by_metadata(
    db: Session, 
    pattern: str, 
    skip: int = 0, 
    limit: int = 100
):
    """
    Полнотекстовый поиск по JSON полю metadata_json
    Использует регулярные выражения PostgreSQL (оператор ~)
    Работает с созданным GIN индексом ix_artworks_metadata_json_gin
    
    pattern: регулярное выражение для поиска
    Примеры:
    - 'oil' - ищет слово 'oil' в любом месте JSON
    - '.*1000000.*' - ищет число 1000000
    - '.*true.*' - ищет булево значение true
    """
    
    # ВАЖНО: Используем text() для raw SQL запроса
    # Оператор ~ в PostgreSQL означает "соответствует регулярному выражению"
    # ILIKE - регистронезависимый поиск, но не использует GIN индекс
    # Мы используем ~ для работы с GIN индексом
    
    # Вариант 1: Простой поиск (регистрозависимый)
    query = text("""
        SELECT * 
        FROM artworks 
        WHERE metadata_json::text ~ :pattern
        ORDER BY id
        LIMIT :limit 
        OFFSET :offset
    """)
    
    # Вариант 2: Регистронезависимый поиск (если нужно)
    # query = text("""
    #     SELECT * 
    #     FROM artworks 
    #     WHERE metadata_json::text ~* :pattern
    #     ORDER BY id
    #     LIMIT :limit 
    #     OFFSET :offset
    # """)
    
    # Выполняем запрос с параметрами
    result = db.execute(query, {
        "pattern": pattern,
        "limit": limit,
        "offset": skip
    })
    
    # Преобразуем результат в список словарей
    artworks = []
    for row in result:
        # row - это Row объект, преобразуем в dict
        artwork_dict = dict(row._mapping)  # Используем _mapping для Python 3.11+
        artworks.append(artwork_dict)
    
    return artworks

def get_artworks_paginated(db: Session, page: int = 1, size: int = 10):
    """
    Получить произведения с пагинацией
    page: номер страницы с 1
    size: количество записей на странице
    """
    # сколько записей пропустить
    offset = (page - 1) * size
    
    # Получim данные для текущей страницы
    artworks = db.query(models.Artwork).offset(offset).limit(size).all()
    
    # Получаем общее количество записей
    total = db.query(models.Artwork).count()
    
    # Рассчитываем общее количество страниц
    total_pages = (total + size - 1) // size  # Округление вверх
    
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