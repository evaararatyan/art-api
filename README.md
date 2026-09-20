# Art API — RESTful Service for Artwork and Museum Management

A RESTful web API for managing artworks, artists, museums, and genres built with FastAPI, SQLAlchemy, and PostgreSQL. The project covers relational database design, data initialization pipelines, migrations, specialized querying, and pagination.

---

## Project Requirements Checklist

| Requirement | Description | Status |
|---|---|---|
| Database Initialization Script | SQL script for initial schema creation and setup (`init_db.sql`) | Completed |
| Base CRUD Operations | Core CRUD endpoints for all primary entities | Completed |
| Data Seeding API | Automated data population pipeline via API (`seed_data.py`) | Completed |
| Database Migrations | Schema evolution tracked via Alembic (2 migrations) | Completed |
| Complex SQL Queries | Advanced relational queries (aggregations, joins, filtering) | Completed |
| Full-Text / JSON Indexing | JSON field implementation, GIN indexing, and optimized search | Completed |
| Pagination | Limit/offset pagination for dataset endpoints | Completed |

---

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Database Migrations:** Alembic
- **Data Validation & Serialization:** Pydantic
- **ASGI Server:** Uvicorn

---

## Project Structure

```text
art-api/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI application entry point
│   ├── database.py    # Database connection and session management
│   ├── models.py      # SQLAlchemy ORM models
│   ├── schemas.py     # Pydantic validation schemas
│   └── crud.py        # Database operations and query logic
├── alembic/
│   ├── versions/      # Database migration scripts
│   └── env.py         # Alembic configuration
├── scripts/
│   ├── init_db.sql    # Raw SQL database initialization script
│   └── seed_data.py   # Automated data seeding script
├── requirements.txt   # Python project dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```


## Features & Implementation Details
### Database Initialization & Migration
The application uses PostgreSQL as its primary database store. Initial schema creation is defined in scripts/init_db.sql. Subsequent schema alterations and updates are versioned and applied using Alembic.

### Advanced Querying & Performance
1. Complex Queries: The API implements specialized queries for multi-table joins, grouped aggregations, and filtered views across artworks, museums, and artists.

2. JSON Field & GIN Index: Artwork metadata and flexible attributes are stored in a JSONB column, indexed using a GIN (Generalized Inverted Index) to optimize full-text and key-value search operations.

3. Pagination: Collection endpoints feature pagination to control payload sizes and optimize response times.


## Setup and Installation
1. Repository Setup
Clone the repository and navigate to the project root:
```
git clone <repository-url>
cd art-api
```
Create and activate a virtual environment:

```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```
Install dependencies:

```
pip install -r requirements.txt
```

### 2. Database Configuration
Create the PostgreSQL database and execute the initialization script:

```
psql -U postgres -f scripts/init_db.sql
```

### 3. Database Migrations
Apply database migrations using Alembic to bring the schema up to date:

```
alembic upgrade head
```

4. Data Seeding
Start the application server in one terminal window:

```
uvicorn app.main:app --reload
```
In a separate terminal window, populate the database with sample data:


```
python scripts/seed_data.py
```

## Application Execution
To run the API server locally:
```
uvicorn app.main:app --reload
```
The application will be accessible at http://localhost:8000.



## API Documentation
Interactive API documentation is automatically generated and accessible via:

* Swagger UI: http://localhost:8000/docs

- ReDoc: http://localhost:8000/redoc