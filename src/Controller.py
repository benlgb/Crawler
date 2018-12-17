# -*- coding: utf-8 -*-

'''
请求响应管理器
'''

import json
import inspect
import asyncio
import aiohttp
import requests
from src.Items import Item
from src.Request import Request, Response
from src.Exception import DropRequestException

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
        if inspect.isgenerator(result):
            for _result in result:
                self.result_handler(_result)
        elif isinstance(result, Request):
            self.queue.put(result, 0)
        elif isinstance(result, Item):
            result.save()
        elif isinstance(result, dict):
            try:
                print(json.dumps(result, indent=4))
            except TypeError:
                print(result)
        elif result is not None:
            print(result)

class AsyncRequestController:
    """异步请求控制器

    Description:
        负责单独一个协程的请求处理，可同时启动多个
    """

    def __init__(self, crawler):
        self.crawler = crawler
        self.queue = crawler.queue
        self.middlewares = crawler.middlewares

    async def __call__(self):
        """请求协程启动

        Description:
            处理请求数据直至主程序通知停止
        """
        async with aiohttp.ClientSession() as session:
            self.session = session
            while True:
                while not self.queue.empty():
                    req = self.queue.get()
                    self.crawler.request_start(req)
                    await self._request(req)
                    self.crawler.request_end(req)
                if self.crawler.end():
                    break
                await asyncio.sleep(0)
                
    async def _request(self, req):
        try:
            await self._middleware('before_request', req)
            method = getattr(self.session, req.method)
            async with method(req.url, **req.kwargs) as res:
                res = Response(res, req)
                await self._middleware('after_request', res)
                await self.result_handler(res.cb())
        except DropRequestException: # 自动抛弃无用请求
            pass
        except aiohttp.ClientError as e: # 请求异常处理
            await self._middleware('request_exception', req, error=e)

    async def _middleware(self, method, req, **kwargs):
        for middleware in self.middlewares:
            _method = getattr(middleware, method)
            result = _method(req, crawler=self.crawler, **kwargs)
            await self.result_handler(result)
            
    async def result_handler(self, result):
        """处理响应解析结果

        Description:
            处理响应解析结果，包括如下情况
                异步函数结果
                异步生成器结果
                生成器结果
                Request对象
                Item对象
                字典s
                其他

        Args:
            result: 响应解析结果
        """
        if inspect.isasyncgen(result):
            async for _result in result:
                await self.result_handler(_result)
        elif inspect.iscoroutine(result):
            await self.result_handler(await result)
        elif inspect.isgenerator(result):
            for _result in result:
                await self.result_handler(_result)
        elif isinstance(result, Request):
            self.queue.put(result, 0)
        elif isinstance(result, Item):
            result.save()
        elif isinstance(result, dict):
            try:
                print(json.dumps(result, indent=4))
            except TypeError:
                print(result)
        elif result is not None:
            print(result)