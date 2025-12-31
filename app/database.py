from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Сюда пишем твои данные для подключения к PostgreSQL
DATABASE_URL = "postgresql://art_user:art_pass@localhost:5432/art_db"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Базовый класс для моделей
Base = declarative_base()

# Сессия для работы с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
