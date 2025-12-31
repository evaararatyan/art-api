# scripts/seed_data.py
import requests
import random
import time

BASE_URL = "http://127.0.0.1:8000"

def main():
    print("🚀 Начинаем заполнение базы данных...")

    # ВАЖНО: Убедись, что сервер (uvicorn app.main:app --reload) уже запущен в другом окне терминала!

    # ---------- 1. СОЗДАЕМ ХУДОЖНИКОВ (ИСПРАВЛЕНО) ----------
    artists = [
        {"name": "Leonardo da Vinci", "country": "Italy", "birth_year": 1452, "death_year": 1519},
        {"name": "Vincent van Gogh", "country": "Netherlands", "birth_year": 1853, "death_year": 1890},
        {"name": "Pablo Picasso", "country": "Spain", "birth_year": 1881, "death_year": 1973},
        {"name": "Claude Monet", "country": "France", "birth_year": 1840, "death_year": 1926},
    ]

    artist_ids = []
    for a in artists:
        r = requests.post(f"{BASE_URL}/artists/", json=a)
        if r.status_code == 200:
            artist_id = r.json()["id"]  # <-- ВОТ САМАЯ ВАЖНАЯ СТРОКА: сохраняем ID
            artist_ids.append(artist_id)
            print(f"   ✅ Художник создан: {a['name']} (ID: {artist_id})")
        else:
            print(f"   ❌ Ошибка с {a['name']}: {r.status_code}")

    # ---------- 2. СОЗДАЕМ ЖАНРЫ (ИСПРАВЛЕНО) ----------
    genres = [
        {"name": "Renaissance", "description": "15–16 century art"},
        {"name": "Post-Impressionism", "description": "19 century"},
        {"name": "Cubism", "description": "20 century"},
        {"name": "Baroque", "description": "17-18 century art"},
    ]

    genre_ids = []
    for g in genres:
        r = requests.post(f"{BASE_URL}/genres/", json=g)
        if r.status_code == 200:
            genre_id = r.json()["id"]  # <-- Сохраняем ID жанра
            genre_ids.append(genre_id)
            print(f"   ✅ Жанр создан: {g['name']}")
        else:
            print(f"   ❌ Ошибка с {g['name']}: {r.status_code}")

    # ---------- 3. СОЗДАЕМ МУЗЕИ (ИСПРАВЛЕНО) ----------
    museums = [
        {"name": "Louvre", "city": "Paris", "country": "France"},
        {"name": "Van Gogh Museum", "city": "Amsterdam", "country": "Netherlands"},
        {"name": "Prado Museum", "city": "Madrid", "country": "Spain"},
    ]

    museum_ids = []
    for m in museums:
        r = requests.post(f"{BASE_URL}/museums/", json=m)
        if r.status_code == 200:
            museum_id = r.json()["id"]  # <-- Сохраняем ID музея
            museum_ids.append(museum_id)
            print(f"   ✅ Музей создан: {m['name']}")
        else:
            print(f"   ❌ Ошибка с {m['name']}: {r.status_code}")

    # ---------- 4. СОЗДАЕМ ПРОИЗВЕДЕНИЯ (ИСПРАВЛЕНО) ----------
    artwork_titles = ["Mona Lisa", "Starry Night", "Guernica", "The Persistence of Memory", "The Scream", "Water Lilies"]
    created_count = 0

    # Проверяем, что у нас есть хотя бы по одному ID в каждом списке
    if not artist_ids or not genre_ids or not museum_ids:
        print("❌ КРИТИЧЕСКАЯ ОШИБКА: Не удалось создать необходимые записи. Проверь логи выше.")
        return

    print("\n🎨 Начинаем создавать произведения искусства...")
    for i in range(80):  # Создадим 80 произведений для "большого количества данных"
        try:
            # ВАЖНО: Используем правильные имена полей, как в схеме ArtworkCreate
            artwork_data = {
                "title": f"{random.choice(artwork_titles)} #{i+1}",
                "year_created": random.randint(1400, 1950),  # <-- Исправлено: было "year"
                "description": f"Описание для шедевра #{i+1}",
                "artist_id": random.choice(artist_ids),  # Теперь список НЕ пустой
                "genre_id": random.choice(genre_ids),    # Теперь список НЕ пустой
                "museum_id": random.choice(museum_ids),  # Теперь список НЕ пустой
                "metadata_json": {  # <-- Исправлено: было "extra_data"
                    "style": random.choice(["oil", "watercolor", "charcoal", "fresco"]),
                    "size_cm": f"{random.randint(30, 200)}x{random.randint(30, 200)}",
                    "is_famous": random.choice([True, False]),
                    "estimated_value_usd": random.randint(10000, 100000000)
                }
            }

            r = requests.post(f"{BASE_URL}/artworks/", json=artwork_data)
            if r.status_code == 200:
                created_count += 1
                if created_count % 20 == 0:  # Выводим прогресс каждые 20 записей
                    print(f"   ... создано произведений: {created_count}")
            else:
                print(f"   ⚠️ Не удалось создать произведение #{i+1}: {r.status_code}")

        except Exception as e:
            print(f"   ⚠️ Исключение при создании произведения: {e}")

    # ---------- ИТОГ ----------
    print(f"\n{'='*50}")
    print("✅ ЗАПОЛНЕНИЕ БАЗЫ ЗАВЕРШЕНО!")
    print(f"{'='*50}")
    print(f"   Художников создано: {len(artist_ids)}")
    print(f"   Жанров создано: {len(genre_ids)}")
    print(f"   Музеев создано: {len(museum_ids)}")
    print(f"   Произведений искусства создано: {created_count}")
    print(f"\n📊 Проверить данные можно через Swagger: http://127.0.0.1:8000/docs")
    print("   Или выполнив запрос: GET http://127.0.0.1:8000/artworks/")

if __name__ == "__main__":
    main()