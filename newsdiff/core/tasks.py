import logging

from newsdiff.celery import app
from newsdiff.core.parsers.haaretz import HaaretzParser

@app.task()
def process_haaretz_homepage():
    hp = HaaretzParser()
    articles = hp.process_homepage()
    for article_url in articles:
        process_haaretz_article.delay(article_url)

@app.task(rate_limit='12/m')
def process_haaretz_article(url):
    hp = HaaretzParser()
    hp.process_article(url)
