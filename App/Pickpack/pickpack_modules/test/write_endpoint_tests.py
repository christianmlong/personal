"""
write_endpoint_tests.py

Script to automatically generate a test for each mock order in
pickpack_data_mock.
"""

# Nose should not run this when it is runing tests.
__test__ = False

import requests, pprint, os.path
import sys, os

from Pickpack.pickpack_modules.pickpack_data_mock import MOCK_ORDERS
from Pickpack.pickpack_modules.test import utility_functions_for_testing

NONEXISTENT_ORDERS = ['AB00100',
                      'AB00200',
                      'ZXXY700',
                      '0000000',
                      '1111100',
                      '9999900',
                      'AAAAA00',
                      'ZZZZZ00',
                     ]


BASE_FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

# BASE_URL = 'http://partsdev01.joco2.com:8082'
# REQUESTS_TIMEOUT = 4

BASE_URL = 'http://10.52.121.146:8082'
REQUESTS_TIMEOUT = 0.1


HEADER_TEMPLATE = '''# pylint: disable=too-many-lines,too-many-public-methods,line-too-long
"""
Tests for the {service_name} service

DO NOT EDIT THIS FILE
IT IS AUTOMATICALLY GENERATED
BY {generator_filename}

"""

import requests
from nose import tools

from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules.test import utility_functions_for_testing

from Pickpack.pickpack_modules.test.write_endpoint_tests import REQUESTS_TIMEOUT


if pickpack_constants.SHOW_FULL_DIFF:
    # Force Nose to output the full diff
    from unittest import TestCase
    TestCase.maxDiff = None

class Test{service_name}Service(object):
    def __init__(self):
        pass
'''

CALL_SERVICE_TEMPLATE = '''    @staticmethod
    def call_service(order_id_scan,
                     expected_result,
                    ):
        """
        Call the {service_name} service
        """
        parameters = {{'order_id_scan' : order_id_scan}}
        response = requests.get('{service_url}',
                                params = parameters,
                                timeout = REQUESTS_TIMEOUT,
                               )
        actual_result = utility_functions_for_testing.read_json_from_response(response)
        tools.assert_equal(actual_result, expected_result)
'''

TEST_TEMPLATE = """
    def test{order_id_scan}(self):
        order_id_scan = '{order_id_scan}'
        expected_result = {expected_result}
        self.call_service(order_id_scan, expected_result)
"""

def write_tests(service_name,
                generator_filename,
                service_url_path,
               ):
    """
    Call the given endpoint and get a response. Create a test based on that response.
    Write that test to the file.
    """
    service_url = "%s/%s" % (BASE_URL, service_url_path)

    header = HEADER_TEMPLATE.format(
        service_name = service_name,
        generator_filename = generator_filename,
    )
    call_service = CALL_SERVICE_TEMPLATE.format(
        service_name = service_name,
        service_url = service_url,
    )
    test_file_path = os.path.join(BASE_FILE_PATH,
                                  "test_%s_service.py" % service_name.lower(),
                                 )

    my_mock_orders = list(MOCK_ORDERS)
    my_mock_orders.sort()

    with open(test_file_path, 'w') as file_object:
        file_object.write(header)
        file_object.write(call_service)
        for order_id_scan in my_mock_orders:
            write_test(file_object,
                       order_id_scan,
                       service_url,
                      )
        for order_id_scan in NONEXISTENT_ORDERS:
            write_test(file_object,
                       order_id_scan,
                       service_url,
                      )

def write_test(file_object,
               order_id_scan,
               service_url,
              ):
    """
    Generate the code for a test, based on a template. Write the test out to the
    file.
    """
    parameters = {'order_id_scan' : order_id_scan}
    response = requests.get(service_url,
                            params = parameters,
                            timeout = REQUESTS_TIMEOUT,
                           )

    try:
        expected_result = pprint.pformat(utility_functions_for_testing.read_json_from_response(response))
    except ValueError:
        print "=============================================="
        print "=============================================="
        print "Error while writing test for %s" % order_id_scan
        print "=============================================="
        print "=============================================="
        raise

    output = TEST_TEMPLATE.format(order_id_scan = order_id_scan,
                                  expected_result = expected_result,
                                 )

    file_object.write(output)
