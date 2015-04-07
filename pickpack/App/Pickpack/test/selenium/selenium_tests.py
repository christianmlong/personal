# pylint: disable=C0111,W0142,R0915

from Pickpack.test.selenium.common_selenium_tests import BaseForPickpackTests
from Pickpack.test.selenium.table_tester import TableTester, QuickTableTester

class TestBatteryRules(BaseForPickpackTests):
    """
    This class holds some Selenium tests for the battery warnings for the Pick
    Pack project. This tests the battery warning rules.
    """
    def __init__(self):
        BaseForPickpackTests.__init__(self)

    def test_18_battery_warning_popups(self):
        """
        Battery warnings. Big order, multiple warnings.
        """
        order_id_scan = "AA02200"

        # Useful regex, to linebreak the text we get from a testing error
        # Find:
        #><((?:/?)(?:tr|td|span)|/tbody)
        #
        # Replace:
        #>'\n            u'<\1

        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion1_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion2_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack TRPR batteries with other items, max 20 per box<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_info_image_blank(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_row_info_image_blank(4)
        self.u.assert_row_status_blank(5)
        self.u.assert_row_info_image_blank(5)
        self.u.assert_row_status_blank(6)
        self.u.assert_row_info_image_blank(6)
        self.u.assert_row_status_blank(7)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_info_image_blank(11)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(12)

        self.u.scan("058685")
        self.u.scan("136748")
        self.u.scan("164421")
        self.u.scan("164422")
        self.u.scan("164485")
        self.u.scan("187441")
        self.u.scan("187442")
        self.u.scan("187443")
        self.u.scan("213858")
        self.u.scan("216322")
        self.u.scan("216322")
        self.u.scan("216322")
        self.u.scan("216322")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan("222003")
        self.u.scan__allow_info("604612")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(11)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_info_image_blank(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_info_image_blank(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_info_image_blank(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_info_image_blank(6)
        self.u.assert_row_status_green(7)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_status_green(8)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_status_green(9)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_status_green(10)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_status_green(11)
        self.u.assert_row_info_image_blank(11)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_19_battery_warning_popups(self):
        """
        Battery warnings. Mixed ion and metal.
        """
        order_id_scan = "AA02500"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion1_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_ion(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)

        self.u.scan("058685")
        self.u.scan__allow_info("648484140133")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_ion(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_20_battery_warning_popups(self):
        """
        Battery warnings. Mixed ion and metal.
        """
        order_id_scan = "AA02500"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion1_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_ion(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)

        self.u.scan("648484149532")
        self.u.scan__allow_info("136748")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_ion(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_21_battery_warning_popups(self):
        """
        Battery warnings. TRPR batteries.
        """
        order_id_scan = "AA02600"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion2_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack TRPR batteries with other items, max 20 per box<br>'
            u'</span>'
            u'</td>'
            u'</tr></tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_ion(0)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan__allow_info("058685")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_ion(0)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_22_battery_warning_popups(self):
        """
        Battery warnings. SmartBands/SmartBelts.
        """
        order_id_scan = "AA02700"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion1_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>SmartBands/SmartBelts get Ion label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_ion(0)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(1)

        self.u.scan__allow_info("648484149532")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(0)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_ion(0)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_23_battery_warning_popups(self):
        """
        Battery warnings.
        """
        order_id_scan = "AA03000"

        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion2_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack SmartBand batteries with other items, max 75 per box<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_ion(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_info_image_blank(2)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(3)

        self.u.scan("648484320016")
        self.u.scan("648484320016")
        self.u.scan("648484320016")
        self.u.scan("648484320016")
        self.u.scan("648484320016")
        self.u.scan("648484320016")
        self.u.scan("648484423588")
        self.u.scan("648484423588")
        self.u.scan__allow_info("648484583114")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_ion(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)


# Break it up in to more classes, to avoid this error: "An operation on a socket
# could not be performed because the system lacked sufficient buffer space or
# because a queue was full"
class TestBatteryRules2(BaseForPickpackTests):
    """
    This class holds more Selenium tests for the battery warnings for the
    Pick Pack project. This tests the battery warning rules.
    """
    def __init__(self):
        BaseForPickpackTests.__init__(self)

    def setup(self):
        """
        This will run once for each test method in this class
        """
        # Pause 5 seconds before each test method in this class. This prevents
        # this error "An operation on a socket could not be performed because
        # the system lacked sufficient buffer space or because a queue was
        # full".
        self.u.pause(5)

        # Call base class's implementation
        BaseForPickpackTests.setup(self)

    def test_30_battery_warning_popups(self):
        """
        Battery warnings. Worst-case scenario.
        """
        order_id_scan = "AA02800"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/metal2_small.png">'
            u'</span>'
            u'<span><img src="/static/img/battery_doc4_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack coin batteries in a separate box<br>'
            u'</span>'
            u'<span>Mark "Metal, Batteries Only" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion1_small.png">'
            u'</span>'
            u'<span><img src="/static/img/battery_doc2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each Helmet + SmartBand/SmartBelt kit with Ion label<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion1_small.png">'
            u'</span>'
            u'<span><img src="/static/img/battery_doc2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/ion2_small.png">'
            u'</span>'
            u'<span><img src="/static/img/battery_doc7_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Max 2 SmartBands/SmartBelts per box<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box<br>'
            u'</span>'
            u'<span>------------------<br>'
            u'</span>'
            u'<span>Package Ion batteries in a separate box, max 2 per box<br>'
            u'</span>'
            u'<span>Mark "Ion, Batteries Only" on the document for the battery box<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_status_blank(5)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_status_blank(6)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_status_blank(7)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_info_image_blank(12)


        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(13)

        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("058685")
        self.u.scan("136748")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164421")
        self.u.scan("164422")
        self.u.scan("164422")
        self.u.scan("164422")
        self.u.scan("164422")
        self.u.scan("164422")
        self.u.scan("164422")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("164485")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187441")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187442")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("187443")
        self.u.scan("213858")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("245237")
        self.u.scan("222003")
        self.u.scan("604612")
        self.u.scan__allow_info("239725")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(12)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_status_green(3)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_status_green(4)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_status_green(5)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_status_green(6)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_status_green(7)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_status_green(8)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_status_green(9)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_status_green(10)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_status_green(11)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_status_green(12)
        self.u.assert_row_info_image_blank(12)

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_31_worst_case_ground(self):
        """
        Battery and thorium and ORM-D warnings. Going by Ground. Worst-case
        scenario.
        """
        order_id_scan = "AA13900"
        html = (
            u'<div>'
            u'<table id="table_of_order_notes">'
            u'<tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/metal2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack coin batteries with other items<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion1_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each Helmet + SmartBand/SmartBelt kit with Ion label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion1_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack TRPR batteries with other items, max 20 per box<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/un_2909_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/boxes_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Ship in multiple packages<br>'
            u'</span>'
            u'<span>Max 20 packs of rods per package<br>'
            u'</span>'
            u'<span>Wrap thoriated rods in a small box inside each shipping carton<br>'
            u'</span>'
            u'<span>Label shipping cartons with UN 2909 label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ormd_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/box_rating_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label ORM-D. Make sure the box rating is visible<br>'
            u'</span>'
            u'<span>Must ship by Ground<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody>'
            u'</table>'
            u'</div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(45)

        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_row_status_blank(5)
        self.u.assert_row_status_blank(6)
        self.u.assert_row_status_blank(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_row_status_blank(17)
        self.u.assert_row_status_blank(18)
        self.u.assert_row_status_blank(19)
        self.u.assert_row_status_blank(20)
        self.u.assert_row_status_blank(21)
        self.u.assert_row_status_blank(22)
        self.u.assert_row_status_blank(23)
        self.u.assert_row_status_blank(24)
        self.u.assert_row_status_blank(25)
        self.u.assert_row_status_blank(26)
        self.u.assert_row_status_blank(27)
        self.u.assert_row_status_blank(28)
        self.u.assert_row_status_blank(29)
        self.u.assert_row_status_blank(30)
        self.u.assert_row_status_blank(31)
        self.u.assert_row_status_blank(32)
        self.u.assert_row_status_blank(33)
        self.u.assert_row_status_blank(34)
        self.u.assert_row_status_blank(35)
        self.u.assert_row_status_blank(36)
        self.u.assert_row_status_blank(37)
        self.u.assert_row_status_blank(38)
        self.u.assert_row_status_blank(39)
        self.u.assert_row_status_blank(40)
        self.u.assert_row_status_blank(41)
        self.u.assert_row_status_blank(42)
        self.u.assert_row_status_blank(43)
        self.u.assert_row_status_blank(44)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_info_image_thorium(12)
        self.u.assert_row_info_image_thorium(13)
        self.u.assert_row_info_image_thorium(14)
        self.u.assert_row_info_image_thorium(15)
        self.u.assert_row_info_image_thorium(16)
        self.u.assert_row_info_image_thorium(17)
        self.u.assert_row_info_image_thorium(18)
        self.u.assert_row_info_image_thorium(19)
        self.u.assert_row_info_image_thorium(20)
        self.u.assert_row_info_image_thorium(21)
        self.u.assert_row_info_image_thorium(22)
        self.u.assert_row_info_image_thorium(23)
        self.u.assert_row_info_image_thorium(24)
        self.u.assert_row_info_image_thorium(25)
        self.u.assert_row_info_image_thorium(26)
        self.u.assert_row_info_image_thorium(27)
        self.u.assert_row_info_image_thorium(28)
        self.u.assert_row_info_image_thorium(29)
        self.u.assert_row_info_image_thorium(30)
        self.u.assert_row_info_image_thorium(31)
        self.u.assert_row_info_image_thorium(32)
        self.u.assert_row_info_image_thorium(33)
        self.u.assert_row_info_image_thorium(34)
        self.u.assert_row_info_image_thorium(35)
        self.u.assert_row_info_image_thorium(36)
        self.u.assert_row_info_image_thorium(37)
        self.u.assert_row_info_image_thorium(38)
        self.u.assert_row_info_image_thorium(39)
        self.u.assert_row_info_image_thorium(40)
        self.u.assert_row_info_image_thorium(41)
        self.u.assert_row_info_image_thorium(42)
        self.u.assert_row_info_image_ormd(43)
        self.u.assert_row_info_image_ormd(44)

        table_data = [(1, '648484149532', '058685', 0, 21.0, '2PK', 0,       ),         #    MetalCoinBattery
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 0,        ),
                      (3, '648484023498', '164421', 0, 10.0, '2PK', 0,       ),
                      (4, '648484111669', '164422', 0, 6.0, 'EA', 0,         ),         #    CompleteTRPR
                      (5, '648484028745', '164485', 0, 11.0, '10PK', 0,      ),         #    TRPRWithoutLens
                      (6, '648484220033', '187441', 0, 11.0, 'EA', 0,        ),         #    SmartBand
                      (7, '648484209892', '187442', 0, 11.0, 'EA', 0,        ),         #    SmartBelt
                      (8, '648484209908', '187443', 0, 11.0, 'EA', 0,        ),         #    TRPRBattery
                      (12, '648484330244', '213858', 0, 1.0, 'EA', 0,        ),         #    SmartBandBattery
                      (9, '648484316972', '245237', 0, 40.0, 'EA', 0,        ),         #    SmartBeltBattery
                      (10, '648484338141', '222003', 0, 1.0, 'EA', 0,        ),         #    MetalAndIonPackageKit
                      (11, '648484030595', '604612', 0, 1.0, '4PK', 0,       ),         #    another SmartBelt
                      (13, '',             '6LGT5', 0, 10.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (14, '',             '6LGT6', 0, 11.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (15, '',             '6LGT7', 0, 12.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (16, '',             '6LGT8', 0, 13.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (17, '',             '6LGT9', 0, 14.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (18, '',             '6UHJ2', 0, 15.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (19, '',             '6UHJ4', 0, 16.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (20, '',             '6UHJ6', 0, 17.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (21, '',             '6UHJ8', 0, 18.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (22, '',             '6UHK1', 0, 19.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (23, '',             '6UHK3', 0, 20.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (24, '',             '6UHK4', 0, 21.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (25, '',             '6UHK6', 0, 22.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (26, '720949054084', 'AK-1', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (27, '720949054138', 'AK-125', 0, 2.0, 'EA', 0,        ),         #    TIG kit
                      (28, '720949054169', 'AK-18', 0, 22.0, 'EA', 0,        ),         #    TIG kit
                      (29, '720949054206', 'AK-1A', 0, 32.0, 'EA', 0,        ),         #    TIG kit
                      (30, '720949054244', 'AK-2', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (31, '720949054312', 'AK-27', 0, 12.0, 'EA', 0,        ),         #    TIG kit
                      (32, '720949054343', 'AK-3', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (33, '720949054442', 'AK-4', 0, 6.0, 'EA', 0,          ),         #    TIG kit
                      (34, '720949054473', 'AK-4A', 0, 2.0, 'EA', 0,         ),         #    TIG kit
                      (35, '720949054497', 'AK-5', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (36, '720949054534', 'AK-5W', 0, 2.0, 'EA', 0,         ),         #    TIG kit
                      (37, '720949054626', 'AK-8', 0, 7.0, 'EA', 0,          ),         #    TIG kit
                      (38, '720949230716', 'WT018X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (39, '720949230686', 'WT040X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (40, '720949230693', 'WT116X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (41, '720949230709', 'WT332X7', 0, 3.0, '10PK', 0,     ),         #    Thoriated rods
                      (42, '720949230723', 'WT532X7', 0, 10.0, '10PK', 0,    ),         #    Thoriated rods
                      (43, '648484364348', 'WTP20RM', 0, 2.0, 'EA', 0,       ),         #    Discontinued thorium product
                      (44, '379222001730', '84006', 0, 20.0, 'EA', 0,        ),         #    ORM-D
                      (45, '648484060479', '098205', 0, 6.0, 'EA', 0,        ),         #    ORM-D
                     ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )

        t.multi_scan(40, "upc")
        t.multi_scan(t.how_much_farther() - 1, "item")
        self.u.scan__allow_info("098205")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(44)

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
        self.u.assert_row_status_green(17)
        self.u.assert_row_status_green(18)
        self.u.assert_row_status_green(19)
        self.u.assert_row_status_green(20)
        self.u.assert_row_status_green(21)
        self.u.assert_row_status_green(22)
        self.u.assert_row_status_green(23)
        self.u.assert_row_status_green(24)
        self.u.assert_row_status_green(25)
        self.u.assert_row_status_green(26)
        self.u.assert_row_status_green(27)
        self.u.assert_row_status_green(28)
        self.u.assert_row_status_green(29)
        self.u.assert_row_status_green(30)
        self.u.assert_row_status_green(31)
        self.u.assert_row_status_green(32)
        self.u.assert_row_status_green(33)
        self.u.assert_row_status_green(34)
        self.u.assert_row_status_green(35)
        self.u.assert_row_status_green(36)
        self.u.assert_row_status_green(37)
        self.u.assert_row_status_green(38)
        self.u.assert_row_status_green(39)
        self.u.assert_row_status_green(40)
        self.u.assert_row_status_green(41)
        self.u.assert_row_status_green(42)
        self.u.assert_row_status_green(43)
        self.u.assert_row_status_green(44)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_info_image_thorium(12)
        self.u.assert_row_info_image_thorium(13)
        self.u.assert_row_info_image_thorium(14)
        self.u.assert_row_info_image_thorium(15)
        self.u.assert_row_info_image_thorium(16)
        self.u.assert_row_info_image_thorium(17)
        self.u.assert_row_info_image_thorium(18)
        self.u.assert_row_info_image_thorium(19)
        self.u.assert_row_info_image_thorium(20)
        self.u.assert_row_info_image_thorium(21)
        self.u.assert_row_info_image_thorium(22)
        self.u.assert_row_info_image_thorium(23)
        self.u.assert_row_info_image_thorium(24)
        self.u.assert_row_info_image_thorium(25)
        self.u.assert_row_info_image_thorium(26)
        self.u.assert_row_info_image_thorium(27)
        self.u.assert_row_info_image_thorium(28)
        self.u.assert_row_info_image_thorium(29)
        self.u.assert_row_info_image_thorium(30)
        self.u.assert_row_info_image_thorium(31)
        self.u.assert_row_info_image_thorium(32)
        self.u.assert_row_info_image_thorium(33)
        self.u.assert_row_info_image_thorium(34)
        self.u.assert_row_info_image_thorium(35)
        self.u.assert_row_info_image_thorium(36)
        self.u.assert_row_info_image_thorium(37)
        self.u.assert_row_info_image_thorium(38)
        self.u.assert_row_info_image_thorium(39)
        self.u.assert_row_info_image_thorium(40)
        self.u.assert_row_info_image_thorium(41)
        self.u.assert_row_info_image_thorium(42)
        self.u.assert_row_info_image_ormd(43)
        self.u.assert_row_info_image_ormd(44)

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_32_worst_case_air(self):
        """
        Battery and thorium and ORM-D warnings. Going by Air. Worst-case
        scenario.
        """
        order_id_scan = "AA14000"
        html = (
            u'<div>'
            u'<table id="table_of_order_notes">'
            u'<tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/metal2_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc4_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack coin batteries in a separate box<br>'
            u'</span>'
            u'<span>Mark "Metal, Batteries Only" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion1_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each Helmet + SmartBand/SmartBelt kit with Ion label<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion1_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion2_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc7_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Max 2 SmartBands/SmartBelts per box<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box<br>'
            u'</span>'
            u'<span>------------------<br>'
            u'</span>'
            u'<span>Package Ion batteries in a separate box, max 2 per box<br>'
            u'</span>'
            u'<span>Mark "Ion, Batteries Only" on the document for the battery box<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/un_2909_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/boxes_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Ship in multiple packages<br>'
            u'</span>'
            u'<span>Max 20 packs of rods per package<br>'
            u'</span>'
            u'<span>Wrap thoriated rods in a small box inside each shipping carton<br>'
            u'</span>'
            u'<span>Label shipping cartons with UN 2909 label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/red_x_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.<br>'
            u'</span>'
            u'<span>Label ORM-D. Make sure the box rating is visible<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody>'
            u'</table>'
            u'</div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(45)

        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_row_status_blank(5)
        self.u.assert_row_status_blank(6)
        self.u.assert_row_status_blank(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_row_status_blank(17)
        self.u.assert_row_status_blank(18)
        self.u.assert_row_status_blank(19)
        self.u.assert_row_status_blank(20)
        self.u.assert_row_status_blank(21)
        self.u.assert_row_status_blank(22)
        self.u.assert_row_status_blank(23)
        self.u.assert_row_status_blank(24)
        self.u.assert_row_status_blank(25)
        self.u.assert_row_status_blank(26)
        self.u.assert_row_status_blank(27)
        self.u.assert_row_status_blank(28)
        self.u.assert_row_status_blank(29)
        self.u.assert_row_status_blank(30)
        self.u.assert_row_status_blank(31)
        self.u.assert_row_status_blank(32)
        self.u.assert_row_status_blank(33)
        self.u.assert_row_status_blank(34)
        self.u.assert_row_status_blank(35)
        self.u.assert_row_status_blank(36)
        self.u.assert_row_status_blank(37)
        self.u.assert_row_status_blank(38)
        self.u.assert_row_status_blank(39)
        self.u.assert_row_status_blank(40)
        self.u.assert_row_status_blank(41)
        self.u.assert_row_status_blank(42)
        self.u.assert_row_status_blank(43)
        self.u.assert_row_status_blank(44)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_info_image_thorium(12)
        self.u.assert_row_info_image_thorium(13)
        self.u.assert_row_info_image_thorium(14)
        self.u.assert_row_info_image_thorium(15)
        self.u.assert_row_info_image_thorium(16)
        self.u.assert_row_info_image_thorium(17)
        self.u.assert_row_info_image_thorium(18)
        self.u.assert_row_info_image_thorium(19)
        self.u.assert_row_info_image_thorium(20)
        self.u.assert_row_info_image_thorium(21)
        self.u.assert_row_info_image_thorium(22)
        self.u.assert_row_info_image_thorium(23)
        self.u.assert_row_info_image_thorium(24)
        self.u.assert_row_info_image_thorium(25)
        self.u.assert_row_info_image_thorium(26)
        self.u.assert_row_info_image_thorium(27)
        self.u.assert_row_info_image_thorium(28)
        self.u.assert_row_info_image_thorium(29)
        self.u.assert_row_info_image_thorium(30)
        self.u.assert_row_info_image_thorium(31)
        self.u.assert_row_info_image_thorium(32)
        self.u.assert_row_info_image_thorium(33)
        self.u.assert_row_info_image_thorium(34)
        self.u.assert_row_info_image_thorium(35)
        self.u.assert_row_info_image_thorium(36)
        self.u.assert_row_info_image_thorium(37)
        self.u.assert_row_info_image_thorium(38)
        self.u.assert_row_info_image_thorium(39)
        self.u.assert_row_info_image_thorium(40)
        self.u.assert_row_info_image_thorium(41)
        self.u.assert_row_info_image_thorium(42)
        self.u.assert_row_info_image_ormd(43)
        self.u.assert_row_info_image_ormd(44)

        table_data = [(1, '648484149532', '058685', 0, 21.0, '2PK', 0,       ),         #    MetalCoinBattery
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 0,        ),
                      (3, '648484023498', '164421', 0, 10.0, '2PK', 0,       ),
                      (4, '648484111669', '164422', 0, 6.0, 'EA', 0,         ),         #    CompleteTRPR
                      (5, '648484028745', '164485', 0, 11.0, '10PK', 0,      ),         #    TRPRWithoutLens
                      (6, '648484220033', '187441', 0, 11.0, 'EA', 0,        ),         #    SmartBand
                      (7, '648484209892', '187442', 0, 11.0, 'EA', 0,        ),         #    SmartBelt
                      (8, '648484209908', '187443', 0, 11.0, 'EA', 0,        ),         #    TRPRBattery
                      (12, '648484330244', '213858', 0, 1.0, 'EA', 0,        ),         #    SmartBandBattery
                      (9, '648484316972', '245237', 0, 40.0, 'EA', 0,        ),         #    SmartBeltBattery
                      (10, '648484338141', '222003', 0, 1.0, 'EA', 0,        ),         #    MetalAndIonPackageKit
                      (11, '648484030595', '604612', 0, 1.0, '4PK', 0,       ),         #    another SmartBelt
                      (13, '',             '6LGT5', 0, 10.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (14, '',             '6LGT6', 0, 11.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (15, '',             '6LGT7', 0, 12.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (16, '',             '6LGT8', 0, 13.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (17, '',             '6LGT9', 0, 14.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (18, '',             '6UHJ2', 0, 15.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (19, '',             '6UHJ4', 0, 16.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (20, '',             '6UHJ6', 0, 17.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (21, '',             '6UHJ8', 0, 18.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (22, '',             '6UHK1', 0, 19.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (23, '',             '6UHK3', 0, 20.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (24, '',             '6UHK4', 0, 21.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (25, '',             '6UHK6', 0, 22.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (26, '720949054084', 'AK-1', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (27, '720949054138', 'AK-125', 0, 2.0, 'EA', 0,        ),         #    TIG kit
                      (28, '720949054169', 'AK-18', 0, 22.0, 'EA', 0,        ),         #    TIG kit
                      (29, '720949054206', 'AK-1A', 0, 32.0, 'EA', 0,        ),         #    TIG kit
                      (30, '720949054244', 'AK-2', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (31, '720949054312', 'AK-27', 0, 12.0, 'EA', 0,        ),         #    TIG kit
                      (32, '720949054343', 'AK-3', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (33, '720949054442', 'AK-4', 0, 6.0, 'EA', 0,          ),         #    TIG kit
                      (34, '720949054473', 'AK-4A', 0, 2.0, 'EA', 0,         ),         #    TIG kit
                      (35, '720949054497', 'AK-5', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (36, '720949054534', 'AK-5W', 0, 2.0, 'EA', 0,         ),         #    TIG kit
                      (37, '720949054626', 'AK-8', 0, 7.0, 'EA', 0,          ),         #    TIG kit
                      (38, '720949230716', 'WT018X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (39, '720949230686', 'WT040X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (40, '720949230693', 'WT116X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (41, '720949230709', 'WT332X7', 0, 3.0, '10PK', 0,     ),         #    Thoriated rods
                      (42, '720949230723', 'WT532X7', 0, 10.0, '10PK', 0,    ),         #    Thoriated rods
                      (43, '648484364348', 'WTP20RM', 0, 2.0, 'EA', 0,       ),         #    Discontinued thorium product
                      (44, '379222001730', '84006', 0, 20.0, 'EA', 0,        ),         #    ORM-D
                      (45, '648484060479', '098205', 0, 6.0, 'EA', 0,        ),         #    ORM-D
                     ]

        t = TableTester(table_data,           # pylint: disable=C0103
                        self.u,
                       )

        t.multi_scan(40, "upc")
        t.multi_scan(t.how_much_farther() - 1, "item")
        self.u.scan__allow_info("098205")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(44)

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
        self.u.assert_row_status_green(17)
        self.u.assert_row_status_green(18)
        self.u.assert_row_status_green(19)
        self.u.assert_row_status_green(20)
        self.u.assert_row_status_green(21)
        self.u.assert_row_status_green(22)
        self.u.assert_row_status_green(23)
        self.u.assert_row_status_green(24)
        self.u.assert_row_status_green(25)
        self.u.assert_row_status_green(26)
        self.u.assert_row_status_green(27)
        self.u.assert_row_status_green(28)
        self.u.assert_row_status_green(29)
        self.u.assert_row_status_green(30)
        self.u.assert_row_status_green(31)
        self.u.assert_row_status_green(32)
        self.u.assert_row_status_green(33)
        self.u.assert_row_status_green(34)
        self.u.assert_row_status_green(35)
        self.u.assert_row_status_green(36)
        self.u.assert_row_status_green(37)
        self.u.assert_row_status_green(38)
        self.u.assert_row_status_green(39)
        self.u.assert_row_status_green(40)
        self.u.assert_row_status_green(41)
        self.u.assert_row_status_green(42)
        self.u.assert_row_status_green(43)
        self.u.assert_row_status_green(44)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_info_image_thorium(12)
        self.u.assert_row_info_image_thorium(13)
        self.u.assert_row_info_image_thorium(14)
        self.u.assert_row_info_image_thorium(15)
        self.u.assert_row_info_image_thorium(16)
        self.u.assert_row_info_image_thorium(17)
        self.u.assert_row_info_image_thorium(18)
        self.u.assert_row_info_image_thorium(19)
        self.u.assert_row_info_image_thorium(20)
        self.u.assert_row_info_image_thorium(21)
        self.u.assert_row_info_image_thorium(22)
        self.u.assert_row_info_image_thorium(23)
        self.u.assert_row_info_image_thorium(24)
        self.u.assert_row_info_image_thorium(25)
        self.u.assert_row_info_image_thorium(26)
        self.u.assert_row_info_image_thorium(27)
        self.u.assert_row_info_image_thorium(28)
        self.u.assert_row_info_image_thorium(29)
        self.u.assert_row_info_image_thorium(30)
        self.u.assert_row_info_image_thorium(31)
        self.u.assert_row_info_image_thorium(32)
        self.u.assert_row_info_image_thorium(33)
        self.u.assert_row_info_image_thorium(34)
        self.u.assert_row_info_image_thorium(35)
        self.u.assert_row_info_image_thorium(36)
        self.u.assert_row_info_image_thorium(37)
        self.u.assert_row_info_image_thorium(38)
        self.u.assert_row_info_image_thorium(39)
        self.u.assert_row_info_image_thorium(40)
        self.u.assert_row_info_image_thorium(41)
        self.u.assert_row_info_image_thorium(42)
        self.u.assert_row_info_image_ormd(43)
        self.u.assert_row_info_image_ormd(44)

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    #
    #def testAA14100(self):
    #    self.try_it_order_number(
    #        order_id_scan = 'AA14100',
    #        expected_warnings = [
    #            [('STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.',
    #              'Label ORM-D. Make sure the box rating is visible',
    #             ),
    #             'red_x',
    #            ],
    #        ],
    #        expected_data_to_add = [5, 5],
    #    )


    def test_33_orm_d_air(self):
        """
        Test the ORM-D warning that alerts the user that ORM-D can not go by
        Air.
        """
        order_id_scan = "AA14100"
        html = (
            u'<div>'
            u'<table id="table_of_order_notes">'
            u'<tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/red_x_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.<br>'
            u'</span>'
            u'<span>Label ORM-D. Make sure the box rating is visible<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody>'
            u'</table>'
            u'</div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)

        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_ormd(0)
        self.u.assert_row_info_image_ormd(1)

        self.u.scan("379222001730")
        self.u.scan("84006")
        self.u.scan("84006")
        self.u.scan("84006")
        self.u.scan("84006")
        self.u.scan("379222001730")
        self.u.scan("379222001730")
        self.u.scan("379222001730")
        self.u.scan("379222001730")
        self.u.scan("379222001730")

        self.u.scan__allow_info("648484060479")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(1)

        self.u.assert_row_status_green(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_ormd(0)
        self.u.assert_row_info_image_ormd(1)

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_34_worst_case_plus_ecommerce(self):
        """
        Battery and thorium and ORM-D and no-longer-implememted ecommerce
        warnings. Going by Air. Worst-case scenario.
        """
        # This test has some problems, where it throws "An operation on a socket
        # could not be performed because the system lacked sufficient buffer
        # space or because a queue was full"
        #
        # This bypasses that error, by performing fewer operations.
        quick_test = True

        order_id_scan = "AA42200"
        #html_promotion_active = (
        #    u'<div>'
        #    u'<table id="table_of_order_notes">'
        #    u'<tbody>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/metal2_small.png">'
        #    u'</span>'
        #    u'<span>'
        #    u'<img src="/static/img/battery_doc4_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>Pack coin batteries in a separate box<br>'
        #    u'</span>'
        #    u'<span>Mark "Metal, Batteries Only" on document<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/ion1_small.png">'
        #    u'</span>'
        #    u'<span>'
        #    u'<img src="/static/img/battery_doc2_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>Label each Helmet + SmartBand/SmartBelt kit with Ion label<br>'
        #    u'</span>'
        #    u'<span>Mark "Ion, With Equipment" on document<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/ion1_small.png">'
        #    u'</span>'
        #    u'<span>'
        #    u'<img src="/static/img/battery_doc2_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>Label each TRPR box with Ion label<br>'
        #    u'</span>'
        #    u'<span>Mark "Ion, With Equipment" on document<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/ion2_small.png">'
        #    u'</span>'
        #    u'<span>'
        #    u'<img src="/static/img/battery_doc7_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>Max 2 SmartBands/SmartBelts per box<br>'
        #    u'</span>'
        #    u'<span>Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box<br>'
        #    u'</span>'
        #    u'<span>------------------<br>'
        #    u'</span>'
        #    u'<span>Package Ion batteries in a separate box, max 2 per box<br>'
        #    u'</span>'
        #    u'<span>Mark "Ion, Batteries Only" on the document for the battery box<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/un_2909_small.png">'
        #    u'</span>'
        #    u'<span>'
        #    u'<img src="/static/img/boxes_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>Ship in multiple packages<br>'
        #    u'</span>'
        #    u'<span>Max 20 packs of rods per package<br>'
        #    u'</span>'
        #    u'<span>Wrap thoriated rods in a small box inside each shipping carton<br>'
        #    u'</span>'
        #    u'<span>Label shipping cartons with UN 2909 label<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/red_x_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.<br>'
        #    u'</span>'
        #    u'<span>Label ORM-D. Make sure the box rating is visible<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'<tr>'
        #    u'<td class="pkpk_order_note_image">'
        #    u'<span>'
        #    u'<img src="/static/img/dollar_sign_small.png">'
        #    u'</span>'
        #    u'</td>'
        #    u'<td class="pkpk_order_note_text">'
        #    u'<span>Include Gas Purchase Mail-In Rebate Form.<br>'
        #    u'</span>'
        #    u'</td>'
        #    u'</tr>'
        #    u'</tbody>'
        #    u'</table>'
        #    u'</div>'
        #)
        html_promotion_not_active = (
            u'<div>'
            u'<table id="table_of_order_notes">'
            u'<tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/metal2_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc4_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Pack coin batteries in a separate box<br>'
            u'</span>'
            u'<span>Mark "Metal, Batteries Only" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion1_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each Helmet + SmartBand/SmartBelt kit with Ion label<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion1_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc2_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Label each TRPR box with Ion label<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on document<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/ion2_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/battery_doc7_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Max 2 SmartBands/SmartBelts per box<br>'
            u'</span>'
            u'<span>Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box<br>'
            u'</span>'
            u'<span>------------------<br>'
            u'</span>'
            u'<span>Package Ion batteries in a separate box, max 2 per box<br>'
            u'</span>'
            u'<span>Mark "Ion, Batteries Only" on the document for the battery box<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/un_2909_small.png">'
            u'</span>'
            u'<span>'
            u'<img src="/static/img/boxes_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>Ship in multiple packages<br>'
            u'</span>'
            u'<span>Max 20 packs of rods per package<br>'
            u'</span>'
            u'<span>Wrap thoriated rods in a small box inside each shipping carton<br>'
            u'</span>'
            u'<span>Label shipping cartons with UN 2909 label<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span>'
            u'<img src="/static/img/red_x_small.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.<br>'
            u'</span>'
            u'<span>Label ORM-D. Make sure the box rating is visible<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody>'
            u'</table>'
            u'</div>'
        )
        #if self.ecommerce_promotion_is_active():
        #    expected_html = html_promotion_active
        #else:
        #    expected_html = html_promotion_not_active
        expected_html = html_promotion_not_active

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(expected_html)
        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(45)

        self.u.assert_row_status_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_status_blank(3)
        self.u.assert_row_status_blank(4)
        self.u.assert_row_status_blank(5)
        self.u.assert_row_status_blank(6)
        self.u.assert_row_status_blank(7)
        self.u.assert_row_status_blank(8)
        self.u.assert_row_status_blank(9)
        self.u.assert_row_status_blank(10)
        self.u.assert_row_status_blank(11)
        self.u.assert_row_status_blank(12)
        self.u.assert_row_status_blank(13)
        self.u.assert_row_status_blank(14)
        self.u.assert_row_status_blank(15)
        self.u.assert_row_status_blank(16)
        self.u.assert_row_status_blank(17)
        self.u.assert_row_status_blank(18)
        self.u.assert_row_status_blank(19)
        self.u.assert_row_status_blank(20)
        self.u.assert_row_status_blank(21)
        self.u.assert_row_status_blank(22)
        self.u.assert_row_status_blank(23)
        self.u.assert_row_status_blank(24)
        self.u.assert_row_status_blank(25)
        self.u.assert_row_status_blank(26)
        self.u.assert_row_status_blank(27)
        self.u.assert_row_status_blank(28)
        self.u.assert_row_status_blank(29)
        self.u.assert_row_status_blank(30)
        self.u.assert_row_status_blank(31)
        self.u.assert_row_status_blank(32)
        self.u.assert_row_status_blank(33)
        self.u.assert_row_status_blank(34)
        self.u.assert_row_status_blank(35)
        self.u.assert_row_status_blank(36)
        self.u.assert_row_status_blank(37)
        self.u.assert_row_status_blank(38)
        self.u.assert_row_status_blank(39)
        self.u.assert_row_status_blank(40)
        self.u.assert_row_status_blank(41)
        self.u.assert_row_status_blank(42)
        self.u.assert_row_status_blank(43)
        self.u.assert_row_status_blank(44)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_info_image_thorium(12)
        self.u.assert_row_info_image_thorium(13)
        self.u.assert_row_info_image_thorium(14)
        self.u.assert_row_info_image_thorium(15)
        self.u.assert_row_info_image_thorium(16)
        self.u.assert_row_info_image_thorium(17)
        self.u.assert_row_info_image_thorium(18)
        self.u.assert_row_info_image_thorium(19)
        self.u.assert_row_info_image_thorium(20)
        self.u.assert_row_info_image_thorium(21)
        self.u.assert_row_info_image_thorium(22)
        self.u.assert_row_info_image_thorium(23)
        self.u.assert_row_info_image_thorium(24)
        self.u.assert_row_info_image_thorium(25)
        self.u.assert_row_info_image_thorium(26)
        self.u.assert_row_info_image_thorium(27)
        self.u.assert_row_info_image_thorium(28)
        self.u.assert_row_info_image_thorium(29)
        self.u.assert_row_info_image_thorium(30)
        self.u.assert_row_info_image_thorium(31)
        self.u.assert_row_info_image_thorium(32)
        self.u.assert_row_info_image_thorium(33)
        self.u.assert_row_info_image_thorium(34)
        self.u.assert_row_info_image_thorium(35)
        self.u.assert_row_info_image_thorium(36)
        self.u.assert_row_info_image_thorium(37)
        self.u.assert_row_info_image_thorium(38)
        self.u.assert_row_info_image_thorium(39)
        self.u.assert_row_info_image_thorium(40)
        self.u.assert_row_info_image_thorium(41)
        self.u.assert_row_info_image_thorium(42)
        self.u.assert_row_info_image_ormd(43)
        self.u.assert_row_info_image_ormd(44)

        table_data = [(1, '648484149532', '058685', 0, 21.0, '2PK', 0,       ),         #    MetalCoinBattery
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 0,        ),
                      (3, '648484023498', '164421', 0, 10.0, '2PK', 0,       ),
                      (4, '648484111669', '164422', 0, 6.0, 'EA', 0,         ),         #    CompleteTRPR
                      (5, '648484028745', '164485', 0, 11.0, '10PK', 0,      ),         #    TRPRWithoutLens
                      (6, '648484220033', '187441', 0, 11.0, 'EA', 0,        ),         #    SmartBand
                      (7, '648484209892', '187442', 0, 11.0, 'EA', 0,        ),         #    SmartBelt
                      (8, '648484209908', '187443', 0, 11.0, 'EA', 0,        ),         #    TRPRBattery
                      (12, '648484330244', '213858', 0, 1.0, 'EA', 0,        ),         #    SmartBandBattery
                      (9, '648484316972', '245237', 0, 40.0, 'EA', 0,        ),         #    SmartBeltBattery
                      (10, '648484338141', '222003', 0, 1.0, 'EA', 0,        ),         #    MetalAndIonPackageKit
                      (11, '648484030595', '604612', 0, 1.0, '4PK', 0,       ),         #    another SmartBelt
                      (13, '',             '6LGT5', 0, 10.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (14, '',             '6LGT6', 0, 11.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (15, '',             '6LGT7', 0, 12.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (16, '',             '6LGT8', 0, 13.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (17, '',             '6LGT9', 0, 14.0, '10PK', 0,      ),         #    Thoriated rods - Harper
                      (18, '',             '6UHJ2', 0, 15.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (19, '',             '6UHJ4', 0, 16.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (20, '',             '6UHJ6', 0, 17.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (21, '',             '6UHJ8', 0, 18.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (22, '',             '6UHK1', 0, 19.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (23, '',             '6UHK3', 0, 20.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (24, '',             '6UHK4', 0, 21.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (25, '',             '6UHK6', 0, 22.0, 'EA', 0,        ),         #    TIG kit - Harper
                      (26, '720949054084', 'AK-1', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (27, '720949054138', 'AK-125', 0, 2.0, 'EA', 0,        ),         #    TIG kit
                      (28, '720949054169', 'AK-18', 0, 22.0, 'EA', 0,        ),         #    TIG kit
                      (29, '720949054206', 'AK-1A', 0, 32.0, 'EA', 0,        ),         #    TIG kit
                      (30, '720949054244', 'AK-2', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (31, '720949054312', 'AK-27', 0, 12.0, 'EA', 0,        ),         #    TIG kit
                      (32, '720949054343', 'AK-3', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (33, '720949054442', 'AK-4', 0, 6.0, 'EA', 0,          ),         #    TIG kit
                      (34, '720949054473', 'AK-4A', 0, 2.0, 'EA', 0,         ),         #    TIG kit
                      (35, '720949054497', 'AK-5', 0, 2.0, 'EA', 0,          ),         #    TIG kit
                      (36, '720949054534', 'AK-5W', 0, 2.0, 'EA', 0,         ),         #    TIG kit
                      (37, '720949054626', 'AK-8', 0, 7.0, 'EA', 0,          ),         #    TIG kit
                      (38, '720949230716', 'WT018X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (39, '720949230686', 'WT040X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (40, '720949230693', 'WT116X7', 0, 2.0, '10PK', 0,     ),         #    Thoriated rods
                      (41, '720949230709', 'WT332X7', 0, 3.0, '10PK', 0,     ),         #    Thoriated rods
                      (42, '720949230723', 'WT532X7', 0, 10.0, '10PK', 0,    ),         #    Thoriated rods
                      (43, '648484364348', 'WTP20RM', 0, 2.0, 'EA', 0,       ),         #    Discontinued thorium product
                      (44, '379222001730', '84006', 0, 20.0, 'EA', 0,        ),         #    ORM-D
                      (45, '648484060479', '098205', 0, 6.0, 'EA', 0,        ),         #    ORM-D
                     ]

        if quick_test:
            t = QuickTableTester(table_data,            # pylint: disable=C0103
                                 self.u,
                                )
            t.scan_almost_to_end()
        else:
            t = TableTester(table_data,                 # pylint: disable=C0103
                            self.u,
                           )
            t.multi_scan(40, "upc")
            t.multi_scan(t.how_much_farther() - 1, "item")

        self.u.scan__allow_info("098205")
        self.u.wait_for_multimedia_info_box(expected_html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(44)

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
        self.u.assert_row_status_green(17)
        self.u.assert_row_status_green(18)
        self.u.assert_row_status_green(19)
        self.u.assert_row_status_green(20)
        self.u.assert_row_status_green(21)
        self.u.assert_row_status_green(22)
        self.u.assert_row_status_green(23)
        self.u.assert_row_status_green(24)
        self.u.assert_row_status_green(25)
        self.u.assert_row_status_green(26)
        self.u.assert_row_status_green(27)
        self.u.assert_row_status_green(28)
        self.u.assert_row_status_green(29)
        self.u.assert_row_status_green(30)
        self.u.assert_row_status_green(31)
        self.u.assert_row_status_green(32)
        self.u.assert_row_status_green(33)
        self.u.assert_row_status_green(34)
        self.u.assert_row_status_green(35)
        self.u.assert_row_status_green(36)
        self.u.assert_row_status_green(37)
        self.u.assert_row_status_green(38)
        self.u.assert_row_status_green(39)
        self.u.assert_row_status_green(40)
        self.u.assert_row_status_green(41)
        self.u.assert_row_status_green(42)
        self.u.assert_row_status_green(43)
        self.u.assert_row_status_green(44)
        self.u.assert_row_info_image_metal(0)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_row_info_image_ion(3)
        self.u.assert_row_info_image_ion(4)
        self.u.assert_row_info_image_ion(5)
        self.u.assert_row_info_image_ion(6)
        self.u.assert_row_info_image_ion(7)
        self.u.assert_row_info_image_ion(8)
        self.u.assert_row_info_image_ion(9)
        self.u.assert_row_info_image_ion(10)
        self.u.assert_row_info_image_ion(11)
        self.u.assert_row_info_image_thorium(12)
        self.u.assert_row_info_image_thorium(13)
        self.u.assert_row_info_image_thorium(14)
        self.u.assert_row_info_image_thorium(15)
        self.u.assert_row_info_image_thorium(16)
        self.u.assert_row_info_image_thorium(17)
        self.u.assert_row_info_image_thorium(18)
        self.u.assert_row_info_image_thorium(19)
        self.u.assert_row_info_image_thorium(20)
        self.u.assert_row_info_image_thorium(21)
        self.u.assert_row_info_image_thorium(22)
        self.u.assert_row_info_image_thorium(23)
        self.u.assert_row_info_image_thorium(24)
        self.u.assert_row_info_image_thorium(25)
        self.u.assert_row_info_image_thorium(26)
        self.u.assert_row_info_image_thorium(27)
        self.u.assert_row_info_image_thorium(28)
        self.u.assert_row_info_image_thorium(29)
        self.u.assert_row_info_image_thorium(30)
        self.u.assert_row_info_image_thorium(31)
        self.u.assert_row_info_image_thorium(32)
        self.u.assert_row_info_image_thorium(33)
        self.u.assert_row_info_image_thorium(34)
        self.u.assert_row_info_image_thorium(35)
        self.u.assert_row_info_image_thorium(36)
        self.u.assert_row_info_image_thorium(37)
        self.u.assert_row_info_image_thorium(38)
        self.u.assert_row_info_image_thorium(39)
        self.u.assert_row_info_image_thorium(40)
        self.u.assert_row_info_image_thorium(41)
        self.u.assert_row_info_image_thorium(42)
        self.u.assert_row_info_image_ormd(43)
        self.u.assert_row_info_image_ormd(44)

        if quick_test:
            url_encoded_post_content = self.u.build_post_content(
                order_id_scan,
                special_keys_encoded = "%3A%20058685%3A%5B%2B%5D%20%20136748%3A%5B%2B%5D%20%20"
                                       "164421%3A%5B%2B%5D%20%20164422%3A%5B%2B%5D%20%20164485%3A%5B%2B%5D%20%20"
                                       "187441%3A%5B%2B%5D%20%20187442%3A%5B%2B%5D%20%20187443%3A%5B%2B%5D%20%20"
                                       "245237%3A%5B%2B%5D%20%20222003%3A%5B%2B%5D%20%20604612%3A%5B%2B%5D%20%20"
                                       "213858%3A%5B%2B%5D%20%206LGT5%3A%5B%2B%5D%20%206LGT6%3A%5B%2B%5D%20%20"
                                       "6LGT7%3A%5B%2B%5D%20%206LGT8%3A%5B%2B%5D%20%206LGT9%3A%5B%2B%5D%20%20"
                                       "6UHJ2%3A%5B%2B%5D%20%206UHJ4%3A%5B%2B%5D%20%206UHJ6%3A%5B%2B%5D%20%20"
                                       "6UHJ8%3A%5B%2B%5D%20%206UHK1%3A%5B%2B%5D%20%206UHK3%3A%5B%2B%5D%20%20"
                                       "6UHK4%3A%5B%2B%5D%20%206UHK6%3A%5B%2B%5D%20%20AK-1%3A%5B%2B%5D%20%20"
                                       "AK-125%3A%5B%2B%5D%20%20AK-18%3A%5B%2B%5D%20%20AK-1A%3A%5B%2B%5D%20%20"
                                       "AK-2%3A%5B%2B%5D%20%20AK-27%3A%5B%2B%5D%20%20AK-3%3A%5B%2B%5D%20%20"
                                       "AK-4%3A%5B%2B%5D%20%20AK-4A%3A%5B%2B%5D%20%20AK-5%3A%5B%2B%5D%20%20"
                                       "AK-5W%3A%5B%2B%5D%20%20AK-8%3A%5B%2B%5D%20%20WT018X7%3A%5B%2B%5D%20%20"
                                       "WT040X7%3A%5B%2B%5D%20%20WT116X7%3A%5B%2B%5D%20%20WT332X7%3A%5B%2B%5D%20%20"
                                       "WT532X7%3A%5B%2B%5D%20%20WTP20RM%3A%5B%2B%5D%20%2084006%3A%5B%2B%5D%20%20"
                                       "098205%3A%5B-%3E%20-%3E%20-%3E%20-%3E%20-%3E%5D",
               )
        else:
            url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    #def test_35_ecommerce(self):
    #    """
    #    Test the seasonal ecommerce warning.
    #    """
    #    order_id_scan = "AA41400"
    #    html = (
    #        u'<div>'
    #        u'<table id="table_of_order_notes">'
    #        u'<tbody>'
    #        u'<tr>'
    #        u'<td class="pkpk_order_note_image">'
    #        u'<span>'
    #        u'<img src="/static/img/dollar_sign_large.png">'
    #        u'</span>'
    #        u'</td>'
    #        u'<td class="pkpk_order_note_text">'
    #        u'<span>Include Gas Purchase Mail-In Rebate Form.<br>'
    #        u'</span>'
    #        u'</td>'
    #        u'</tr>'
    #        u'</tbody>'
    #        u'</table>'
    #        u'</div>'
    #    )
    #
    #    if self.ecommerce_promotion_is_active():
    #        self.u.scan__allow_info(order_id_scan)
    #        self.u.wait_for_multimedia_info_box(html)
    #        self.u.key_press(" ")
    #        self.u.wait_for_info_box_cleared()
    #    else:
    #        self.u.scan(order_id_scan)
    #    self.u.assert_brand_new_order(order_id_scan)
    #    self.u.assert_row_count(1)
    #
    #    self.u.assert_row_status_blank(0)
    #    self.u.assert_row_info_image_blank(0)
    #
    #    self.u.scan("187442")
    #    self.u.scan("187442")
    #
    #    if self.ecommerce_promotion_is_active():
    #        self.u.scan__allow_info("187442")
    #        self.u.wait_for_multimedia_info_box(html)
    #        self.u.key_press(" ")
    #        self.u.wait_for_info_box_cleared()
    #    else:
    #        self.u.scan("187442")
    #
    #    self.u.wait_for_big_green()
    #    self.u.assert_row_highlighted(0)
    #
    #    self.u.assert_row_status_green(0)
    #    self.u.assert_row_info_image_blank(0)
    #
    #    url_encoded_post_content = self.u.build_post_content(order_id_scan)
    #    self.u.wait_for_comment_posting(url_encoded_post_content)
    #
    #def test_36_ecommerce(self):
    #    """
    #    Test the seasonal ecommerce warning.
    #    """
    #    order_id_scan = "AA42000"
    #    html_promotion_active = (
    #        u'<div>'
    #        u'<table id="table_of_order_notes">'
    #        u'<tbody>'
    #        u'<tr>'
    #        u'<td class="pkpk_order_note_image">'
    #        u'<span><img src="/static/img/ion2_large.png">'
    #        u'</span>'
    #        u'</td>'
    #        u'<td class="pkpk_order_note_text">'
    #        u'<span>Pack SmartBand batteries with other items, max 75 per box<br>'
    #        u'</span>'
    #        u'</td>'
    #        u'</tr>'
    #        u'<tr>'
    #        u'<td class="pkpk_order_note_image">'
    #        u'<span>'
    #        u'<img src="/static/img/dollar_sign_large.png">'
    #        u'</span>'
    #        u'</td>'
    #        u'<td class="pkpk_order_note_text">'
    #        u'<span>Include Gas Purchase Mail-In Rebate Form.<br>'
    #        u'</span>'
    #        u'</td>'
    #        u'</tr>'
    #        u'</tbody>'
    #        u'</table>'
    #        u'</div>'
    #    )
    #    html_promotion_not_active = (
    #        u'<div>'
    #        u'<table id="table_of_order_notes">'
    #        u'<tbody>'
    #        u'<tr>'
    #        u'<td class="pkpk_order_note_image">'
    #        u'<span><img src="/static/img/ion2_large.png">'
    #        u'</span>'
    #        u'</td>'
    #        u'<td class="pkpk_order_note_text">'
    #        u'<span>Pack SmartBand batteries with other items, max 75 per box<br>'
    #        u'</span>'
    #        u'</td>'
    #        u'</tr>'
    #        u'</tbody>'
    #        u'</table>'
    #        u'</div>'
    #    )
    #    if self.ecommerce_promotion_is_active():
    #        expected_html = html_promotion_active
    #    else:
    #        expected_html = html_promotion_not_active
    #
    #    self.u.scan__allow_info(order_id_scan)
    #    self.u.wait_for_multimedia_info_box(expected_html)
    #    self.u.key_press(" ")
    #    self.u.wait_for_info_box_cleared()
    #    self.u.assert_brand_new_order(order_id_scan)
    #    self.u.assert_row_count(3)
    #
    #    self.u.assert_row_status_blank(0)
    #    self.u.assert_row_status_blank(1)
    #    self.u.assert_row_status_blank(2)
    #    self.u.assert_row_info_image_blank(0)
    #    self.u.assert_row_info_image_ion(1)
    #    self.u.assert_row_info_image_blank(2)
    #
    #    self.u.scan("216326")
    #    self.u.scan("216326")
    #    self.u.scan("216326")
    #    self.u.scan("216326")
    #    self.u.scan("216326")
    #    self.u.scan("216326")
    #    self.u.scan("243927")
    #    self.u.scan("243927")
    #    self.u.scan__allow_info("252907")
    #    self.u.wait_for_multimedia_info_box(expected_html)
    #
    #    self.u.key_press(" ")
    #    self.u.wait_for_info_box_cleared()
    #
    #    self.u.wait_for_big_green()
    #    self.u.assert_row_highlighted(2)
    #
    #    self.u.assert_row_status_green(0)
    #    self.u.assert_row_status_green(1)
    #    self.u.assert_row_status_green(2)
    #    self.u.assert_row_info_image_blank(0)
    #    self.u.assert_row_info_image_ion(1)
    #    self.u.assert_row_info_image_blank(2)
    #
    #    url_encoded_post_content = self.u.build_post_content(order_id_scan)
    #    self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_37_helmet_warning(self):
        """
        Three or more helmets must go ground.
        """
        order_id_scan = "AA63005"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/helmet_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>This order has 4 helmets. The helmets must go Ground<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_info_image_blank(2)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(3)

        self.u.scan("058685")
        self.u.scan("247058")
        self.u.scan("247058")
        self.u.scan("247058")
        self.u.scan("247058")

        self.u.scan__allow_info("136748")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_38_heavy_order(self):
        """
        Orders over 35 lbs that are Signature Service or Normal must go ground.
        """
        order_id_scan = "AA64000"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/helmet_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>This order has 102 helmets. The helmets must go Ground<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/heavy_weight_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>This order weighs 40 lbs. Orders over 35 lbs. must go Ground. Apply the yellow Ground sticker.<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_blank(2)
        self.u.assert_row_info_image_blank(2)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(3)

        self.u.scan("34C389", repeat = 100)
        self.u.scan("247058")

        self.u.scan__allow_info("257214")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(2)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_row_status_green(2)
        self.u.assert_row_info_image_blank(2)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_39_heavy_order(self):
        """
        Orders over 35 lbs that are Signature Service or Normal must go ground.
        """
        order_id_scan = "AA64003"
        html = (
            u'<div><table id="table_of_order_notes"><tbody>'
            u'<tr>'
            u'<td class="pkpk_order_note_image">'
            u'<span><img src="/static/img/heavy_weight_large.png">'
            u'</span>'
            u'</td>'
            u'<td class="pkpk_order_note_text">'
            u'<span>This order weighs 40 lbs. Orders over 35 lbs. must go Ground. Apply the yellow Ground sticker.<br>'
            u'</span>'
            u'</td>'
            u'</tr>'
            u'</tbody></table></div>'
        )

        self.u.scan__allow_info(order_id_scan)
        self.u.wait_for_multimedia_info_box(html)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()
        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)

        self.u.scan("34C389")
        self.u.scan__allow_info("257214")
        self.u.wait_for_multimedia_info_box(html)

        self.u.key_press(" ")
        self.u.wait_for_info_box_cleared()

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)

    def test_40_heavy_order(self):
        """
        Orders over 35 lbs that are Today Sure or Service File should not display a warning.
        """
        order_id_scan = "AA64004"

        self.u.scan(order_id_scan)

        self.u.assert_brand_new_order(order_id_scan)
        self.u.assert_row_count(2)
        self.u.assert_row_status_blank(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_blank(1)
        self.u.assert_row_info_image_blank(1)

        self.u.scan("34C389")
        self.u.scan("257214")

        self.u.wait_for_big_green()
        self.u.assert_row_highlighted(1)
        self.u.assert_row_status_green(0)
        self.u.assert_row_info_image_blank(0)
        self.u.assert_row_status_green(1)
        self.u.assert_row_info_image_blank(1)
        self.u.assert_order_status_green()

        url_encoded_post_content = self.u.build_post_content(order_id_scan)
        self.u.wait_for_comment_posting(url_encoded_post_content)



class TestOtherCases(BaseForPickpackTests):
    """
    This class holds some Selenium tests for the Pick Pack project. This tests
    edge cases and error handling.
    """
    def __init__(self):
        BaseForPickpackTests.__init__(self)

    def common_code_for_handleable_server_errors(self,
                                                 order_id_scan,
                                                 alert_text,
                                                ):
        """
        Boilerplate code for testing a case where the server returns an error
        and we display it to the user.
        """
        self.u.scan__allow_error(order_id_scan)
        self.u.wait_for_error_box(alert_text)
        self.u.assert_no_rows()
        self.u.assert_order_status_red()
        self.u.key_press(" ")
        self.u.wait_for_error_box_cleared()
        self.u.assert_no_rows()
        self.u.assert_order_status_blank()
        self.u.assert_order_number_blank()

    def test_1_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA60100"
        alert_text = "Order AA601/00 is on Warehouse Hold. Do not ship."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_2_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA60200"
        alert_text = "Order AA602/00 is on Warehouse Hold. Do not ship."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_3_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA60300"
        alert_text = "Order AA603/00 is on Warehouse Hold. Do not ship."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_4_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA61100"
        alert_text = "Order AA611/00 has one or more items that have not been picked. Items: 238626."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_5_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA61200"
        alert_text = "Order AA612/00 has one or more items that have not been picked. Items: 244094."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_6_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA61300"
        alert_text = "Order AA613/00 has one or more items that have not been picked. Items: 149962, 155454, 172075, 231921."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_7_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA61401"
        alert_text = "Order AA614/01 has one or more items that have not been picked. Items: 149962, 155454, 231921, 231921, 231921."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_8_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA70000"
        alert_text = "Order AA700/00 has an invalid service level: . Should be T, SS, S or N."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_9_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA70001"
        alert_text = "Order AA700/01 has an invalid service level: X. Should be T, SS, S or N."
        self.common_code_for_handleable_server_errors(order_id_scan,
                                                      alert_text,
                                                     )

    def test_10_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA71000"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        #alert_text = "Order AA710/00 has an invalid carrier code: ZZZZ."
        #self.common_code_for_handleable_server_errors(order_id_scan,
        #                                              alert_text,
        #                                             )

    def test_11_handleable_server_error(self):
        """
        The server can return a handleable error that the client can display
        to the user in a friendly manner. Test this feature.
        """
        order_id_scan = "AA71001"
        self.u.scan(order_id_scan)
        self.u.assert_brand_new_order(order_id_scan)
        #alert_text = "Order AA641/00 has an invalid carrier code: ."
        #self.common_code_for_handleable_server_errors(order_id_scan,
        #                                              alert_text,
        #                                             )


class TestPickpackSetAndUnsetUserId(BaseForPickpackTests):
    """
    These are some Selenium tests for the Pick Pack project. These tests test
    the ability to set and unset the user id.
    """
    def __init__(self):
        BaseForPickpackTests.__init__(self)

    def test_01_unset_cookie(self):
        """
        Test unsetting the cookie.
        """
        self.u.assert_display_user_id(self.u.DEFAULT_USER)

        self.u.special_key(self.u.F12)

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

    def test_02_set_cookie_after_unset(self):
        """
        Test setting the cookie by adding user id data.
        """
        # This test starts out the same as the others
        self.test_01_unset_cookie()

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












#
