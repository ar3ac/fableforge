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

from datetime import datetime

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
            "error": "Invalid credentials. Use admin/password123.",
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


@app.get("/admin/new")
def admin_new(request: Request):
    if not get_current_admin(request):
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(
        "editor.html",
        {
            "request": request,
        },
    )


@app.post("/admin/new")
def admin_new_post(request: Request, title: str = Form(...), content: str = Form(...)):
    if not get_current_admin(request):
        return RedirectResponse(url="/login", status_code=303)
    articles = load_articles()
    new_id = max([a["id"] for a in articles], default=0) + 1
    new_article = {
        "id": new_id,
        "title": title,
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    add_article(new_article)
    # redirect to home page after adding article
    return RedirectResponse(url="/", status_code=303)


@app.get("/admin/edit/{article_id}")
def admin_edit(request: Request, article_id: int):
    if not get_current_admin(request):
        return RedirectResponse(url="/login", status_code=303)
    article = get_article_by_id(article_id)
    if article is None:
        return {"error": "Article not found"}
    return templates.TemplateResponse(
        "editor.html",
        {
            "request": request,
            "article": article,
        },
    )


@app.post("/admin/edit/{article_id}")
def admin_edit_post(
    request: Request, article_id: int, title: str = Form(...), content: str = Form(...)
):
    if not get_current_admin(request):
        return RedirectResponse(url="/login", status_code=303)
    updated_data = {
        "title": title,
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    success = update_article(article_id, updated_data)
    if not success:
        return {"error": "Article not found"}
    return RedirectResponse(url="/", status_code=303)


@app.post("/admin/delete/{article_id}")
def admin_delete(request: Request, article_id: int):
    if not get_current_admin(request):
        return RedirectResponse(url="/login", status_code=303)
    success = delete_article(article_id)
    if not success:
        return {"error": "Article not found"}
    return RedirectResponse(url="/", status_code=303)
