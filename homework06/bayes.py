import math
import csv
import string
from typing import List, Dict

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.vectors = {}  # all unique vectors
        self.d = 0  # number of unique vectors
        self.labels_d = {}  # number of vectors in specific class (label)
        self.labels_p = {}  # probability of each class (label)

    def fit(self, X: List[str], y: List[str]) -> None:
        """
        Fit Naive Bayes classifier according to X, y.
        :param X: array of messages
        :param y: array of messages' classes (labels)
        :return: None
        """
        # 1. Add all unique vectors from messages (X)
        for i in range(len(X)):
            for word in X[i].split():
                if self.vectors.get(word):
                    if self.vectors[word]['n'].get(y[i]):
                        self.vectors[word]['n'][y[i]] += 1
                    else:
                        self.vectors[word]['n'][y[i]] = 1
                else:
                    self.vectors[word] = {'n': {y[i]: 1}}
                    self.d += 1

                if self.labels_d.get(y[i]):
                    self.labels_d[y[i]] += 1
                else:
                    self.labels_d[y[i]] = 1

            self.labels_p[y[i]] = 1 if not self.labels_p.get(y[i]) else self.labels_p[y[i]] + 1

        # 2. Count probabilities in each added vector of each class (label)
        for vector in self.vectors:
            for label in self.labels_d:
                n = 0 if not self.vectors[vector]['n'].get(label) else self.vectors[vector]['n'][label]
                p = (n + self.alpha) / (self.labels_d[label] + (self.d * self.alpha))

                if self.vectors[vector].get('p'):
                    self.vectors[vector]['p'][label] = p
                else:
                    self.vectors[vector]['p'] = {label: p}

        # 3. Count probability of each class
        sum = 0
        for label in self.labels_p:
            sum += self.labels_p[label]

        for label in self.labels_p:
            self.labels_p[label] = self.labels_p[label] / sum

    def predict(self, X: List[str]) -> str:
        """
        Perform classification on an array of test vectors X.
        :param X: array of vectors
        :return: predicted class of message (label)
        """
        sums = {}

        # 1. For each class write to 'sums' ln( P(C=c|D) )
        for label in self.labels_p:
            sums[label] = math.log(self.labels_p[label])

        # 2. For each class write to 'sums' vector's ln( P(w|C) )
        for vector in X:
            if self.vectors.get(vector):
                for label in self.vectors[vector]['p']:
                    sums[label] += math.log(self.vectors[vector]['p'][label])

        # 3. Find max sum from 'sums'
        predicted = {'sum': 0, 'label': None}
        for label in sums:
            if (not predicted['sum']) or (sums[label] > predicted['sum']):
                predicted['sum'] = sums[label]
                predicted['label'] = label

        return predicted['label']

    def score(self, X_test: List[str], y_test: List[str]) -> int:
        """
        Returns the mean accuracy on the given test data and labels.
        :param X_test: array of test messages
        :param y_test: array of test messages' classes (labels)
        :return: mean accuracy on the given test data and classes (labels)
        """
        predictions_count = 0
        right_predictions_count = 0

        for i in range(len(X_test)):
            label = self.predict(X_test[i].split())
            predictions_count += 1
            right_predictions_count += 1 if label == y_test[i] else 0

        return right_predictions_count / predictions_count


def clean(s: str) -> str:
    """
    Clean string from the punctuations symbols
    :param s: string to clean
    :return: cleaned string
    """
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)
