""" Common shared functions """
import os
import json
import jsend
import azure.functions as func

def func_json_response(response, headers=None, json_root="items"):
    """ json func_json_response """
    json_data = json.loads(response.text)

    if response.status_code == 200:
        func_response = json.dumps(jsend.success({json_root: json_data}))
    else:
        func_response = json.dumps(json_data)

    func_status_code = response.status_code

    return func.HttpResponse(
        func_response,
        status_code=func_status_code,
        mimetype="application/json",
        headers=headers
    )

def validate_access(req: func.HttpRequest):
    """ validate access method """
    access_key = os.getenv('ACCESS_KEY')
    print(access_key)
    verify_key = req.headers.get('x-api-key') if req.headers.get('x-api-key') \
        else req.headers.get('ACCESS_KEY')
    if not access_key or verify_key != access_key:
        raise ValueError("Access Denied")
