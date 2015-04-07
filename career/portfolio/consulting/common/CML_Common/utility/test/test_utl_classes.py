"""

test_utl_classes.py

This module provides tests for utl_classes.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from CML_Common.utility import utl_classes

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(utl_classes))

#class UnitTestThisModule(unittest.TestCase):
#    pass


# ============================================================
# ============================================================

#class Enum(object):
#    pass
#    def __init__(self, listOfNamedConstants):
#        pass
#    def __contains__(self, item):
#        pass
# ============================================================
# ============================================================

if __name__ == '__main__':
    unittest.main()
