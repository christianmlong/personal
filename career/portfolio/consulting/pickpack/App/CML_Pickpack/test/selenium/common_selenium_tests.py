# pylint: disable=C0111,R0904

#from CML_Pickpack.pickpack_modules.test import utility_functions_for_testing

from CML_Pickpack.test.selenium.utility import PickpackTestingUtility
from CML_Pickpack.test.selenium.utility import PickpackTestingUtilityNoCookie
from CML_Pickpack.test.selenium.utility import ShopfloorMonitorTestingUtility
from CML_Pickpack.test.selenium.table_tester import TableTester

class BaseForSeleniumTests(object):
    """
    Base class for test classes
    """

    @classmethod
    def setup_class(cls):
        """
        This will run only once, before each test run
        """
        cls.u.start_selenium_server()                                   # pylint: disable=E1101

    @classmethod
    def teardown_class(cls):
        """
        This will run only once, after each test run
        """
        cls.u.stop_selenium_server()                                    # pylint: disable=E1101

    def setup(self):
        """
        This will run once for each test method in this class
        """
        self.u.open_aut()                                               # pylint: disable=E1101


class BaseForPickpackTests(BaseForSeleniumTests):
    """
    Base class for test classes for Pickpack
    """

    u = PickpackTestingUtility()           # pylint: disable=C0103

    def __init__(self):
        BaseForSeleniumTests.__init__(self)

    #@staticmethod
    #def ecommerce_promotion_is_active():
    #    """
    #    Passthrough
    #    """
    #    return utility_functions_for_testing.ecommerce_promotion_is_active()


class BaseForShopfloorMonitorTests(BaseForSeleniumTests):
    """
    Base class for test classes for Shopfloor Monitor
    """

    u = ShopfloorMonitorTestingUtility()           # pylint: disable=C0103

    def __init__(self):
        BaseForSeleniumTests.__init__(self)


class BaseForPickpackTestsNoCookie(BaseForSeleniumTests):
    """
    Base class for test classes for Pickpack with no cookie set
    """

    u = PickpackTestingUtilityNoCookie()           # pylint: disable=C0103

    def __init__(self):
        BaseForSeleniumTests.__init__(self)


class TestPickpackCommon(BaseForPickpackTests):
    """
    These are some Selenium tests for the Pick Pack project. These tests apply
    to all versions of the project.
    """
    def __init__(self):
        BaseForPickpackTests.__init__(self)

    def test_01_quicktest(self):
        """
        Quick smoke test
        """
        order_id_scan = "AA00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_highlighted(0)

        self.u.key_press("+")
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_info_image_blank(3)
        self.u.assert_order_status_gray()

    def test_02_walkthrough(self):
        """
        Walkthrough a basic order, testing the most common functionality such
        as scanning, error handling, and notifications.
        """
        order_id_scan = "AA00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_highlighted(0)

        self.u.key_press("+")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("648484173810")
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("648484225984")
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("192056")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_gray(3)
        self.u.assert_order_status_gray()

        self.u.scan("192056")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_gray()

        # One more puts us over the limit.
        self.u.scan("648484225977")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_red(3)
        self.u.assert_order_status_red()

        # Use the arrow to restore green
        self.u.special_key(self.u.LEFT_ARROW)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_gray()

        scan_data = "123456"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data
        self.u.wait_for_error_box(err_message)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_red()

        another_scan_data = "654321"
        self.u.scan__allow_error(another_scan_data)
        err_message = ("That item is not on this order. Item: %s\n"
                       "I can not proceed while the red error box is visible. Please "
                       "dismiss this box by pressing the space bar." % scan_data
                      )
        self.u.wait_for_error_box(err_message)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_gray()
        self.u.wait_for_error_box_cleared()

        self.u.scan("648484225984")
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_gray()

        self.u.scan("648484225984")
        self.u.assert_row_highlighted(2)
        self.u.scan("648484225984")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            special_keys_encoded = "%3A%20135428%3A%5B%2B%5D%20%20192056%3A%5B%3C-%5D",
        )
        self.u.wait_for_comment_posting(url_encoded_post_content)

        self.u.special_key__allow_info(self.u.RIGHT_ARROW)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)

        # Another order, while the info box is visible
        order_id_scan = "AA01600"
        self.u.scan__allow_info(order_id_scan)
        message = ("This order is complete. You can no longer make changes to this order.\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar."
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        # Another order
        order_id_scan = "AA01600"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(7)
        # Make sure that the lastPOST is still the same - that is, make sure we
        # have not made any new POST requests as a result of this new order.
        self.u.wait_for_comment_posting(url_encoded_post_content)

        # Another order
        order_id_scan = "AA01000"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)
        # Make sure that the lastPOST is still the same - that is, make sure we
        # have not made any new POST requests as a result of this new order.
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_03_walkthrough2(self):
        """
        Walkthrough a basic order
        """
        order_id_scan = "AA00800"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(43)

        self.u.scan("648484327657")
        self.u.assert_row_highlighted(21)
        self.u.assert_row_status_gray(21)
        self.u.assert_order_status_gray()

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_highlighted(0)

        self.u.key_press("+")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_gray(21)
        self.u.assert_order_status_gray()

        scan_data = "AA00800"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data
        self.u.wait_for_error_box(err_message)
        self.u.assert_row_highlighted(0)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_gray(21)
        self.u.assert_order_status_gray()
        self.u.wait_for_error_box_cleared()

        scan_data = "AA00800"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data
        self.u.wait_for_error_box(err_message)
        self.u.assert_row_highlighted(0)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_gray(21)
        self.u.assert_order_status_gray()
        self.u.wait_for_error_box_cleared()

        scan_data = "bla"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_gray(21)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_gray(21)
        self.u.assert_order_status_gray()
        self.u.wait_for_error_box_cleared()

        self.u.special_key(self.u.DOWN_ARROW)
        self.u.assert_row_highlighted(1)
        self.u.special_key(self.u.UP_ARROW)
        self.u.assert_row_highlighted(0)
        self.u.special_key(self.u.UP_ARROW)
        self.u.assert_row_highlighted(42)

    def test_04_walkthrough3(self):
        """
        Walkthrough a basic order
        """
        order_id_scan = "AA01600"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(7)

        self.u.scan("648484383936")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_gray()

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_highlighted(0)

        for i in range(1, 6):
            self.u.special_key(self.u.DOWN_ARROW)
            self.u.assert_row_highlighted(i)

        for i in range(4, -1, -1):
            self.u.special_key(self.u.UP_ARROW)
            self.u.assert_row_highlighted(i)

        for i in range(6, 3, -1):
            self.u.special_key(self.u.UP_ARROW)
            self.u.assert_row_highlighted(i)

    def test_05_1_walkthrough(self):
        """
        Scan invalid items before any valid items have been scanned
        """
        order_id_scan = "AA01600"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(7)

        # Scan an invalid item number before any items have been scanned
        scan_data = "ZZ585"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        scan_data = "zz585"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        scan_data = "123459"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        scan_data = "AAAAA"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        scan_data = "aaaaa"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        scan_data = "235458"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        self.u.scan("648484383936")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_gray()

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_highlighted(0)

        for i in range(1, 6):
            self.u.special_key(self.u.DOWN_ARROW)
            self.u.assert_row_highlighted(i)

        for i in range(4, -1, -1):
            self.u.special_key(self.u.UP_ARROW)
            self.u.assert_row_highlighted(i)

        for i in range(6, 3, -1):
            self.u.special_key(self.u.UP_ARROW)
            self.u.assert_row_highlighted(i)

    def test_05_walkthrough4(self):
        """
        Scan an invalid order number before any items have been scanned
        """
        order_id_scan = "AA00100"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(12)

        # Scan an invalid order number before any items have been scanned
        scan_data = "ZZ58500"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        scan_data = "zz58500"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        scan_data = "1234599"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        scan_data = "AAAAA74"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        scan_data = "aaaaa34"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        scan_data = "235458"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        # Now, we scan a real order, twice
        order_id_scan = "AA00100"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(12)

        order_id_scan = "AA00100"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(12)

        scan_data = "235458"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_display(order_id_scan)

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_display(order_id_scan)
        self.u.wait_for_error_box_cleared()

        scan_data = "2354585"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_number_blank()
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        order_id_scan = "AA00700"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        scan_data = "27gzq46"
        self.u.scan__allow_error(scan_data)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(scan_data)
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_number_blank()
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()

        scan_data = "235458"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data.upper()
        self.u.wait_for_error_box(err_message)
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_red()
        self.u.assert_order_number_blank()

        self.u.key_press(" ")
        self.u.assert_all_rows_blank_and_not_highlighted()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()
        self.u.wait_for_error_box_cleared()


    def test_06_f2(self):
        """
        Test the functioning of the F2 button
        """
        order_id_scan = "AA00700"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        table_data = [
            (4, '648484320016', '216326', 0, 2.0,  '5PK', 0),
            (3, '648484320399', '216327', 0, 4.0,  '5PK', 0),
            (1, '648484324984', '216331', 0, 1.0,  'EA', 0),
            (2, '648484296366', '770246', 0, 10.0,  'EA', 0),
        ]

        t = TableTester(table_data,                # pylint: disable=C0103
                        self.u,
                       )
        t.multi_scan_upc(5)
        self.u.assert_row_status_green(0)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.special_key(self.u.F2)
        t.back_up(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        t.multi_scan_item(5)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.special_key(self.u.F2)
        t.back_up(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        t.finish_order_upc()
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def table_scan(self, item_or_upc):
        """
        Iterate through a whole table of items
        """
        order_id_scan = "AA00600"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(11)

        table_data = [
            (8, '648484059046', '011244', 0, 5.0,  'EA', 0),
            (9, '648484096508', '046797', 0, 2.0,  'EA', 0),
            (5, '648484080835', '071642', 0, 1.0,  'EA', 0),
            (10, '648484038621', '129179', 0, 1.0,  'EA', 0),
            (11, '648484225892', '192053', 0, 20.0,  'EA', 0),
            (7, '648484258357', '192703', 0, 15.0,  'EA', 0),
            (6, '648484302883', '193146', 0, 2.0,  'EA', 0),
            (4, '648484320016', '216326', 0, 20.0,  '5PK', 0),
            (3, '648484320399', '216327', 0, 20.0,  '5PK', 0),
            (1, '648484324984', '216331', 0, 1.0,  'EA', 0),
            (2, '648484296366', '770246', 0, 10.0,  'EA', 0),
        ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )
        t.multi_scan(20, item_or_upc)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_highlighted(4)
        self.u.assert_row_status_gray(4)
        self.u.assert_row_status_blank(5)
        self.u.assert_row_status_blank(6)
        self.u.assert_row_status_blank(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_order_status_gray()

        t.finish_order(item_or_upc)
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_status_green(7)
        self.u.assert_row_status_green(8)
        self.u.assert_row_status_green(9)
        self.u.assert_row_highlighted(10)
        self.u.assert_row_status_green(10)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

        # Another order
        order_id_scan = "AA00700"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)
        # Make sure that the lastPOST is still the same - that is, make sure we
        # have not made any new POST requests as a result of this new order.
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_07_table_scan_item(self):
        """
        Iterate through a whole table of items, scanning item number
        """
        self.table_scan("item")
    # An attribute of the test, used by Nose
    test_07_table_scan_item.long_running = True

    def test_08_table_scan_upc(self):
        """
        Iterate through a whole table of items, scanning upc
        """
        self.table_scan("upc")
    # An attribute of the test, used by Nose
    test_08_table_scan_upc.long_running = True

    def test_09_two_lines_one_item(self):
        """
        Test cases where the same item is on multiple lines (MLSI orders)
        """
        order_id_scan = "AA00500"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(5)

        # AA00500
        # 0    1, '648484130929', '135428', 0, 3.0,
        # 1    2, '648484173810', '169599', 0, 1.0,
        # 2    3, '648484225984', '192048', 0, 4.0,
        # 3    4, '648484225977', '192056', 0, 2.0,
        # 4    5, '648484225977', '192056', 0, 2.0,

        self.u.scan("648484225984")
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_gray(2)
        self.u.assert_row_qty(2, 1)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_order_status_gray()

        self.u.key_press("+")
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_qty(2, 4)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_order_status_gray()

        self.u.scan("648484225977")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_gray(3)
        self.u.assert_row_qty(3, 1)
        self.u.assert_row_status_blank(4)
        self.u.assert_order_status_gray()

        self.u.scan("192056")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_qty(3, 2)
        self.u.assert_row_status_blank(4)
        self.u.assert_order_status_gray()

        #  The first row has been filled. Spill over to the next row.
        self.u.scan("648484225977")
        self.u.assert_row_highlighted(4)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_qty(3, 2)
        self.u.assert_row_status_gray(4)
        self.u.assert_row_qty(4, 1)
        self.u.assert_order_status_gray()

        self.u.scan("192056")
        self.u.assert_row_highlighted(4)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_qty(3, 2)
        self.u.assert_row_status_green(4)
        self.u.assert_row_qty(4, 2)
        self.u.assert_order_status_gray()

        # One more puts us over the limit. Note that the first row receives the
        # over-the-limit scan.
        self.u.scan("192056")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_red(3)
        self.u.assert_row_qty(3, 3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_qty(4, 2)
        self.u.assert_order_status_red()

        # Use the plus key to restore green
        self.u.key_press("+")
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_qty(3, 2)
        self.u.assert_row_status_green(4)
        self.u.assert_row_qty(4, 2)
        self.u.assert_order_status_gray()

        # Plus keys to finish off the order
        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_highlighted(0)

        self.u.key_press("+")
        self.u.assert_row_status_green(0)
        self.u.assert_row_highlighted(0)
        self.u.assert_order_status_gray()

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_highlighted(1)

        self.u.key_press("+")
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            special_keys_encoded = "%3A%20135428%3A%5B%2B%5D%20%20169599%3A%5B"
                                   "%2B%5D%20%20192048%3A%5B%2B%5D%20%20192056"
                                   "%3A%5B%2B%5D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_10_serial_numbers(self):
        """
        Test the input and management of serial number data.
        """
        order_id_scan = "AA01100"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        item_number = "235671"
        self.u.scan(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.wait_for_serial_number_box(item_number)
        serial_number = "0999910"
        self.u.scan__allow_error(serial_number)
        err_message = "%s is not a valid serial number. Please scan a serial number." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_order_status_blank()

        serial_number = "20081015000008"
        self.u.scan(serial_number)
        self.u.wait_for_serial_number_box_cleared()
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_highlighted(0)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            serial_numbers_encoded = "%7B%221%22%3A%7B%22item_number%22%3A%22235671%22%2C%20%22"
                                     "serial_numbers%22%3A%5B%2220081015000008%22%5D%7D%7D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_11_mlsi_serial_numbers(self):
        """
        Test serial numbers, on orders where there are multiple lines of the
        same item (MLSI orders)
        """
        order_id_scan = "AA01300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)

        item_number = "235671"
        self.u.scan(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_not_highlighted(1)
        self.u.assert_row_status_blank(1)
        self.u.wait_for_serial_number_box(item_number)

        serial_number = "200810"
        self.u.scan__allow_error(serial_number)
        err_message = "%s is not a valid serial number. Please scan a serial number." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_not_highlighted(1)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_blank()

        serial_number = "99991015000001X99991015000001X99991015000001X"
        self.u.scan__allow_error(serial_number)
        err_message = "%s is not a valid serial number. Please scan a serial number." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_not_highlighted(1)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_blank()

        serial_number = "20081015000008"
        self.u.scan(serial_number)
        self.u.wait_for_serial_number_box_cleared()
        self.u.assert_row_status_gray(0)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_gray()

        serial_number_template = "2008101500000%s"
        for i in (9, 2, 3, 4):
            self.u.scan(item_number)
            self.u.wait_for_serial_number_box(item_number)
            serial_number = serial_number_template % i
            self.u.scan(serial_number)
            self.u.wait_for_serial_number_box_cleared()

        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()

        # Rescan some prevoiusly-scanned serial numbers
        item_number = "235671"
        self.u.scan(item_number)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()
        self.u.wait_for_serial_number_box(item_number)

        serial_number = "20081015000008"
        self.u.scan__allow_error(serial_number)
        err_message = "Serial number %s has already been scanned." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()

        serial_number = "20081015000004"
        self.u.scan__allow_error(serial_number)
        err_message = "Serial number %s has already been scanned." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()

        serial_number = "20081015000000"
        self.u.scan__allow_error(serial_number)
        err_message = "Serial number %s has already been used." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()

        serial_number = "20081015000001"
        self.u.scan__allow_error(serial_number)
        err_message = "Serial number %s has already been used." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()

        serial_number = "20081015000005"
        self.u.scan(serial_number)
        self.u.wait_for_serial_number_box_cleared()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_gray()

        for i in range(6, 8):
            self.u.scan(item_number)
            self.u.wait_for_serial_number_box(item_number)
            serial_number = serial_number_template % i
            self.u.scan(serial_number)
            self.u.wait_for_serial_number_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_highlighted(1)
        self.u.assert_order_status_green()


        serial_numbers_json = ('{"1":{"item_number":"235671", "serial_numbers":["20081015000008", '
                               '"20081015000009", "20081015000002", "20081015000003"]}, "2":{"item'
                               '_number":"235671", "serial_numbers":["20081015000004", "20081015000'
                               '005", "20081015000006", "20081015000007"]}}'
                              )
        self.u.assert_serial_number_json(serial_numbers_json)

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            serial_numbers_encoded = "%7B%221%22%3A%7B%22item_number%22%3A%"
                                     "22235671%22%2C%20%22serial_numbers%22%3A%5B%222008101"
                                     "5000008%22%2C%20%2220081015000009%22%2C%20%2220081015"
                                     "000002%22%2C%20%2220081015000003%22%5D%7D%2C%20%222%22%"
                                     "3A%7B%22item_number%22%3A%22235671%22%2C%20%22serial_n"
                                     "umbers%22%3A%5B%2220081015000004%22%2C%20%2220081015"
                                     "000005%22%2C%20%2220081015000006%22%2C%20%22200810150000"
                                     "07%22%5D%7D%7D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_12_info_box(self):
        """
        The info box should display additional warnings if the user continues
        without dismissing it.
        """
        order_id_scan = "AA00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        table_data = [
            (1, '648484130929', '135428', 0, 3.0,  '10PK', 0),
            (2, '648484173810', '169599', 0, 1.0,  'EA', 0),
            (3, '648484225984', '192048', 0, 4.0,  '5PK', 0),
            (4, '648484225977', '192056', 0, 2.0,  '5PK', 0),
        ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )
        t.finish_order_upc()
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

        self.u.special_key__allow_info(self.u.LEFT_ARROW)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)

        scan_data = "123456"
        self.u.scan__allow_info(scan_data)
        message = ("This order is complete. You can no longer make changes to this order.\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar."
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        scan_data = "648484225984"
        self.u.scan__allow_info(scan_data)
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        self.u.special_key__allow_info(self.u.RIGHT_ARROW)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        self.u.special_key__allow_info(self.u.UP_ARROW)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        self.u.special_key__allow_info(self.u.DOWN_ARROW)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        self.u.key_press__allow_info("+")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        message = "This order is complete. You can no longer make changes to this order."
        self.u.wait_for_text_info_box(message)

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.wait_for_info_box_cleared()

        order_id_scan = "AA00200"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(11)

    def test_13_handle_server_side_error(self):
        """
        Order number AA01800 is "booby-trapped" in pickpack_data_mock.py. It
        throws a server-side error when trying to post complete. Here we test
        the client-side handling of that server-side error.
        """
        order_id_scan = "AA01800"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        table_data = [
            (4, '648484320016', '216326', 0, 2.0,  '5PK', 0),
            (3, '648484320399', '216327', 0, 4.0,  '5PK', 0),
            (1, '648484324984', '216331', 0, 1.0,  'EA', 0),
            (2, '648484296366', '770246', 0, 1.0,  'EA', 0),
        ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )
        t.multi_scan(7, "item")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        scan_data = "648484296366"
        self.u.scan__allow_error(scan_data)
        alert_text = ("Error while writing to the database for order number AA018/00.\n\n"
                      "Press the space bar to try resending the data."
                     )
        self.u.wait_for_error_box(alert_text,
                                  exact_match = False,
                                 )

        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_red()

    def test_14_harper_labels(self):
        """
        Harper item number labels contain a space character. Here we test the
        handling of those labels.
        """
        order_id_scan = "AA01900"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(17)

        table_data = [                                          # Simulate Harper label scans
            (1,  '648484570312', '10N009',  0, 2.0,   'EA', 0, {'harper_label' : '1 10N009'}),
            (2,  '648484570329', '10N010',  0, 10.0,  'EA', 0, {'harper_label' : '1 10N010'}),
            (3,  '648484570336', '10N011',  0, 1.0,   'EA', 0, {'harper_label' : '1 10N011'}),
            (4,  '648484570350', '10N012',  0, 3.0,   'EA', 0),
            (5,  '648484570367', '10N013',  0, 6.0,   'EA', 0, {'harper_label' : '1 10N013'}),
            (6,  '648484570374', '10N014',  0, 7.0,   'EA', 0),
            (7,  '648484570381', '10N015',  0, 2.0,   'EA', 0, {'harper_label' : '1 10N015'}),
            (8,  '648484570398', '10N016',  0, 7.0,   'EA', 0, {'harper_label' : '1 10N016'}),    # 34 gets us to gray on this item
            (9,  '648484570404', '10N017',  0, 7.0,   'EA', 0, {'harper_label' : '1 10N017'}),
            (10, '648484570411', '10N018',  0, 3.0,   'EA', 0, {'harper_label' : '1 10N018'}),
            (11, '648484570480', '10N019',  0, 8.0,   'EA', 0),
            (12, '648484570428', '10N020',  0, 2.0,   'EA', 0, {'harper_label' : '1 10N020'}),
            (13, '648484570435', '10N021',  0, 9.0,   'EA', 0, {'harper_label' : '1 10N021'}),
            (14, '648484570442', '10N022',  0, 10.0,  'EA', 0, {'harper_label' : '1 10N022'}),
            (15, '648484570459', '10N023',  0, 6.0,   'EA', 0, {'harper_label' : '1 10N023'}),
            (16, '648484570466', '10N024',  0, 1.0,   'EA', 0),
            (17, '648484570473', '10N025',  0, 7.0,   'EA', 0),
        ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )

        t.multi_scan(34, "item")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_highlighted(7)
        self.u.assert_row_status_gray(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_order_status_gray()

        harper_item_number = "10N099"
        raw_harper_scan = "1 %s" % harper_item_number
        self.u.scan__allow_error(raw_harper_scan)
        err_message = "That item is not on this order. Item: %s" % harper_item_number
        self.u.wait_for_error_box(err_message)

        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_highlighted(7)
        self.u.assert_row_status_gray(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_highlighted(7)
        self.u.assert_row_status_gray(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_order_status_gray()
        self.u.wait_for_error_box_cleared()

        other_item_number = "000068"
        self.u.scan__allow_error(other_item_number)
        err_message = "That item is not on this order. Item: %s" % other_item_number
        self.u.wait_for_error_box(err_message)

        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_highlighted(7)
        self.u.assert_row_status_gray(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_highlighted(7)
        self.u.assert_row_status_gray(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_order_status_gray()
        self.u.wait_for_error_box_cleared()

        t.finish_order_item()
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_status_green(7)
        self.u.assert_row_status_green(8)
        self.u.assert_row_status_green(9)
        self.u.assert_row_status_green(10)
        self.u.assert_row_status_green(11)
        self.u.assert_row_status_green(12)
        self.u.assert_row_status_green(13)
        self.u.assert_row_status_green(14)
        self.u.assert_row_status_green(15)
        self.u.assert_row_status_green(16)
        self.u.assert_row_highlighted(16)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_15_item_notes(self):
        """
        Some items have one or more PACK notes in item_comments. These should be
        displayed to the user.
        """
        order_id_scan = "AA02000"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)
        self.u.assert_no_info_box()

        self.u.scan__allow_info("648484189750")
        message = "Item Notes for 040206\n\nTest notes for 040206"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_blank()

        self.u.scan__allow_info("648484192644")
        message = ("Item Notes for 040206\n\nTest notes for 040206\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar."
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_blank()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_gray(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("040206")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()
        # No need for self.u.assert_no_info_box here. self.u.scan() checks for info and
        # alert boxes every time

        # One more puts us over the limit.
        self.u.scan("040206")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_red(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_red()

        # Use the arrow to restore green
        self.u.special_key(self.u.LEFT_ARROW)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan__allow_info("040207")
        message = "Item Notes for 040207\n\nTest notes for 040207"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("040207")
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("040207")
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("648484190787")
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan__allow_info("040208")
        message = "Item Notes for 040208\n\nTest notes for 040208"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        # Test getting an info box on the last item
        self.u.scan__allow_info("648484189767")
        message = "Item Notes for 040209\n\nTest notes for 040209\nMore test notes for 040209"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            special_keys_encoded = "%3A%20040206%3A%5B%3C-%5D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_16_more_item_notes(self):
        """
        Some items have one or more PACK notes in item_comments. These should be
        displayed to the user. This test checks some more rare interactions
        between item notes and other ways of incrementing row count.
        """
        order_id_scan = "AA02000"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)
        self.u.assert_no_info_box()

        self.u.special_key(self.u.DOWN_ARROW)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_blank()

        self.u.special_key__allow_info(self.u.RIGHT_ARROW)
        message = "Item Notes for 040206\n\nTest notes for 040206"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_blank()

        self.u.special_key__allow_info(self.u.RIGHT_ARROW)
        message = ("Item Notes for 040206\n\nTest notes for 040206\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar."
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_blank()

        self.u.special_key__allow_info(self.u.LEFT_ARROW)
        message = ("Item Notes for 040206\n\nTest notes for 040206\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar.\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar."
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_blank()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_gray(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan("040206")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()
        # No need for self.u.assert_no_info_box here. self.u.scan() checks for info and
        # alert boxes every time

        self.u.special_key(self.u.DOWN_ARROW)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press__allow_info("+")
        message = "Item Notes for 040207\n\nTest notes for 040207"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        # One more puts us over the limit.
        self.u.scan("040206")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_red(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_red()

        # Use the arrow to restore green
        self.u.special_key(self.u.LEFT_ARROW)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        # One more puts us over the limit.
        self.u.scan("648484190787")
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_red(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_red()

        # Use the arrow to restore green
        self.u.special_key(self.u.LEFT_ARROW)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.scan__allow_info("040208")
        message = "Item Notes for 040208\n\nTest notes for 040208"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        # Test getting an info box on the last item, using the plus key
        self.u.special_key(self.u.DOWN_ARROW)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press__allow_info("+")
        message = "Item Notes for 040209\n\nTest notes for 040209\nMore test notes for 040209"
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            special_keys_encoded = "%3A%20040209%3A%5B%2B%5D%20%20040207%3A%5B"
                                   "%2B%20%3C-%5D%20%20040206%3A%5B-%3E%20%3C-%5D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_17_html_escape_notes(self):
        """
        Some items have one or more PACK notes in item_comments. These should be
        displayed to the user. Here we're testing that html tags and other
        strange characters in the notes are properly html-escaped by the server
        before being sent to the client.
        """
        order_id_scan = "AA02100"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)
        self.u.assert_no_info_box()

        self.u.special_key(self.u.DOWN_ARROW)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_blank()

        self.u.special_key__allow_info(self.u.RIGHT_ARROW)
        message = ("Item Notes for 212728\n\n"
                   "THIS IS A TEST OF PICK PACK ITEM COMMENTS\n"
                   "Here is line 2\n"
                   " /***** SUPER IMPORTANT STUFF *******/\n"
                   "MORE ITEM COMMENTS\n"
                   " Testing HTML escapes\n"
                   '<img src="bla.jpg">\n'
                   "<p>Red</p>\n"
                   "&amp;lt;\n"
                   "<h1>Big</h1>"
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_blank()

        self.u.special_key__allow_info(self.u.RIGHT_ARROW)
        message = ("Item Notes for 212728\n\n"
                   "THIS IS A TEST OF PICK PACK ITEM COMMENTS\n"
                   "Here is line 2\n"
                   " /***** SUPER IMPORTANT STUFF *******/\n"
                   "MORE ITEM COMMENTS\n"
                   " Testing HTML escapes\n"
                   '<img src="bla.jpg">\n'
                   "<p>Red</p>\n"
                   "&amp;lt;\n"
                   "<h1>Big</h1>\n"
                   "I can not proceed while this information box is visible. Please "
                   "dismiss this box by pressing the space bar."
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_blank()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_gray(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_gray()
        # No need for self.u.assert_no_info_box here. self.u.key_press() checks for info
        # and alert boxes every time.

        self.u.key_press("+")
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_gray()

        self.u.scan__allow_info('648484019750')
        message = ('Item Notes for 039611\n\n'
                   'Testing html in comments, to make sure it is escaped properly.\n'
                   'If it is properly escaped, it will be displayed to the user '
                   'verbatim, instead of being parsed as HTML.\n'
                   '<pre>TEST</pre>\n'
                   '& &; &lt; &amp; &amp;lt;'
                  )
        self.u.wait_for_text_info_box(message)
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_order_status_gray()

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_gray(1)
        self.u.assert_order_status_gray()

        self.u.scan("039611")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            special_keys_encoded = "%3A%20212728%3A%5B-%3E%20%2B%5D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_options_pane(self):
        """
        Test the options pane
        """
        order_id_scan = "AA00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        self.u.assert_no_options_pane()
        self.u.assert_no_help_pane()

        self.u.special_key(self.u.F4)
        self.u.wait_for_options_pane_to_appear()
        self.u.special_key(self.u.F1)
        self.u.assert_no_help_pane()
        self.u.special_key(self.u.F1)
        self.u.assert_no_help_pane()

        # Type in a user ID
        self.u.type_data_in_field(self.u.DEFAULT_USER, self.u.USER_ID_FIELD)

        self.u.special_key(self.u.F4)
        self.u.wait_for_options_pane_to_disappear()

        self.u.special_key(self.u.F4)
        self.u.wait_for_options_pane_to_appear()
        self.u.special_key(self.u.F1)
        self.u.assert_no_help_pane()
        self.u.special_key(self.u.F1)
        self.u.assert_no_help_pane()
        self.u.special_key(self.u.F4)
        self.u.wait_for_options_pane_to_disappear()

        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

    def test_help_pane(self):
        """
        Test the help pane
        """
        order_id_scan = "AA00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        self.u.assert_no_options_pane()
        self.u.assert_no_help_pane()

        self.u.special_key(self.u.F1)
        self.u.wait_for_help_pane_to_appear()
        self.u.special_key(self.u.F4)
        self.u.assert_no_options_pane()
        self.u.special_key(self.u.F4)
        self.u.assert_no_options_pane()
        self.u.special_key(self.u.F1)
        self.u.wait_for_help_pane_to_disappear()

        self.u.special_key(self.u.F1)
        self.u.wait_for_help_pane_to_appear()
        self.u.special_key(self.u.F4)
        self.u.assert_no_options_pane()
        self.u.special_key(self.u.F4)
        self.u.assert_no_options_pane()
        self.u.special_key(self.u.F1)
        self.u.wait_for_help_pane_to_disappear()

        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

    def test_18_order_not_found(self):
        """
        Test what happens when an order is not found.
        """
        # The app should see it as an item number
        scan_data = "000068"
        self.u.scan__allow_error(scan_data)
        err_message = "That item is not on this order. Item: %s" % scan_data
        self.u.wait_for_error_box(err_message)

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()

    def test_19_order_not_found(self):
        """
        Test what happens when an order is not found.
        """
        order_id_scan = "7XH6Q66"
        self.u.scan__allow_error(order_id_scan)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(order_id_scan)
        self.u.wait_for_error_box(err_message)

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()

    def test_19_serial_number_box(self):
        """
        Test the behavior of the serial number input box.
        """
        order_id_scan = "AA01100"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        item_number = "235671"
        self.u.scan(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.wait_for_serial_number_box(item_number)
        serial_number = "9999104443339999104443339999104"
        self.u.scan__allow_error(serial_number)
        err_message = "%s is not a valid serial number. Please scan a serial number." % serial_number
        self.u.wait_for_error_box(err_message)
        self.u.assert_order_status_red()

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.wait_for_serial_number_box(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_order_status_blank()

        self.u.key_press(" ")
        self.u.wait_for_serial_number_box_cleared()
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_order_status_blank()

        item_number = "235671"
        self.u.scan(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.wait_for_serial_number_box(item_number)

        self.u.key_press(" ")
        self.u.wait_for_serial_number_box_cleared()
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.assert_order_status_blank()

        item_number = "235671"
        self.u.scan(item_number)
        self.u.assert_row_not_highlighted(0)
        self.u.assert_row_status_blank(0)
        self.u.wait_for_serial_number_box(item_number)

        serial_number = "20081015000008"
        self.u.scan(serial_number)
        self.u.wait_for_serial_number_box_cleared()
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_highlighted(0)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(
            order_id_scan,
            serial_numbers_encoded = "%7B%221%22%3A%7B%22item_number%22%3A%22"
                                     "235671%22%2C%20%22serial_numbers%22%3A%5B%22"
                                     "20081015000008%22%5D%7D%7D",
           )
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_20_order_not_found_case_insensitive(self):
        """
        Test what happens when an order is not found.
        """
        order_id_scan = "zz12301"
        self.u.scan__allow_error(order_id_scan)
        err_message = "Order number %s not found." % self.u.build_order_number_for_display(order_id_scan)
        self.u.wait_for_error_box(err_message)

        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()

    def test_21_case_insensitive(self):
        """
        Quick smoke test
        """
        order_id_scan = "aa00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan.upper())
        self.u.assert_row_count(4)

    def test_22_one_digit_order_generation(self):
        """
        Test the handling of order generation numbers. 1
        """
        order_id_scan = "AA51000"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan("216331")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_23_one_digit_order_generation(self):
        """
        Test the handling of order generation numbers. 2
        """
        order_id_scan = "AA51109"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan("648484395663")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_24_two_digit_order_generation(self):
        """
        Test the handling of order generation numbers. 3
        """
        order_id_scan = "AA51210"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan("648484324984")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_25_two_digit_order_generation(self):
        """
        Test the handling of order generation numbers. 4
        """
        order_id_scan = "AA51320"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan("235671")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_26_two_digit_order_generation(self):
        """
        Test the handling of order generation numbers. 5
        """
        order_id_scan = "AA51499"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan("648484324984")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_27_two_digit_order_generation(self):
        """
        Test the handling of order generation numbers. 6
        """
        order_id_scan = "AA51599"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan("235671")
        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_order_status_green()
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_28_trimming_input(self):
        """
        The javascript that handles user input should trim leading and trailing
        spaces off of the user input before passing it to the rest of the
        program. However, if the user presses the space bar alone, the program
        should respond to that as a command (dismiss the dialog box).
        """
        order_id_scan = "AA73000"
        self.u.scan(order_id_scan)

        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)

        self.u.scan("282828")
        self.u.scan("282828      ")
        self.u.scan("       282828")
        self.u.scan("       282828      ")
        self.u.scan("648484352520")
        self.u.scan("648484352520      ")
        self.u.scan("       648484352520")
        self.u.scan("       648484352520      ")

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)


class TestPickpackNoCookie(BaseForPickpackTestsNoCookie):
    """
    These are some Selenium tests for the Pick Pack project. These tests test
    what happens when no cookie is set.
    """
    def __init__(self):
        BaseForPickpackTestsNoCookie.__init__(self)

    def test_01_quicktest(self):
        """
        Quick smoke test
        """
        self.u.assert_display_user_id(self.u.USER_NOT_SET)
        order_id_scan = "AA00300"
        self.u.scan__allow_info(order_id_scan)

        message = "Press F4 to set your user id."
        self.u.wait_for_text_info_box(message)
        self.u.assert_order_status_blank()
        self.u.assert_display_user_id(self.u.USER_NOT_SET)

        self.u.key_press(" ")
        self.u.assert_order_status_blank()
        self.u.wait_for_info_box_cleared()
        self.u.assert_display_user_id(self.u.USER_NOT_SET)

    def test_02_multitest(self):
        """
        Test seeing the info box several times
        """
        for ignore in range(2):
            self.test_01_quicktest()

    def test_03_set_cookie_test(self):
        """
        Test setting the cookie by adding user id data.
        """
        # This test starts out the same as the others
        self.test_01_quicktest()

        self.u.special_key(self.u.F4)
        self.u.wait_for_options_pane_to_appear()
        self.u.assert_display_user_id(self.u.USER_NOT_SET)
        self.u.assert_options_pane_user_id(self.u.USER_NOT_SET)

        # Type in a user ID
        self.u.type_data_in_field(self.u.DEFAULT_USER, self.u.USER_ID_FIELD)

        # The user id has been changed in the options pane, but not yet in the
        # display.
        self.u.assert_display_user_id(self.u.USER_NOT_SET)
        self.u.assert_options_pane_user_id(self.u.DEFAULT_USER)

        self.u.special_key(self.u.F4)
        self.u.wait_for_options_pane_to_disappear()

        # Now the user id has been changed in the display.
        self.u.assert_display_user_id(self.u.DEFAULT_USER)

        order_id_scan = "AA00300"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(4)

        self.u.special_key(self.u.F3)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_highlighted(0)

        table_data = [
            (1, '648484130929', '135428', 0, 3.0,  '10PK', 0, {'highlight' : True}),
            (2, '648484173810', '169599', 0, 1.0,  'EA', 0),
            (3, '648484225984', '192048', 0, 4.0,  '5PK', 0),
            (4, '648484225977', '192056', 0, 2.0,  '5PK', 0),
        ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )
        t.finish_order_upc()
        self.u.wait_for_big_green()
        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_highlighted(3)
        self.u.assert_row_status_green(3)
        self.u.assert_order_status_green()
        self.u.assert_display_user_id(self.u.DEFAULT_USER)
        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)


#class TestPickpackWithWebdriver(object):
#    """
#    This class holds all the Webdriver tests for the Pick Pack project.
#    """
#
#    w = WebdriverTestingUtility()           # pylint: disable=C0103
#
#    @classmethod
#    def setup_class(cls):
#        """
#        This will run only once, before each test run
#        """
#        cls.w.start_webdriver_server()
#
#    @classmethod
#    def teardown_class(cls):
#        """
#        This will run only once, after each test run
#        """
#        cls.w.stop_webdriver_server()
#
#    def setup(self):
#        """
#        This will run once for each test method in this class
#        """
#        self.w.open_aut()
#
#    def test_01_quicktest(self):
#        """
#        Quick smoke test
#        """





# Debugging breakpoints, in Komodo and in iPython
#
#
#
# Set remote breakpoint in Komodo. Komodo must be running on 1bk2zq1-190.
# Debugging listener must be listening on port 8201. See debug.py for
# configuration of remote debugging.
#
## DE BUG Note: In order for this de-bugging to be triggered, mra must be run
## using the dbg, dbg2, dbg3 commands on partsappdev.
#from CML_Common.error.debug import debug_utility_object as debugObj
#debugObj.debugBreakpoint()
#
#
#
#
# Set local breakpoint in iPython.
#
## DE BUG Note: In order for this de-bugging to be triggered, mra must be run
## using the dbg, dbg2, dbg3 commands on partsappdev.
#from CML_Common.error.debug import debug_utility_object as debugObj
#debugObj.debugIpythonBreakpoint()
#
#
#
#
#
# Set local breakpoint in pudb.
#
## DE BUG Note: In order for this de-bugging to be triggered, mra must be run
## using the dbg, dbg2, dbg3 commands on partsappdev.
#from CML_Common.error.debug import debug_utility_object as debugObj
#debugObj.debugPudbBreakpoint()
