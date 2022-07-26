""" Test for webhook endpoint """
# pylint: disable=redefined-outer-name,no-member,unused-argument,unused-import,too-many-locals

import os
import json
from unittest import mock
from unittest.mock import patch, Mock
import azure.functions as func
from webhook import main
from tests import mocks
from tests.fixtures import mock_env_access_key, mock_env_no_access_key, CLIENT_HEADERS

def test_function_validation_error(mock_env_no_access_key):
    """ webhook validation error """
    print("*** test_function_validation_error")

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=json.dumps(mocks.NOCO_WEBHOOK),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    resp_json = json.loads(resp.get_body())
    print(resp_json)
    # Check the output.
    assert resp_json['status'] == 'error'

@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_unverified(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with unverified status """
    print("*** test_function_unverified")

    get_requests = []
    submission_get = Mock()
    submission_get.text = json.dumps(mocks.SUBMISSION)
    submission_get.json.return_value = mocks.SUBMISSION
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata_get.text = json.dumps(mocks.IDADATA)
    idadata_get.json.return_value = mocks.IDADATA
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests
    patch_requests_put.return_value.content = json.dumps(mocks.IDADATA).encode('utf8')

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(mocks.NOCO_WEBHOOK).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 202

@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_submitted(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with submitted status """
    print("*** test_function_submitted")

    get_requests = []
    submission_get = Mock()
    submission = mocks.SUBMISSION.copy()
    submission["IDA_SUBMISSION_STATUS_id"] = 4
    submission_get.text = json.dumps(submission)
    submission_get.json.return_value = submission
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata_get.text = json.dumps(mocks.IDADATA)
    idadata_get.json.return_value = mocks.IDADATA
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests
    patch_requests_put.return_value.content = json.dumps(mocks.SUBMISSION).encode('utf8')

    # Construct a mock HTTP request.
    params = mocks.NOCO_WEBHOOK.copy()
    params["status_id"] = 4
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(params).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

@patch.dict(os.environ, {"SPOT_CHECK_PERCENT": "100"})
@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_spot_check(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with submitted status and 100% spot check """
    print("*** test_function_spot_check")

    get_requests = []
    submission_get = Mock()
    submission = mocks.SUBMISSION.copy()
    submission["IDA_SUBMISSION_STATUS_id"] = 4
    submission_get.text = json.dumps(submission)
    submission_get.json.return_value = submission
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata_get.text = json.dumps(mocks.IDADATA)
    idadata_get.json.return_value = mocks.IDADATA
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests
    patch_requests_put.return_value.content = json.dumps(mocks.IDADATA).encode('utf8')

    # Construct a mock HTTP request.
    params = mocks.NOCO_WEBHOOK.copy()
    params["status_id"] = 4
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(params).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_recorded(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with recorded status """
    print("*** test_function_recorded")

    get_requests = []
    submission_get = Mock()
    submission = mocks.SUBMISSION.copy()
    submission["IDA_SUBMISSION_STATUS_id"] = 6
    submission_get.text = json.dumps(submission)
    submission_get.json.return_value = submission
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata_get.text = json.dumps(mocks.IDADATA)
    idadata_get.json.return_value = mocks.IDADATA
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests
    patch_requests_put.return_value.content = json.dumps(mocks.IDADATA).encode('utf8')

    # Construct a mock HTTP request.
    params = mocks.NOCO_WEBHOOK.copy()
    params["status_id"] = 6
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(params).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_recorded_existing_class(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with recorded status resulting in existing_class """
    print("*** test_function_recorded_existing_class")

    get_requests = []
    submission_get = Mock()
    submission = mocks.SUBMISSION.copy()
    submission["IDA_SUBMISSION_STATUS_id"] = 6
    submission_get.text = json.dumps(submission)
    submission_get.json.return_value = submission
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata = mocks.IDADATA.copy()
    idadata["IDA_CATEGORY_ID"] = 3
    idadata_get.text = json.dumps(idadata)
    idadata_get.json.return_value = idadata
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests
    patch_requests_put.return_value.content = json.dumps(mocks.IDADATA).encode('utf8')

    # Construct a mock HTTP request.
    params = mocks.NOCO_WEBHOOK.copy()
    params["status_id"] = 6
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(params).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_submitted_existing_class(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with submitted status resulting in existing_class """
    print("*** test_function_submitted_existing_class")

    get_requests = []
    submission_get = Mock()
    submission = mocks.SUBMISSION.copy()
    submission["IDA_SUBMISSION_STATUS_id"] = 4
    submission_get.text = json.dumps(submission)
    submission_get.json.return_value = submission
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata = mocks.IDADATA.copy()
    idadata["IDA_CATEGORY_ID"] = 3
    idadata_get.text = json.dumps(idadata)
    idadata_get.json.return_value = idadata
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests
    patch_requests_put.return_value.content = json.dumps(mocks.IDADATA).encode('utf8')

    # Construct a mock HTTP request.
    params = mocks.NOCO_WEBHOOK.copy()
    params["status_id"] = 6
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(params).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

@patch('shared_code.email.requests.post')
@patch('shared_code.noco.requests.put')
@patch('shared_code.noco.requests.get')
def test_function_submitted_undelete_idata(
    patch_requests_get,
    patch_requests_put,
    patch_email,
    mock_env_access_key):
    """ success webhook get with submitted status where ida_data record was deleted """
    print("*** test_function_submitted")

    get_requests = []
    submission_get = Mock()
    submission = mocks.SUBMISSION.copy()
    submission["IDA_SUBMISSION_STATUS_id"] = 4
    submission_get.text = json.dumps(submission)
    submission_get.json.return_value = submission
    get_requests.append(submission_get)

    idadata_get = Mock()
    idadata = mocks.IDADATA.copy()
    idadata["DELETEDate"] = "2022-01-01"
    idadata_get.text = json.dumps(idadata)
    idadata_get.json.return_value = idadata
    get_requests.append(idadata_get)

    patch_requests_get.side_effect = get_requests

    put_requests = []
    idadata_put = Mock()
    idadata_put.content = json.dumps(idadata).encode('utf8')
    put_requests.append(idadata_put)

    submission_put = Mock()
    submission_put.content = json.dumps(mocks.SUBMISSION).encode('utf8')
    put_requests.append(submission_put)

    patch_requests_put.side_effect = put_requests

    # Construct a mock HTTP request.
    params = mocks.NOCO_WEBHOOK.copy()
    params["status_id"] = 4
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=json.dumps(params).encode('utf8'),
        url='/api/webhook')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200
    (_, kwargs) = patch_requests_put.call_args_list[0]
    assert kwargs['json'] == {"DELETEDate": None}
