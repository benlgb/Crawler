# -*- coding: utf-8 -*-

class DropRequestException(Exception):
    def __init__(self, req, status):
        self.req = req
        super().__init__(req.url, status)

class DropResponseException(DropRequestException):
    pass