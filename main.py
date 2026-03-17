from storage import (
    load_articles,
    save_articles,
    get_article_by_id,
    add_article,
    update_article,
    delete_article,
)

from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request

app = FastAPI(title="FableForge", version="1.0")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    articles = load_articles()
    return templates.TemplateResponse(
        "home.html", {"request": request, "articles": articles}
    )


@app.get("/article/{article_id}")
def read_article(request: Request, article_id: int):
    article = get_article_by_id(article_id)
    if article is None:
        return {"error": "Article not found"}
    return templates.TemplateResponse(
        "article.html", {"request": request, "article": article}
    )
