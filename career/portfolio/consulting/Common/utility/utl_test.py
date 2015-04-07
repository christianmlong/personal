"""
utl_test.py

Helper class for unit testing.


Christian M. Long, developer

Initial implementation: September 10, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import Python standard modules
import unittest

class TestHelper(object):
    """
    A helper cass for compiling tests.
    """
    def __init__(self, unittest_modules):
        self._unittest_modules = unittest_modules

    def runPackageTests(self):
        """
        Run the tests for the Common.error package
        """
        runner = unittest.TextTestRunner()
        runner.run(self.packageTestSuite())

    def packageTestSuite(self):
        """
        Build the test suite for the Common.error package, including
        doctest and unittest tests.
        """
        suite = unittest.TestSuite()

        if self._unittest_modules is not None:
            for module in self._unittest_modules:
                try:
                    helper = module.test_helper
                except AttributeError:
                    pass
                else:
                    suite.addTest(helper.packageTestSuite())

                try:
                    unit_tests = module.UnitTestThisModule
                except AttributeError:
                    pass
                else:
                    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(unit_tests))

                try:
                    doctest_suite = module.doctest_suite
                except AttributeError:
                    pass
                else:
                    suite.addTest(doctest_suite)

        return suite
