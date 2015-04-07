"""
pickpack_format.py

This takes data returned from the database and formats it appropriately for
transmission to the client.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import json

from twisted.internet import defer

from CML_Pickpack.pickpack_modules import pickpack_data
from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_result_builders
from CML_Pickpack.pickpack_modules import pickpack_errors


def getPackingList_deferred(order_id,
                            ctx,
                           ):
    """
    Queries the database, and returns a deferred.
    """
    deferred = pickpack_data.getPackingList_deferred(order_id, ctx)
    deferred.addCallback(json.dumps)
    return deferred

def itemByUPC_deferred(upc):
    """
    Queries the database, and returns a deferred.
    """
    deferred = pickpack_data.itemByUPCData_deferred(upc)
    deferred.addCallback(_formatItemByUPC)
    return deferred

def _formatItemByUPC(upc_data):
    if len(upc_data) == 0:
        return pickpack_constants.NO_DATA_FOUND

    item_number = upc_data[0][0]

    if len(item_number) == 0:
        return pickpack_constants.NO_DATA_FOUND

    # Should this be wrapped in json before return?
    return item_number

def characterizeUserInput_deferred(userInput):
    """
    Queries the database, and returns a deferred.
    """
    deferred1 = pickpack_data.isValidItemNumberData_deferred(userInput)
    deferred2 = pickpack_data.isValidOrderNumberData_deferred(userInput)
    listOfDeferreds = defer.DeferredList([deferred1, deferred2],
                                          fireOnOneCallback=0,
                                          fireOnOneErrback=1,
                                          consumeErrors=0
                                        )
    listOfDeferreds.addCallback(_formatCharacterizeUserInput)
    return listOfDeferreds

def _formatCharacterizeUserInput(results):
    # results will look something like this: [(True, [(1,)]), (True, [])]
    # The "True" values come from defer.DeferredList. DeferredList returns a
    # list of (success, value) pairs.
    itemNumberResult, orderNumberResult = results

    if itemNumberResult[0]:
        if len(itemNumberResult[1]) == 0:
            itemNumberReturnValue = pickpack_constants.DB_FALSE
        else:
            itemNumberReturnValue = pickpack_constants.DB_TRUE
    else:
        raise pickpack_errors.ApplicationError("Error: isValidItemNumberData_deferred failed.")

    if orderNumberResult[0]:
        if orderNumberResult[1] is None:
            # The input could not be parsed as an order number
            orderNumberReturnValue = pickpack_constants.DB_FALSE
        elif len(orderNumberResult[1]) == 0:
            orderNumberReturnValue = pickpack_constants.DB_FALSE
        else:
            orderNumberReturnValue = pickpack_constants.DB_TRUE
    else:
        raise pickpack_errors.ApplicationError("Error: isValidOrderNumberData_deferred failed.")

    return json.dumps([itemNumberReturnValue, orderNumberReturnValue])

def writeOrderComplete_deferred(order_id,
                                comment_text,
                                serial_numbers_json,
                                user_id,
                               ):
    """
    Writes data to the database, and returns a deferred.
    """
    serial_numbers = json.loads(serial_numbers_json)
    deferred = pickpack_data.writeOrderCompleteData_deferred(order_id,
                                                             comment_text,
                                                             serial_numbers,
                                                             user_id,
                                                            )
    deferred.addCallback(notifyThatTheOrderCompleteWasWrittenSuccessfully)
    return deferred

def notifyThatTheOrderCompleteWasWrittenSuccessfully(returnValueFromTheDeferred):
    """
    A passthrough link in the deferred chain.
    """
    # The function called by dbpool.runInteraction must return a value -
    # otherwise the transaction does not get committed. We chose to use "True"
    # as the return value for that function, so we expect to receive True here.
    # If we receive True, pass None down the chain. If we do not receive True,
    # raise an exception.
    if returnValueFromTheDeferred != True:
        raise pickpack_errors.ApplicationError("Error: writeOrderComplete_deferred returned a value (%s). Expected True." % returnValueFromTheDeferred)
    return None

def isValidSerialNumber_deferred(item_number,
                                 serial_number,
                                ):
    """
    Queries the database, and returns a deferred.
    """
    deferred = pickpack_data.isValidSerialNumberData_deferred(item_number,
                                                              serial_number,
                                                             )
    deferred.addCallback(json.dumps)
    return deferred

def getClippershipWarnings_deferred(order_id,
                                    allow_shipped,
                                   ):
    """
    Queries the database, and returns a deferred.
    """
    deferred = pickpack_data.getClippershipWarningsData_deferred(order_id,
                                                                 allow_shipped,
                                                                )
    deferred.addCallback(_formatClippershipWarnings)
    return deferred

def _formatClippershipWarnings(clippership_warning_data_internal):
    clippership_warning_data_external = pickpack_result_builders.ClippershipWarningsBuilderExternal(
        clippership_warning_data_internal
    ).render()

    return json.dumps(clippership_warning_data_external)
