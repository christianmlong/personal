"""

Tests for the Shopfloor Monitor application.

"""


from Pickpack.test.selenium.common_selenium_tests import BaseForShopfloorMonitorTests

class TestShopfloorMonitorCommon(BaseForShopfloorMonitorTests):
    """
    These are some Selenium tests for the Shopfloor Monitor project.
    """
    def __init__(self):
        BaseForShopfloorMonitorTests.__init__(self)

    def test_01_quicktest(self):
        """
        Quick smoke test
        """
