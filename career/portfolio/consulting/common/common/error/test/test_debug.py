"""

test_debug.py

This module provides tests for debug.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from Common.error import debug

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(debug))

#class UnitTestThisModule(unittest.TestCase):
#    pass


# ============================================================
# ============================================================

#class DebugUtility(object):
#    pass
#    def __init__(self):
#        pass
#    def debugLevel():
#        pass
#        def fget(self):
#            pass
#        def fset(self, value):
#            pass
#    def debugPause(self, callingLocation, msg = None):
#        pass
#    def debugPrint(self, item = None, itemList = None, itemDict = None):
#        pass
#    def debugBreakpoint(self):
#        pass
# ============================================================
# ============================================================

if __name__ == '__main__':
    unittest.main()
