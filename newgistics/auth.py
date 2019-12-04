# -*- coding: utf-8 -*-

"""
newgistics.auth
~~~~~~~~~~~~~~~

Auth classes attaching HTTP Authentication & Content-Type to the given PreparedRequest object.
"""

from requests import auth, PreparedRequest


class WebAPIAuth(auth.AuthBase):
    def __init__(self, api_key: str, content_type="application/json"):
        # setting up api key and content type
        self.api_key = api_key
        self.content_type = content_type

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Content-Type"] = self.content_type
        r.headers["x-API-Key"] = self.api_key

        return r


class FulfillmentAuth(auth.AuthBase):
    def __init__(self, api_key: str, content_type="application/xml"):
        # Newgistics Fulfillment API v2.8.2 supports only XML
        # setting up api key and content type
        self.api_key = api_key
        self.content_type = content_type

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Content-Type"] = self.content_type
        r.prepare_url(r.url, dict(key=self.api_key))

        return r
