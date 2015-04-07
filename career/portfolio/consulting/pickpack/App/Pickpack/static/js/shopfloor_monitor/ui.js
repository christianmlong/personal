/*
 * ui.js: Functions that deal with manipulating the user interface for
 * the client-side JavaScript for the Pick Pack application.
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit */
/*global common */

/*jshint bitwise: true,
         curly: true,
         eqeqeq: true,
         forin: true,
         freeze: true,
         immed: true,
         indent: 4,
         latedef: true,
         newcap: true,
         noarg: true,
         noempty: true,
         nonew: true,
         plusplus: true,
         undef: true,
         unused: strict,
         strict: true,
         trailing: true,

         browser: true

*/


// Create namespace if it does not yet exist
var shopfloor_monitor;

if (!shopfloor_monitor) {
    shopfloor_monitor = {};
}
else if (typeof shopfloor_monitor !== "object") {
    throw new Error("shopfloor_monitor already exists, and is not an object");
}

if (shopfloor_monitor.ui) {
    throw new Error("shopfloor_monitor.ui already exists");
}
else {
    shopfloor_monitor.ui = {};
}


(
    function () {
        'use strict';

        //function doEscape() {
        //    location.reload();
        //}

        //function buildImagePath(image_name) {
        //    return shopfloor_monitor.constants.PATH_TO_IMG +
        //           image_name +
        //           shopfloor_monitor.constants.IMG_EXT;
        //}

        function dismissConfigPane() {
            // Hide configuration screen
            common.ui.dismissModalPane(shopfloor_monitor.constants.OPTIONS_PANE_ID);

            //// Write the user preferences to a cookie.
            //// Note: we do this "on change" instead
            //shopfloor_monitor.globals.optionController.saveOptionValuesToCookie();
        }

        function showConfigPane() {
            // Show configuration screen
            showModalPane(shopfloor_monitor.constants.OPTIONS_PANE_ID);

            // Load the stored values from the cookie into the SELECT elements.
            shopfloor_monitor.globals.optionController.loadOptionValuesFromCookie();
        }

        function dismissHelpPane() {
            // Hide help screen
            common.ui.dismissModalPane(shopfloor_monitor.constants.HELP_PANE_ID);
        }

        function showHelpPane() {
            // Show help screen
            showModalPane(shopfloor_monitor.constants.HELP_PANE_ID);
        }

        function showModalPane(pane_id) {
            guardModal("283");
            common.ui.showModalPane(pane_id);
        }

        function hideInfoBox(keep_contents) {
            var info_box = MochiKit.DOM.getElement(shopfloor_monitor.constants.INFO_BOX_ID);
            var info_body_element = MochiKit.DOM.getElement(shopfloor_monitor.constants.INFO_BOX_BODY_ID);
            common.ui.hideElement(info_box);

            if (!keep_contents) {
                // Disconnect all the event handlers for the dom elements we added
                // for the order numbers
                MochiKit.Signal.disconnectAllTo(shopfloor_monitor.event_handlers.handleOrderNumberSpanOnClick);

                // Clean out all those order number dom elements.
                //info_body_element.innerHTML = "";
                MochiKit.DOM.replaceChildNodes(info_body_element);
            }
        }

        //function showInfoBox(info_msg) {
        //    _showInfoBox(info_msg, false);
        //}

        function showInfoBoxWithDomElements(dom_elements) {
            _showInfoBox(dom_elements, true, true);
        }

        function showPreviouslyHiddenInfoBox() {
            _showInfoBox(null, false, false);
        }

        function _showInfoBox(new_stuff, use_dom, replace_contents) {
            var info_box = MochiKit.DOM.getElement(shopfloor_monitor.constants.INFO_BOX_ID);
            var info_body_element = MochiKit.DOM.getElement(shopfloor_monitor.constants.INFO_BOX_BODY_ID);
            if (replace_contents) {
                if (use_dom) {
                    MochiKit.DOM.replaceChildNodes(info_body_element, new_stuff);
                }
                else {
                    info_body_element.innerHTML = new_stuff;
                }
            }
            if (!infoBoxIsActive()) {
                common.ui.showElement(info_box);
            }
        }

        function hideOrderDetailBox() {
            var order_detail_box = MochiKit.DOM.getElement(shopfloor_monitor.constants.ORDER_DETAIL_BOX_ID);
            var order_detail_body_element = MochiKit.DOM.getElement(shopfloor_monitor.constants.ORDER_DETAIL_BOX_BODY_ID);
            common.ui.hideElement(order_detail_box);

            // Clean out all the dom elements.
            //order_detail_body_element.innerHTML = "";
            MochiKit.DOM.replaceChildNodes(order_detail_body_element);

            // Show the previous info box
            showPreviouslyHiddenInfoBox();
        }

        //function showOrderDetailBox(order_detail_msg) {
        //    _showOrderDetailBox(order_detail_msg, false);
        //}

        function showOrderDetailBoxWithDomElements(dom_elements) {
            _showOrderDetailBox(dom_elements, true);
        }

        function _showOrderDetailBox(new_stuff, use_dom) {
            var order_detail_box = MochiKit.DOM.getElement(shopfloor_monitor.constants.ORDER_DETAIL_BOX_ID);
            var order_detail_body_element = MochiKit.DOM.getElement(shopfloor_monitor.constants.ORDER_DETAIL_BOX_BODY_ID);
            if (use_dom) {
                MochiKit.DOM.replaceChildNodes(order_detail_body_element, new_stuff);
            }
            else {
                order_detail_body_element.innerHTML = new_stuff;
            }
            if (!orderDetailBoxIsActive()) {

                // Hide the info box, keep the contents for later.
                hideInfoBox(true);

                common.ui.showElement(order_detail_box);
            }
        }

        function clearAlert() {
            common.ui.clearAlert(shopfloor_monitor.constants.ERROR_BOX_ID,
                                        shopfloor_monitor.constants.ERROR_TEXT_ID);
        }

        function postAlert(message) {
            common.ui.postAlert(message,
                                       shopfloor_monitor.constants.ERROR_BOX_ID,
                                       shopfloor_monitor.constants.ERROR_TEXT_ID);
        }

        function postAlertWithTraceback(message, traceback) {
            common.ui.showTraceback(traceback, "sfmo_debug_info");
            postAlert(message);
        }

        function getElementId(element) {
            return element.id;
        }

        function getElementValue(element) {
            // Will accept an element object, or an ID string
            var elementToRead = MochiKit.DOM.getElement(element);
            var elementTag = elementToRead.tagName.toLowerCase();
            var elementType = MochiKit.DOM.getNodeAttribute(elementToRead, "type");

            if (elementTag === "select") {
                var index = elementToRead.selectedIndex;
                var optionElement = elementToRead.options[index];
                return optionElement.value;
            }
            else if ((elementTag === "input") && (elementType === "checkbox")) {
                return common.utility_functions.smarterBooleanConversion(elementToRead.checked);
            }
            else {
                shopfloor_monitor.error.throwApplicationError("Incompatible element");

                // A sop to silence the JavaScript syntax checker warning about
                // not all branches of the if statement returning a return
                // value.
                return null;
            }
        }

        function setElementValue(element, valueToSet) {
            var elementToWrite = MochiKit.DOM.getElement(element);
            var elementTag = elementToWrite.tagName.toLowerCase();
            var elementType = MochiKit.DOM.getNodeAttribute(elementToWrite, "type");
            var i;

            if (elementTag === "select") {
                var optionsArray = elementToWrite.options;
                for (i = 0; i < optionsArray.length; i += 1) {
                    if (optionsArray[i].value === valueToSet) {
                        elementToWrite.selectedIndex = i;
                        break;
                    }
                }
            }
            else if ((elementTag === "input") && (elementType === "checkbox")) {
                elementToWrite.checked = common.utility_functions.smarterBooleanConversion(valueToSet);
            }
            else {
                shopfloor_monitor.error.throwApplicationError("Incompatible element");
            }
        }

        function clearBox() {
            // Clear the boxes in descending order of importance.
            if (alertBoxIsActive()) {
                clearAlert();
                return;
            }
            if (orderDetailBoxIsActive()) {
                hideOrderDetailBox();
                return;
            }
            if (infoBoxIsActive()) {
                hideInfoBox(false);
                return;
            }
        }

        function aModalPaneIsActive() {
            return (optionsPaneIsActive() ||
                    helpPaneIsActive()
                   );
        }

        function aBoxIsActive() {
            return (alertBoxIsActive() ||
                    infoBoxIsActive() ||
                    orderDetailBoxIsActive()
                   );
        }

        function noModalPane() {
            // No modal panes (e.g. the options pane) are active.
            return !aModalPaneIsActive();
        }

        function guardModal(error_no) {
            if (aModalPaneIsActive()) {
                shopfloor_monitor.error.throwApplicationError(error_no);
            }
        }

        //function guardInfoBoxOrErrorBoxIsActive() {
        //    // The user is trying to make changes to the order while there is an
        //    // active error or info box. Post an error message and disallow the
        //    // changes.
        //    var info_msg = "I can not proceed while this information box is visible. " +
        //                   "Please dismiss this box by pressing the space bar.";
        //    var error_msg = "I can not proceed while the red error box is visible. " +
        //                    "Please dismiss this box by pressing the space bar.";
        //    if (alertBoxIsActive()) {
        //        shopfloor_monitor.error.throwHandleableError(error_msg);
        //    }
        //    else if (infoBoxIsActive()) {
        //        shopfloor_monitor.error.throwInfoException(info_msg);
        //    }
        //}

        function optionsPaneIsActive() {
            return common.ui.paneIsActive(shopfloor_monitor.constants.OPTIONS_PANE_ID);
        }

        function helpPaneIsActive() {
            return common.ui.paneIsActive(shopfloor_monitor.constants.HELP_PANE_ID);
        }

        function alertBoxIsActive() {
            return common.ui.boxIsActive(shopfloor_monitor.constants.ERROR_BOX_ID);
        }

        function infoBoxIsActive() {
            return common.ui.boxIsActive(shopfloor_monitor.constants.INFO_BOX_ID);
        }

        function orderDetailBoxIsActive() {
            return common.ui.boxIsActive(shopfloor_monitor.constants.ORDER_DETAIL_BOX_ID);
        }

        function showOneUp() {
            showGraph(1);
        }

        function showFourUp() {
            showGraph(2);
        }

        function showFourUpNarrow() {
            showGraph(3);
        }

        function showGraph(show_one_up) {
            var one_up = MochiKit.DOM.getElement("sfmo_1up_container");
            var four_up = MochiKit.DOM.getElement("sfmo_4up_container");
            var four_up_narrow = MochiKit.DOM.getElement("sfmo_4up_narrow_container");
            if (show_one_up === 1) {
                common.ui.hideElement(four_up);
                common.ui.hideElement(four_up_narrow);
                common.ui.showElement(one_up);
            }
            else if (show_one_up === 2) {
                common.ui.hideElement(one_up);
                common.ui.hideElement(four_up_narrow);
                common.ui.showElement(four_up);
            }
            else if (show_one_up === 3) {
                common.ui.hideElement(one_up);
                common.ui.hideElement(four_up);
                common.ui.showElement(four_up_narrow);
            }
            else {
                throw new Error("Invalid value for show_one_up: " + show_one_up);
            }
        }

        function displayGraph(data) {
            // First draw the graph. Then, display it by making its container
            // visible. Also, hide the container of the other graph layout.
            if (shopfloor_monitor.globals.optionController.dataDisplay === "4up") {
                shopfloor_monitor.draw_graph.drawFourUp(
                    data,
                    shopfloor_monitor.globals.optionController.showBackorder,
                    false);
                showFourUp();
            }
            else if (shopfloor_monitor.globals.optionController.dataDisplay === "4up_narrow") {
                shopfloor_monitor.draw_graph.drawFourUp(
                    data,
                    shopfloor_monitor.globals.optionController.showBackorder,
                    true);
                showFourUpNarrow();
            }
            else {
                shopfloor_monitor.draw_graph.drawOneUp(
                    data,
                    shopfloor_monitor.globals.optionController.showBackorder);
                showOneUp();
            }
        }

        function displayOrderNumberList(data, bar_index) {
            var dom_elements = buildOrderNumberElements(data, bar_index);
            showInfoBoxWithDomElements(dom_elements);
        }

        function displayOrderDetails(data) {
            var dom_elements = buildOrderDetailElements(data);
            showOrderDetailBoxWithDomElements(dom_elements);
        }

        function buildOrderNumberElements(data, bar_index) {
            // Translate bar_index in to order_type
            var function_to_call;
            if (shopfloor_monitor.globals.optionController.showBackorder) {
                function_to_call = {0 : buildOrderNumberElementsTodaySureBackorder,
                                    1 : buildOrderNumberElementsSignatureServiceBackorder,
                                    2 : buildOrderNumberElementsServiceFileBackorder,
                                    3 : buildOrderNumberElementsNormalBackorder};
            }
            else {
                function_to_call = {0 : buildOrderNumberElementsTodaySure,
                                    1 : buildOrderNumberElementsSignatureService,
                                    2 : buildOrderNumberElementsServiceFile,
                                    3 : buildOrderNumberElementsNormal};
            }
            var dom_elements = function_to_call[bar_index](data);
            return dom_elements;
        }

        function buildOrderNumberElementsTodaySure(data) {
            return buildOrderNumberElementsTodayAndTomorrow(data, shopfloor_monitor.constants.TODAY_SURE);
        }

        function buildOrderNumberElementsSignatureService(data) {
            return buildOrderNumberElementsTodayAndTomorrow(data, shopfloor_monitor.constants.SIGNATURE_SERVICE);
        }

        function buildOrderNumberElementsServiceFile(data) {
            return buildOrderNumberElementsTodayOnly(data, shopfloor_monitor.constants.SERVICE_FILE);
        }

        function buildOrderNumberElementsNormal(data) {
            return buildOrderNumberElementsTodayAndTomorrow(data, shopfloor_monitor.constants.NORMAL);
        }

        function buildOrderNumberElementsTodayOnly(data, order_type) {
            var order_number_elements = [
                formatSection(shopfloor_monitor.constants.LABEL_TODAY, data.should_ship_today, order_type)
            ];
            return buildToplevelStructure(order_type, order_number_elements, false, data);
        }

        function buildOrderNumberElementsTodayAndTomorrow(data, order_type) {
            var order_number_elements = [
                formatSection(shopfloor_monitor.constants.LABEL_TODAY, data.should_ship_today, order_type),
                MochiKit.DOM.HR(),
                formatSection(shopfloor_monitor.constants.LABEL_TOMORROW, data.can_ship_tomorrow, order_type)
            ];
            return buildToplevelStructure(order_type, order_number_elements, false, data);
        }

        function buildOrderNumberElementsTodaySureBackorder(data) {
            return buildOrderNumberElementsBackorder(data, shopfloor_monitor.constants.TODAY_SURE);
        }

        function buildOrderNumberElementsSignatureServiceBackorder(data) {
            return buildOrderNumberElementsBackorder(data, shopfloor_monitor.constants.SIGNATURE_SERVICE);
        }

        function buildOrderNumberElementsServiceFileBackorder(data) {
            return buildOrderNumberElementsBackorder(data, shopfloor_monitor.constants.SERVICE_FILE);
        }

        function buildOrderNumberElementsNormalBackorder(data) {
            return buildOrderNumberElementsBackorder(data, shopfloor_monitor.constants.NORMAL);
        }

        function buildOrderNumberElementsBackorder(data, order_type) {
            var order_number_elements = [
                formatSection(shopfloor_monitor.constants.LABEL_BACKORDER, data.backorder, order_type)
            ];
            return buildToplevelStructure(order_type, order_number_elements, true, data);
        }

        function buildToplevelStructure(order_type, order_number_elements, is_backorder, data) {
            var d = MochiKit.DOM;

            var last_print_date_time_dom_contents;
            var order_number_dom_contents;
            var last_print_label_dom_contents;
            var order_entry_label_dom_contents;
            var order_entry_date_time_dom_contents;

            if (is_backorder) {
                order_number_dom_contents = "";
                last_print_label_dom_contents = "";
                last_print_date_time_dom_contents = "";
                order_entry_label_dom_contents = "";
                order_entry_date_time_dom_contents = "";
            }
            else if (data.last_print_data.last_print_formatted_order_number === common.constants.NO_DATA_FOUND) {
                order_number_dom_contents = "";
                last_print_label_dom_contents = "No recent print";
                last_print_date_time_dom_contents = "";
                order_entry_label_dom_contents = "";
                order_entry_date_time_dom_contents = "";
            }
            else {
                order_number_dom_contents = formatNumber(data.last_print_data.last_print_formatted_order_number);
                last_print_label_dom_contents = common.constants.NBSP + "Last Print:" + common.constants.NBSP;
                last_print_date_time_dom_contents = shopfloor_monitor.utility_functions.omitDate(data.last_print_data.last_print_date, data.last_print_data.last_print_time);
                order_entry_label_dom_contents = "entered" + common.constants.NBSP;
                order_entry_date_time_dom_contents = shopfloor_monitor.utility_functions.omitDate(data.last_print_data.entry_date_of_last_printed_order, data.last_print_data.entry_time_of_last_printed_order);
            }

            // MochiKit.DOM.createDom will flatten this array.
            return [d.DIV(
                        {"class" : "sfmo_detail_header"},
                        d.SPAN(
                            {"class" : "float_left"},
                            shopfloor_monitor.utility_functions.getCurrentCaption() + " - " + order_type + " orders"
                        ),
                        d.SPAN(
                            {"class" : "float_right"},
                            d.SPAN(
                                null,
                                last_print_label_dom_contents
                            ),
                            d.SPAN(
                                null,
                                last_print_date_time_dom_contents
                            )
                        )
                    ),
                    d.BR(),
                    d.DIV(
                        {"class" : "sfmo_detail_header"},
                        d.SPAN(
                            {"class" : "float_right"},
                            //d.SPAN(
                            //    null,
                            //    order_number_label_dom_contents
                            //),
                            d.SPAN(
                                null,
                                order_number_dom_contents
                            ),
                            d.SPAN(
                                null,
                                order_entry_label_dom_contents
                            ),
                            d.SPAN(
                                null,
                                order_entry_date_time_dom_contents
                            )
                        )
                    ),
                    d.BR(),
                    // MochiKit.DOM.createDom will flatten the order_number_elements array.
                    order_number_elements];
        }

        function formatSection(section_name,
                               sub_sections,
                               order_type) {
            var d = MochiKit.DOM;
            var return_value;
            var formatted_subsections = formatSubSections(sub_sections);
            if (formatted_subsections === null) {
                return_value = null;
            }
            else {
                return_value = d.P(null,
                                   buildImgTag(section_name, order_type),
                                   // These don't work:
                                   // d.NBSP,
                                   // MochiKit.DOM.NBSP,
                                   //
                                   // but this does:
                                   common.constants.NBSP,
                                   d.SPAN(null, section_name),
                                   d.BR(),
                                   formatted_subsections);
            }
            return return_value;
        }

        function buildImgTag(section_name,
                             order_type) {
            var d = MochiKit.DOM;
            var fill_type;
            var order_type_letter;

            switch (section_name) {
            case shopfloor_monitor.constants.LABEL_TOMORROW:
                fill_type = "ghost";
                break;
            case shopfloor_monitor.constants.LABEL_TODAY:
                fill_type = "solid";
                break;
            case shopfloor_monitor.constants.LABEL_HOLD:
                fill_type = "dark";
                break;
            case shopfloor_monitor.constants.LABEL_BACKORDER:
                fill_type = "stripe";
                break;
            }

            switch (order_type) {
            case shopfloor_monitor.constants.TODAY_SURE:
                order_type_letter = "ts";
                break;
            case shopfloor_monitor.constants.SIGNATURE_SERVICE:
                order_type_letter = "ss";
                break;
            case shopfloor_monitor.constants.SERVICE_FILE:
                order_type_letter = "s";
                break;
            case shopfloor_monitor.constants.NORMAL:
                order_type_letter = "n";
                break;
            }

            var image_path = "/static/img/shopfloor_monitor/" + order_type_letter + "_key_" + fill_type + ".png";
            return d.SPAN(null,
                          d.IMG({"class" : "sfmo_graph_key_img",
                                 "src" : image_path}));
        }

        function formatSubSections(sub_sections) {
            if (!sub_sections) {
                return null;
            }
            else {
                var formatted_sub_sections = [formatSubSection(shopfloor_monitor.constants.LABEL_READY_TO_PRINT, sub_sections.ready_to_print),
                                              formatSubSection(shopfloor_monitor.constants.LABEL_PICKSLIP_PRINTED, sub_sections.pick_slip_printed)];
                var packed_sub_section;
                if (shopfloor_monitor.globals.optionController.showUntil === shopfloor_monitor.constants.SHOW_UNTIL_SCALE) {
                    packed_sub_section = formatSubSection(shopfloor_monitor.constants.LABEL_PACKED, sub_sections.packed);
                    if (packed_sub_section) {
                        formatted_sub_sections.push(packed_sub_section);
                    }
                }
                return formatted_sub_sections;
            }
        }

        function formatSubSection(sub_section_name,
                                  sub_section_numbers) {
            var d = MochiKit.DOM;
            var return_value;
            var formatted_numbers = formatNumbers(sub_section_numbers);
            if (formatted_numbers === null) {
                return_value = null;
            }
            else {
                return_value = d.P(null,
                                   d.SPAN(null, common.constants.BULLET_POINT + common.constants.NBSP + sub_section_name),
                                   d.BR(),
                                   formatted_numbers);
            }
            return return_value;
        }

        function mapFormat(function_to_call, iterable) {
            var return_value;
            if (iterable.length === 0) {
                return_value = null;
            }
            else {
                return_value = MochiKit.Base.map(function_to_call, iterable);
            }
            return return_value;
        }

        function formatNumbers(order_numbers) {
            var return_value;
            if (order_numbers.length === 0) {
                return_value = null;
            }
            else {
                return_value = MochiKit.Base.map(formatNumber, order_numbers);
            }
            return mapFormat(formatNumber, order_numbers);
        }

        function formatNumber(order_number) {
            var d = MochiKit.DOM;
            var activate;
            var html_class;
            var dom_element;

            if (common.utility_functions.startsWith(order_number, '...')) {
                // Don't make the "... N more" comment active.
                activate = false;
            }
            else {
                activate = true;
            }

            if (activate) {
                html_class = 'sfmo_order_number';
            }
            else {
                html_class = 'sfmo_inert';
            }

            dom_element = d.SPAN({"class" : html_class}, order_number);

            if (activate) {
                MochiKit.Signal.connect(dom_element, "onclick", shopfloor_monitor.event_handlers.handleOrderNumberSpanOnClick);
            }

            return dom_element;
        }

        function buildOrderDetailElements(data) {
            var d = MochiKit.DOM;
            var dom_elements;

            var order_status_text;
            if (data.order_status_code === common.constants.NO_DATA_FOUND) {
                order_status_text = "No data found";
            }
            else if (data.order_status_code === 1) {
                order_status_text = shopfloor_monitor.constants.LABEL_READY_TO_PRINT;
            }
            else if (data.order_status_code === 2 && data.packer_id === "") {
                order_status_text = shopfloor_monitor.constants.LABEL_PICKSLIP_PRINTED;
            }
            else if (data.order_status_code === 2 && data.packer_id !== "") {
                order_status_text = shopfloor_monitor.constants.LABEL_PACKED;
            }
            else {
                order_status_text = data.order_status_code.toString();
            }

            var formatted_order_number;
            if (data.order_number === common.constants.NO_DATA_FOUND) {
                formatted_order_number = "No data found";
            }
            else {
                formatted_order_number = common.utility_functions.formatOrderNumberAndGenerationForDisplay(data.order_number,
                                                                                                                  data.order_generation);
            }

            // Clean up the rest of data.
            var clean_data = emptyStringForNoDataFound(data);

            dom_elements = [d.DIV(
                                null,
                                d.TABLE({id : shopfloor_monitor.constants.ORDER_DETAIL_TABLE_ID},
                                    d.TBODY(null,
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Order"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 formatted_order_number
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Picker"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.picker_id
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Ship To"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.customer_number + '-' + clean_data.customer_name
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Packer"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.packer_id
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "# of lines"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.number_of_lines
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Status"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 order_status_text
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Weight"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.shipped_order_weight.toString() + " lbs."
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Carrier Code"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.carrier_code
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Ship Type"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.complete_ship_code
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Print time"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.print_date + common.constants.NBSP + clean_data.print_time
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Entered By"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.entered_by
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Printed by"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.printer_id
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Service Level"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.service_level
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Req Date"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.requested_ship_date
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Order Entry"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.order_entry_date + common.constants.NBSP + clean_data.order_entry_time
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Backorder code"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.backorder_code
                                            )
                                        ),
                                        d.TR(null,
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Ship Instructions"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.shipping_instructions
                                            ),
                                            d.TD({"class" : "sfmo_table_label"},
                                                 "Team"
                                            ),
                                            d.TD({"class" : "sfmo_table_data"},
                                                 clean_data.truck_team
                                            )
                                        ),
                                        formatOrderNote("Order Notes"),
                                        formatOrderNotes(clean_data.order_notes)
                                    )
                                )
                            )
                           ];
            return dom_elements;
        }

        function emptyStringForNoDataFound(order_data) {
            // JavaScript does not have an easy deepcopy. So, I just make
            // a new object manually.
            // http://stackoverflow.com/questions/728360/most-elegant-way-to-clone-a-javascript-object
            var cleaned_order_data = {
                customer_number         : order_data.customer_number,
                order_number            : order_data.order_number,
                order_generation        : order_data.order_generation,
                order_status_code       : order_data.order_status_code,
                customer_name           : order_data.customer_name,
                entered_by              : order_data.entered_by,
                backorder_code          : order_data.backorder_code,
                shipping_instructions   : order_data.shipping_instructions,
                carrier_code            : order_data.carrier_code,
                packer_id               : order_data.packer_id,
                picker_id               : order_data.picker_id,
                printer_id              : order_data.printer_id,
                shipped_order_weight    : order_data.shipped_order_weight,
                number_of_lines         : order_data.number_of_lines,
                truck_team              : order_data.truck_team,
                complete_ship_code      : order_data.complete_ship_code,
                service_level           : order_data.service_level,
                print_date              : order_data.print_date,
                print_time              : order_data.print_time,
                order_entry_date        : order_data.order_entry_date,
                order_entry_time        : order_data.order_entry_time,
                requested_ship_date     : order_data.requested_ship_date,
                order_notes             : order_data.order_notes
            };

            var item;
            for (item in cleaned_order_data) {
                if (cleaned_order_data.hasOwnProperty(item) && cleaned_order_data[item] === common.constants.NO_DATA_FOUND) {
                    cleaned_order_data[item] = "";
                }
            }
            return cleaned_order_data;
        }

        function formatOrderNotes(order_notes) {
            return mapFormat(formatOrderNote, order_notes);
        }

        function formatOrderNote(text) {
            var d = MochiKit.DOM;
            return d.TR(null,
                        d.TD({"class" : "sfmo_full_width", "colspan" : 4},
                             text
                        )
                   );
        }

        function setOptionsByShortcut(key_string) {
            var data_display;
            var show_backorder;
            var show_until;
            var set_data_display = false;
            var set_show_backorder = false;
            var set_show_until = false;

            switch (key_string) {
            case "1":
                data_display = "wcc";
                show_backorder = false;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "2":
                data_display = "parts";
                show_backorder = false;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "3":
                data_display = "both";
                show_backorder = false;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "4":
                data_display = "all";
                show_backorder = false;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "5":
                data_display = "4up_narrow";
                show_backorder = false;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "6":
                data_display = "4up";
                show_backorder = false;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "7":
                data_display = "wcc";
                show_backorder = true;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "8":
                data_display = "parts";
                show_backorder = true;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "9":
                data_display = "both";
                show_backorder = true;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "0":
                data_display = "all";
                show_backorder = true;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "-":
                data_display = "4up_narrow";
                show_backorder = true;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "=":
                data_display = "4up";
                show_backorder = true;
                set_data_display = true;
                set_show_backorder = true;
                break;
            case "S":
                show_until = "scale";
                set_show_until = true;
                break;
            case "B":
                show_until = "packing_bench";
                set_show_until = true;
                break;
            default:
                throw new Error("Invalid key_string: " + key_string);
            }
            if (set_data_display) {
                shopfloor_monitor.ui.setElementValue("data_display", data_display);
            }
            if (set_show_backorder) {
                shopfloor_monitor.ui.setElementValue("show_backorder", show_backorder);
            }
            if (set_show_until) {
                shopfloor_monitor.ui.setElementValue("show_until", show_until);
            }
            shopfloor_monitor.globals.optionController.saveOptionValuesToCookie();
        }




        // Export symbols to namespace
        var ns = shopfloor_monitor.ui;
        ns.dismissConfigPane = dismissConfigPane;
        ns.showConfigPane = showConfigPane;
        ns.dismissHelpPane = dismissHelpPane;
        ns.showHelpPane = showHelpPane;
        ns.getElementId = getElementId;
        ns.getElementValue = getElementValue;
        ns.setElementValue = setElementValue;
        ns.postAlert = postAlert;
        ns.postAlertWithTraceback = postAlertWithTraceback;
        ns.aBoxIsActive = aBoxIsActive;
        ns.clearBox = clearBox;
        ns.noModalPane = noModalPane;
        ns.optionsPaneIsActive = optionsPaneIsActive;
        ns.helpPaneIsActive = helpPaneIsActive;
        ns.displayGraph = displayGraph;
        ns.displayOrderNumberList = displayOrderNumberList;
        ns.displayOrderDetails = displayOrderDetails;
        ns.setOptionsByShortcut = setOptionsByShortcut;
    }
()); // End of function (closure). Now invoke it.
