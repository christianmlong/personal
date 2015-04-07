"""
pickpack_main.py

Main module for the Pick Pack server. This sets up the structure of the Twisted
application.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import datetime

from twisted.python import log
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.web import http
from twisted.web.server import NOT_DONE_YET

from Common.utility import utl_aplus

from Pickpack.pickpack_modules import pickpack_format
from Pickpack.pickpack_modules import pickpack_context
from Pickpack.pickpack_modules import pickpack_errors


class FileWithCacheControl(File):                                               # pylint: disable=R0904
    """
    An extension of the File resource, that includes cache control headers in
    the response.
    """
    def __init__(self, path, *args, **kwargs):
        # Call the constructor of our base class
        File.__init__(self, path, *args, **kwargs)

    def render_GET(self, request):
        # For static resources, set a header with a 10-hour-long cache time.
        request.setHeader("Cache-Control", "public, max-age=36000")

        # Delegate the rest of the work to the base class
        return File.render_GET(self, request)


class PickPackResource(Resource):
    """
    A base class with the infrastructure needed to work as a Resource that
    responds to requests.
    """
    isLeaf = True

    def __init__(self):
        # Call the constructor of our base class
        Resource.__init__(self)

    @staticmethod
    def _writeData(data, request):
        if data:
            # Avoid chunked encoding by setting the content length.
            # http://msoulier.wordpress.com/2010/06/11/twisted-python-and-chunked-encoding/
            # http://stackoverflow.com/questions/22352417/twisted-set-cache-headers
            request.setHeader('Content-Length', len(data))
            request.write(data)
            return data
        else:
            #request.write('.')
            return True

    @staticmethod
    def _errorWhileWriting(failure, request):
        request.setResponseCode(http.INTERNAL_SERVER_ERROR)

        # The processingFailed method includes a call to request.finish()
        # at the end. No need to call request.finish() here.
        request.processingFailed(failure)

        # We've handled the error here, and sent the error status code and error
        # message to the client. We stay on the errback side by returning the
        # failure.
        return failure

    @staticmethod
    def _finishResponse(ignore_result_of_previous_callback, request):
        request.finish()
        return True

    def _renderSomething(self, request):
        deferred = self.dataMethod(request)
        deferred.addCallback(self.writeResponseHeaders, request)
        deferred.addCallback(self._writeData, request)
        deferred.addErrback(self._errorWhileWriting, request)
        deferred.addCallback(self._finishResponse, request)

        # We're adding this errback at the end of the chain, so it should catch
        # and log all exceptions in any callback in the chain.
        deferred.addErrback(log.err)

        return NOT_DONE_YET

    def dataMethod(self,
                   request,
                  ):
        """
        Override in derived classes.
        """
        raise NotImplementedError

    @staticmethod
    def writeResponseHeaders(the_result_of_the_previous_callback, ignore_request):
        """
        Write http headers to the response. This class's implementation does
        nothing; override in derived classes.
        """
        return the_result_of_the_previous_callback

    @staticmethod
    def makeContext(request):
        """
        Make a context object that will carry needed info down the call chain.
        """
        port = request.getHost().port
        ctx = pickpack_context.Context(port)
        return ctx


class PickPackGettableResource(PickPackResource):
    """
    A base class with the infrastructure needed to work as a Resource that
    responds to GET requests.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackResource.__init__(self)

        # Establish that render_GET is another name for _renderSomething
        self.render_GET = self._renderSomething

    def dataMethod(self,
                   request,
                  ):
        """
        Override in derived classes.
        """
        raise NotImplementedError

    @staticmethod
    def writeResponseHeaders(the_result_of_the_previous_callback, request):
        """
        Write http headers to our response to the GET request.
        """
        # Aggressively tell Internet Explorer 9 to not cache xmlhttprequests
        request.setHeader("Last-Modified", datetime.datetime.now())
        request.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, private, max-age=0")
        request.setHeader("Pragma", "no-cache")

        # Tell Internet Explorer 9 and up to use the latest cutting-edge
        # compatibility mode.
        request.setHeader("X-UA-Compatible", "IE=edge")

        return the_result_of_the_previous_callback


class PickPackPostableResource(PickPackResource):
    """
    A base class with the infrastructure needed to work as a Resource that
    responds to POST requests.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackResource.__init__(self)

        # Establish that render_POST is another name for _renderSomething
        self.render_POST = self._renderSomething

    def dataMethod(self,
                   request,
                  ):
        """
        Override in derived classes.
        """
        raise NotImplementedError


class PackingList(PickPackGettableResource):
    """
    This class implements the server-side logic for retreiving the packing list
    for an order.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackGettableResource.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        order_id = utl_aplus.order_id_from_barcode_scan(request.args["order_id_scan"][0])
        return pickpack_format.getPackingList_deferred(order_id,
                                                       self.makeContext(request),
                                                      )


class ItemByUPC(PickPackGettableResource):
    """
    This class implements the server-side logic for looking an item up by UPC.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackGettableResource.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        return pickpack_format.itemByUPC_deferred(request.args["upc"][0])


class UserInput(PickPackGettableResource):
    """
    This class implements the server-side logic for determining if user input is
    an item number or an order number or something else.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackGettableResource.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        return pickpack_format.characterizeUserInput_deferred(request.args["input"][0])


class SerialNumber(PickPackGettableResource):
    """
    This class implements the server-side logic for querying a serial number.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackGettableResource.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        return pickpack_format.isValidSerialNumber_deferred(request.args["item_number"][0],
                                                            request.args["serial_number"][0],
                                                           )


class OrderComplete(PickPackPostableResource):
    """
    This class implements the server-side logic for writing to the database when
    the order is complete.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackPostableResource.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        order_id = utl_aplus.order_id_from_order_number_and_generation(
            request.args["order_number"][0],
            request.args["order_generation"][0],
        )
        comment_text = request.args["comment_text"][0]
        serial_numbers_json = request.args["serial_numbers"][0]
        user_id = request.args["user_id"][0]
        return pickpack_format.writeOrderComplete_deferred(order_id,
                                                           comment_text,
                                                           serial_numbers_json,
                                                           user_id,
                                                          )


# Disabled pylint warnings
# W0223 Method 'dataMethod' is abstract in class 'PickPackGettableResource' but is not overridden
class WarningsEndpoint(PickPackGettableResource):                               # pylint: disable=W0223
    """
    Base class for endpoints that serve warnings data to other applications
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackGettableResource.__init__(self)

    @staticmethod
    def parse_allow_shipped(request):
        """
        Parse the allow_shipped query string field, and return True or False.
        """
        # Here are some examples of what request.args looks like in here
        #   {'order_id_scan': ['AA10500']}
        #   {'allow_shipped': ['1'], 'order_id_scan': ['AA10400']}

        # If the client supplies a field called "allow_shipped" in the query
        # string, with a value of 1, then we use a different SQL query.
        allow_shipped = False
        temp1 = request.args.get("allow_shipped")
        if temp1 is not None:
            if temp1[0] == '1':
                allow_shipped = True
            else:
                raise pickpack_errors.ApplicationError(
                    "Unrecognized value for allow_shipped parameter: %s %s" % (temp1[0],
                                                                               type(temp1[0]),
                                                                              )
                )
        return allow_shipped


class ClippershipWarnings(WarningsEndpoint):
    """
    This class implements the server-side logic for serving order warning data
    to Clippership.
    """
    def __init__(self):
        # Call the constructor of our base class
        WarningsEndpoint.__init__(self)

    def dataMethod(self,
                   request,
                  ):
        """
        Implements the specific logic for this class's data needs. Returns a
        deferred.
        """
        order_id = utl_aplus.order_id_from_barcode_scan(request.args["order_id_scan"][0])
        return pickpack_format.getClippershipWarnings_deferred(order_id,
                                                               self.parse_allow_shipped(request),
                                                              )
