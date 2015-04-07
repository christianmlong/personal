# pylint: disable=C0111, C0103
from Pickpack.test.selenium.common_selenium_tests import TestPickpackCommon


def main():
    t = TestPickpackCommon()

    t.setup_class()
    try:
        run_tests(t)
    finally:
        t.teardown_class()


def run_tests(t):
    #print "bla"

    test_names = [
        #"test_01_quicktest",
        #"test_02_walkthrough",
        #"test_03_walkthrough2",
        #"test_04_walkthrough3",
        #"test_05_walkthrough4",
        #"test_06_f2",
        "test_07_table_scan_item",
        "test_08_table_scan_upc",
        "test_09_two_lines_one_item",
        "test_10_serial_numbers",
        "test_11_mlsi_serial_numbers",
        "test_12_info_box",
        "test_13_handle_server_side_error",
        "test_14_harper_labels",
        "test_15_item_notes",
        "test_16_more_item_notes",
        "test_17_html_escape_notes",
    ]

    test_names.reverse()

    for name in test_names:
        run_test(t, name)

def run_test(t, test_name):

    print test_name,
    test_to_run = getattr(t, test_name)
    t.setup()
    test_to_run()
    print "    complete"

if __name__ == '__main__':
    main()
