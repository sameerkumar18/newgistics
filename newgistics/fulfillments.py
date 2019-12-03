# -*- coding: utf-8 -*-

"""
newgistics.fulfillments
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the resource wrapper for Newgistics Fulfillments System.
"""

import os
import json

import requests
import xmltodict

from .auth import FulfillmentAuth
from . import exceptions


class Fulfillment(object):
    def __init__(
        self, api_key: str = os.environ.get("NG_FL_API_KEY"), staging: bool = False
    ):
        """
        Python client for Newgistics REST Web API
        :param api_key: API Key for Newgistics Fulfillments API (provided by your Newgistics's account manager).
        :param staging: False if in production else True
        Usage::
          >>> from newgistics import NewgisticsFulfillment
          >>> ngf_client = NewgisticsFulfillment(api_key='API-KEY', staging=False)
        """

        if not api_key:
            raise exceptions.IncorrectParameterError("Missing API Key")
        self.staging = staging
        self.api_key = api_key
        self.staging_url = "https://apistaging.newgisticsfulfillment.com"
        self.production_url = "https://apistaging.newgisticsfulfillment.com"
        self.session = requests.Session().request
        self.returns = Return(self)
        self.inbound_returns = InboundReturn(self)
        self.shipments = Shipment(self)

    @property
    def api_endpoint(self) -> str:
        if self.staging:
            return self.staging_url
        return self.production_url


class BaseClient(object):
    """
    Parent class for all resources like InboundReturn, Return, Shipment
    """

    def __init__(self, client):
        self.client = client

    def _make_request(self, method_name: str, resource_endpoint: str, **kwargs):
        """
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
        xml_payload = None
        if dict_payload:
            xml_payload = xmltodict.unparse(dict_payload)
        request_params = {
            "url": "{api_endpoint}/{resource_endpoint}".format(
                api_endpoint=self.client.api_endpoint,
                resource_endpoint=resource_endpoint,
            ),
            "data": xml_payload,
            "auth": FulfillmentAuth(api_key=self.client.api_key),
            "params": query_params,
            "headers": headers,
        }
        req = self.client.session(method_name, **request_params)
        return req

    @staticmethod
    def process(response: requests.Response):

        parsed_dict = xmltodict.parse(response.content)
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


class InboundReturn(BaseClient):
    """
    The resource class which communicates with the Return API.
    Functionalities under this class:
        Fetch InboundReturn(s)
    """

    def fetch(self, params: dict = None) -> requests.Response:
        """
        Fetches Inbound Return(s)
        :param params: HTTP Request Parameters (Optional)
        :return: requests.Response object

        Usage::
          >>> ngf_client.inbound_returns.create(params={})
        """
        resource = "inbound_returns.aspx"
        response = self._make_request(
            "GET", resource_endpoint=resource, query_params=params
        )
        return self.process(response)

    def create(self, payload: dict = None, params: dict = None) -> requests.Response:
        """
        Create Inbound Return
        :param: HTTP Request Parameters (Optional)
        :payload: HTTP Request Payload (Optional)
        :return: requests.Response object

        Usage::
          >>> ngf_client.inbound_returns.create(payload={}, params={})

        Sample Payload
        line_items: [{"SKU": XXX, "Qty": XX, "Reason": XXX}]
        shipment_id: '12806'
        rma_id: 123456789-12806
        comment: Service Request XYZ
        """
        payload["Returns"]["@apiKey"] = payload["Returns"]["apiKey"]
        try:
            payload["Returns"]["@apiKey"]["Return"]["@id"] = payload["Returns"][
                "@apiKey"
            ]["Return"]["id"]
        except:
            payload["Returns"]["@apiKey"]["Return"]["@orderID"] = payload["Returns"][
                "@apiKey"
            ]["Return"]["orderID"]
        del payload["Returns"]["apiKey"]

        # Explicit is better than Implicit
        # ng_items = []
        # for item in line_items:
        #     ng_items.append(
        #         {"SKU": item["SKU"], "Qty": item["Qty"], "Reason": item["Reason"]}
        #     )
        # payload = {
        #     "Returns": {
        #         "@apiKey": self.client.api_key,
        #         "Return": {
        #             "@id": shipment_id,
        #             "RMA": rma_id,
        #             "Comments": comments,
        #             "Items": {"Item": ng_items},
        #         },
        #     }
        # }
        resource = "post_inbound_returns.aspx"
        response = self._make_request(
            "POST",
            resource_endpoint=resource,
            query_params={"rmaID": params["rmaID"]},
            dict_payload=payload,
        )
        return self.process(response)


class Return(BaseClient):
    """
    The resource class which communicates with the Return API.
    Functionalities under this class:
        Fetch Return(s)
    """

    def fetch(self, params: dict = None) -> requests.Response:
        """
        Fetches Return(s)
        :param params: HTTP Request Parameters (Optional)
        :return: requests.Response object

        Usage::
          >>> ngf_client.returns.fetch(params={})
        """

        resource = "returns.aspx"
        response = self._make_request(
            "GET", resource_endpoint=resource, query_params=params
        )
        return self.process(response)


class Shipment(BaseClient):
    """
    The resource class which communicates with the Shipments API.
    Functionalities under this class:
        Fetch Shipment(s)
        Create Shipment
    """

    def fetch(self, params: dict = None) -> requests.Response:
        """
        Fetches Shipment(s)
        :param params: HTTP Request Parameters (Optional)
        :return: requests.Response object

        Usage::
          >>> ngf_client.shipments.create(params={})
        """
        resource = "shipments.aspx"
        response = self._make_request(
            "GET", resource_endpoint=resource, query_params=params
        )
        return self.process(response)

    def create(self, payload: dict = None, params: dict = None) -> requests.Response:
        """
        Creates Shipment
        :param params: Request parameters
        :param payload: Request payload
        :return: requests.Response object

        Usage::
          >>> ngf_client.shipments.create(payload={}, params={})
        """
        payload["Orders"]["@apiKey"] = payload["Orders"]["apiKey"]
        payload["Orders"]["@apiKey"]["Order"]["@id"] = payload["Orders"]["@apiKey"][
            "Order"
        ]["id"]
        del payload["Orders"]["apiKey"]
        """
        Sample Payload:
        line_items: [{"SKU": XXX, "Qty": XX]
        order_id: '12806'
        customer_info: {
                    "Company": null,
                    "FirstName": "Debra", "LastName": "Barron", "Address1": "13823 Waverton Lane",
                    "Address2": null, "City": "Huntersville", "State": "NC", "Zip": "28078",
                    "Country": "US", "Email": "flygirlmom2@gmail.com", "Phone": null, "IsResidential": "true"
                     }
        """
        resource = "post_shipments.aspx"
        response = self._make_request(
            "POST",
            resource_endpoint=resource,
            dict_payload=payload,
            query_params=params,
        )
        return self.process(response)
