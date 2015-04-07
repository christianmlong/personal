"""

test_error.py

This module provides tests for error.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from CML_Common.error import error

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(error))

#class UnitTestThisModule(unittest.TestCase):
#    pass


# ============================================================
# ============================================================

#class BaseException(Exception):
#    pass
#class AlertError(BaseException):
#    pass
#class DataError(AlertError):
#    pass
#class NoData(AlertError):
#    pass
#class OsError(AlertError):
#    pass
#class ApplicationError(AlertError):
#    pass
#class NDSVersionError(AlertError):
#    pass
#class HandleableError(AlertError):
#    pass
#class HandleableDatabaseError(HandleableError):
#    pass
#class NDSError(HandleableDatabaseError):
#    pass
#class RollbackTransaction(HandleableDatabaseError):
#    pass
#class DatabaseKeyError(HandleableDatabaseError):
#    pass
# ============================================================
# ============================================================

if __name__ == '__main__':
    unittest.main()
