"""
Tests for the Shopfloor Monitor service

"""
# pylint: disable=too-many-lines,too-many-public-methods,line-too-long,missing-docstring

import requests
from nose import tools

from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules.test import utility_functions_for_testing

if pickpack_constants.SHOW_FULL_DIFF:
    # Force Nose to output the full diff
    from unittest import TestCase
    TestCase.maxDiff = None

class ShopfloorMonitorOrderStatusService(object):
    def call_service(self,
                     shipping_station,
                     expected_result,
                    ):
        """
        Call the Shopfloor Monitor service
        """
        parameters = {'scale' : shipping_station,
                      'show_backorder' : self.show_backorder,                   # pylint: disable=no-member
                     }
        response = requests.get('http://partsappdev.joco.com:8082/shopfloor_monitor/j_status_orders',
                                params = parameters,
                               )
        actual_result = utility_functions_for_testing.read_json_from_response(response)
        tools.assert_equal(actual_result, expected_result)


class TestShopfloorMonitorOrderStatusServiceOrdinary(ShopfloorMonitorOrderStatusService):
    def __init__(self):
        ShopfloorMonitorOrderStatusService.__init__(self)
        self.show_backorder = "false"

    def test1(self):
        shipping_station = 'all'
        expected_result = {
            u'today_sure_can_ship_tomorrow_ready_to_print': 7,
            u'today_sure_can_ship_tomorrow_pick_slip_printed': 4,
            u'today_sure_can_ship_tomorrow_packed': 1,
            u'today_sure_should_ship_today_ready_to_print': 21,
            u'today_sure_should_ship_today_pick_slip_printed': 16,
            u'today_sure_should_ship_today_packed': 2,
            u'signature_service_can_ship_tomorrow_ready_to_print': 127,
            u'signature_service_can_ship_tomorrow_pick_slip_printed': 47,
            u'signature_service_can_ship_tomorrow_packed': 10,
            u'signature_service_should_ship_today_ready_to_print': 531,
            u'signature_service_should_ship_today_pick_slip_printed': 29,
            u'signature_service_should_ship_today_packed': 10,
            u'service_files_should_ship_today_ready_to_print': 47,
            u'service_files_should_ship_today_pick_slip_printed': 22,
            u'service_files_should_ship_today_packed': 3,
            u'normal_can_ship_tomorrow_ready_to_print': 21,
            u'normal_can_ship_tomorrow_pick_slip_printed': 3,
            u'normal_can_ship_tomorrow_packed': 0,
            u'normal_should_ship_today_ready_to_print': 361,
            u'normal_should_ship_today_pick_slip_printed': 50,
            u'normal_should_ship_today_packed': 5,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test2(self):
        shipping_station = 'wcc'
        expected_result = {
            u'today_sure_can_ship_tomorrow_ready_to_print': 3,
            u'today_sure_can_ship_tomorrow_pick_slip_printed': 3,
            u'today_sure_can_ship_tomorrow_packed': 1,
            u'today_sure_should_ship_today_ready_to_print': 7,
            u'today_sure_should_ship_today_pick_slip_printed': 10,
            u'today_sure_should_ship_today_packed': 0,
            u'signature_service_can_ship_tomorrow_ready_to_print': 43,
            u'signature_service_can_ship_tomorrow_pick_slip_printed': 33,
            u'signature_service_can_ship_tomorrow_packed': 1,
            u'signature_service_should_ship_today_ready_to_print': 475,
            u'signature_service_should_ship_today_pick_slip_printed': 10,
            u'signature_service_should_ship_today_packed': 3,
            u'service_files_should_ship_today_ready_to_print': 8,
            u'service_files_should_ship_today_pick_slip_printed': 14,
            u'service_files_should_ship_today_packed': 0,
            u'normal_can_ship_tomorrow_ready_to_print': 3,
            u'normal_can_ship_tomorrow_pick_slip_printed': 3,
            u'normal_can_ship_tomorrow_packed': 0,
            u'normal_should_ship_today_ready_to_print': 221,
            u'normal_should_ship_today_pick_slip_printed': 21,
            u'normal_should_ship_today_packed': 3,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test3(self):
        shipping_station = 'parts'
        expected_result = {
            u'today_sure_can_ship_tomorrow_ready_to_print': 2,
            u'today_sure_can_ship_tomorrow_pick_slip_printed': 1,
            u'today_sure_can_ship_tomorrow_packed': 0,
            u'today_sure_should_ship_today_ready_to_print': 8,
            u'today_sure_should_ship_today_pick_slip_printed': 6,
            u'today_sure_should_ship_today_packed': 1,
            u'signature_service_can_ship_tomorrow_ready_to_print': 65,
            u'signature_service_can_ship_tomorrow_pick_slip_printed': 14,
            u'signature_service_can_ship_tomorrow_packed': 7,
            u'signature_service_should_ship_today_ready_to_print': 29,
            u'signature_service_should_ship_today_pick_slip_printed': 17,
            u'signature_service_should_ship_today_packed': 2,
            u'service_files_should_ship_today_ready_to_print': 28,
            u'service_files_should_ship_today_pick_slip_printed': 8,
            u'service_files_should_ship_today_packed': 1,
            u'normal_can_ship_tomorrow_ready_to_print': 16,
            u'normal_can_ship_tomorrow_pick_slip_printed': 0,
            u'normal_can_ship_tomorrow_packed': 0,
            u'normal_should_ship_today_ready_to_print': 106,
            u'normal_should_ship_today_pick_slip_printed': 8,
            u'normal_should_ship_today_packed': 1,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test4(self):
        shipping_station = 'both'
        expected_result = {
            u'today_sure_can_ship_tomorrow_ready_to_print': 2,
            u'today_sure_can_ship_tomorrow_pick_slip_printed': 0,
            u'today_sure_can_ship_tomorrow_packed': 0,
            u'today_sure_should_ship_today_ready_to_print': 6,
            u'today_sure_should_ship_today_pick_slip_printed': 0,
            u'today_sure_should_ship_today_packed': 1,
            u'signature_service_can_ship_tomorrow_ready_to_print': 19,
            u'signature_service_can_ship_tomorrow_pick_slip_printed': 0,
            u'signature_service_can_ship_tomorrow_packed': 2,
            u'signature_service_should_ship_today_ready_to_print': 27,
            u'signature_service_should_ship_today_pick_slip_printed': 2,
            u'signature_service_should_ship_today_packed': 5,
            u'service_files_should_ship_today_ready_to_print': 11,
            u'service_files_should_ship_today_pick_slip_printed': 0,
            u'service_files_should_ship_today_packed': 2,
            u'normal_can_ship_tomorrow_ready_to_print': 2,
            u'normal_can_ship_tomorrow_pick_slip_printed': 0,
            u'normal_can_ship_tomorrow_packed': 0,
            u'normal_should_ship_today_ready_to_print': 34,
            u'normal_should_ship_today_pick_slip_printed': 21,
            u'normal_should_ship_today_packed': 1,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test5(self):
        shipping_station = '4up'
        expected_result = {
            'all' : {
                u'today_sure_can_ship_tomorrow_ready_to_print': 7,
                u'today_sure_can_ship_tomorrow_pick_slip_printed': 4,
                u'today_sure_can_ship_tomorrow_packed': 1,
                u'today_sure_should_ship_today_ready_to_print': 21,
                u'today_sure_should_ship_today_pick_slip_printed': 16,
                u'today_sure_should_ship_today_packed': 2,
                u'signature_service_can_ship_tomorrow_ready_to_print': 127,
                u'signature_service_can_ship_tomorrow_pick_slip_printed': 47,
                u'signature_service_can_ship_tomorrow_packed': 10,
                u'signature_service_should_ship_today_ready_to_print': 531,
                u'signature_service_should_ship_today_pick_slip_printed': 29,
                u'signature_service_should_ship_today_packed': 10,
                u'service_files_should_ship_today_ready_to_print': 47,
                u'service_files_should_ship_today_pick_slip_printed': 22,
                u'service_files_should_ship_today_packed': 3,
                u'normal_can_ship_tomorrow_ready_to_print': 21,
                u'normal_can_ship_tomorrow_pick_slip_printed': 3,
                u'normal_can_ship_tomorrow_packed': 0,
                u'normal_should_ship_today_ready_to_print': 361,
                u'normal_should_ship_today_pick_slip_printed': 50,
                u'normal_should_ship_today_packed': 5,
            },
            'wcc' : {
                u'today_sure_can_ship_tomorrow_ready_to_print': 3,
                u'today_sure_can_ship_tomorrow_pick_slip_printed': 3,
                u'today_sure_can_ship_tomorrow_packed': 1,
                u'today_sure_should_ship_today_ready_to_print': 7,
                u'today_sure_should_ship_today_pick_slip_printed': 10,
                u'today_sure_should_ship_today_packed': 0,
                u'signature_service_can_ship_tomorrow_ready_to_print': 43,
                u'signature_service_can_ship_tomorrow_pick_slip_printed': 33,
                u'signature_service_can_ship_tomorrow_packed': 1,
                u'signature_service_should_ship_today_ready_to_print': 475,
                u'signature_service_should_ship_today_pick_slip_printed': 10,
                u'signature_service_should_ship_today_packed': 3,
                u'service_files_should_ship_today_ready_to_print': 8,
                u'service_files_should_ship_today_pick_slip_printed': 14,
                u'service_files_should_ship_today_packed': 0,
                u'normal_can_ship_tomorrow_ready_to_print': 3,
                u'normal_can_ship_tomorrow_pick_slip_printed': 3,
                u'normal_can_ship_tomorrow_packed': 0,
                u'normal_should_ship_today_ready_to_print': 221,
                u'normal_should_ship_today_pick_slip_printed': 21,
                u'normal_should_ship_today_packed': 3,
            },
            'parts' : {
                u'today_sure_can_ship_tomorrow_ready_to_print': 2,
                u'today_sure_can_ship_tomorrow_pick_slip_printed': 1,
                u'today_sure_can_ship_tomorrow_packed': 0,
                u'today_sure_should_ship_today_ready_to_print': 8,
                u'today_sure_should_ship_today_pick_slip_printed': 6,
                u'today_sure_should_ship_today_packed': 1,
                u'signature_service_can_ship_tomorrow_ready_to_print': 65,
                u'signature_service_can_ship_tomorrow_pick_slip_printed': 14,
                u'signature_service_can_ship_tomorrow_packed': 7,
                u'signature_service_should_ship_today_ready_to_print': 29,
                u'signature_service_should_ship_today_pick_slip_printed': 17,
                u'signature_service_should_ship_today_packed': 2,
                u'service_files_should_ship_today_ready_to_print': 28,
                u'service_files_should_ship_today_pick_slip_printed': 8,
                u'service_files_should_ship_today_packed': 1,
                u'normal_can_ship_tomorrow_ready_to_print': 16,
                u'normal_can_ship_tomorrow_pick_slip_printed': 0,
                u'normal_can_ship_tomorrow_packed': 0,
                u'normal_should_ship_today_ready_to_print': 106,
                u'normal_should_ship_today_pick_slip_printed': 8,
                u'normal_should_ship_today_packed': 1,
            },
            'both' : {
                u'today_sure_can_ship_tomorrow_ready_to_print': 2,
                u'today_sure_can_ship_tomorrow_pick_slip_printed': 0,
                u'today_sure_can_ship_tomorrow_packed': 0,
                u'today_sure_should_ship_today_ready_to_print': 6,
                u'today_sure_should_ship_today_pick_slip_printed': 0,
                u'today_sure_should_ship_today_packed': 1,
                u'signature_service_can_ship_tomorrow_ready_to_print': 19,
                u'signature_service_can_ship_tomorrow_pick_slip_printed': 0,
                u'signature_service_can_ship_tomorrow_packed': 2,
                u'signature_service_should_ship_today_ready_to_print': 27,
                u'signature_service_should_ship_today_pick_slip_printed': 2,
                u'signature_service_should_ship_today_packed': 5,
                u'service_files_should_ship_today_ready_to_print': 11,
                u'service_files_should_ship_today_pick_slip_printed': 0,
                u'service_files_should_ship_today_packed': 2,
                u'normal_can_ship_tomorrow_ready_to_print': 2,
                u'normal_can_ship_tomorrow_pick_slip_printed': 0,
                u'normal_can_ship_tomorrow_packed': 0,
                u'normal_should_ship_today_ready_to_print': 34,
                u'normal_should_ship_today_pick_slip_printed': 21,
                u'normal_should_ship_today_packed': 1,
            },
        }
        self.call_service(shipping_station,
                          expected_result,
                         )


class TestShopfloorMonitorOrderStatusServiceBackorder(ShopfloorMonitorOrderStatusService):
    def __init__(self):
        ShopfloorMonitorOrderStatusService.__init__(self)
        self.show_backorder = "true"

    def test1(self):
        shipping_station = 'all'
        expected_result = {
            u'today_sure_backorder_ready_to_print': 8,
            u'today_sure_backorder_pick_slip_printed': 1,
            u'today_sure_backorder_packed': 0,
            u'signature_service_backorder_ready_to_print': 151,
            u'signature_service_backorder_pick_slip_printed': 26,
            u'signature_service_backorder_packed': 4,
            u'service_files_backorder_ready_to_print': 50,
            u'service_files_backorder_pick_slip_printed': 17,
            u'service_files_backorder_packed': 2,
            u'normal_backorder_ready_to_print': 22,
            u'normal_backorder_pick_slip_printed': 1,
            u'normal_backorder_packed': 0,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test2(self):
        shipping_station = 'wcc'
        expected_result = {
            u'today_sure_backorder_ready_to_print': 5,
            u'today_sure_backorder_pick_slip_printed': 1,
            u'today_sure_backorder_packed': 0,
            u'signature_service_backorder_ready_to_print': 57,
            u'signature_service_backorder_pick_slip_printed': 16,
            u'signature_service_backorder_packed': 3,
            u'service_files_backorder_ready_to_print': 6,
            u'service_files_backorder_pick_slip_printed': 14,
            u'service_files_backorder_packed': 1,
            u'normal_backorder_ready_to_print': 4,
            u'normal_backorder_pick_slip_printed': 1,
            u'normal_backorder_packed': 0,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test3(self):
        shipping_station = 'parts'
        expected_result = {
            u'today_sure_backorder_ready_to_print': 2,
            u'today_sure_backorder_pick_slip_printed': 0,
            u'today_sure_backorder_packed': 0,
            u'signature_service_backorder_ready_to_print': 75,
            u'signature_service_backorder_pick_slip_printed': 10,
            u'signature_service_backorder_packed': 0,
            u'service_files_backorder_ready_to_print': 34,
            u'service_files_backorder_pick_slip_printed': 2,
            u'service_files_backorder_packed': 0,
            u'normal_backorder_ready_to_print': 15,
            u'normal_backorder_pick_slip_printed': 0,
            u'normal_backorder_packed': 0,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test4(self):
        shipping_station = 'both'
        expected_result = {
            u'today_sure_backorder_ready_to_print': 1,
            u'today_sure_backorder_pick_slip_printed': 0,
            u'today_sure_backorder_packed': 0,
            u'signature_service_backorder_ready_to_print': 19,
            u'signature_service_backorder_pick_slip_printed': 0,
            u'signature_service_backorder_packed': 1,
            u'service_files_backorder_ready_to_print': 10,
            u'service_files_backorder_pick_slip_printed': 1,
            u'service_files_backorder_packed': 1,
            u'normal_backorder_ready_to_print': 3,
            u'normal_backorder_pick_slip_printed': 0,
            u'normal_backorder_packed': 0,
        }
        self.call_service(shipping_station,
                          expected_result,
                         )

    def test5(self):
        shipping_station = '4up'
        expected_result = {
            u'all' : {
                u'today_sure_backorder_ready_to_print': 8,
                u'today_sure_backorder_pick_slip_printed': 1,
                u'today_sure_backorder_packed': 0,
                u'signature_service_backorder_ready_to_print': 151,
                u'signature_service_backorder_pick_slip_printed': 26,
                u'signature_service_backorder_packed': 4,
                u'service_files_backorder_ready_to_print': 50,
                u'service_files_backorder_pick_slip_printed': 17,
                u'service_files_backorder_packed': 2,
                u'normal_backorder_ready_to_print': 22,
                u'normal_backorder_pick_slip_printed': 1,
                u'normal_backorder_packed': 0,
            },
            u'wcc' : {
                u'today_sure_backorder_ready_to_print': 5,
                u'today_sure_backorder_pick_slip_printed': 1,
                u'today_sure_backorder_packed': 0,
                u'signature_service_backorder_ready_to_print': 57,
                u'signature_service_backorder_pick_slip_printed': 16,
                u'signature_service_backorder_packed': 3,
                u'service_files_backorder_ready_to_print': 6,
                u'service_files_backorder_pick_slip_printed': 14,
                u'service_files_backorder_packed': 1,
                u'normal_backorder_ready_to_print': 4,
                u'normal_backorder_pick_slip_printed': 1,
                u'normal_backorder_packed': 0,
            },
            u'parts' : {
                u'today_sure_backorder_ready_to_print': 2,
                u'today_sure_backorder_pick_slip_printed': 0,
                u'today_sure_backorder_packed': 0,
                u'signature_service_backorder_ready_to_print': 75,
                u'signature_service_backorder_pick_slip_printed': 10,
                u'signature_service_backorder_packed': 0,
                u'service_files_backorder_ready_to_print': 34,
                u'service_files_backorder_pick_slip_printed': 2,
                u'service_files_backorder_packed': 0,
                u'normal_backorder_ready_to_print': 15,
                u'normal_backorder_pick_slip_printed': 0,
                u'normal_backorder_packed': 0,
            },
            u'both' : {
                u'today_sure_backorder_ready_to_print': 1,
                u'today_sure_backorder_pick_slip_printed': 0,
                u'today_sure_backorder_packed': 0,
                u'signature_service_backorder_ready_to_print': 19,
                u'signature_service_backorder_pick_slip_printed': 0,
                u'signature_service_backorder_packed': 1,
                u'service_files_backorder_ready_to_print': 10,
                u'service_files_backorder_pick_slip_printed': 1,
                u'service_files_backorder_packed': 1,
                u'normal_backorder_ready_to_print': 3,
                u'normal_backorder_pick_slip_printed': 0,
                u'normal_backorder_packed': 0,
            },
        }
        self.call_service(shipping_station,
                          expected_result,
                         )
