# -*- coding: utf-8 -*-

'''
爬虫主体
'''

from src.Queue import RequestQueue
from src.Controller import RequestController

class Crawler:
    SETTINGS = {
        'MIDDLEWARES': []
    }

    def __init__(self):
        self.queue = RequestQueue()
        self.settings = Crawler.SETTINGS
        self.settings.update(self.SETTINGS)
        self.middlewares = self.settings['MIDDLEWARES']
        self.controller = RequestController(self.queue, self.middlewares)

    def run(self):
        self.controller.result_handler(self.start())
        while not self.queue.empty():
            self.controller.request()
        
    def start(self):
        pass