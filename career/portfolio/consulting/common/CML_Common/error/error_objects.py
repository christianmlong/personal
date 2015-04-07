"""
error_objects.py

Objects with logic in them for handling errors.


Christian M. Long, developer

Initial implementation: September 5, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Note: this was split out from error because it imports utl_decorators
# The problem is, utl_decorators imports error. To avoid the circular
# import, I left only the lowest-level error definitions in error, and
# I brought the logic-containing bits over here.

# Import shared modules
from CML_Common.error import error
from CML_Common.utility import utl_decorators

class ExternalHandleableExceptions(object):
    """
    This class is used by client code to register its own exceptions as being
    handleable, or 'expected'. These handleable errors could be something like
    OperationFailed, where a validation check failed.

    In client code, this allows us to use the same function both inside and
    outside of the data_access.transactionManager, while still using the
    exceptions defined in the client code.

    The client code registers its exceptions, defined in one of its modules.

    This way, some piece of client code (a validation function, for example),
    running under data_access.transactionManager, can raise its own local
    OperationFailed exception, and data_access.transactionManager will treat it
    like an expected, handleable error instead of like an unexpected, freak-out
    error.
    """

    def __init__(self):
        self._exception_tuple = ()

    def append(self, stuff_to_append):
        """
        Accepts either an exception class or a sequence of exception classes.
        Appends them to a sequence of 'handleable' exceptions.
        """
        try:
            # If it's iterable, try calling self.append for each item
            for item in stuff_to_append:
                self.append(item)

        except TypeError:
            # Not iterable. Check if it's an exception class
            if not issubclass(stuff_to_append, Exception):
                err_msg = "%s is not an exception class" % stuff_to_append
                raise error.ApplicationError(err_msg)

            if not stuff_to_append in self._exception_tuple:
                self._exception_tuple += (stuff_to_append, )

    #    Properties                  +++++++++++++++++++
    # pylint: disable=E0202, E0211, W0212, C0111
    @utl_decorators.makeProperty
    def exceptions():
        doc = """
              A tuple of exception classes which are considered 'handleable'.
              These exceptions were registered by client code, using the append
              method.
              """
        def fget(self):
            return self._exception_tuple
        return locals()
    # pylint: enable=E0202, E0211, W0212, C0111

# Create a single, shared, module-level instance of ExternalHandleableExceptions
external_handleable_exceptions_object = ExternalHandleableExceptions()
