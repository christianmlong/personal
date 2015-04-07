# pylint: disable=C0111,W0142,R0903,R0904
import time, os.path, urllib, urlparse, socket
from nose import tools
from selenium import webdriver
from selenium import selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from CML_Pickpack.test.selenium import constants


# Decorators
#
# Note: These decorators are used to decorate methods in the classes in this
# module. I tried defining these decorators inside the classes themselves; I
# defined them as @staticmethods. However, that didn't work, because when
# a method that is defined as a static method (decorated with the @staticmethod
# decorator) is referred to inside the class, the reference gets a staticmethod
# object, not a bound method object. staticmethod objects are not callable.
#
# This was the error
#
# TypeError: 'staticmethod' object is not callable
#
# Only by looking the static method up in an object do you get the bound method.
#
# More info:
# http://stackoverflow.com/questions/6412146/python-decorator-as-a-staticmethod
# http://stackoverflow.com/a/6412373/456550

def no_error_allowed(fn):
    """
    This function is used as a decorator. Functions that are decorated with
    it must not show any error or info box.
    """
    def wrapper(self, *args, **kwargs):
        # Call the input function (_scan, _key_press, etc.)
        fn(self, *args, **kwargs)

        # Assert that no error occurred as a result of that input, and that
        # the info box is not visible, and that no JavaScript alert box is
        # visible.
        self.assert_no_error_condition()

        # The original function (scan, key_press, etc.) had no return value,
        # so this new decorated function also has no return value.

    return wrapper

def only_info_allowed(fn):
    """
    This function is used as a decorator. Functions that are decorated with
    it must not show the error box. They can show the info box.
    """
    def wrapper(self, *args, **kwargs):
        # Call the input function (_scan, _key_press, etc.)
        fn(self, *args, **kwargs)

        # Assert that no error occurred as a result of that input, and that
        # no JavaScript alert box is visible. An info box is allowed.
        self.assert_only_info_condition()

        # The original function (scan, key_press, etc.) had no return value,
        # so this new decorated function also has no return value.

    return wrapper


class BaseTestingUtility(object):
    """
    Base class for utility classes for testing with Selenium
    """
    # These are Selenium RC element locators. For more info on locators in
    # Selenium RC, see the comments at the bottom of this document.
    FOCUS_FOR_INPUT = "dom=document"
    USER_ID_FIELD = "id=user_id"
    DISPLAY_USER_ID_FIELD = "id=display_user_id"
    F1  = "\\112"
    F2  = "\\113"
    F3  = "\\114"
    F4  = "\\115"
    F6  = "\\117"
    #F7  = "\\118"
    #F8  = "\\119"
    #F9  = "\\120"
    #F10 = "\\121"
    #F11 = "\\122"
    F12 = "\\123"
    TAB_KEY = "\\9"


    # A path to a real resource, used for pre-loading something from
    # the domain so Selenium can set a cookie.
    DUMMY_PATH = '/static/img/yellow2.png'

    def __init__(self):
        # Selenium server is running on the current machine.
        self.host = socket.getfqdn()
        self.port = 4444
        self.browser = '*firefox %s' % constants.PATH_TO_FIREFOX
        self.aut_url = "http://%s:%s%s" % (constants.HOST_TO_TEST,
                                           constants.PORT_TO_TEST,
                                           self.PATH,
                                          )
        self.dummy_url = "http://%s:%s%s" % (constants.HOST_TO_TEST,
                                             constants.PORT_TO_TEST,
                                             self.DUMMY_PATH,
                                            )
        self._selenium_server = None

    def set_up_selenium_connection_to_selenium_server(self):
        print "host %s" % self.host
        print "port %s" % self.port
        print "browser %s" % self.browser
        print "aut_url %s" % self.aut_url
        print
        self._selenium_server = selenium(self.host,
                                         self.port,
                                         self.browser,
                                         self.aut_url,
                                        )
        self._selenium_server.start()

    def set_up_webdriver_backed_selenium_connection_to_selenium_server(self):
        def _build_url(host,
                       url_path,
                      ):
            url_elements = ('http',
                            host,
                            urllib.quote(url_path),
                            None,
                            None,
                           )
            return urlparse.urlunsplit(url_elements)

        url_of_remote_selenium_server = _build_url('%s:%s' % (self.host, self.port),
                                                   '/wd/hub',
                                                  )
        _webdriver_driver = webdriver.Remote(url_of_remote_selenium_server,
                                             DesiredCapabilities.FIREFOX,
                                            )
        self._selenium_server = selenium(self.host,
                                         self.port,
                                         '*webdriver',
                                         self.aut_url,
                                        )
        self._selenium_server.start(driver = _webdriver_driver)

    #def set_up_webdriver_connection_to_local_htmlunit(self):
    #    pass

    def start_selenium_server(self):
        self.set_up_selenium_connection_to_selenium_server()

    def stop_selenium_server(self):
        self._selenium_server.stop()

    def set_up_environment(self):
        """
        Set up the browser environment for the test. For example, set cookies
        here.
        """
        # We have to navigate to a dummy url first so we can set the cookie.
        self._selenium_server.open(self.dummy_url)                          # pylint: disable=no-member
        self.set_our_cookie()                                               # pylint: disable=no-member

    def set_cookie(self,
                   cookie_name,
                   cookie_value,
                   cookie_path,
                  ):
        """
        Set a cookie in the browser.
        """
        # WebDriver api
        #cookie_data = {'name' : cookie_name,
        #               'value' : cookie_value,
        #               'path' : cookie_path,
        #              }
        #self._selenium_server.add_cookie(cookie_data)

        # Classic selenium api
        cookie_string = '%s=%s' % (cookie_name,
                                   cookie_value,
                                  )
        cookie_options = "path=%s" % cookie_path
        #cookie_options = "path=%s,max_age=60" % cookie_path
        self._selenium_server.create_cookie(cookie_string,
                                            cookie_options,
                                           )

    def open_aut(self):
        """
        Open a browser, and load the Application Under Test (AUT)
        """
        # Set up the environment first, so the cookies are there before the
        # page opens.
        self.set_up_environment()
        self._selenium_server.open(self.aut_url)

    def scan(self,
             scanned_input,
             repeat = None,
            ):
        if repeat is None:
            repeat = 1

        for ignore_i in range(repeat):
            self.scan__allow_error(scanned_input)

        # Fast, no error checking after each scan
        #self.scan__allow_error(scanned_input)

        # Slow (~ 5x slower)
        #self._scan(scanned_input)

    def key_press(self,
                  key,
                  target = None,
                 ):
        # Fast, no error checking after each scan
        self.key_press__allow_error(key,
                                    target = target,
                                   )

        # Slow (~ 5x slower)
        #self.key_press__verify_no_error(key,
        #                                target = target,
        #                               )

    def special_key(self, key_code_string):
        # Fast, no error checking after each scan
        self.special_key__allow_error(key_code_string)

        # Slow (~ 5x slower)
        #self.special_key__verify_no_error(key_code_string)

    def type_data_in_field(self,
                           data_to_type,
                           field_locator,
                          ):
        # field_locator is a Selenium RC element locator. For more info on
        # locators in Selenium RC, see the comments at the bottom of this
        # document.
        self._selenium_server.type(field_locator,
                                   data_to_type,
                                  )

    @no_error_allowed
    def scan__verify_no_error(self, scanned_input):
        self._scan(scanned_input)

    @no_error_allowed
    def key_press__verify_no_error(self,
                  key,
                  target = None,
                 ):
        self._key_press(key,
                        target = target,
                       )

    @no_error_allowed
    def special_key__verify_no_error(self, key_code_string):
        self._special_key(key_code_string)

    @only_info_allowed
    def scan__allow_info(self, scanned_input):
        self._scan(scanned_input)

    @only_info_allowed
    def key_press__allow_info(self,
                              key,
                              target = None,
                             ):
        self._key_press(key,
                        target = target,
                       )

    @only_info_allowed
    def special_key__allow_info(self, key_code_string):
        self._special_key(key_code_string)

    def scan__allow_error(self, scanned_input):
        self._scan(scanned_input)

    def key_press__allow_error(self,
                               key,
                               target = None,
                              ):
        self._key_press(key,
                        target = target,
                       )

    def special_key__allow_error(self, key_code_string):
        self._special_key(key_code_string)

    def _scan(self, scanned_input):
        for char in scanned_input:
            self._key_press(char)
        self._special_key(self.TAB_KEY)

    def _key_press(self,
                   key,
                   target = None,
                  ):
        if target is None:
            target = self.FOCUS_FOR_INPUT
        self._selenium_server.key_press(target, key)

    def _special_key(self, key_code_string):
        self._selenium_server.key_down(self.FOCUS_FOR_INPUT, key_code_string)
        self._selenium_server.key_up(self.FOCUS_FOR_INPUT, key_code_string)

    def assert_eval(self,
                    javascript,
                    expected_result,
                   ):
        # Assert a JavaScript expression evaluates to the desired result (right now,
        # with no timeout).
        actual_result = self._selenium_server.get_eval(javascript)
        self.assert_eq(actual_result, expected_result)

    def fail_if_eval(self,
                     javascript,
                     unwanted_result,
                    ):
        # Assert a JavaScript expression does not evaluate to the given result
        # (right now, with no timeout).
        actual_result = self._selenium_server.get_eval(javascript)
        self.assert_neq(actual_result, unwanted_result)

    def wait_for_eval(self,
                      javascript,
                      expected_result,
                     ):
        # Wait for a JavaScript expression to evaluate to the desired result.
        # Fail if it does not do so within the allotted time. Default time is 5
        # seconds - use the "timeout" argument to specify a value other than the
        # default.
        self.wait_in_python_for_selenium_condition(expected_result, self._selenium_server.get_eval, javascript)

    @staticmethod
    def fail(msg):
        tools.assert_true(False, msg)           # pylint: disable=E1101

    def locate_box(self,
                   div_id,
                   span_id,
                  ):
        self.wait_for_element_visible("id=%s" % div_id)
        return "xpath=//div[@id='%s']//span[@id='%s']" % (div_id, span_id)

    def wait_for_box_text(self,
                          div_id,
                          span_id,
                          expected_msg,
                          exact_match = True,
                         ):
        locator = self.locate_box(div_id,
                                  span_id,
                                 )
        actual_msg = self.get_text(locator).encode() # unicode to ascii
        if exact_match:
            self.assert_eq(actual_msg, expected_msg)
        else:
            tools.ok_(actual_msg.startswith(expected_msg))

    def wait_for_box_html(self,
                          div_id,
                          span_id,
                          expected_html,
                         ):
        locator = self.locate_box(div_id,
                                  span_id,
                                 )
        #javascript = """selenium.browserbot.findElement("%s", browserbot.getCurrentWindow()).innerHTML"""
        javascript = """selenium.browserbot.findElement("%s").innerHTML""" % locator
        actual_html = self._selenium_server.get_eval(javascript)
        self.assert_eq(actual_html, expected_html)


        # Other ways to formulate the JavaScript
        #
        #html = selenium.getEval("this.browserbot.findElement(\"id=someElementId\").innerHTML");
        #selenium.getEval("selenium.browserbot.getCurrentWindow().document.getElementById('test').innerHTML");
        #selenium.getEval("selenium.browserbot.getCurrentWindow().document.getElementById('test').innerHTML");
        #
        #String name = selenium.getEval(
        #    "selenium.browserbot.findElement('id=foo', browserbot.getCurrentWindow()).tagName");
        #
        #becomes:
        #
        #WebElement element = driver.findElement(By.id("foo"));
        #String name = (String) ((JavascriptExecutor) driver).executeScript(
        #    "return arguments[0].tagName", element);

    def wait_for_element_present(self, element_locator):
        self.wait_in_python_for_selenium_condition(True, self._selenium_server.is_element_present, element_locator)

    def wait_for_element_not_present(self, element_locator):
        self.wait_in_python_for_selenium_condition(False, self._selenium_server.is_element_present, element_locator)

    def wait_for_element_visible(self, element_locator):
        self.wait_in_python_for_selenium_condition(True, self._selenium_server.is_visible, element_locator)

    def wait_for_element_not_visible(self, element_locator):
        self.wait_in_python_for_selenium_condition(False, self._selenium_server.is_visible, element_locator)

    def wait_in_python_for_selenium_condition(self, expected_result, func, *args):
        timeout = 5
        time_increment = .1
        self._timeout(expected_result,
                      True,
                      func,
                      timeout,
                      time_increment,
                      *args
                     )

    def assert_no_error_condition(self):
        self.assert_selenium_condition_did_not_occur_within_timeout(True, self._error_condition)

    def assert_only_info_condition(self):
        self.assert_selenium_condition_did_not_occur_within_timeout(True, self._only_info_condition)

    #def assert_no_alert(self):
    #    assert_selenium_condition_did_not_occur_within_timeout(True, self._selenium_server.is_alert_present)


    def wait_for_error_box(self,
                           expected_msg,
                           exact_match = True,
                          ):
        self.wait_for_box_text("%s_error_box" % self.ID_PREFIX,                                 # pylint: disable=E1101
                               "%s_error_text" % self.ID_PREFIX,                                 # pylint: disable=E1101
                               expected_msg,
                               exact_match = exact_match,
                              )

    def wait_for_error_box_cleared(self):
        self.wait_for_element_not_visible("id=%s_error_box" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def wait_for_text_info_box(self, expected_msg):
        # Sometimes the info box contains only text
        self.wait_for_box_text("%s_info_box" % self.ID_PREFIX,                                 # pylint: disable=E1101
                               "%s_info_body" % self.ID_PREFIX,                                 # pylint: disable=E1101
                               expected_msg,
                              )

    def wait_for_multimedia_info_box(self, expected_html):
        # Sometimes the info box contains images, or a combination of text and
        # images
        self.wait_for_box_html("%s_info_box" % self.ID_PREFIX,                                 # pylint: disable=E1101
                               "%s_info_body" % self.ID_PREFIX,                                 # pylint: disable=E1101
                               expected_html,
                              )

    def wait_for_info_box_cleared(self):
        self.wait_for_element_not_visible("id=%s_info_box" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def wait_for_options_pane_to_appear(self):
        self.wait_for_element_visible("id=%s_options_pane" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def wait_for_options_pane_to_disappear(self):
        self.wait_for_element_not_visible("id=%s_options_pane" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def wait_for_help_pane_to_appear(self):
        self.wait_for_element_visible("id=%s_help_pane" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def wait_for_help_pane_to_disappear(self):
        self.wait_for_element_not_visible("id=%s_help_pane" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def assert_no_error_occurred(self):
        self.assert_element_was_not_visible_within_timeout("id=%s_error_box" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def assert_no_info_box(self):
        self.assert_element_was_not_visible_within_timeout("id=%s_info_box" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def assert_no_options_pane(self):
        self.assert_element_was_not_visible_within_timeout("id=%s_options_pane" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def assert_no_help_pane(self):
        self.assert_element_was_not_visible_within_timeout("id=%s_help_pane" % self.ID_PREFIX)                                 # pylint: disable=E1101

    def _error_condition(self):
        is_visible_pkpk_error_box = self._selenium_server.is_visible("id=%s_error_box" % self.ID_PREFIX)                                 # pylint: disable=E1101
        is_visible_pkpk_info_box = self._selenium_server.is_visible("id=%s_info_box" % self.ID_PREFIX)                                 # pylint: disable=E1101
        is_alert_present = self._selenium_server.is_alert_present()
        alert_msg = ""

        if is_alert_present:
            alert_msg = self._selenium_server.get_alert()

        there_is_an_error_condition =  (  is_visible_pkpk_error_box
                                       or is_visible_pkpk_info_box
                                       or is_alert_present
                                       )

        if there_is_an_error_condition:
            # Output a little detail to stdout
            print 'is_visible_pkpk_error_box: %s' % is_visible_pkpk_error_box
            print 'is_visible_pkpk_info_box: %s' % is_visible_pkpk_info_box
            print 'is_alert_present: %s message: %s' % (is_alert_present, alert_msg)

        return there_is_an_error_condition

    def _only_info_condition(self):
        is_visible_pkpk_error_box = self._selenium_server.is_visible("id=%s_error_box" % self.ID_PREFIX)                                 # pylint: disable=E1101
        is_alert_present = self._selenium_server.is_alert_present()
        alert_msg = ""

        if is_alert_present:
            alert_msg = self._selenium_server.get_alert()

        there_is_an_error_condition =  (  is_visible_pkpk_error_box
                                       or is_alert_present
                                       )

        if there_is_an_error_condition:
            # Output a little detail to stdout
            print 'is_visible_pkpk_error_box: %s' % is_visible_pkpk_error_box
            print 'is_alert_present: %s message: %s' % (is_alert_present, alert_msg)

        return there_is_an_error_condition

    def assert_element_was_not_visible_within_timeout(self, element_locator):
        self.assert_selenium_condition_did_not_occur_within_timeout(True, self._selenium_server.is_visible, element_locator)

    def assert_selenium_condition_did_not_occur_within_timeout(self, unwanted_result, func, *args):
        timeout = 1
        #timeout = .5
        time_increment = .1
        self._timeout(unwanted_result,
                      False,
                      func,
                      timeout,
                      time_increment,
                      *args
                     )

    def _timeout(self,
                 tested_result,
                 positive,
                 func,
                 timeout,
                 time_increment,
                 *args
                ):
        actual_result = None
        loop_iterations = int(timeout/time_increment)

        if positive:
            # We're looking for a positive result. Fail if it does not happen in
            # time.
            for ignore_i in range(loop_iterations):
                #try:
                actual_result = func(*args)
                if actual_result == tested_result:
                    break
                #except:
                    #pass
                time.sleep(time_increment)
            else:
                # This is an else clause on the for loop. It executes if the loop
                # terminates naturally (by running its course without encountering a
                # "break" statement).
                error_msg = "Time out. The expected result of call to function '%s' " \
                            "with arguments %s was '%s'. Actual result '%s' " \
                            % (func.__name__, args, tested_result, actual_result)
                self.fail(error_msg)
        else:
            # We're asserting the condition did not occur within the timeout. If
            # it did, fail.
            for ignore_i in range(loop_iterations):
                actual_result = func(*args)
                if actual_result == tested_result:
                    error_msg = "Failure. The unwanted result %s occurred within " \
                                "%s seconds. Call to function '%s' with arguments %s  " \
                                % (tested_result, timeout, func.__name__, args)
                    self.fail(error_msg)
                time.sleep(time_increment)

    def wait_for_alert(self,
                       expected_alert_text,
                       exact_match = True,
                      ):
        timeout = 5
        time_increment = .1
        loop_iterations = int(timeout/time_increment)

        # Strip out the newlines
        expected_alert_text = ' '.join(expected_alert_text.split('\n'))

        # We're looking for an alert box. Fail if it does not appear in time.
        # Note: selenium.get_alert also dismisses the alert box.
        for ignore_i in range(loop_iterations):
            if self._selenium_server.is_alert_present():
                if exact_match:
                    self.assert_eq(self._selenium_server.get_alert(), expected_alert_text)
                else:
                    tools.ok_(self._selenium_server.get_alert().startswith(expected_alert_text))
                break
            time.sleep(time_increment)
        else:
            # This is an else clause on the for loop. It executes if the loop
            # terminates naturally (by running its course without encountering a
            # "break" statement).
            error_msg = "Did not see an alert within %s seconds." % timeout
            self.fail(error_msg)

    def element_has_class(self, locator, desired_class):
        element_classes = self.get_attribute(locator, "class")
        return element_classes.count(desired_class) == 1

    def get_attribute(self,
                      locator,
                      attribute,
                     ):
        attribute_locator = "%s@%s" % (locator, attribute)
        return self._selenium_server.get_attribute(attribute_locator)

    def get_text(self,
                 locator,
                ):
        """
        Get the text content of an element. Like innerHtml.
        """
        return self._selenium_server.get_text(locator)

    def get_value(self,
                 locator,
                ):
        """
        Get the value of an input element.
        """
        return self._selenium_server.get_value(locator)

    @staticmethod
    def assert_gt(a, b):
        # tools.ok_ is the same as "assert"
        tools.ok_(a > b, "%r is not greater than %r" % (a, b))

    @staticmethod
    def assert_geq(a, b):
        tools.ok_(a >= b, "%r is not greater than or equal to %r" % (a, b))

    @staticmethod
    def assert_lt(a, b):
        tools.ok_(a < b, "%r is not less than %r" % (a, b))

    @staticmethod
    def assert_leq(a, b):
        tools.ok_(a <= b, "%r is not less than or equal to %r" % (a, b))

    @staticmethod
    def assert_neq(a, b):
        tools.ok_(a != b, "%r is equal to %r" % (a, b))

    @staticmethod
    def assert_eq(a, b):
        tools.eq_(a, b)

    @staticmethod
    def pause(time_in_seconds):
        time.sleep(time_in_seconds)


class PickpackTestingUtility(BaseTestingUtility):
    """
    A class to hold all kinds of utility functions for testing Pick Pack with
    Selenium
    """
    PATH = '/'
    ID_PREFIX = 'pkpk'

    DATA_TABLE_ID = "table_of_items"
    # This is a Selenium RC element locator. For more info on locators in
    # Selenium RC, see the comments at the bottom of this document.
    DATA_TABLE_LOCATOR = "xpath=//table[@id='%s']" % DATA_TABLE_ID
    LEFT_ARROW = "\\37"
    UP_ARROW = "\\38"
    RIGHT_ARROW = "\\39"
    DOWN_ARROW = "\\40"
    #DEFAULT_USER = "5454"
    #DEFAULT_USER = "%3F%3F%3F"
    DEFAULT_USER = "CML"
    USER_NOT_SET = "***"

    class Columns(object):
        status = 0
        status_img = 1
        cur_qty = 2
        qty = 3
        item = 4
        um = 5
        serialized = 6
        info_img = 7

    class Status(object):
        blank = 0
        gray = 1
        red = 2
        yellow = 3
        green = 4

    def __init__(self):
        BaseTestingUtility.__init__(self)

    def set_our_cookie(self):
        """
        Set a cookie in the browser.
        """
        cookie_name = 'pkpkOptions'
        cookie_value = 'orderCompleteSound:crystal_glass&errorSound:whistle&scanBeep:none&useFade:true&userId:%s' % self.DEFAULT_USER
        cookie_path = self.PATH
        self.set_cookie(cookie_name,
                        cookie_value,
                        cookie_path,
                       )

    def wait_for_packing_list_request_made_and_data_returned(self, scanned_input):
        self.wait_for_packing_list_request(scanned_input)
        self.wait_for_element_present(self.DATA_TABLE_LOCATOR)

    def assert_brand_new_order(self, order_id_scan):
        # Wait for the packing list request to be made
        self.wait_for_packing_list_request_made_and_data_returned(order_id_scan)

        # Make sure the order number is displayed properly
        self.wait_for_order_number_display(
            self.build_order_number_for_display(order_id_scan)
        )

        # Make sure the order status is blank
        self.assert_order_status_blank()

        # Make sure all the rows are blank and not highlighted
        self.assert_all_rows_blank_and_not_highlighted()

    def build_order_number_for_display(self, order_id_scan):
        (order_number,
         ignore_order_generation,
         text_order_generation,
        ) = self.parse_order_id_scan(order_id_scan)

        return "%s/%s" % (order_number, text_order_generation)

    @staticmethod
    def parse_order_id_scan(order_id_scan):
        order_id_scan = order_id_scan.upper()
        order_number = order_id_scan[:5]
        order_generation = int(order_id_scan[5:7])

        if 0 <= order_generation < 10:
            text_order_generation = "0%s" % order_generation
        else:
            text_order_generation = str(order_generation)

        return (order_number,
                order_generation,
                text_order_generation,
               )

    def assert_all_rows_blank_and_not_highlighted(self,
                                                  excluded_indicies = None,
                                                 ):
        if excluded_indicies is None:
            excluded_indicies = []

        number_of_rows = self.count_item_rows()
        for i in range(number_of_rows):
            if i not in excluded_indicies:
                self.assert_row_status_blank(i)
                self.assert_row_not_highlighted(i)

    def assert_no_rows(self):
        number_of_rows = self.count_item_rows()
        self.assert_eq(number_of_rows, 0)

    def assert_scanned_undetermined_number(self, scanned_input):
        self.wait_for_characterize_user_input(scanned_input)

    def wait_for_serial_number_box(self, item_number):
        expected_msg = "Please scan a serial number for item %s" % item_number
        self.wait_for_box_text("%s_serial_no_box" % self.ID_PREFIX,
                               "%s_serial_no_text" % self.ID_PREFIX,
                               expected_msg,
                              )

    def wait_for_serial_number_box_cleared(self):
        self.wait_for_element_not_visible("id=%s_serial_no_box" % self.ID_PREFIX)

    def wait_for_big_green(self):
        self.wait_for_big_green_to_appear()
        self.wait_for_big_green_to_disappear()

    def wait_for_big_green_to_appear(self):
        self.wait_for_element_visible("id=big_green")

    def wait_for_big_green_to_disappear(self):
        self.wait_for_element_not_visible("id=big_green")

    def assert_no_serial_number_box(self):
        self.assert_element_was_not_visible_within_timeout("id=%s_serial_no_box" % self.ID_PREFIX)

    def cell_contents(self,
                      row,
                      column,
                     ):
        # Returns the value found in the specified cell
        #
        # Note: the row and column arguments are both zero-based positional
        # specifiers.
        cell_specifier = "%s.%s.%s" % (self.DATA_TABLE_ID, row, column)
        return self._selenium_server.get_table(cell_specifier)

    def cell_contents_by_row_id_and_column_class(self,
                                                 row_id,
                                                 column_class,
                                                ):
        # Returns the value found in the specified cell
        #
        # Note: the row argument is the html id attribute of the <tr>, which is
        # also the oe_detail line_no. The column_class argument is the html
        # class attribute of the desired <td> table cell.
        cell_specifier = "css=tr#%s>td.%s" % (row_id, column_class)
        return self.get_text(cell_specifier)

    def cell_integer(self, row, column):
        # Returns the value found in the specified cell, converted to an integer
        return int(self.cell_contents(row, column))

    def wait_for_order_number_display(self, concat_order_number):
        order_number_locator = "id=display_order_number"
        self.wait_in_python_for_selenium_condition(concat_order_number,
                                                   self.get_text,
                                                   order_number_locator,
                                                  )

    def assert_display_user_id(self, user_id):
        self.assert_eq(self.get_display_user_id(), user_id)

    def assert_options_pane_user_id(self, user_id):
        self.assert_eq(self.get_options_pane_user_id(), user_id)

    def assert_order_number_display(self, order_id_scan):
        if order_id_scan == "":
            display_order_number = ""
        else:
            display_order_number = self.build_order_number_for_display(order_id_scan)
        order_number_locator = "id=display_order_number"
        self.assert_eq(self.get_text(order_number_locator), display_order_number)

    def assert_order_number_blank(self):
        self.assert_order_number_display("")

    def wait_for_order_number_blank(self):
        self.wait_for_order_number_display("")

    def assert_order_status_green(self):
        self._assert_order_status(self.Status.green, "green")

    def assert_order_status_red(self):
        self._assert_order_status(self.Status.red, "red")

    def assert_order_status_gray(self):
        self._assert_order_status(self.Status.gray, "gray")

    def assert_order_status_blank(self):
        self._assert_order_status(self.Status.blank, "blank")

    def assert_order_status_yellow(self):
        self._assert_order_status(self.Status.yellow, "yellow")

    def _assert_order_status(self,
                             status_digit,
                             status_color,
                            ):
        # Check status digit
        status_digit_locator = "id=order_status"
        self.assert_eq(int(self.get_text(status_digit_locator)), status_digit)

        # Check status image - make sure we're showing the appropriate color
        self.assert_eq(self.get_order_status_image(), status_color)

    def assert_row_status_green(self, row):
        self._assert_row_status(row, self.Status.green, "green")

        # Check that item quantities match
        self.assert_eq(self.cell_integer(row, self.Columns.cur_qty), self.cell_integer(row, self.Columns.qty))

    def assert_row_status_red(self, row):
        self._assert_row_status(row, self.Status.red, "red")

        # Check that item quantities are appropriate for red status
        self.assert_gt(self.cell_integer(row, self.Columns.cur_qty), self.cell_integer(row, self.Columns.qty))

    def assert_row_status_gray(self, row):
        self._assert_row_status(row, self.Status.gray, "gray")

        # Check that item quantities are appropriate for gray status
        self.assert_lt(self.cell_integer(row, self.Columns.cur_qty), self.cell_integer(row, self.Columns.qty))

    def assert_row_status_blank(self, row):
        self._assert_row_status(row, self.Status.blank, "blank")

        # Check that item quantities are appropriate for blank status
        self.assert_eq(self.cell_integer(row, self.Columns.cur_qty), 0)
        self.assert_gt(self.cell_integer(row, self.Columns.qty), 0)

    def _assert_row_status(self,
                           row,
                           status_digit,
                           status_color,
                          ):
        # Check status column
        self.assert_eq(self.cell_integer(row, self.Columns.status), status_digit)

        # Check status image - make sure we're showing blank
        self.assert_eq(self.get_row_status_image(row), status_color)

    def assert_row_info_image_blank(self, row):
        # Check info image - make sure we're showing blank
        self.assert_eq(self.get_row_info_image(row), "inline_blank")

    def assert_row_info_image_metal(self, row):
        # Check info image - make sure we're showing metal
        self.assert_eq(self.get_row_info_image(row), "inline_m")

    def assert_row_info_image_ion(self, row):
        # Check info image - make sure we're showing ion
        self.assert_eq(self.get_row_info_image(row), "inline_i")

    def assert_row_info_image_metal_ion(self, row):
        # Check info image - make sure we're showing metal and ion
        self.assert_eq(self.get_row_info_image(row), "inline_mi")

    def assert_row_info_image_thorium(self, row):
        # Check info image - make sure we're showing thorium
        self.assert_eq(self.get_row_info_image(row), "inline_th")

    def assert_row_info_image_ormd(self, row):
        # Check info image - make sure we're showing ORM-D
        self.assert_eq(self.get_row_info_image(row), "inline_ormd")

    def assert_row_qty(self, row, expected_qty):
        # Check that item quantities match the expected quantity
        self.assert_eq(self.cell_integer(row, self.Columns.cur_qty), expected_qty)

    def assert_row_highlighted(self, row):
        # debug
        tools.assert_true(self.row_is_highlighted(row))           # pylint: disable=E1101

        # Make sure all of the other rows are not highlighted
        number_of_rows = self.count_item_rows()
        for i in range(number_of_rows):
            if i != row:
                self.assert_row_not_highlighted(i)

        # debug
        #tools.assert_true(self.row_is_highlighted(row))

    def assert_row_not_highlighted(self, row):
        tools.assert_false(self.row_is_highlighted(row))           # pylint: disable=E1101

    def row_is_highlighted(self, row):
        # Adjust row: The xpath "array access" style (tr[%s]) is 1-based
        #
        # Note: our rowids (from Oracle rowid) are also 1-based. Currently we are
        # relying on Oracle (or pickpack_data_mock) to always return packing lists
        # in the same order, and we use the xpath "array access" style (tr[%s]) to
        # get to the nth row. We are not relying on row ids (tr id) for access to
        # the rows. Perhaps we could in future do two kinds of access - an ordered
        # access (using xpath nth row) for testing arrow keys, and an indexed access
        # (using tr id) for testing scan access.

        xpath = "%s//tr[%s]" % (self.DATA_TABLE_LOCATOR, row + 1)
        #
        ## Debug only
        #if self.element_has_class(xpath, "highlight"):
        #    print
        #    print
        #    print "Row %s is highlighted" % row
        #    print
        #    print

        return self.element_has_class(xpath, "highlight")

    def get_row_status_image(self, row):
        # Adjust row and column: The xpath "array access" style (tr[%s]) is 1-based
        locator = "%s//tr[%s]/td[%s]/img" % (self.DATA_TABLE_LOCATOR, row + 1, self.Columns.status_img + 1)
        return self.get_status_image_name(locator)

    def get_row_info_image(self, row):
        # Adjust row and column: The xpath "array access" style (tr[%s]) is 1-based
        locator = "%s//tr[%s]/td[%s]/img" % (self.DATA_TABLE_LOCATOR, row + 1, self.Columns.info_img + 1)
        return self.get_info_image_name(locator)

    def get_order_status_image(self):
        locator = "id=order_status_img"
        return self.get_status_image_name(locator)

    def get_status_image_name(self, locator):
        # Returns the name of the image, shorn of path, extension, and trailing
        # digit ("green", not "green1").
        #
        # Shear off trailing digit
        return self.get_image_name(locator)[:-1]

    def get_info_image_name(self, locator):
        # Returns the name of the image, shorn of path and extension.
        return self.get_image_name(locator)

    def get_image_name(self, locator):
        # Returns the name of the image, shorn of path, extension, and trailing
        # digit ("green", not "green1").
        image_path = self.get_attribute(locator, "src")
        return os.path.splitext(os.path.basename(image_path))[0]

    def get_display_user_id(self):
        return self.get_text(self.DISPLAY_USER_ID_FIELD)

    def get_options_pane_user_id(self):
        return self.get_value(self.USER_ID_FIELD)

    def assert_row_count(self, expected_count):
        actual_count = self.count_item_rows()
        self.assert_eq(actual_count, expected_count)

    def count_item_rows(self):
        xpath = "//table[@id='%s']//tr" % self.DATA_TABLE_ID
        #row_locator = "xpath=" % xpath
        return int(self._selenium_server.get_xpath_count(xpath))

    def wait_for_packing_list_request(self, param_value):
        self.wait_for_get("order_id_scan", param_value)

    def wait_for_characterize_user_input(self, param_value):
        self.wait_for_get("input", param_value)

    def wait_for_get(self, keys, values):
        javascript = "window.pickpack.server.lastGET();"
        if not isinstance(keys, list):
            keys = [keys]
        if not isinstance(values, list):
            values = [values]
        query_string = urllib.urlencode(zip(keys, values))
        self.wait_for_eval(javascript, query_string)

    def wait_for_comment_posting(self, post_contents):
        javascript = "window.pickpack.server.lastPOST();"
        self.wait_for_eval(javascript, post_contents)

    def build_post_content(self,
                           order_id_scan,
                           special_keys_encoded = None,
                           serial_numbers_encoded = None,
                          ):
        """
        Builds and returns a url-encoded string that represents the POST data
        from one order.
        """
        (order_number,
         order_generation,
         ignore_text_order_generation,
        ) = self.parse_order_id_scan(order_id_scan)

        order_number_part = "order_number={}".format(order_number)
        order_generation_part = "order_generation={}".format(order_generation)

        if special_keys_encoded is None:
            special_keys_part = ""
        else:
            special_keys_part = "%20Special%20keys{}".format(special_keys_encoded)

        comment_part = "comment_text=Scanned%3A%20complete.{}".format(special_keys_part)

        if serial_numbers_encoded is None:
            serial_numbers_part = "serial_numbers=%7B%7D"
        else:
            serial_numbers_part = "serial_numbers={}".format(serial_numbers_encoded)

        user_id_part = "user_id={}".format(self.DEFAULT_USER)

        return '&'.join((order_number_part,
                         order_generation_part,
                         comment_part,
                         serial_numbers_part,
                         user_id_part,
                        )
                       )

    def assert_serial_number_json(self, serial_numbers_string):
        javascript = "window.pickpack.globals.serializedItemContainer.serializedItemsAsJSON();"
        self.assert_eval(javascript, serial_numbers_string)


class ShopfloorMonitorTestingUtility(BaseTestingUtility):
    """
    A class to hold all kinds of utility functions for testing Shopfloor Monitor
    with Selenium
    """

    PATH = '/static/html/shopfloor_monitor/order_status.html'
    ID_PREFIX = 'sfmo'

    def __init__(self):
        BaseTestingUtility.__init__(self)

    def set_our_cookie(self):
        """
        Set a cookie in the browser.
        """
        cookie_name = 'sfmnOptions'
        cookie_value = 'dataDisplay:wcc&showHeld:true'
        cookie_path = self.PATH
        self.set_cookie(cookie_name,
                        cookie_value,
                        cookie_path,
                       )


class PickpackTestingUtilityNoCookie(PickpackTestingUtility):
    """
    A class for testing Pick Pack with Selenium when cookies are unset.
    """

    def __init__(self):
        PickpackTestingUtility.__init__(self)

    def set_our_cookie(self):
        """
        Do not set a cookie in the browser.
        """
        pass

#class WebdriverTestingUtility(object):
#    """
#    A class to hold all kinds of utility functions for testing with Webdriver
#    """
#    FOCUS_FOR_INPUT = "dom=document"
#    DATA_TABLE_ID = "table_1"
#    DATA_TABLE_LOCATOR = "xpath=//table[@id='%s']" % DATA_TABLE_ID
#    TAB_KEY = "\\9"
#    F2 = "\\113"
#    F3 = "\\114"
#    LEFT_ARROW = "\\37"
#    UP_ARROW = "\\38"
#    RIGHT_ARROW = "\\39"
#    DOWN_ARROW = "\\40"
#
#    class Columns(object):
#        status = 0
#        status_img = 1
#        cur_qty = 2
#        qty = 3
#        item = 4
#        um = 5
#
#    class Status(object):
#        blank = 0
#        gray = 1
#        red = 2
#        yellow = 3
#        green = 4
#
#    def __init__(self):
#        #self.host = '1bk2zq1-190.joco.com'
#        #self.host = '1bk2zq1-190'
#        self.host = 'localhost'
#        self.port = 4444
#        self.browser = '*chrome'
#        #self.browser = '*firefox'
#        self.aut_url = "http://partsappdev.joco.com:8082/"
#        #self.aut_url = "http://partsapp01.joco.com:8083/"
#        self._webdriver_server = None
#
#    def set_up_webdriver_connection_to_webdriver_server(self):
#        def _build_url(host,
#                       url_path,
#                      ):
#            url_elements = ('http',
#                            host,
#                            urllib.quote(url_path),
#                            None,
#                            None,
#                           )
#            return urlparse.urlunsplit(url_elements)
#
#        url_of_remote_webdriver_server = _build_url('%s:%s' % (self.host, self.port),
#                                                   '/wd/hub',
#                                                  )
#        self._webdriver_server = webdriver.Remote(url_of_remote_webdriver_server,
#                                             DesiredCapabilities.FIREFOX,
#                                            )
#
#    #def set_up_webdriver_connection_to_local_htmlunit(self):
#    #    pass
#
#    def start_webdriver_server(self):
#        self.set_up_webdriver_connection_to_webdriver_server()
#
#    def stop_webdriver_server(self):
#        self._webdriver_server.stop()
#
#    def open_aut(self):
#        """
#        Open a browser, and load the Application Under Test (AUT)
#        """
#        self._webdriver_server.open("/")
#        #self._webdriver_server.open(self.aut_url)




# Selenium RC element locators
#
# From this old documentation
# http://release.seleniumhq.org/selenium-core/0.8.2/reference.html
#
#
#    Element Locators
#
#    Element Locators tell Selenium which HTML element a command refers to. The
#    format of a locator is:
#
#        locatorType=argument
#
#    We support the following strategies for locating elements:
#
#        identifier=id: Select the element with the specified @id attribute. If
#        no match is found, select the first element whose @name attribute is
#        id. (This is normally the default; see below.) id=id: Select the
#        element with the specified @id attribute. name=name: Select the first
#        element with the specified @name attribute.
#            username
#            name=username
#
#        The name may optionally be followed by one or more element-filters,
#        separated from the name by whitespace. If the filterType is not
#        specified, value is assumed.
#            name=flavour value=chocolate
#        dom=javascriptExpression: Find an element by evaluating the specified
#        string. This allows you to traverse the HTML Document Object Model
#        using JavaScript. Note that you must not return a value in this string;
#        simply make it the last expression in the block.
#            dom=document.forms['myForm'].myDropdown
#            dom=document.images[56]
#            dom=function foo() { return document.links[1]; }; foo();
#        xpath=xpathExpression: Locate an element using an XPath expression.
#            xpath=//img[@alt='The image alt text']
#            xpath=//table[@id='table1']//tr[4]/td[2]
#            xpath=//a[contains(@href,'#id1')]
#            xpath=//a[contains(@href,'#id1')]/@class
#            xpath=(//table[@class='stylee'])//th[text()='theHeaderText']/../td
#            xpath=//input[@name='name2' and @value='yes']
#            xpath=//*[text()="right"]
#        link=textPattern: Select the link (anchor) element which contains text
#        matching the specified pattern.
#            link=The link text
#        css=cssSelectorSyntax: Select the element using css selectors. Please
#        refer to CSS2 selectors, CSS3 selectors for more information. You can
#        also check the TestCssLocators test in the selenium test suite for an
#        example of usage, which is included in the downloaded selenium core
#        package.
#            css=a[href="#id3"]
#            css=span#firstChild + span
#
#        Currently the css selector locator supports all css1, css2 and css3
#        selectors except namespace in css3, some pseudo classes(:nth-of-type,
#        :nth-last-of-type, :first-of-type, :last-of-type, :only-of-type,
#        :visited, :hover, :active, :focus, :indeterminate) and pseudo
#        elements(::first-line, ::first-letter, ::selection, ::before, ::after).
#
#    Without an explicit locator prefix, Selenium uses the following default
#    strategies:
#
#        dom, for locators starting with "document."
#        xpath, for locators starting with "//"
#        identifier, otherwise
