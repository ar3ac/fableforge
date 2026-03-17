from storage import (
    load_articles,
    save_articles,
    get_article_by_id,
    add_article,
    update_article,
    delete_article,
)

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form

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


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "password123":
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(
            key="username", value=username, httponly=True, max_age=1800, path="/"
        )
        return response
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": "Credenziali errate. Usa admin/password123.",
        },
        status_code=400,
    )


def get_current_admin(request: Request):
    if request.cookies.get("username") == "admin":
        return True
    return False


@app.get("/admin/dashboard")
def admin_dashboard(request: Request):
    if not get_current_admin(request):
        return RedirectResponse(url="/login", status_code=303)
    articles = load_articles()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "articles": articles,
            "admin": True,
        },
    )


@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("username", path="/")
    return response
