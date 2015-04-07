"""
shopfloor_monitor_format.py

This takes data returned from the database and formats it appropriately for
transmission to the client.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules import shopfloor_monitor_data

def jStatusOrders_deferred(shipping_station,
                           show_backorder,
                          ):
    """
    Queries the database, and returns a deferred.
    """
    deferred = shopfloor_monitor_data.jStatusOrdersData_deferred(shipping_station,
                                                                 show_backorder,
                                                                )
    return deferred

def jStatusOrderNumbers_deferred(shipping_station,
                                 show_backorder,
                                 order_type,
                                ):
    """
    Queries the database, and returns a deferred.
    """
    deferred = shopfloor_monitor_data.jStatusOrderNumbersData_deferred(shipping_station,
                                                                       show_backorder,
                                                                       order_type,
                                                                      )
    return deferred

def format4UpData(deferred_list_result):
    """
    Generate appropriate output for the 4up request.
    """
    # results will look something like this:
    #
    #   [(True, {"today_sure_can_ship_tomorrow": 13,
    #            "normal_should_ship_today": 34,
    #            . . .
    #           }
    #    ),
    #    (True, {"today_sure_can_ship_tomorrow": 57,
    #            "normal_should_ship_today": 123,
    #            . . .
    #           }
    #    ),
    #   ]
    #
    # The "True" values come from defer.DeferredList. DeferredList returns a
    # list of (success, value) pairs.

    # Unzip the list.
    #
    # If we do this (note the star):
    # zip(*[('a', 1), ('b', 2), ('c', 3), ('d', 4)])
    #
    # it gives us this - the list is "unzipped"
    # [('a', 'b', 'c', 'd'), (1, 2, 3, 4)]
    (successes,
     results,
    ) = zip(*deferred_list_result)

    if not all(successes):
        descriptions = ("consumables",
                        "service parts",
                        "both",
                        "all",
                       )
        raise pickpack_errors.ApplicationError("Error while retreiving data for the following: %s " %
                          ", ".join(desc
                                    for (desc, success)
                                    in zip(descriptions, successes)
                                    if success is False
                                   )
                         )

    return dict(
        zip(
            ("wcc",
             "parts",
             "both",
             "all",
            ),
            results,
        )
    )

def orderNumberDetail_deferred(order_number, order_generation):
    """
    Queries the database, and returns a deferred.
    """
    deferred = shopfloor_monitor_data.orderNumberDetailData_deferred(order_number, order_generation)
    return deferred
