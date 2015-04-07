"""

test_data_package.py

This module runs all the tests for the modules in the Common.data package. It
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
from Common.data.test import test_data_access
from Common.data.test import test_data_connection
from Common.data.test import test_data_datetime
from Common.data.test import test_data_shared_sql

unittest_modules = (test_data_access,
                   test_data_connection,
                   test_data_datetime,
                   test_data_shared_sql)

test_helper = utl_test.TestHelper(unittest_modules)

if __name__ == '__main__':
    test_helper.runPackageTests()
