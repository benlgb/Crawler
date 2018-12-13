# -*- coding: utf-8 -*-

'''
请求响应管理器
'''

import requests
from collections import Iterable
from src.Request import Request, Response

class Manager:
    def __init__(self, req_queue, res_queue, session=requests):
        self.req_queue = req_queue
        self.res_queue = res_queue
        self.session = session

class RequestManager(Manager):
    def run(self):
        while not self.req_queue.done():
            while not self.req_queue.empty():
                self.request()

    def request(self):
        req = self.req_queue.get()
        api = getattr(self.session, req.method)
        print('[+] request start:', req.url)
        res = api(req.url, **req.kwargs)
        print('[+] request end')
        self.res_queue.put(Response(res, req))

class ResponseManager(Manager):
    def run(self):
        while not self.req_queue.done():
            while not self.res_queue.empty():
                self.response()
                self.res_queue.task_done()

    def response(self):
        res = self.res_queue.get()
        self.handle(res.cb())

    def handle(self, result):
        if isinstance(result, Iterable):
            for _result in result:
                self.handle(_result)
        elif isinstance(result, Request):
            self.req_queue.put(result, 0)
        elif result is None:
            pass
        else:
            print(result)
        