from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleCreate(BaseModel):
    title: str
    content: str
    author: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True