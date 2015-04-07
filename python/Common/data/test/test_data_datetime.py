"""

test_data_datetime.py

This module provides tests for data_datetime.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from Common.data import data_datetime

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(data_datetime))

#class UnitTestThisModule(unittest.TestCase):
#    pass


# ============================================================
# ============================================================

#def makeOracleDate(date_tuple):
#    pass
#def getTodayAsDateTuple():
#    pass
#def pythonTimeTupleFromDateTuple(date_tuple):
#    pass
#def formatDateTuple(date_tuple, format_string):
#    pass
#def formatNow(format_string):
#    pass
#def getNowAsOracleTimestamp():
#    pass
# ============================================================
# ============================================================

if __name__ == '__main__':
    unittest.main()
