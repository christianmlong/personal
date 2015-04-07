"""
pickpack_main.py

Main module for the Pick Pack server. This sets up the structure of the Twisted
application.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from twisted.web.resource import Resource

from Pickpack.pickpack_modules import pickpack_resource
from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import shopfloor_monitor_resource

class PickPackAppRoot(Resource):
    """
    This is the main structure of the Pick Pack server application. URLs are
    served based upon this structure.
    """
    def __init__(self):
        # Call the constructor of our base class
        Resource.__init__(self)

        # Build the structure of the Pick Pack web app
        self.putChild("", pickpack_resource.FileWithCacheControl(pickpack_constants.APP_ROOT_PATH))
        self.putChild("static", pickpack_resource.FileWithCacheControl(pickpack_constants.STATIC_PATH))
        self.putChild("packinglist", pickpack_resource.PackingList())
        self.putChild("itembyupc", pickpack_resource.ItemByUPC())
        self.putChild("userinput", pickpack_resource.UserInput())
        self.putChild("validateserialnumber", pickpack_resource.SerialNumber())
        self.putChild("ordercomplete", pickpack_resource.OrderComplete())

        # In addition to serving Pick Pack, this twisted.web server also serves
        # data to our Clippership shipping automation software. It serves this
        # data at /clippership/warnings. We build the URL path structure here,
        # using a chain of Resource objects.
        clippership_path_segment_resource = Resource()
        self.putChild("clippership", clippership_path_segment_resource)
        clippership_path_segment_resource.putChild("warnings", pickpack_resource.ClippershipWarnings())

        # Also, serve some data to the order status monitoring application.
        shopfloor_monitor_path_segment_resource = Resource()
        self.putChild("shopfloor_monitor", shopfloor_monitor_path_segment_resource)
        shopfloor_monitor_path_segment_resource.putChild("j_status_orders", shopfloor_monitor_resource.JStatusOrders())
        shopfloor_monitor_path_segment_resource.putChild("j_status_order_numbers", shopfloor_monitor_resource.JStatusOrderNumbers())
        shopfloor_monitor_path_segment_resource.putChild("order_number_detail", shopfloor_monitor_resource.OrderNumberDetail())
