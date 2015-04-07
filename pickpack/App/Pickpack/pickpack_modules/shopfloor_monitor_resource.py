"""
shopfloor_monitor_main.py

The starting point for the Shopfloor Monitor
application.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from twisted.internet import defer

from Pickpack.pickpack_modules import shopfloor_monitor_format
from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import pickpack_common

from Pickpack.pickpack_modules.pickpack_cache import CachedResource


class JStatusOrdersBase(CachedResource):
    """
    Base class for classes that serve order status data to the shop-floor
    monitoring process.
    """
    def __init__(self):
        # Call the constructor of our base class
        CachedResource.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Override in derived classes.
        """
        raise NotImplementedError

    @staticmethod
    def parseCommonRequestArgs(request):
        """
        Read the user-provided request arguments from the request object. Return
        normalized constants, that are used throughout the application.
        """
        shipping_station_dict = {
            "wcc"       : pickpack_constants.CONSUMABLES_SCALE,
            "parts"     : pickpack_constants.SERVICE_PARTS_SCALE,
            "both"      : pickpack_constants.BOTH_SCALE,
            "all"       : pickpack_constants.ALL_SCALES,
            "4up"       : pickpack_constants.FOUR_UP,
        }
        shipping_station = shipping_station_dict[request.args["scale"][0]]

        true_false_dict = {
            "true"      : True,
            "false"     : False,
        }
        show_backorder = true_false_dict[request.args["show_backorder"][0]]

        return (shipping_station,
                show_backorder,
               )


class JStatusOrders(JStatusOrdersBase):
    """
    This class serves order status data to the shop-floor monitoring process.
    """
    # Class-level persistent cache. We store the cache on the class, because
    # Twisted makes a new instance of JStatusOrders for each request.
    cache_dict = {}

    def __init__(self):
        # Call the constructor of our base class
        JStatusOrdersBase.__init__(self)

    def dataMethod(self, request):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        (shipping_station,
         show_backorder,
        ) = self.parseRequest(request)

        if shipping_station == pickpack_constants.FOUR_UP:
            # This is a request for data for all four of the graphs on the
            # four-up display. We turn this in to four deferred requests, each
            # of which might return cached data. We do not cache the aggregate
            # result, just the individual results. This is to prevent
            # double-caching and serving stale data.

            # Kick off four data requests, that can run simultaneously. Each one
            # of these deferreds will succeed immediately if there is a cache
            # hit. Otherwise, they will go to the database for fresh data.
            #
            # DeferredList groups several deferreds together. It returns a list
            # of (success, value) pairs.
            deferred1 = self.getCachedData_deferred(pickpack_constants.CONSUMABLES_SCALE,
                                                    show_backorder,
                                                   )
            deferred2 = self.getCachedData_deferred(pickpack_constants.SERVICE_PARTS_SCALE,
                                                    show_backorder,
                                                   )
            deferred3 = self.getCachedData_deferred(pickpack_constants.BOTH_SCALE,
                                                    show_backorder,
                                                   )
            deferred4 = self.getCachedData_deferred(pickpack_constants.ALL_SCALES,
                                                    show_backorder,
                                                   )
            listOfDeferreds = defer.DeferredList([deferred1,
                                                  deferred2,
                                                  deferred3,
                                                  deferred4,
                                                 ],
                                                  fireOnOneCallback=0,
                                                  fireOnOneErrback=1,
                                                  consumeErrors=0
                                                )
            listOfDeferreds.addCallback(shopfloor_monitor_format.format4UpData)

            # We dump to JSON at the last minute. The cache stores python
            # objects, not JSON. This is so we can compose a response to a 4up
            # request using cached data, and not have the response be
            # "double-jsonned".
            listOfDeferreds.addCallback(pickpack_common.dumpToJSON)

            return listOfDeferreds
        else:
            # This is a request for individual data.
            deferred = self.getCachedData_deferred(shipping_station,
                                                   show_backorder,
                                                  )

            # We dump to JSON at the last minute. The cache stores python
            # objects, not JSON. This is so we can compose a response to a 4up
            # request using cached data, and not have the response be
            # "double-jsonned".
            deferred.addCallback(pickpack_common.dumpToJSON)

            return deferred

    @staticmethod
    def getDbData_deferred(shipping_station,
                           show_backorder,
                          ):
        """
        Get the data from the db.
        """
        return shopfloor_monitor_format.jStatusOrders_deferred(shipping_station,
                                                               show_backorder,
                                                              )

    def parseRequest(self, request):
        """
        Read the user-provided request arguments from the request object. Return
        normalized constants, that are used throughout the application.
        """
        (shipping_station,
         show_backorder,
        ) = self.parseCommonRequestArgs(request)

        return (shipping_station,
                show_backorder,
               )


class JStatusOrderNumbers(JStatusOrdersBase):
    """
    This class serves order number data to the shop-floor monitoring process.
    """
    # Class-level persistent cache. We store the cache on the class, because
    # Twisted makes a new instance of JStatusOrders for each request.
    cache_dict = {}

    def __init__(self):
        # Call the constructor of our base class
        JStatusOrdersBase.__init__(self)

    def dataMethod(self, request):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        (shipping_station,                                                      # pylint: disable=unbalanced-tuple-unpacking
         show_backorder,
         order_type,
        ) = self.parseRequest(request)

        deferred = self.getCachedData_deferred(shipping_station,
                                               show_backorder,
                                               order_type,
                                              )

        # We dump to JSON at the last minute. The cache stores python objects,
        # not JSON. This is so we can compose a response to a 4up request using
        # cached data, and not have the response be "double-jsonned".
        deferred.addCallback(pickpack_common.dumpToJSON)

        return deferred

    @staticmethod
    def getDbData_deferred(shipping_station,
                           show_backorder,
                           order_type,
                          ):
        """
        Get the data from the db.
        """
        return shopfloor_monitor_format.jStatusOrderNumbers_deferred(shipping_station,
                                                                     show_backorder,
                                                                     order_type,
                                                                    )

    def parseRequest(self, request):
        """
        Read the user-provided request arguments from the request object. Return
        normalized constants, that are used throughout the application.
        """
        (shipping_station,
         show_backorder,
        ) = self.parseCommonRequestArgs(request)

        order_type_dict = {
            'today_sure'        : pickpack_constants.TODAY_SURE,
            'signature_service' : pickpack_constants.SIGNATURE_SERVICE,
            'service_file'      : pickpack_constants.SERVICE_FILE,
            'normal'            : pickpack_constants.NORMAL,
        }
        order_type = order_type_dict[request.args["order_type"][0]]

        return (shipping_station,
                show_backorder,
                order_type,
               )


class OrderNumberDetail(CachedResource):
    """
    This class serves order number detail data to the shop-floor monitoring
    process.
    """
    # Class-level persistent cache. We store the cache on the class, because
    # Twisted makes a new instance of JStatusOrders for each request.
    cache_dict = {}

    def __init__(self):
        # Call the constructor of our base class
        CachedResource.__init__(self)

    def dataMethod(self, request):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """

        order_number = request.args["order_number"][0]
        order_generation = request.args["order_generation"][0]

        deferred = self.getCachedData_deferred(order_number, order_generation)

        # We dump to JSON at the last minute. The cache stores python objects,
        # not JSON. This is so we can compose a response to a 4up request using
        # cached data, and not have the response be "double-jsonned".
        deferred.addCallback(pickpack_common.dumpToJSON)

        return deferred

    @staticmethod
    def getDbData_deferred(order_number, order_generation):
        """
        Get the data from the db.
        """
        return shopfloor_monitor_format.orderNumberDetail_deferred(order_number, order_generation)
