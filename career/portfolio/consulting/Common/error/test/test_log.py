"""

test_log.py

This module provides tests for log.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""

import unittest
import doctest

# Import module to test
from Common.error import log

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(log))

#class UnitTestThisModule(unittest.TestCase):
#    pass


# ============================================================
# ============================================================

#class LogUtility(object):
#    pass
#    def __init__(self, log_directory, max_logfile_size, time_format):
#        pass
#    def writeToLogFile(self, logText, log_fileName, userId):
#        pass
# ============================================================
# ============================================================

if __name__ == '__main__':
    unittest.main()
