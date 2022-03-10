""" NocoDB functions """
import os
import requests

def get_by_id(table, idn):
    """ get record by id number """
    noco_api = os.getenv('NOCO_API_URL')
    noco_request_url = f"{noco_api}{table}/{idn}"
    print(noco_request_url)
    response = requests.get(
        noco_request_url,
        headers={'xc-auth': os.getenv('NOCO_API_KEY')}
    )
    return response

def update_by_id(table, idn, fields):
    """ Update record by id """
    noco_api = os.getenv('NOCO_API_URL')
    noco_request_url = f"{noco_api}{table}/{idn}"
    print(fields)
    response = requests.put(
        noco_request_url,
        headers={'xc-auth': os.getenv('NOCO_API_KEY')},
        json=fields
    )
    return response
