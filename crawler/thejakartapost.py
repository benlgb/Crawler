# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src import Crawler, AsyncCrawler, Request, UserAgentMiddleware, ShowUrlMiddleware

class ThejakartapostCrawler(Crawler):
    SETTINGS = {
        'MIDDLEWARES': [
            UserAgentMiddleware(),
            ShowUrlMiddleware()
        ]
    }

    def start(self):
        yield Request('http://www.thejakartapost.com/index', cb=self.list_parse)

    def list_parse(self, res):
        soup = BeautifulSoup(res.text, 'lxml')

        # 列表页信息获取
        for li in soup.select('div.listNews.whtPD.columns'):
            print(li.find('h2', 'titleNews').get_text(strip=True))
            print(urljoin(res.url, li.a['href']))
            print()
            break
        
        # 下一页
        next_page = soup.select('.navigation-page a.jp-last')
        if next_page:
            url = urljoin(res.url, next_page[0]['href'])
            yield Request(url, cb=self.list_parse)

class ThejakartapostAsyncCrawler(AsyncCrawler):
    SETTINGS = {
        'MIDDLEWARES': {
            UserAgentMiddleware()
        },
        'THREAD': 3
    }

    def start(self):
        for i in range(1, 21):
            url = 'https://www.thejakartapost.com/index/page/%d' % i
            yield Request(url, cb=self.list_parse)

    async def list_parse(self, res):
        soup = BeautifulSoup(await res.text(), 'lxml')

        # 列表页信息获取
        for li in soup.select('div.listNews.whtPD.columns'):
            print(li.find('h2', 'titleNews').get_text(strip=True))
            print(urljoin(str(res.url), li.a['href']))
            print()
            break

        # 下一页
        # next_page = soup.select('.navigation-page a.jp-last')
        # if next_page:
        #     url = urljoin(str(res.url), next_page[0]['href'])
        #     yield Request(url, cb=self.list_parse)