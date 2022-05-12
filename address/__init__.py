""" address init file """
import os
import json
import logging
import traceback
from http import client
import requests
import jsend
import azure.functions as func
from requests.models import Response
from shared_code import common
from shared_code import noco

address_fields = [
    "PROPERTYStreetNumber",
    "PROPERTYStreetNumberSfx",
    "PROPERTYStreetName",
    "PROPERTYStreetSfx",
    "PROPERTYUnit",
    "PROPERTYUnitSfx"
]

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ update combined address field """
    logging.info('Processing address endpoint request')

    try:
        common.validate_access(req)

        response = common.get_http_response_by_status(200)

        req_body = req.get_body()
        print(f"request.get_body(): {req.get_body()}")
        if req_body and len(req_body):
            response = common.get_http_response_by_status(202)

            req_json = req.get_json()
            print(f"request.get_json(): {req_json}")

            address_values = []
            for field in address_fields:
                address_values.append(req_json.get(field, None))
            address = " ".join(filter(None, address_values))

            if req_json["FULL_ADDRESS"] != address:
                updates = {
                    "FULL_ADDRESS": address
                }
                print(f'updates: {updates}')
                noco.update_by_id("IDADATA", req_json["idadata_id"], updates)

        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        return common.func_json_response(response, headers, "message")

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Address concatenation error occurred: %s", traceback.format_exc())
        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
