from bottle import (
    route, run, template, request, redirect, TEMPLATE_PATH
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from bayes import clean


@route("/")
@route("/news")
def news_list():
    TEMPLATE_PATH.insert(0, '')
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Get label and query id from request parameters
    label = request.query['label']
    entry_id = request.query['id']

    # 2. Update database
    s = session()
    entry = s.query(News).get(entry_id)
    entry.label = label
    s.commit()

    # 3. Redirect to main page with news
    redirect("/news")


@route("/update_news")
def update_news():
    # 1. Get all available news from hacker news
    new_news = get_news('https://news.ycombinator.com/', 17)

    # 2. Get all news from our database and transform response to list with Tuples - (title, author)
    s = session()
    old_news = s.query(News).all()
    old_news = [(news.title, news.author) for news in old_news]

    # 3. Add news in database, if the aren't already there
    for entry in new_news:
        if (entry['title'], entry['author']) not in old_news:
            print('adding to db...')

            new = News(title=entry['title'],
                       author=entry['author'],
                       url=entry['url'],
                       comments=entry['comments'],
                       points=entry['points'])
            s.add(new)
            s.commit()

    # 4. Redirect to main page with news
    redirect("/news")


@route('/recommendations')
def recommendations():
    TEMPLATE_PATH.insert(0, '')
    s = session()

    # 1. Classify labeled news
    rows = s.query(News).filter(News.label != None).all()

    X, y = [], []
    for row in rows:
        X.append(row.title)
        y.append(row.label)

    X = [clean(x).lower() for x in X]

    model = NaiveBayesClassifier()
    model.fit(X, y)

    # 2. Get unlabeled news
    new_rows = s.query(News).filter(News.label == None).all()

    # 3. Get predictions
    marked = []
    for row in new_rows:
        marked.append((model.predict(row.title.split()), row))

    # 4. Print ranked table
    return template('news_ranked', rows=marked)


if __name__ == "__main__":
    run(host="localhost", port=8080)
