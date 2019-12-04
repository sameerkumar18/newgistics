""" Newgistics Fulfillments API """

from newgistics import NewgisticsFulfillment

ngf_client = NewgisticsFulfillment(api_key="", staging=False)

# Create Shipment
request_payload = {
    "Orders": {
        "Order": {
            "AllowDuplicate": False,
            "CustomerInfo": {
                "Address1": "32142 Waverton Lane",
                "Address2": None,
                "City": "Huntersville",
                "Company": None,
                "Country": "US",
                "Email": "yestestmail@gmail.com",
                "FirstName": "John",
                "IsResidential": "true",
                "LastName": "Barron",
                "Phone": None,
                "State": "NC",
                "Zip": "28078",
            },
            "HoldForAllInventory": False,
            "Items": {"Item": [{"Qty": 10, "SKU": "HLU"}]},
            "OrderDate": "04-12-2019",
            "RequiresSignature": False,
            "id": "4321",
        }
    }
}
resp = ngf_client.shipments.create(payload=request_payload)
resp.json()

# Fetch Shipment
resp = ngf_client.shipments.fetch(params={"id": "4231"})
resp.json()

# Create Inbound Return
inbound_returns_payload = {
    "Returns": {
        "Return": {
            "id": "SHIPMENTID",
            "RMA": "1234",
            "Comments": "COMMENTS",
            "Items": {"Item": [{"SKU": "HLU", "Qty": 10, "Reason": "Some_Reason"}]},
        }
    }
}
resp = ngf_client.inbound_returns.create(payload=inbound_returns_payload)
resp.json()

# Fetch Inbound Return
resp = ngf_client.inbound_returns.fetch(
    params={"startCreatedTimestamp": "", "endCreatedTimestamp": ""}
)
resp.json()

# Fetch Return
resp = ngf_client.returns.fetch(params={"Id": "1234"})
resp.json()

""" Newgistics Web API """
from newgistics import NewgisticsWeb

ngw_client = NewgisticsWeb(api_key="", staging=False)
label_payload = {
    "clientServiceFlag": "Standard",
    "consumer": {
        "Address": {
            "Address1": "2700 Via Fortuna Drive",
            "Address2": "",
            "Address3": "",
            "City": "Austin",
            "CountryCode": "US",
            "State": "TX",
            "Zip": "78746",
        },
        "DaytimePhoneNumber": "5122256000",
        "EveningPhoneNumber": "",
        "FaxNumber": "",
        "FirstName": "testname",
        "Honorific": "",
        "LastName": "tester",
        "MiddleInitial": "",
        "PrimaryEmailAddress": "croosken@newgistics.com",
    },
    "deliveryMethod": "SelfService",
    "dispositionRuleSetId": 99,
    "labelCount": 1,
    "merchantID": "NGST",
    "returnId": "123456789A",
}
resp = ngw_client.labels.create(payload=label_payload)
resp.json()
