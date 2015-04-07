"""

test_data_shared_sql.py

This module provides tests for data_shared_sql.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from CML_Common.data import data_shared_sql

# Import test helper
#from CML_Common.utility import utl_test

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(data_shared_sql))

# Constants
UPC = '715959120500'
ITEM_NUMBER = '000068'

# Can not have server-specific connections here.
# Suggestion: Make this test cycle through all possible server connections, and
# fail if none are viable? Or, just forget it.

#class UnitTestThisModule(utl_test.TestCaseWithNDSConnection):
#
#    def testGetItemNumberByUPC(self):
#        self.assertEqual(data_shared_sql.getItemNumberByUPC(UPC), ITEM_NUMBER)
#    def testGetUPCByItemNumber(self):
#        self.assertEqual(data_shared_sql.getUPCByItemNumber(ITEM_NUMBER), UPC)

if __name__ == '__main__':
    unittest.main()
