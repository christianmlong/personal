"""

test_data_connection.py

This module provides tests for data_connection.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from CML_Common.data import data_connection

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(data_connection))


if __name__ == '__main__':
    unittest.main()
