from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)