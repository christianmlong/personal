"""
Tests for the functions in the pickpack_common.py module
"""
from nose import tools, twistedtools

from Common.utility import utl_aplus

#from Pickpack.pickpack_modules import pickpack_common
from Pickpack.pickpack_modules import pickpack_data_mock
#from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules import pickpack_constants

#from Pickpack.pickpack_modules.test.utility_classes_for_testing import HandleableServerException

if pickpack_constants.SHOW_FULL_DIFF:
    # Force Nose to output the full diff
    from unittest import TestCase
    TestCase.maxDiff = None




# POSSIBLE IMPROVEMENT Write tests for pickpack_utility_classes.PackingListContainer and PackingListItem
#
#
#
#def testAddDataToPackingList():
#    """
#    Test the system that adds a column of data to the packing list.
#    """
#
#    b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#    c = ['a', 'b', 'c']
#
#    # Repeated calls should yield the same result
#    for ignore_i in range(2):
#        result = pickpack_common.addDataToPackingList(b, c)
#        tools.assert_equal(b,
#                           [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
#                          )
#        tools.assert_equal(result,
#                           [[1, 2, 'a'], [4, 5, 'b'], [7, 8, 'c']],
#                          )
#
#        # Some fancy footwork with zip. The first * means
#        # spread-out-the-iterable. The second * is a multiplication sign. Here
#        # it repeats iterable c three times.
#        #
#        # zip(*[c]*3)
#        # [('a', 'a', 'a'), ('b', 'b', 'b'), ('c', 'c', 'c')]
#        result = pickpack_common.addDataToPackingList(b, zip(*[c]*3))
#        tools.assert_equal(b,
#                           [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
#                          )
#        tools.assert_equal(result,
#                           [[1, 2, 'a', 'a', 'a'],
#                            [4, 5, 'b', 'b', 'b'],
#                            [7, 8, 'c', 'c', 'c'],
#                           ],
#                          )
#
#    d = ['e', 'f', 'g', 'h']
#    with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
#        result = pickpack_common.addDataToPackingList(b, d)
#
#    exception = context_mgr.exception
#    tools.assert_equal(exception.message,
#                       "Error: the two lists are not the same length.",
#                      )






# Note: If we don't use nose's twisted integration, the defereds will raise
# errors, but nose will not count them in the overall pass/fail.
#
#def try_server_exception2(order_id,
#                         err_msg,
#                        ):
#    """
#    Run one test of the server exception
#    """
#    HandleableServerException(
#        order_id,
#        err_msg,
#    ).try_handleable_server_error()

# Use Nose's Twisted integration
@twistedtools.deferred()
def try_server_exception(order_number,
                         expected_error_message,
                        ):
    """
    Run one test of the server exception
    """

    def try_handleable_server_error_deferred(result):
        """
        Handle the result of the deferred. Make sure it matches the expected
        result.
        """
        actual_error_message = result['server_error']
        tools.assert_equal(expected_error_message,
                           actual_error_message,
                          )

    order_id = utl_aplus.order_id_from_barcode_scan(order_number)
    deferred = pickpack_data_mock.getPackingList_deferred(order_id,
                                                          None,
                                                         )
    deferred.addCallback(try_handleable_server_error_deferred)
    return deferred

def test_server_exception1():
    order_scan = 'AA60100'
    try_server_exception(order_scan,
                         "Order AA601/00 is on Warehouse Hold. Do not ship.",
                        )

def test_server_exception2():
    order_scan = 'AA60200'
    try_server_exception(order_scan,
                         "Order AA602/00 is on Warehouse Hold. Do not ship.",
                        )

def test_server_exception3():
    order_scan = 'AA60300'
    try_server_exception(order_scan,
                         "Order AA603/00 is on Warehouse Hold. Do not ship.",
                        )

def test_server_exception4():
    order_scan = 'AA61100'
    try_server_exception(order_scan,
                         "Order AA611/00 has one or more items that have not been picked. Items: 238626.",
                        )

def test_server_exception5():
    order_scan = 'AA61200'
    try_server_exception(order_scan,
                         "Order AA612/00 has one or more items that have not been picked. Items: 244094.",
                        )

def test_server_exception6():
    order_scan = 'AA61300'
    try_server_exception(order_scan,
                         "Order AA613/00 has one or more items that have not been picked. Items: 149962, 155454, 172075, 231921.",
                        )

def test_server_exception7():
    order_scan = 'AA61401'
    try_server_exception(order_scan,
                         "Order AA614/01 has one or more items that have not been picked. Items: 149962, 155454, 231921, 231921, 231921.",
                        )

def test_server_exception8():
    order_scan = 'AA70000'
    try_server_exception(order_scan,
                         "Order AA700/00 has an invalid service level: . Should be T, SS, S or N.",
                        )

def test_server_exception9():
    order_scan = 'AA70001'
    try_server_exception(order_scan,
                         "Order AA700/01 has an invalid service level: X. Should be T, SS, S or N.",
                        )

#def test_server_exception10():
#    order_scan = 'AA71000'
#    try_server_exception(order_scan,
#                         "Order AA710/00 has an invalid carrier code: ZZZZ.",
#                        )
#
#def test_server_exception11():
#    order_scan = 'AA71001'
#    try_server_exception(order_scan,
#                         "Order AA641/00 has an invalid carrier code:  .",
#                        )



















#
