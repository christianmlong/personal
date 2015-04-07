"""

test_package.py

This module runs all the tests for the modules in the package. It can
also provide a suite so higher-level packages can bundle its suite with others.


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""
# pylint: disable=C0103
# C0103: Invalid name "test_MRA_package"

# Import test helper
from Common.utility import utl_test

# Import the tests for each package
from Common.data.test import test_data_package
from Common.error.test import test_error_package
from Common.utility.test import test_utility_package

unittest_modules = (test_data_package,
                   test_error_package,
                   test_utility_package)

test_helper = utl_test.TestHelper(unittest_modules)

if __name__ == '__main__':
    test_helper.runPackageTests()
