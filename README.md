[logo]: https://logo.clearbit.com/newgistics.com "Newgistics Python Client Logo"

![alt text][logo] Newgistics Python Client
==================================================== 

[![PyPI version](https://badge.fury.io/py/newgistics.svg)](https://badge.fury.io/py/newgistics)
<!--[![Build Status](https://travis-ci.org/sameerkumar18/newgistics.svg?branch=master)](https://travis-ci.org/sameerkumar18/newgistics)-->
[![image](https://img.shields.io/pypi/v/newgistics.svg)](https://pypi.org/project/newgistics/)
[![image](https://img.shields.io/pypi/l/newgistics.svg)](https://pypi.org/project/newgistics/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/sameerkumar18)
[![image](https://img.shields.io/badge/Paypal-Donate-blue.svg)](https://www.paypal.me/sameerkumar18)

Python Client for Newgistics Fulfillments API v2.8.2 and Newgistics Web API v2.2.
Please refer to the API docs before using this package.

Installation
------------

Supports Python 3+
To install, simply use pip
```
$ sudo pip install newgistics
✨🍰✨
```

Usage
-----

###### Newgistics Fulfillments System API
```python

>>> from newgistics import NewgisticsFulfillment

>>> ngf_client = NewgisticsFulfillment(api_key='<NG-Fulfillments-API-Key>', staging=False)
>>> ngf_client.inbound_returns.create(payload=request_payload)
    <Response [200]>
```

###### Newgistics REST Web API
```python

>>> from newgistics import NewgisticsWeb

>>> ngw_client = NewgisticsWeb(api_key='<NG-Web-API-Key>', staging=False)
>>> ngw_client.labels.create(payload=label_payload)
    <Response [200]>
```

You can pass the `api_key` explicitly. Alternatively, you may declare these environment variables `NG_FL_API_KEY` and/or `NG_WEB_API_KEY`.

For wrapper usage code snippets please check examples.py

#### Features
Note: Below package usages return a requests module's Response object. Append .json() to get a python dictionary response
- Newgistics Fulfillments
    - Shipments
        - Create Shipment
            ```python
            >>> request_payload = {'Orders': 
                    {'Order': {'AllowDuplicate': False,
                               'CustomerInfo': {'Address1': '32142 Waverton Lane',
                                'Address2': None,
                                'City': 'Huntersville',
                                'Company': None,
                                'Country': 'US',
                                'Email': 'yestestmail@gmail.com',
                                'FirstName': 'John',
                                'IsResidential': 'true',
                                'LastName': 'Barron',
                                'Phone': None,
                                'State': 'NC',
                                'Zip': '28078'},
                               'HoldForAllInventory': False,
                               'Items': {'Item': [{'Qty': 10, 'SKU': 'HLU'}]},
                               'OrderDate': '04-12-2019',
                               'RequiresSignature': False,
                               'id': '4321'}}}
            >>> ngf_client.shipments.create(payload=request_payload)
            ```
            Submit orders to WMS system
        - Fetch Shipment(s)
            ```python
            >>> ngf_client.shipments.fetch(params={'id': '4231'})
            ```
            Retrieves a list of shipments based on one or more parameters    
    - Inbound Returns
        - Create Inbound Return
            ```python
            >>> request_payload = {'Returns': {
                                      'Return': {'id': '8732832',
                                       'Comments': 'COMMENTS',
                                       'Items': {'Item': [{'Qty': 10, 'Reason': 'Some_Reason', 'SKU': 'HLU'}]},
                                       'RMA': '1234'}}}
            >>> ngf_client.inbound_returns.create(payload=request_payload)
            ```
            Submits incoming returns by RMA ID to the WMS system
        - Fetch Inbound Return(s)
            ```python
            >>> ngf_client.inbound_returns.fetch(params={'startCreatedTimestamp': '', 'endCreatedTimestamp': ''})
            ```
            Retrieves a list of incoming returns by RMA ID to the WMS system
    - Returns
        - Fetch Return(s)
            ```python
            >>> ngf_client.returns.fetch(params={'Id': '1234'})
            ```
            Retrieves a list of returns received by Newgistics Fulfillment for a given date/time range or a specific return by order ID
- Newgistics Web API
    - Shipments
        - Create Shipment Label
            ```python
            >>> payload = {
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
            >>> ngw_client.labels.create(payload=payload)
            ```
            Creates a SmartLabel return label


## Default Values

- Newgistics Web API endpoint: 
    - Prod: https://api.newgistics.com
    - Staging: https://apiint.newgistics.com
- Newgistics Fulfillments API: 
    - Prod: https://api.newgisticsfulfillment.com
    - Staging: https://apistaging.newgisticsfulfillment.com

## About Newgistics

Newgistics provides services and technology to support the e-commerce operations of retailers around the world. Its offerings include software and services to build and maintain e-commerce websites, perform order fulfillment, and manage parcel delivery and returns.
This package reduces the shortcomings/difficulties whule integrating Newgistics's APIs. It's still not what I'd appreciate, but it should just work! Looking for your active contribution to the project (See roadmap below)

## Support

For any wrapper related query/issue, please raise a GitHub issue.
## About
#### Why
Integrating with 3PL APIs like Newgistics(owned by PitneyBowes) can be pain at times. For instance, some APIs are XML only, whereas some can accept JSON as payload but return a XML response

#### RoadMap/Shortcomings

    1. Write Tests with a token from Newgistics(Observation: staging and production tokens are same on NG)
    2. Cover more APIs from both Web & Fulfillment
    3. Return better objects, eg: every function returns a python requests's Response object
    4. Overall code and design improvements 

 
[Sameer Kumar](https://www.sameerkumar.website/)

Find me on [Twitter](https://twitter.com/sameer_kumar018)