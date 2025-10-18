from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

def create_todo(db: Session, data: schemas.TodoCreate) -> models.Todo:
    todo = models.Todo(title=data.title, done=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos(db: Session, page: int, page_size: int, done: bool | None):
    stmt = select(models.Todo)
    if done is not None:
        stmt = stmt.where(models.Todo.done == done)
    stmt = stmt.order_by(models.Todo.id.desc()).limit(page_size).offset((page - 1) * page_size)
    return db.execute(stmt).scalars().all()

def get_todo(db: Session, todo_id: int):
    return db.get(models.Todo, todo_id)

def update_todo(db: Session, todo: models.Todo, data: schemas.TodoUpdate) -> models.Todo:
    if data.title is not None:
        todo.title = data.title
    if data.done is not None:
        todo.done = data.done
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo: models.Todo) -> None:
    db.delete(todo)
    db.commit()
