# -*- coding: utf-8 -*-

"""
newgistics.web
~~~~~~~~~~~~~~

This module contains the resource wrapper for Newgistics Web REST API.
"""

import os
import json

import requests
import xmltodict

from .auth import WebAPIAuth
from . import exceptions


class NewgisticsREST(object):
    """
    Python client for Newgistics REST Web API
    """

    def __init__(
        self, api_key: str = os.environ.get("NG_WEB_API_KEY"), staging: bool = False
    ):
        """
        :param api_key: API Key for Newgistics Web REST API
                        (provided by your Newgistics's account manager).
        :param staging: False if in production else True

        Usage::
          >>> from newgistics import NewgisticsWeb
          >>> ngweb_client = NewgisticsWeb(api_key='API-KEY', staging=False)
        """

        if not api_key:
            raise exceptions.IncorrectParameterError("Missing API Key")
        self.staging = staging
        self.api_key = api_key
        self.staging_url = "https://apiint.newgistics.com"
        self.production_url = "https://api.newgistics.com"
        self.session = requests.Session().request
        self.labels = ShipmentLabel(self)

    @property
    def api_endpoint(self) -> str:
        """
        :return: API base URL on the basis of environment
        """
        if self.staging:
            return self.staging_url
        return self.production_url


class BaseClient(object):
    """
    Parent class for all resources like Shipment
    """

    def __init__(self, client):
        self.client = client

    def _make_request(self, method_name: str, resource_endpoint: str, **kwargs):
        """
        Method that handles all HTTP stuff
        :param method_name: HTTP Method Name. Example: GET POST
        :param resource_endpoint: The resource after the base URL
        :param dict_payload: HTTP Request Payload (Optional)
        :param query_params: HTTP Request Query Params (Optional)
        :param headers: HTTP Request Headers (Optional)
        :return: requests.Response object
        """

        dict_payload = kwargs.get("dict_payload")
        query_params = kwargs.get("query_params")
        headers = kwargs.get("headers")
        request_params = {
            "url": "{api_endpoint}/{resource_endpoint}".format(
                api_endpoint=self.client.api_endpoint,
                resource_endpoint=resource_endpoint,
            ),
            "json": dict_payload,
            "auth": WebAPIAuth(api_key=self.client.api_key),
            "headers": headers or {},
            "params": query_params or {},
        }
        req = self.client.session(method_name, **request_params)
        return req

    @staticmethod
    def process(response: requests.Response) -> requests.Response:

        # Convert XML response to JSON
        parsed_dict = xmltodict.parse(response.content)

        # Override requests object with JSON response in-place of originally XML
        response._content = str.encode(json.dumps(parsed_dict))
        try:
            response.raise_for_status()
        except requests.HTTPError as http_err:
            status_code = http_err.response.status_code
            if status_code == 401:
                raise exceptions.AccessNotGrantedError(http_err, response)
            if status_code == 403:
                raise exceptions.AuthenticationParameterError(http_err, response)
            if status_code == 404:
                raise exceptions.ResourceEntityNotFound(http_err, response)
            if status_code == 422:
                raise exceptions.AuthenticationParameterError(http_err, response)
            if status_code == 500:
                raise exceptions.InternalServerError(http_err, response)
        except requests.RequestException as req_err:
            raise exceptions.NewgisticsException(req_err, response)
        return response


class ShipmentLabel(BaseClient):
    """
    The resource class which communicates with the Shipments API.
    Functionalities under this class:
        Create Shipment
    """

    def create(self, payload: dict = None, params: dict = None) -> requests.Response:
        """
        Creates Shipment Label
        :param params: HTTP Request Query Params (Optional)
        :param payload: HTTP Request Payload (Optional)
        :return: requests.Response object

        Usage::
          >>> ngweb_client.labels.create(payload={}, params={})
        Sample Payload:
        {
        "clientServiceFlag": "Standard",
        "consumer": {
            "Address": {
                "Address1": "2700 Via Fortuna Drive",
                "Address2": "",
                "Address3": "",
                "City": "Austin",
                "CountryCode": "US",
                "State": "TX",
                "Zip": "78746"
            },
            "DaytimePhoneNumber": "5122256000",
            "EveningPhoneNumber": "",
            "FaxNumber": "",
            "FirstName": "testname",
            "Honorific": "",
            "LastName": "tester",
            "MiddleInitial": "",
            "PrimaryEmailAddress": "croosken@newgistics.com"
        },
        "deliveryMethod": "SelfService",
        "dispositionRuleSetId": 99,
        "labelCount": 1,
        "merchantID": "NGST",
        "returnId": "123456789A"
        }
        """
        resource = "WebAPI/Shipment"
        response = self._make_request(
            "POST",
            resource_endpoint=resource,
            dict_payload=payload,
            query_params=params,
        )
        return self.process(response)
