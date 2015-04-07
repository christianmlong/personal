# pylint: disable=C0111



class BaseTableTester(object):
    """
    Base class for table testers.
    """
    def __init__(self,
                 table_data,
                 utility_object,
                ):
        # <tr id="%s" class="barcode_%s item_%s">
        # <td class="pkpk_status"       >%s</td>
        # <td class="pkpk_status_img"   ><img class="pkpk_status_img" src="/static/img/blank1.png" /></td>
        # <td class="pkpk_cur_qty"      >0</td>
        # <td class="pkpk_qty"          >%i</td>
        # <td class="pkpk_item"         >%s</td>
        # <td class="pkpk_um"           >%s</td>
        # <td class="pkpk_serialized"   >%s</td>
        # </tr>
        #
        #  0 oed.line_no,
        #  1 sms.bar_code || sms.check_digit barcode,
        #  2 oed.item_no,
        #  3 nvl2(sms.bar_code, 0, 3) status,
        #  4 oed.qty_shipped,
        #  5 oed.sales_um,
        #  6 nvl2(mis.item_no, 1, 0) serialized
        #
        # [[1, "648484149532", "058685", 0, 1.0, "2PK", 0], [2, "648484140133", "136748", 0, 1.0, "2PK", 0],
        #
        #
        #    // Build up the row using MochiKit.DOM.createDOM. This syntax is
        #    // based on Nevow's Stan.
        #    return d.TR({"id" : json_row[0], "class" : "barcode_" + json_row[1] + " item_" + json_row[2]}
        #               , d.TD({"class" : "pkpk_status"}, json_row[3])
        #               , d.TD({"class" : "pkpk_status_img"}
        #                     , d.IMG({"class" : "pkpk_status_img", "src" : buildImagePath(json_row[3], "1")})
        #                     )
        #               , d.TD({"class" : "pkpk_cur_qty"}, 0)
        #               , d.TD({"class" : "pkpk_qty"}, json_row[4])
        #               , d.TD({"class" : "pkpk_item"}, json_row[2])
        #               , d.TD({"class" : "pkpk_um"}, json_row[5])
        #               , d.TD({"class" : "pkpk_serialized"}, json_row[6])
        #               );

        self.utility_object = utility_object
        self.table_data = table_data
        self.assert_correct_table_values()

    def assert_correct_table_values(self):
        # Make sure the HTML <table> has all the right values
        for row in self.table_data:
            self.assert_correct_row_values(row)

    def assert_correct_row_values(self, row):
        # Make sure the HTML <tr> row has all the right values

        # First check the easy things. We start by checking that all the html
        # cell values in the html table row match the corresponding data values
        # in the data row.

        # This tuple maps all the column numbers of the data set to the
        # equivalent column in the html table. The data columns are numbered
        # starting with column zero. The html columns are referenced by their
        # htm class attribute.
        #                                     data  html_column_class
        data_columns_and_html_table_columns = ((2,  "pkpk_item", False),              # item number
                                               (3,  "pkpk_status", True),             # numeric status (convert_to_str = True)
                                               (4,  "pkpk_qty", True),                # quantity ordered (convert_to_str = True)
                                               (5,  "pkpk_um", False),                # unit of measure
                                               (6,  "pkpk_serialized", True),         # serialized (convert_to_str = True)
                                              )
        for column in data_columns_and_html_table_columns:
            self.assert_correct_cell_value(row,
                                           *column
                                          )

        if len(row) == 7:
            # No extra info for this row.
            row_should_be_highlighted = False
        elif len(row) == 8:
            # Get data from the 'extras' dict at the end of the row. If the
            # 'extras' dict does not have highlight info, then no highlight was
            # specified.
            row_should_be_highlighted = row[7].get('highlight', False)
        else:
            err_msg = "Invalid row length"
            raise AssertionError(err_msg)

        if row_should_be_highlighted:
            expected_class_template = "barcode_%s item_%s highlight"
        else:
            expected_class_template = "barcode_%s item_%s"

        # Now make sure the other elements of the row are correct.
        expected_class = expected_class_template % (row[1], row[2])
        # row[0] is the oe_detail.line_no, which is also used as the <tr> id. Id
        # is the default locator in Selenium, so we can just pass row[0] here.
        actual_class = self.utility_object.get_attribute(row[0], "class")
        self.utility_object.assert_eq(expected_class, actual_class)

    def assert_correct_cell_value(self,
                                  row,
                                  data_column_number,
                                  html_column_class,
                                  convert_to_str,
                                 ):
        # Make sure the HTML <td> cell has the right value
        row_number = row[0]
        expected_value = row[data_column_number]
        if convert_to_str:
            expected_value = str(int(expected_value))

        ## Handle Harper item labels
        #if data_column_number == 2:
        #    if expected_value.startswith('1 '):
        #        expected_value = expected_value[2:]

        actual_value = self.utility_object.cell_contents_by_row_id_and_column_class(row_number, html_column_class)
        #print "Expected %s Type %s" % (expected_value, type(expected_value))
        #print "Actual %s Type %s" % (actual_value, type(actual_value))
        #print expected_value == actual_value
        self.utility_object.assert_eq(expected_value, actual_value)
        #print "Assert OK!"


class TableTester(BaseTableTester):
    """
    This class takes a list representing a table of items. It can run a bunch of
    scans based on that data, and assert that the normal case is working. For
    data, it uses the same format as the sample data in pickpack_data_mock.py
    """
    def __init__(self,
                 table_data,
                 utility_object,
                ):
        BaseTableTester.__init__(self,
                                 table_data,
                                 utility_object,
                                )
        self.all_items_to_scan = []
        for i in range(len(table_data)):
            self.all_items_to_scan.extend([i]*int(table_data[i][4]))
        self.qty_scanned_so_far = 0

    def back_up(self, how_far):
        self.qty_scanned_so_far -= how_far

    def how_much_farther(self):
        return len(self.all_items_to_scan) - self.qty_scanned_so_far

    def multi_scan_item(self, num_beeps):
        self.multi_scan(num_beeps, "item")

    def multi_scan_upc(self, num_beeps):
        self.multi_scan(num_beeps, "upc")

    def multi_scan(self, num_beeps, item_or_upc):
        for ignore_i in range(num_beeps):
            self.assert_correct_order_status()
            self.scan_row(self.all_items_to_scan[self.qty_scanned_so_far], item_or_upc)
            self.qty_scanned_so_far += 1
            self.assert_correct_order_status()

    def finish_order_item(self):
        self.finish_order("item")

    def finish_order_upc(self):
        self.finish_order("upc")

    def finish_order(self, item_or_upc):
        # Do all the rest of the items on the order
        self.multi_scan(self.how_much_farther(), item_or_upc)

    def scan_row(self, row_number, item_or_upc):
        row = self.table_data[row_number]
        if item_or_upc == "item":
            if len(row) == 7:
                scan_data = row[2]
            elif len(row) == 8:
                # Simulate Harper label scan. Get data from the
                # 'extras' dict at the end of the row. If the 'extras'
                # dict does not have harper label info, just use
                # the regular scan info.
                scan_data = row[7].get('harper_label', row[2])
            else:
                err_msg = "Invalid row length"
                raise AssertionError(err_msg)
        elif item_or_upc == "upc":
            scan_data = row[1]
        self.utility_object.scan(scan_data)

    def assert_correct_order_status(self):
        if self.qty_scanned_so_far == 0:
            self.utility_object.assert_order_status_blank()
        elif self.qty_scanned_so_far < len(self.all_items_to_scan):
            self.utility_object.assert_order_status_gray()
        elif self.qty_scanned_so_far == len(self.all_items_to_scan):
            self.utility_object.assert_order_status_green()
        else:
            self.utility_object.assert_order_status_red()


class QuickTableTester(BaseTableTester):
    """
    This class takes a list representing a table of items. It runs through the
    order quickly, using the plus key. For data, it uses the same format as the
    sample data in pickpack_data_mock.py
    """
    def __init__(self,
                 table_data,
                 utility_object,
                ):
        BaseTableTester.__init__(self,
                                 table_data,
                                 utility_object,
                                )

    def scan_almost_to_end(self):
        """
        Finish order, almost to the last item. Leave one item, so the main test
        can finish the order with that last item.
        """
        for ignore_row in self.table_data[:-1]:
            self.utility_object.special_key(self.utility_object.DOWN_ARROW)
            self.utility_object.key_press("+")

        qty_last_row = self.table_data[-1][4]

        self.utility_object.special_key(self.utility_object.DOWN_ARROW)
        for ignore in range(int(qty_last_row - 1)):
            self.utility_object.special_key(self.utility_object.RIGHT_ARROW)
