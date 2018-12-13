# -*- coding: utf-8 -*-

'''
爬虫主体
'''

from src.Queue import RequestQueue, ResponseQueue
from src.Manager import RequestManager, ResponseManager

class Crawler:
    def __init__(self):
        self.req_queue = RequestQueue()
        self.res_queue = ResponseQueue()
        args = self.req_queue, self.res_queue
        self.req_manager = RequestManager(*args)
        self.res_manager = ResponseManager(*args)

    def run(self):
        self.res_manager.handle(self.start())
        while not self.req_queue.empty():
            self.req_manager.request()
            self.res_manager.response()
        
    def start(self):
        pass