"""

test_error_package.py

This module runs all the tests for the modules in the CML_Common.error package. It
runs the doctest and the unittest tests. It can also provide a suite so
higher-level packages can bundle its suite with others.


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

# Import test helper
from CML_Common.utility import utl_test

# Import the unit tests.  doctest tests are bundled into unittest suites inside
# the test_* modules
from CML_Common.error.test import test_debug
from CML_Common.error.test import test_error
from CML_Common.error.test import test_log

unittest_modules = (test_debug,
                   test_error,
                   test_log)

test_helper = utl_test.TestHelper(unittest_modules)

if __name__ == '__main__':
    test_helper.runPackageTests()
