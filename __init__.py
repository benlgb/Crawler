# -*- coding: utf-8 -*-

'''
爬虫程序 version: 1.2.0
'''

from crawler.twitter import TwitterCrawler
from crawler.thejakartapost import ThejakartapostCrawler, ThejakartapostAsyncCrawler

if __name__ == '__main__':
    # TwitterCrawler().run()
    # ThejakartapostCrawler().run()
    ThejakartapostAsyncCrawler()()