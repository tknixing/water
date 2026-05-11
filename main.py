# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db
from models import Article
from schemas import ArticleCreate, ArticleUpdate, ArticleResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="文章增删改查 API")


@app.post("/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(
        title=article.title,
        content=article.content,
        author=article.author
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article


@app.get("/articles", response_model=List[ArticleResponse])
def list_articles(db: Session = Depends(get_db)):
    return db.query(Article).order_by(Article.id.desc()).all()


@app.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    return article


@app.put("/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    update_data = article_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    return article


@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    db.delete(article)
    db.commit()

    return {"message": "删除成功"}
