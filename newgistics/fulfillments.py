# -*- coding: utf-8 -*-

"""
newgistics.fulfillments
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the resource wrapper for Newgistics Fulfillments System

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
        self.staging = staging
        self.api_key = api_key
        self.staging_url = "https://apistaging.newgisticsfulfillment.com"
        self.production_url = "https://api.newgisticsfulfillment.com"
        self.session = requests.Session()
        self.returns = Return(self)
        self.inbound_returns = InboundReturn(self)
        self.shipments = Shipment(self)

    @property
    def api_endpoint(self) -> str:
        if self.staging:
            return self.staging_url
        return self.production_url


class BaseClient(object):
    def __init__(self, client):
        self.client = client

    def _make_request(
        self,
        method_name: str,
        resource_endpoint: str,
        dict_payload: dict = None,
        params: dict = None,
        headers: dict = None,
    ):
        """

        :param method_name:
        :param resource_endpoint:
        :param dict_payload:
        :param params:
        :param headers:
        :return:
        """
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
            "params": params,
            "headers": headers,
        }
        req = self.client.session.request(method_name, **request_params)
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
    def fetch(self, **params) -> requests.Response:
        resource = "inbound_returns.aspx"
        response = self._make_request("GET", resource_endpoint=resource, params=params)
        return self.process(response)

    def create(self, payload, params) -> requests.Response:
        # line_items, rma_id, shipment_id, comments
        """
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
            params={"rmaID": params["rmaID"]},
            dict_payload=payload,
        )
        return self.process(response)


class Return(BaseClient):
    def fetch(self, **params) -> requests.Response:
        resource = "returns.aspx"
        response = self._make_request("GET", resource_endpoint=resource, params=params)
        return self.process(response)


class Shipment(BaseClient):
    def fetch(self, **params) -> requests.Response:
        resource = "shipments.aspx"
        response = self._make_request("GET", resource_endpoint=resource, params=params)
        return self.process(response)

    def create(self, payload, params) -> requests.Response:
        """

        :param params: Request parameters
        :param payload: Request payload
        :return: requests.Response object

        """
        #  line_items, customer_info, order_id, custom_fields, order_creation_date, requires_signature, hold_inventory,
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

        # Explicit is better than Implicit
        # ng_items = []
        # for item in line_items:
        #     ng_items.append({"SKU": item["SKU"], "Qty": item["Qty"]})
        # payload = {
        #     "Orders": {
        #         "@apiKey": self.client.api_key,
        #         "Order": {
        #             "@id": order_id,
        #             "CustomerInfo": customer_info,
        #             "AllowDuplicate": False,
        #             "OrderDate": order_creation_date,
        #             "RequiresSignature": requires_signature,
        #             "HoldForAllInventory": hold_inventory,
        #             "CustomFields": custom_fields,
        #             "Items": {"Item": ng_items},
        #         },
        #     }
        # }
        resource = "post_shipments.aspx"
        response = self._make_request(
            "POST", resource_endpoint=resource, dict_payload=payload, params=params
        )
        return self.process(response)
