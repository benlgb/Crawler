# -*- coding: utf-8 -*-

import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src import JsonItem, Crawler, AsyncCrawler, Request, UserAgentMiddleware, ProxyMiddleware, ShowUrlMiddleware, ProxyAsyncMiddleware

class TwitterItem(JsonItem):
    default_save_place = './data/twitter'

    def filename(self):
        return self.data['id'] + '.json'

class TwitterCrawler(Crawler):
    SETTINGS = {
        'MIDDLEWARES': [
            UserAgentMiddleware(),
            ProxyMiddleware()
        ]
    }

    def start(self):
        keyword = 'Trump'
        yield Request('https://twitter.com/i/search/timeline', params={
            'vertical': 'news',
            'q': keyword,
            'src': 'typd',
            'include_available_features': '1',
            'include_entities': '1',
            'reset_error_state': 'false'
        }, headers={
            'accept-language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,zh-TW;q=0.7'
        }, cb=self.list_parse)

    def list_parse(self, res):
        soup = BeautifulSoup(res.json()['items_html'], 'lxml')
        for li in soup.select('li.stream-item'):
            data = self.information(li, res.url)
            if data['footer']['reply_count'] > 0:
                url = 'https://twitter.com/i/%s/conversation/%s' % (data['user']['username'], data['id'])
                yield Request(url, params={
                    'include_available_features': '1',
                    'include_entities': '1',
                    'max_position': '',
                    'reset_error_state': 'false'
                }, headers={
                    'accept-language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,zh-TW;q=0.7'
                }, cb=self.reply_parse, item=data)
            else:
                yield TwitterItem(data)

    def reply_parse(self, res):
        soup = BeautifulSoup(res.json()['items_html'], 'lxml')
        for li in soup.select('li.ThreadedConversation--loneTweet'):
            data = self.information(li.li, res.url)
            data.pop('replies')
            res.item['replies'].append(data)
        yield TwitterItem(res.item)

    def information(self, soup, baseURL):
        user = soup.find('a', 'account-group')
        timer = soup.find('small', 'time')
        replyingTo = soup.find('div', 'ReplyingToContextBelowAuthor')
        content = soup.find('div', 'js-tweet-text-container')
        footer = soup.find('div', 'stream-item-footer')

        return {
            'id': soup['data-item-id'],
            'link': urljoin(baseURL, soup.div['data-permalink-path']),
            'user': {
                'name': soup.div['data-name'],
                **self.userInfo(user, baseURL)
            },
            'time': self.timeInfo(timer),
            'replying_to': self.replyingToInfo(replyingTo, baseURL),
            'content': self.contentInfo(content, baseURL),
            'footer': self.footerInfo(footer),
            'replies': [],
            'html': soup.prettify()
        }

    def userInfo(self, user, baseURL):
        fullname = user.find('strong', 'fullname')
        emojis = []

        # emoji处理
        for span in fullname.select('span.Emoji'):
            src = re.match(r'^background-image:url\(\'(.*)\'\)$', span['style'])
            emoji = {
                'desc': span['title'],
                'src': src and src.group(1),
                'label': span['aria-label'],
                'text': span.next_sibling.extract().get_text()
            }
            span.replace_with('[%s](%s)' % (emoji['desc'], emoji['src']))
            emojis.append(emoji)

        return {
            'id': user['data-user-id'],
            'link': urljoin(baseURL, user['href']),
            'avatar': urljoin(baseURL, user.img['src']),
            'username': user.find('span', 'username').b.get_text(),
            'emojified_name': fullname.get_text(),
            'emojis': emojis
        }

    def timeInfo(self, timer):
        _timer = timer.find('span', '_timestamp')
        return {
            'timestamp': _timer['data-time'],
            'timestamp-ms': _timer['data-time-ms'],
            'local-desc': timer.a['title'],
            'label': _timer.next_sibling.get_text()
        }

    def replyingToInfo(self, replyingTo, baseURL):
        _replyingTo = []
        if replyingTo:
            for user in replyingTo('a', 'pretty-link'):
                _replyingTo.append({
                    'id': user['data-user-id'],
                    'link': urljoin(baseURL, user['href']),
                    'username': user.find('span', 'username').b.get_text()
                })
        return _replyingTo

    def contentInfo(self, content, baseURL):
        p = content.p
        for el in p.select('.u-hidden'):
            el.decompose()
        return {
            'lang': p['lang'],
            'text': p.get_text(' ', strip=True),
            'hashtags': [{
                    'link': urljoin(baseURL, i['href']),
                    'text': i.find('b').get_text(' ', strip=True)
                } for i in p('a', 'twitter-hashtag')],
            'outlinks': [{
                    'link': urljoin(baseURL, i['href']),
                    'text': i.get_text(' ', strip=True)
                } for i in p('a', 'twitter-timeline-link')],
            'atreplies': [{
                    'link': urljoin(baseURL, i['href']),
                    'text': i.find('b').get_text(' ', strip=True)
                } for i in p('a', 'twitter-atreply')],
            'emojis': [{
                    'link': urljoin(baseURL, i['src']),
                    'text': i['title']
                } for i in p('img', 'Emoji')],
            'html': p.prettify()
        }

    def footerInfo(self, footer):
        counts = footer('span', 'ProfileTweet-actionCount')
        return {
            'reply_count': int(counts[0]['data-tweet-stat-count']),
            'retweet_count': int(counts[1]['data-tweet-stat-count']),
            'favorite_count': int(counts[2]['data-tweet-stat-count']),
        }

class TwitterAsyncCrawler(AsyncCrawler, TwitterCrawler):
    SETTINGS = {
        'MIDDLEWARES': [
            UserAgentMiddleware(),
            ProxyAsyncMiddleware(),
            ShowUrlMiddleware()
        ],
        'THREAD': 2
    }

    def start(self):
        keyword = 'Trump'
        yield Request('https://twitter.com/i/search/timeline', params={
            'vertical': 'news',
            'q': keyword,
            'src': 'typd',
            'include_available_features': '1',
            'include_entities': '1',
            'reset_error_state': 'false'
        }, headers={
            'accept-language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,zh-TW;q=0.7'
        }, cb=self.list_parse)

    async def list_parse(self, res):
        data = await res.json()
        soup = BeautifulSoup(data['items_html'], 'lxml')
        for li in soup.select('li.stream-item'):
            data = self.information(li, str(res.url))
            if data['footer']['reply_count'] > 0:
                url = 'https://twitter.com/i/%s/conversation/%s' % (data['user']['username'], data['id'])
                yield Request(url, params={
                    'include_available_features': '1',
                    'include_entities': '1',
                    'max_position': '',
                    'reset_error_state': 'false'
                }, headers={
                    'accept-language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,zh-TW;q=0.7'
                }, cb=self.reply_parse, item=data)
            else:
                yield TwitterItem(data)

    async def reply_parse(self, res):
        data = await res.json()
        soup = BeautifulSoup(data['items_html'], 'lxml')
        for li in soup.select('li.ThreadedConversation--loneTweet'):
            data = self.information(li.li, str(res.url))
            data.pop('replies')
            res.item['replies'].append(data)
        yield TwitterItem(res.item)