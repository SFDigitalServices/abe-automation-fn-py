""" blocklot init file """
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

fields = [
    "BLOCK",
    "LOT"
]

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ update combined blocklot field """
    logging.info('Processing blocklot endpoint request')

    try:
        common.validate_access(req)

        response = common.get_http_response_by_status(200)

        req_body = req.get_body()
        if req_body and len(req_body):
            response = common.get_http_response_by_status(202)

            req_json = req.get_json()
            print(f"req_json: {req_json}")

            blocklot = common.combine_fields(fields, req_json, "")

            if req_json["BLOCKLOT"] != blocklot:
                updates = {
                    "BLOCKLOT": blocklot
                }
                print(f'updates: {updates}')
                noco.update_by_id("IDADATA", req_json["idadata_id"], updates)

        return common.func_json_response(
            response,
            {"Access-Control-Allow-Origin": "*"},
            "message")

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Blocklot concatenation error occurred: %s", traceback.format_exc())
        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
