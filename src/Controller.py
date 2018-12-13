# -*- coding: utf-8 -*-

'''
请求响应管理器
'''

import requests
from collections import Iterable
from src.Request import Request, Response

class RequestController:
    def __init__(self, queue, middlewares=[], session=requests):
        self.queue = queue
        self.session = session
        self.middlewares = middlewares

    def request(self):
        req = self.queue.get()
        if self.add_middlewares('before_request', req):
            return
        method = getattr(self.session, req.method)
        try:
            res = method(req.url, **req.kwargs)
        except Exception as e:
            self.add_middlewares('request_exception', req, e)
            return
        res = Response(res, req)
        if self.add_middlewares('after_request', res):
            return
        self.result_handler(res.cb())

    def add_middlewares(self, method, *args):
        for middleware in self.middlewares:
            result = getattr(middleware, method)(*args)
            if result is not None:
                self.result_handler(result)
                return result

    def result_handler(self, result):
        if isinstance(result, Iterable):
            for _result in result:
                self.result_handler(_result)
        elif isinstance(result, Request):
            self.queue.put(result, 0)
        elif result is not None:
            print(result)