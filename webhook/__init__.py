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
from shared_code import common
from shared_code import noco
from shared_code import email

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
        common.validate_access(req)

        response = common.get_http_response_by_status(500)

        if req.get_body() and len(req.get_body()):
            response = common.get_http_response_by_status(202)
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

                                    if "IDA_CATEGORY_ID" in record_json and \
                                        record_json["IDA_CATEGORY_ID"] is not None:

                                        new_status = statuses.get("EXISTING_CLASS")

                                    else:
                                        chance = random.randint(1,100)

                                        if chance <= int(os.getenv("SPOT_CHECK_PERCENT")):
                                            new_status = statuses.get("SPOT_CHECK")
                                        elif "IDA_CATEGORY_ID_LOOKUP_id" in submission_json \
                                            and submission_json["IDA_CATEGORY_ID_LOOKUP_id"] \
                                                is not None:
                                            new_status = statuses.get("RECORDED")

                                    updates = {
                                        "IDA_SUBMISSION_STATUS_id": new_status
                                    }
                                    record = noco.update_by_id(
                                        "IDA_SUBMISSION", submission_json["ID"], updates)

                                elif submission_json["IDA_SUBMISSION_STATUS_id"] \
                                    == statuses["RECORDED"] \
                                        and "IDA_CATEGORY_ID_LOOKUP_id" in submission_json \
                                            and submission_json["IDA_CATEGORY_ID_LOOKUP_id"] \
                                                is not None:
                                    print("Record Category ID:" + \
                                        str(record_json["IDA_CATEGORY_ID"]))
                                    print("Submission Category ID:" + \
                                        str(submission_json["IDA_CATEGORY_ID_LOOKUP_id"]))
                                    if "IDA_CATEGORY_ID" in record_json and \
                                        record_json["IDA_CATEGORY_ID"] is not None:
                                        if record_json["IDA_CATEGORY_ID"] != \
                                            submission_json["IDA_CATEGORY_ID_LOOKUP_id"]:

                                            new_status = statuses.get("EXISTING_CLASS")
                                            updates = {
                                                "IDA_SUBMISSION_STATUS_id": new_status
                                            }
                                            record = noco.update_by_id(
                                                "IDA_SUBMISSION", submission_json["ID"], updates)

                                    else:
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
                                            "TECHNICAL_INFEASABILITY": \
                                                submission_json["TECHNICAL_INFEASABILITY"],
                                            "UNREASONABLE_HARDSHIP": \
                                                submission_json["UNREASONABLE_HARDSHIP"],
                                            "LASTModifiedBy": user,
                                            "LASTModifiedDate":
                                                str(datetime.now(pytz.timezone('US/Pacific')))
                                        }
                                        print(record_json["IDA_CATEGORY_ID"])
                                        print(updates)
                                        record = noco.update_by_id(
                                            "IDADATA", record_json["ID"], updates)

                                        # send email to applicant
                                        address_parts = [
                                            record_json["PROPERTY_STREET_NUMBER"],
                                            record_json["PROPERTY_STREET_NAME"],
                                            record_json["PROPERTY_STREET_SFX"]
                                        ]
                                        # waived, exempt, compliant
                                        complied_category_ids = [-1, 0, 1]
                                        # non-compliant 0 step, 1 step, >1 step
                                        non_complied_category_ids = [2, 3, 4]
                                        if int(submission_json["IDA_CATEGORY_ID_LOOKUP_id"]) in \
                                            complied_category_ids + non_complied_category_ids:

                                            has_complied = \
                                                int(submission_json["IDA_CATEGORY_ID_LOOKUP_id"]) \
                                                in complied_category_ids
                                            email.send_email(
                                                submission_json["CONTACT_NAME"],
                                                submission_json["CONTACT_EMAIL"],
                                                {
                                                    "projectAddress": " ".join(address_parts),
                                                    "ABE_NUMBER": abe_num
                                                },
                                                has_complied
                                            )

                                        print(record.content)
                    response = common.get_http_response_by_status(200)

        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        return common.func_json_response(response, headers, "message")

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("ABE Webhook error occurred: %s", traceback.format_exc())
        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)

def generate_abe_num(seed:int):
    """ Generate ABE Number """
    date = datetime.now(pytz.timezone('US/Pacific')).strftime('%Y%m%d')
    new_num =  f"ABE{date}{seed % 10000:04}"
    print(f"Generated ABE Number {new_num}")
    return new_num
