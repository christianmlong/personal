"""

test_utility_package.py

This module runs all the tests for the modules in the Common.utility package. It
runs the doctest and the unittest tests. It can also provide a suite so
higher-level packages can bundle its suite with others.


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

# Import test helper
from Common.utility import utl_test

# Import the unit tests.  doctest tests are bundled into unittest suites inside
# the test_* modules
from Common.utility.test import test_utl_classes
from Common.utility.test import test_utl_decorators
from Common.utility.test import test_utl_functions
from Common.utility.test import test_utl_server

unittest_modules = (test_utl_classes,
                   test_utl_decorators,
                   test_utl_functions,
                   test_utl_server)

test_helper = utl_test.TestHelper(unittest_modules)

if __name__ == '__main__':
    test_helper.runPackageTests()
