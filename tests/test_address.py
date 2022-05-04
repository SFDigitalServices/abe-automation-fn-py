""" Test for address endpoint """
# pylint: disable=redefined-outer-name,no-member,unused-argument,unused-import

import os
import json
from unittest import mock
from unittest.mock import patch, Mock
import azure.functions as func
from address import main
from tests import mocks
from tests.fixtures import mock_env_access_key, mock_env_no_access_key, CLIENT_HEADERS

def test_function_validation_error(mock_env_no_access_key):
    """ address validation error """
    print("*** test_function_validation_error")

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=json.dumps(mocks.NOCO_WEBHOOK),
        url='/api/address')

    # Call the function.
    resp = main(req)

    resp_json = json.loads(resp.get_body())
    print(resp_json)
    # Check the output.
    assert resp_json['status'] == 'error'

@patch('shared_code.noco.requests.put')
def test_function_success(
    patch_requests_put,
    mock_env_access_key):
    """ successful address post """
    print("*** test_function_success")

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        headers=CLIENT_HEADERS,
        body=json.dumps(mocks.ADDRESS_POST).encode('utf8'),
        url='/api/address')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 202
