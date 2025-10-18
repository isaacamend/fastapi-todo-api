from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from . import schemas, models, crud

app = FastAPI(title="FastAPI TODO API", version="1.0.0")

# Create tables on startup (simple approach for demo repo)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/todos", response_model=schemas.PaginatedTodos)
def list_todos(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    done: bool | None = Query(None),
    db: Session = Depends(get_db),
):
    items = crud.get_todos(db, page=page, page_size=page_size, done=done)
    return {"items": items, "page": page, "page_size": page_size}

@app.post("/todos", response_model=schemas.TodoOut, status_code=201)
def create_todo(data: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, data)
    return todo

@app.patch("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, data: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    todo = crud.update_todo(db, todo, data)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    crud.delete_todo(db, todo)
    return None
