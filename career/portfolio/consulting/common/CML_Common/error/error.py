"""
error.py

Custom error classes


Christian M. Long, developer

Initial implementation: September 5, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""



#    Classes         +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CMLBaseException(Exception):
    """
    Base class for all exceptions and errors in the common modules
    """

class AlertError(CMLBaseException):
    """
    Base class for all custom errors in the common modules. These are
    application and database errors, and other runtime errors. We notify the
    user of these errors, with a friendly message if possible, and log them.
    """

class DbapiModuleError(AlertError):
    """
    Error raised by the DBAPI data access module. These start out as DBAPI
    module.DatabaseError, and then we wrap them in subclasses of this error, for
    easier handling.
    """

class Db2Error(DbapiModuleError):
    """
    Error raised by the DBAPI data access module (pyodbc) as a result of an
    error during DB2 database access. These start out as DBAPI
    module.DatabaseError, and then we wrap them in this error for easier
    handling.
    """

class NoDataFound(AlertError):
    """
    No data returned from query
    """

class OsError(AlertError):
    """
    Error in os module
    """

class ApplicationError(AlertError):
    """
    Error in common module
    """

class InputError(AlertError):
    """
    Error in the input to a function
    """

class HandleableError(AlertError):
    """
    Superclass for errors that can be handled at lower levels instead of
    breaking out all the way to the main error handler.
    """

class HandleableDatabaseError(HandleableError):
    """
    Superclass for handleable database errors.
    """

class AplusError(HandleableDatabaseError):
    """
    Error in Aplus stored procedure or data access. I raise this manually in
    cases when the database call succeeded, but the results are in some way
    erroneous.
    """

class RollbackTransaction(HandleableDatabaseError):
    """
    Transaction rolled back
    """

class DatabaseKeyError(HandleableDatabaseError):
    """
    Database key error
    """

class ExternalHandleableError(HandleableDatabaseError):
    """
    Raised whenever an exception is caught that is of a type that was previously
    registered by client code in the external_handleable_exceptions_object.
    """

# POSSIBLE IMPROVEMENT
# Set my custom errors up so that they have a Severity and a Break Level as well
# as an error message.
#
# Severity (Information, Error, Fatal) would indicate whether the error message
# should be displayed to the user in plain text or reverse text with a beep.
#
# Break Level would be set to Operation, Module, Application, Loop Break, Loop
# Continue (others?). Loop would allow a subfunction to break out of (or
# continue) a calling function's loop. Operation would just break out to the
# nearest error handler. Module would break out to the top of the module, and
# Applicaiton would break out to the main menu.
