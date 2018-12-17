# -*- coding: utf-8 -*-

'''
爬虫程序 version: 2.1.0
'''

from crawler.twitter import TwitterCrawler, TwitterAsyncCrawler
from crawler.thejakartapost import ThejakartapostCrawler, ThejakartapostAsyncCrawler

if __name__ == '__main__':
    # TwitterCrawler()()
    TwitterAsyncCrawler()()
    # ThejakartapostCrawler()()
    # ThejakartapostAsyncCrawler()()