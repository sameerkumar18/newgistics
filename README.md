What it solves:
1. No need to interact with XML responses, the package internally handles translates XML responses and requests
2. 

Scope:
1. Handles few parts of the Newgistics API like
 Shipments in Newgistics Web API and Inbound Returns, Shipments, Returns 
 in Newgistics Fulfillment API

Input: payload, params
Output: requests Response object where you can play with it like resp.status_code, resp.json()

Limited Scope:
    1. Covers only the following APIs

Project Roadmap:
    1. Cover more APIs from both Web & Fulfillment
    2. Return better objects, eg: every function returns a python requests's Response object
    3. Overall code improvements like better error handling since these APIs 