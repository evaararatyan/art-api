from fastapi import FastAPI
from app.database import engine, Base

# Создаём таблицы (если ещё не созданы)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI с PostgreSQL работает!"}
