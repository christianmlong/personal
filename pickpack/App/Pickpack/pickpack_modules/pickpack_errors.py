"""
pickpack_errors.py

Custom error classes


Christian M. Long, developer

"""



#    Classes         +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PickpackBaseException(Exception):
    """
    Base class for all exceptions and errors in the Pickpack application
    """

class ApplicationError(PickpackBaseException):
    """
    General error in the Pick Pack application.
    """

class CacheMiss(PickpackBaseException):
    """
    Indicates that there was no data in the cache.
    """

class HandleableServerError(PickpackBaseException):
    """
    Represents an error that we will pass back to the client as a text error
    message.
    """
