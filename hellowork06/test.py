from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import csv
from bayes import *


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    with open("data/SMSSpamCollection", encoding='utf-8') as f:
        data = list(csv.reader(f, delimiter="\t"))

    X, y = [], []

    for target, msg in data:
        X.append(msg)
        y.append(target)

    X = [clean(x).lower() for x in X]

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))

    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
