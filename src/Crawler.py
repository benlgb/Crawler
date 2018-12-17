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
    """爬虫控制器

    Description:
        爬虫主程序，描述请求过程和响应处理过程
    """

    SETTINGS = {
        'MIDDLEWARES': [],
        'QUEUE': RequestQueue
    }

    def __init__(self):
        self.settings = AsyncCrawler.SETTINGS.copy()
        self.settings.update(self.SETTINGS)
        self.queue = self.settings['QUEUE']()
        self.middlewares = self.settings['MIDDLEWARES']
        self.controller = RequestController(self)

    def __call__(self):
        self.running_count = 0

        # 加载开始请求
        start_request = self.start() or None
        result_handler = self.controller.result_handler
        result_handler(start_request)

        # 启动请求控制器
        self.controller()
        
    def start(self):
        """开始请求列表

        Description:
            获取初始的请求列表

        Result:
            同响应处理结果
        """
        pass
    
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

class AsyncCrawler(Crawler):
    """异步爬虫控制器

    Description:
        爬虫主程序，描述请求过程和响应处理过程
    """

    SETTINGS = {
        'THREAD': 10,
        'MIDDLEWARES': [],
        'QUEUE': RequestQueue,
    }

    def __init__(self):
        self.settings = AsyncCrawler.SETTINGS.copy()
        self.settings.update(self.SETTINGS)
        self.queue = self.settings['QUEUE']()
        self.middlewares = self.settings['MIDDLEWARES']
        self.controllers = [AsyncRequestController(self)
            for i in range(self.settings['THREAD'])]

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