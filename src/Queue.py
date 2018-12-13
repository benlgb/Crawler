# -*- coding: utf-8 -*-

'''
请求队列
'''

from queue import Queue, PriorityQueue

class RequestQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        self.count = 0

    def put(self, item, priority):
        item = priority, self.count, item
        super().put(item)
        self.count += 1

    def get(self):
        item = super().get()
        return item[2]

    def get_priority(self):
        item = super().get()
        return item[2], item[0]

    def done(self):
        with self.all_tasks_done:
            return not self.unfinished_tasks