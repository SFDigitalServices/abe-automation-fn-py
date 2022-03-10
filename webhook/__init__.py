""" status/http init file """
import os
from datetime import datetime
import json
import logging
import traceback
import random
import pytz
import requests
import jsend
import azure.functions as func
from requests.models import Response
from shared_code.common import func_json_response, validate_access
from shared_code import noco

# pylint: disable=too-many-branches,too-many-locals,too-many-statements
def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for webhook """
    logging.info('Status processed a request.')

    statuses = {
        "UNVERIFIED_ADDRESS": 1,
        "SPOT_CHECK": 2,
        "ON_HOLD": 3,
        "SUBMITTED": 4,
        "CLOSED": 5,
        "RECORDED": 6,
        "EXISTING_CLASS": 7
    }

    # pylint: disable=too-many-nested-blocks
    try:
        validate_access(req)

        response = Response()
        if req.get_body() and len(req.get_body()):
            response.status_code = 202
            # pylint: disable=protected-access
            response._content = b'"202 Accepted"'
            print(req.get_body())
            req_json = req.get_json()
            if "status_id" in req_json and \
                "ida_submission_id" in req_json and \
                "modified_by" in req_json:
                if int(req_json["status_id"]) == statuses["SUBMITTED"] or \
                    int(req_json["status_id"]) == statuses["RECORDED"]:
                    # IF record in SUBMITTED or RECORDED status

                    submission = noco.get_by_id(
                        "IDA_SUBMISSION", int(req_json["ida_submission_id"]))

                    if submission and submission.json():

                        submission_json = submission.json()
                        print(submission_json)

                        if submission_json["IDADATA_id"]:

                            record = noco.get_by_id("IDADATA", submission_json["IDADATA_id"])

                            if record and record.json():

                                record_json = record.json()
                                print(record_json)

                                if submission_json["IDA_SUBMISSION_STATUS_id"] \
                                    == statuses["SUBMITTED"]:

                                    if record_json["IDA_CATEGORY_ID"]:

                                        new_status = statuses.get("EXISTING_CLASS")

                                    else:
                                        chance = random.randint(1,100)

                                        if chance <= int(os.getenv("SPOT_CHECK_PERCENT")):
                                            new_status = statuses.get("SPOT_CHECK")
                                        else:
                                            new_status = statuses.get("RECORDED")

                                    updates = {
                                        "IDA_SUBMISSION_STATUS_id": new_status
                                    }
                                    record = noco.update_by_id(
                                        "IDA_SUBMISSION", submission_json["ID"], updates)

                                elif submission_json["IDA_SUBMISSION_STATUS_id"] \
                                    == statuses["RECORDED"] \
                                        and submission_json["IDA_CATEGORY_ID_LOOKUP_id"]:
                                    user = req_json["modified_by"].split("@")[0]

                                    if user == "ds-admin":
                                        user = "automation"

                                    abe_num = record_json["IDAAppNum"] \
                                        if record_json["IDAAppNum"] \
                                            else generate_abe_num(submission_json["ID"])

                                    updates = {
                                        "IDA_CATEGORY_ID":
                                            submission_json["IDA_CATEGORY_ID_LOOKUP_id"],
                                        "IDAAppNum": abe_num,
                                        "LASTModifiedBy": user,
                                        "LASTModifiedDate":
                                            str(datetime.now(pytz.timezone('US/Pacific')))
                                    }
                                    print(record_json["IDA_CATEGORY_ID"])
                                    print(updates)
                                    record = noco.update_by_id(
                                        "IDADATA", record_json["ID"], updates)

                                    print(record.content)
                    response.status_code = 200
                    response._content = b'"200 TEST"'

        else:
            response.status_code = 200
            # pylint: disable=protected-access
            response._content = b'"200 OK"'

        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        return func_json_response(response, headers, "message")

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Status HTTP error occurred: %s", traceback.format_exc())
        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)

def generate_abe_num(seed:int):
    """ Generate ABE Number """
    date = datetime.now(pytz.timezone('US/Pacific')).strftime('%Y%m%d')
    new_num =  f"ABE{date}{seed % 10000:04}"
    print(f"Generated ABE Number {new_num}")
    return new_num
