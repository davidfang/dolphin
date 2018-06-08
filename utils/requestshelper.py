# -*- coding: utf-8 -*-

import requests
from settings import PROXIES


class RequestsHelper(object):
    def __init__(self):
        pass

    @classmethod
    def get(cls, url, params=None, **kwargs):
        return requests.get(url, params, proxies=PROXIES, **kwargs)

    @classmethod
    def options(cls, url, **kwargs):
        return requests.options(url, proxies=PROXIES, **kwargs)

    @classmethod
    def head(cls, url, **kwargs):
        return requests.head(url, **kwargs)

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, proxies=PROXIES, **kwargs)

    @classmethod
    def put(cls, url, data=None, **kwargs):
        return requests.put(url, data=data, proxies=PROXIES, **kwargs)

    @classmethod
    def patch(cls, url, data=None, **kwargs):
        return requests.patch(url, data=data, proxies=PROXIES, **kwargs)

    @classmethod
    def delete(cls, url, **kwargs):
        return requests.delete(url, proxies=PROXIES, **kwargs)
