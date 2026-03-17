import json


def load_articles():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_articles(articles):
    with open("database.json", "w") as f:
        json.dump(articles, f, indent=4)


def get_article_by_id(article_id):
    articles = load_articles()
    for article in articles:
        if article["id"] == article_id:
            return article
    return None


def add_article(article):
    articles = load_articles()
    articles.append(article)
    save_articles(articles)


def update_article(article_id, updated_data):
    articles = load_articles()
    for article in articles:
        if article["id"] == article_id:
            article.update(updated_data)
            save_articles(articles)
            return True
    return False


def delete_article(article_id):
    articles = load_articles()
    for article in articles:
        if article["id"] == article_id:
            articles.remove(article)
            save_articles(articles)
            return True
    return False
