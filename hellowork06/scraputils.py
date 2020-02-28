import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from db import *


def extract_news(parser: BeautifulSoup) -> List[Dict]:
    """
    Extract news from a given web page
    :param parser: BeautifulSoup web page object
    :return: array with news
    """
    news_list = []

    titles = parser.findAll('tr', attrs={'class': 'athing'})
    subtext = parser.findAll('td', attrs={'class': 'subtext'})

    for i in range(len(titles)):
        a = titles[i].findAll('td', attrs={'class': 'title'})[1].find('a')
        title = a.get_text()
        url = a['href']

        author = subtext[i].find('a', attrs={'class': 'hnuser'})
        if author:
            author = author.get_text()

        comments = subtext[i].findAll('a')[-1].get_text()
        if 'comments' in comments:
            comments = comments.split("\xa0")[0]
        else:
            comments = 0

        points = subtext[i].find('span', attrs={'class': 'score'})
        if points:
            points = points.get_text()

        news_list.append({
            'author': author,
            'comments': comments,
            'points': points,
            'title': title,
            'url': url
        })

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """
    Extract next page URL
    :param parser: BeautifulSoup web page object
    :return: next page URL or empty string if it isn't exist
    """
    more_link = parser.find('a', attrs={'class': 'morelink'})
    return "" if not more_link else more_link['href']


def get_news(url: str, n_pages: int = 1) -> List[Dict]:
    """
    Collect news from a given web page
    :param url: web page url
    :param n_pages: count of pages to scan
    :return: array with news
    """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
