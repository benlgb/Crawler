# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from src import Crawler, Request, UserAgentMiddleware

class ThejakartapostCrawler(Crawler):
    SETTINGS = {
        'MIDDLEWARES': [
            UserAgentMiddleware()
        ]
    }

    def start(self):
        yield Request('http://www.thejakartapost.com/index', cb=self.list_parse)

    def list_parse(self, res):
        soup = res.soup()

        # 列表页信息获取
        for li in soup.select('li.ic-all.latestEntry'):
            a = li.find_all('a')[1]
            url = urljoin(res.url, a['href'])
            title = a.get_text(strip=True)
            print(title)
            print(url)
            print()
        
        # 下一页
        next_page = soup.select('.navigation-page a.jp-last')
        if next_page:
            url = urljoin(res.url, next_page[0]['href'])
            yield Request(url, cb=self.list_parse)