# -*- coding: utf-8 -*-

"""
    Auth classes attaching HTTP Authentication & Content-Type to the given Request object.
"""

from requests import auth, Request


class WebAPIAuth(auth.AuthBase):
    def __init__(self, api_key: str, content_type="application/json"):
        # setting up api key and content type
        self.api_key = api_key
        self.content_type = content_type

    def __call__(self, r: Request) -> Request:
        r.headers["Content-Type"] = self.content_type
        r.headers["x-API-Key"] = self.api_key

        return r


class FulfillmentAuth(auth.AuthBase):
    def __init__(self, api_key: str, content_type="application/xml"):
        # setting up api key and content type
        self.api_key = api_key
        self.content_type = content_type

    def __call__(self, r: Request) -> Request:
        r.headers["Content-Type"] = self.content_type
        r.params["key"] = self.api_key

        return r
