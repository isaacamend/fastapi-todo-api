from pydantic import BaseModel, Field
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    done: Optional[bool] = None

class TodoOut(BaseModel):
    id: int
    title: str
    done: bool
    class Config:
        from_attributes = True

class PaginatedTodos(BaseModel):
    items: list[TodoOut]
    page: int
    page_size: int
