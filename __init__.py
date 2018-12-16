# -*- coding: utf-8 -*-

'''
爬虫程序 version: 1.2.0
'''

# from crawler.thejakartapost import ThejakartapostCrawler

# if __name__ == '__main__':
#     ThejakartapostCrawler().run()

from crawler.twitter import TwitterCrawler

if __name__ == '__main__':
    TwitterCrawler().run()