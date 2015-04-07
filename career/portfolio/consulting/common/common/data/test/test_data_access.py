"""

test_data_access.py

This module provides tests for data_access.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from Common.data import data_access

# Import test helper
#from Common.utility import utl_test

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(data_access))

if __name__ == '__main__':
    unittest.main()
