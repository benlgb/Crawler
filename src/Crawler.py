# -*- coding: utf-8 -*-

'''
爬虫主体
'''
import asyncio
import uvloop
from src.Queue import RequestQueue
from src.Controller import RequestController, AsyncRequestController

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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

class AsyncCrawler:
    SETTINGS = {
        'THREAD': 10,
        'MIDDLEWARES': [],
        'QUEUE': RequestQueue,
    }

    def __init__(self):
        self.settings = self.get_settings()
        self.queue = self.settings['QUEUE']()
        self.middlewares = self.settings['MIDDLEWARES']
        self.controllers = []
        for i in range(self.settings['THREAD']):
            controller = AsyncRequestController(self)
            self.controllers.append(controller)

    def __call__(self):
        self.running_count = 0
        loop = asyncio.get_event_loop()

        # 加载开始请求
        start_request = self.start() or None
        result_handler = self.controllers[0].result_handler
        loop.run_until_complete(result_handler(start_request))

        # 启动请求控制器
        jobs = [i() for i in self.controllers]
        loop.run_until_complete(asyncio.gather(*jobs))

    def start(self):
        pass

    def get_settings(self):
        settings = AsyncCrawler.SETTINGS.copy()
        settings.update(self.SETTINGS)
        return settings
    
    def request_start(self, req):
        """请求处理开始

        Description:
            通知主程序请求处理开始

        Args:
            req: 请求对象
        """
        self.running_count += 1

    def request_end(self, req):
        """请求处理完成

        Description:
            通知主程序请求处理完成
        
        Args:
            req: 请求对象
        """
        self.running_count -= 1

    def end(self):
        """结束判断

        Description:
            获取结束信号，用于判断是否终止请求控制器运行

        Return:
            布尔值，True表示终止运行

        """
        return self.running_count == 0