"""
write_shopfloor_monitor_service_tests.py

Script to automatically generate a service test for each type of Shopfloor
Monitor query.
"""

# Nose should not run this when it is runing tests.
__test__ = False

import os
import requests, pprint

from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules.test import utility_functions_for_testing

from CML_Pickpack.pickpack_modules.test.write_endpoint_tests import BASE_FILE_PATH, BASE_URL, REQUESTS_TIMEOUT

FILE_PATH = os.path.join(BASE_FILE_PATH,
                         'test_shopfloor_monitor_service.py',
                        )
SERVICE_URL = BASE_URL + '/shopfloor_monitor/j_status_orders'


WORKSTATION_DICT = {
    "wcc"       : pickpack_constants.CONSUMABLES_SCALE,
    "parts"     : pickpack_constants.SERVICE_PARTS_SCALE,
    "both"      : pickpack_constants.BOTH_SCALE,
    "all"       : pickpack_constants.ALL_SCALES,
}


HEADER = '''# pylint: disable=too-many-lines,too-many-public-methods,line-too-long,missing-docstring
"""
Tests for the Shopfloor Monitor service.

DO NOT EDIT THIS FILE
IT IS AUTOMATICALLY GENERATED
BY write_shopfloor_monitor_service_tests.py



"""

import requests
from nose import tools

from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules.test import utility_functions_for_testing

from CML_Pickpack.pickpack_modules.test.write_endpoint_tests import REQUESTS_TIMEOUT

if pickpack_constants.SHOW_FULL_DIFF:
    # Force Nose to output the full diff
    from unittest import TestCase
    TestCase.maxDiff = None


class TestShopfloorMonitorService(object):


    def __init__(self):
        pass
'''


CALL_TEMPLATE = '''
    @staticmethod
    def call_summary_service(scale,
                             show_backorder,
                             expected_result,
                            ):
        """
        Call the Shopfloor Monitor summary service
        """
        parameters = {{'scale' : scale,
                      'show_backorder' : show_backorder,
                     }}
        response = requests.get('{service_url}',
                                params = parameters,
                                timeout = REQUESTS_TIMEOUT,
                               )
        actual_result = utility_functions_for_testing.read_json_from_response(response)
        tools.assert_equal(actual_result, expected_result)

'''


TEST_TEMPLATE = '''
    def test_{workstation}_{show_backorder_text}(self):
        expected_result = {expected_result}
        self.call_summary_service('{workstation}',
                                  '{show_backorder}',
                                  expected_result,
                                 )

'''


def main():
    """
    Main function
    """
    write_tests()

def write_tests():
    """
    Call the given service and get a response. Create a test based on that
    response. Write that test to the file.
    """

    shipping_stations = ("wcc", "parts", "both", "all")
    ordinary_or_backorder = ("true", "false")

    with open(FILE_PATH, 'w') as file_object:
        file_object.write(HEADER)
        file_object.write(CALL_TEMPLATE.format(service_url = SERVICE_URL)
                         )
        for shipping_station_code in shipping_stations:
            for o_or_b in ordinary_or_backorder:
                write_summary_test(file_object,
                                   shipping_station_code,
                                   o_or_b,
                                  )










def write_summary_test(file_object,
                       shipping_station_code,
                       o_or_b,
                      ):
    """
    Generate the code for a test, based on a template. Write the test out to the
    file.
    """
    parameters = {'scale' : shipping_station_code,
                  'show_backorder' : o_or_b,
                 }
    response = requests.get(SERVICE_URL,
                            params = parameters,
                            timeout = REQUESTS_TIMEOUT,
                           )

    try:
        expected_result = pprint.pformat(utility_functions_for_testing.read_json_from_response(response))
    except ValueError:
        print "=============================================="
        print "=============================================="
        print "Error while writing test for %s" % shipping_station_code
        print "=============================================="
        print "=============================================="
        raise

    if o_or_b == "true":
        show_backorder_text = 'backorder'
    else:
        show_backorder_text = 'ordinary'

    output = TEST_TEMPLATE.format(workstation = shipping_station_code,
                                  show_backorder = o_or_b,
                                  show_backorder_text = show_backorder_text,
                                  expected_result = expected_result,
                                 )

    file_object.write(output)





if __name__ == '__main__':
    main()
