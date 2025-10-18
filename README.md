# FastAPI TODO API (SQLite + SQLAlchemy + Pytest)

A production-style **Python** project that demonstrates:
- **FastAPI** for a typed, modern REST API
- **SQLite + SQLAlchemy** for persistence
- **Pydantic** models for validation
- **pytest** tests
- **Dockerfile** for containerization
- **GitHub Actions CI**

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

# Initialize DB (auto on first run) & browse docs
# Open http://127.0.0.1:8000/docs
```

## Endpoints
- `GET /health`
- `GET /todos?page=1&page_size=10&done=false`
- `POST /todos` → `{ "title": "Buy milk" }`
- `PATCH /todos/{id}` → `{ "title": "New", "done": true }`
- `DELETE /todos/{id}`

## Tests
```bash
pytest -q
```

## Docker
```bash
docker build -t fastapi-todo-api .
docker run -p 8000:8000 fastapi-todo-api
```

## Project structure
```
fastapi-todo-api/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ db.py
│  ├─ models.py
│  ├─ schemas.py
│  └─ crud.py
├─ tests/
│  └─ test_api.py
├─ requirements.txt
├─ Dockerfile
├─ .gitignore
└─ .github/workflows/ci.yml
```
