""" NocoDB functions """
import os
import requests

def get_by_id(table, idn):
    """ get record by id number """
    noco_api = os.getenv('NOCO_API_URL')
    noco_request_url = f"{noco_api}{table}/{idn}"
    print(f"noco_request_url: {noco_request_url}")
    response = requests.get(
        noco_request_url,
        headers={'xc-auth': os.getenv('NOCO_API_KEY')}
    )
    response.raise_for_status()
    return response

def update_by_id(table, idn, fields):
    """ Update record by id """
    noco_api = os.getenv('NOCO_API_URL')
    noco_request_url = f"{noco_api}{table}/{idn}"
    print(f"update_by_id fields: {fields}")
    response = requests.put(
        noco_request_url,
        headers={'xc-auth': os.getenv('NOCO_API_KEY')},
        json=fields
    )
    response.raise_for_status()
    return response
