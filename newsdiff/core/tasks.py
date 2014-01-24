import logging

from newsdiff.celery import app
from newsdiff.core.parsers.haaretz import HaaretzParser
from newsdiff.core.parsers.ynet import YnetParser

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

@app.task()
def process_ynet_homepage():
    yp = YnetParser()
    articles = yp.process_homepage()
    for article_url in articles:
        process_ynet_article.delay(article_url)

@app.task(rate_limit='12/m')
def process_ynet_article(url):
    yp = YnetParser()
    yp.process_article(url)