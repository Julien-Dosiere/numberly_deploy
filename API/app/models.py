from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


class Tag(BaseModel):
    id: int
    name: str


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    author_id: int
