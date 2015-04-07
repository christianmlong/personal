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
         unused: true,
         strict: true,
         trailing: true,

         browser: true,
         laxcomma: true

*/


// Create namespace if it does not yet exist
var pickpack;

if (!pickpack) {
    pickpack = {};
}
else if (typeof pickpack !== "object") {
    throw new Error("pickpack already exists, and is not an object");
}

if (pickpack.ui) {
    throw new Error("pickpack.ui already exists");
}
else {
    pickpack.ui = {};
}


(
    function () {
        'use strict';

        function fillTable(json_object) {
            // Using DOM, create the table based on the JSON we got from the
            // server.
            var newTable = MochiKit.DOM.TABLE({'id': pickpack.constants.ITEMS_TABLE_ID},
                                              MochiKit.DOM.TBODY(null,
                                                                 MochiKit.Base.map(buildTableRowElementFromJSON, json_object.packing_list_array)
                                                                )
                                             );

            // Display the table we just created.
            MochiKit.DOM.swapDOM(pickpack.constants.ITEMS_TABLE_ID, newTable);

            // Update the order number display
            setOrderNumberAndGeneration(json_object.order_number,
                                        json_object.order_generation
                                       );

            // Update order status, but don't POST a comment to the database
            updateOrderStatus(false);
        }

        function resetApplication() {
            // Using DOM, create a new blank table.
            var newTable = MochiKit.DOM.TABLE({'id': pickpack.constants.ITEMS_TABLE_ID},
                                              MochiKit.DOM.TBODY(null)
                                             );

            // Display the blank table we just created.
            MochiKit.DOM.swapDOM(pickpack.constants.ITEMS_TABLE_ID, newTable);

            clearOrderNumberAndGeneration();
            displayUserId();

            // Clear the info box, if present. We do not clear the error box
            // here - this is to prevent swallowing any possible error here that
            // should only be dismissed by the user pressing the space bar.
            hideInfoBox();

            // Update order status, but don't POST a comment to the database
            updateOrderStatus(false);
        }

        function doInitialPageRendering() {
            // Set up page elements right away after page load completes.
            displayUserId();
        }

        function clearOrderNumberAndGeneration() {
            // Clear the order number display
            var display_order_number_element = MochiKit.DOM.getElement("display_order_number");
            display_order_number_element.innerHTML = "";
        }

        function setOrderNumberAndGeneration(order_number, order_generation) {
            // Update the order number display
            var display_order_number_element = MochiKit.DOM.getElement("display_order_number");
            display_order_number_element.innerHTML = common.utility_functions.formatOrderNumberAndGenerationForDisplay(order_number, order_generation);
        }

        function getOrderNumberAndGeneration() {
            // Get order number and generation back out of the display element.
            // Returns an array.
            var display_order_number_element = MochiKit.DOM.getElement("display_order_number");
            return common.utility_functions.parseOrderNumberAndGenerationFromDisplay(display_order_number_element.innerHTML);
        }

        function formatOrderIdScanForDisplay(order_id_scan,
                                             error_on_fail) {
            if (error_on_fail) {
                return _formatOrderIdScanForDisplay(order_id_scan);
            }
            else {
                try {
                    return _formatOrderIdScanForDisplay(order_id_scan);
                }
                catch (ex) {
                    return null;
                }
            }
        }

        function _formatOrderIdScanForDisplay(order_id_scan) {
            if (typeof order_id_scan !== "string") {
                pickpack.error.throwApplicationError("System error 29520 - order_id_scan is not a string. " + typeof order_id_scan);
            }
            var parsed_elements = common.utility_functions.parseOrderNumberAndGenerationFromScan(order_id_scan);
            return common.utility_functions.formatOrderNumberAndGenerationForDisplay(parsed_elements[0], parsed_elements[1]);
        }

        function displayUserId() {
            // Update the user id display, based on the cookie value
            var display_order_number_element = MochiKit.DOM.getElement("display_user_id");
            display_order_number_element.innerHTML = pickpack.globals.optionController.userId;
        }

        function buildTableRowElementFromJSON(json_row) {
            //<tr id="%s" class="barcode_%s item_%s">
            //<td class="pkpk_status"       >%s</td>
            //<td class="pkpk_status_img"   ><img class="pkpk_status_img" src="/static/img/blank1.png" /></td>
            //<td class="pkpk_cur_qty"      >0</td>
            //<td class="pkpk_qty"          >%i</td>
            //<td class="pkpk_item"         >%s</td>
            //<td class="pkpk_um"           >%s</td>
            //<td class="pkpk_serialized"   >%s</td>
            //<td class="pkpk_info_img"     >%s</td>
            //</tr>
            //
            //
            // 0 line_no
            // 1 barcode
            // 2 item_no
            // 3 status
            // 4 quantity
            // 5 sales_um
            // 6 serialized
            // 7 has_item_note
            // 8 Inline image indicating if this item has warnings
            //
            //
            //[[1, "648484149532", "058685", 0, 1.0, "2PK", 0, 0, 0],
            // [2, "648484140133", "136748", 0, 1.0, "2PK", 0, 0, 2],
            //}

            // Convenient local binding for the MochiKit.DOM namespace
            var d = MochiKit.DOM;

            // Build up the row using MochiKit.DOM.createDOM. This syntax is
            // based on Nevow's Stan.
            //
            // This function returns DOM elements, not an HTML string.
            return d.TR({"id" : json_row[0], "class" : "barcode_" + json_row[1] + " item_" + json_row[2]}
                       , d.TD({"class" : "pkpk_status"}, json_row[3])
                       , d.TD({"class" : "pkpk_status_img"}
                             , d.IMG({"class" : "pkpk_status_img", "src" : buildIconImagePath(json_row[3], "1")})
                             )
                       , d.TD({"class" : "pkpk_cur_qty"}, 0)
                       , d.TD({"class" : "pkpk_qty"}, json_row[4])
                       , d.TD({"class" : "pkpk_item"}, json_row[2])
                       , d.TD({"class" : "pkpk_um"}, json_row[5])
                       , d.TD({"class" : "pkpk_serialized"}, json_row[6])
                       , d.TD({"class" : "pkpk_info_img"}
                             , d.IMG({"class" : "pkpk_info_img", "src" : buildInfoImagePath(json_row[8])})
                             )
                       );
        }

        function readInt(theElement) {
            return parseInt(theElement.innerHTML, 10);
        }

        function handleOrderIdScan(orderIdScan) {
            if (!allowNextOrder()) {
                // The current order is not green or blank
                // POSSIBLE IMPROVEMENT parse orderIdScan, and format it nicely here
                pickpack.error.throwHandleableError("I can not proceed to the next order (" + orderIdScan +
                                                    ") until this order is complete.");
            }

            // Clear the application. This does not post an order status update
            // to the database.
            resetApplication();

            // Fetch packing list data from database.
            pickpack.server.packingListRequest(orderIdScan);
        }

        function handleItemScan(row_reference, increment_by) {
            var the_row_elements;
            var description;
            var lookup;
            var success;
            var row_element;
            var i;

            // No changes allowed if the order is already complete, or if there
            // is an error or info box active.
            guardNoChangesAllowed();

            if (increment_by === pickpack.constants.INCREMENT_BY_UPC) {
                description = "UPC";
                lookup = true;
                the_row_elements = findRowsByUPC(row_reference);
            }
            else if (increment_by === pickpack.constants.INCREMENT_BY_ITEM_NO) {
                description = "Item";
                lookup = false;

                // Strip leading item_quantity information, if any. This is only
                // found on the Harper item labels.
                row_reference = pickpack.regex.checkForHarperItemNumber(row_reference);

                the_row_elements = findRowsByItem(row_reference);
            }
            else {
                pickpack.error.throwApplicationError("System error 28500");
            }

            if ((!(the_row_elements)) || (the_row_elements.length === 0)) {
                pickpack.error.throwHandleableError("That item is not on this order. " + description +
                                                    ": " + row_reference);

                // POSSIBLE IMPROVEMENT
                // Test this - does this get executed after we throw the
                // handleable error?
                if (lookup) {
                    // The user scanned a UPC, but it's not on this order.
                    //
                    // We show the alert right away, and we also ask the server
                    // for the item number that goes with this UPC. When the
                    // server responds, we append the item number to the end of
                    // the alert we are already showing to the user.
                    //
                    // Once the server returns a value, the handleResults
                    // function of the GetItemNumberByUPCRequestObject will
                    // append the item numer to the existing alert.
                    pickpack.server.getItemNumberByUPC(row_reference);
                }
            }
            else if (the_row_elements.length === 1) {
                incrementRowCount(the_row_elements[0]);
            }
            else {
                // Multiple lines with the same item. Distribute.
                success = false;
                for (i = 0; i < the_row_elements.length; i += 1) {
                    row_element = the_row_elements[i];
                    if (isGreen(getRowStatus(row_element))) {
                        // This line is already exactly full? Find the next one.
                        continue;
                    }
                    else {
                        // This line is not exactly full, increment it.
                        incrementRowCount(row_element);
                        success = true;
                        break;
                    }
                }
                if (!success) {
                    // No suitable row found in the loop, just update the first
                    // one. This would happen if (for example) all the rows of
                    // that item are green - this would then send the first row
                    // into red status.
                    incrementRowCount(the_row_elements[0]);
                }
            }
        }

        function findRowsByUPC(UPC_number) {
            var tagName = "tr";
            var className = "barcode_" + UPC_number;
            return MochiKit.DOM.getElementsByTagAndClassName(tagName, className);
        }

        function findRowsByItem(item_number) {
            var tagName = "tr";
            var className = "item_" + item_number;
            return MochiKit.DOM.getElementsByTagAndClassName(tagName, className);
        }

        function countRowsByItem(item_number) {
            // Returns the number of rows with the given item number.
            var the_row_elements = findRowsByItem(item_number);
            var numberOfRows;
            if (!the_row_elements) {
                numberOfRows = 0;
            }
            else {
                numberOfRows = the_row_elements.length;
            }
            return numberOfRows;
        }

        function updateRowStatus(row_element, new_status) {
            var new_count;
            // Adjust some statuses
            if (isGreen(new_status)) {
                new_count = getRowExpectedQuantity(row_element);
            }
            else if (isBlank(new_status)) {
                new_count = 0;
            }

            // Only if we made changes
            if (new_count !== undefined) {
                updateRowCountAbsolute(row_element, new_count);
            }
        }

        function incrementRowCount(row_element) {
            // The user scanned an item or UPC, or scanned a serial number while
            // the serial number box is active.

            var item_number;
            var function_call_specification;

            // Play the scanBeep sound. This is defaulted to None.
            pickpack.globals.soundController.playScanBeep();

            if ((isSerializedItem(row_element)) && (!serialNumberBoxIsActive())) {
                // If this row is a serialized item, and if the serial number
                // box is *not* already open, switch control to the serialized
                // item manager object.

                // The user can not enter serial numbers for a row that is in
                // red status.
                if (isRed(getRowStatus(row_element))) {
                    pickpack.error.throwHandleableError("This row is in error status (red X). Please fix this " +
                                                        "row before scanning any serialized items.");
                }

                // The user scanned a serialized item. Switch control to the
                // serialized item manager object.

                // Check item notes
                item_number = pickpack.ui.getRowItemNumber(row_element);
                if (pickpack.globals.itemNotesHandler.itemHasNotesToDisplay(item_number)) {
                    // There are item notes for this item. Show them now. After
                    // the notes dialog has been dismissed, we switch control to
                    // the serialized item manager object.

                    // Bundle up the function to be called, along with its
                    // arguments, in to an array.
                    function_call_specification = [
                        pickpack.globals.serializedItemContainer.startSerialNumberEntry,
                        row_element
                    ];

                    // Here, we are telling the notes manager to queue up the
                    // call to the serialized item manager object, and to run it
                    // after the notes dialog has been dismissed.
                    pickpack.globals.itemNotesHandler.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed(
                        item_number,
                        function_call_specification
                    );
                }
                else {
                    // There are no item notes. Switch control over to the
                    // serialized item manager object right now.
                    pickpack.globals.serializedItemContainer.startSerialNumberEntry(row_element);
                }
            }
            else {
                // No need to pop up the serial number dialog (no serial
                // numbers, or the dialog is already present). Just increment
                // the row.
                //
                // Note that when the serial number box is open and the user
                // scans a serial number, this gets called to update the
                // corresponding row.
                updateRowCountRelative(row_element, 1);
            }
        }

        function incrementRowCountByRowId(row_id) {
            // The MochiKit.DOM functions accept both DOM elements and IDs.
            // However, in my functions, I want to maintain a clear distiction
            // between functions that accept row elements and row IDs.
            var row_element = MochiKit.DOM.getElement(row_id);
            incrementRowCount(row_element);
        }

        function updateRowCountRelative(row_element, updateQuantity) {
            // Adds updateQuantity to curent quantity of row.
            var new_count = getRowCurrentQuantity(row_element) + updateQuantity;
            updateRowCountAbsolute(row_element, new_count);
        }

        function updateRowCountAbsolute(row_element, new_count) {
            // Sets the curent quantity element to the new_count, and triggers a
            // visual update.
            var item_number = pickpack.ui.getRowItemNumber(row_element);
            var function_call_specification;

            // No serialized check in here. Code paths that get here without
            // passing through a serialized item check (for example, if the user
            // presses the plus key) are not valid for serialized items.

            if (new_count < 0) {
                new_count = 0;
            }
            if (getRowCurrentQuantity(row_element) !== new_count) {
                // Check item notes
                if (pickpack.globals.itemNotesHandler.itemHasNotesToDisplay(item_number)) {
                    // There are item notes for this item. Show them now. After
                    // the notes dialog has been dismissed, we increment the row
                    // count.

                    // Bundle up the function to be called, along with its
                    // arguments, in to an array.
                    function_call_specification = [
                        _updateRowcount,
                        row_element,
                        new_count
                    ];

                    // Here, we are telling the notes manager to queue up the
                    // call to updateRowCountRelative, and to run it after the
                    // notes dialog has been dismissed.
                    pickpack.globals.itemNotesHandler.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed(
                        item_number,
                        function_call_specification
                    );
                }
                else {
                    // There are no item notes. Increment the row count right
                    // now.
                    _updateRowcount(row_element, new_count);
                }
            }
        }

        function _updateRowcount(row_element, new_count) {
            var current_count_element = MochiKit.DOM.getFirstElementByTagAndClassName(
                "td",
                "pkpk_cur_qty",
                row_element
            );
            current_count_element.innerHTML = new_count.toString();
            updateRowStatusByCount(row_element);
        }

        function updateRowStatusByCount(row_element) {
            var current_count = getRowCurrentQuantity(row_element);
            var expected_count = getRowExpectedQuantity(row_element);
            var status_element = MochiKit.DOM.getFirstElementByTagAndClassName("td", "pkpk_status", row_element);

            if (current_count === 0) {
                status_element.innerHTML = pickpack.constants.STATUS_BLANK;
            }
            else if (current_count === expected_count) {
                status_element.innerHTML = pickpack.constants.STATUS_GREEN;
            }
            else if (current_count < expected_count) {
                status_element.innerHTML = pickpack.constants.STATUS_GRAY;
            }
            else {
                status_element.innerHTML = pickpack.constants.STATUS_RED;
            }
            highlightRowAndUpdateStatusImg(row_element);
            // Update order status, and POST a comment to the database if needed
            updateOrderStatus(true);
        }

        function updateRowStatusImg(row_element) {
            var status = getRowStatus(row_element);
            var img = MochiKit.DOM.getFirstElementByTagAndClassName("img", "pkpk_status_img", row_element);

            // Decide which icon to use
            var highlight;
            if (MochiKit.DOM.hasElementClass(row_element, "highlight")) {
                highlight = "2";
            }
            else {
                highlight = "1";
            }

            img.src = buildIconImagePath(status, highlight);
        }

        function buildIconImagePath(status, highlight) {
            return buildImagePath(getIconName(status) +
                                  highlight);
        }

        function buildInfoImagePath(image_number) {
            var part1 = "inline_";
            var part2;
            if (image_number === 0) {
                part2 = "blank";
            }
            else if (image_number === 1) {
                part2 = "m";
            }
            else if (image_number === 2) {
                part2 = "i";
            }
            else if (image_number === 3) {
                part2 = "mi";
            }
            else if (image_number === 4) {
                part2 = "th";
            }
            else if (image_number === 5) {
                part2 = "ormd";
            }
            else {
                pickpack.error.throwApplicationError("Unknown info image " + image_number);
            }
            return buildImagePath(part1 +
                                  part2);
        }

        function buildImagePath(image_name) {
            return pickpack.constants.PATH_TO_IMG +
                   image_name +
                   pickpack.constants.IMG_EXT;
        }

        function getIconName(status) {
            // Returns the name of the icon for the given status
            var icon;
            if (isGreen(status)) {
                icon = "green";
            }
            else if (isRed(status)) {
                icon = "red";
            }
            else if (isBlank(status)) {
                icon = "blank";
            }
            else if (isYellow(status)) {
                icon = "yellow";
            }
            else if (isGray(status)) {
                icon = "gray";
            }
            else {
                icon = "yellow";
            }
            return icon;
        }

        function updateOrderStatus(post_comment) {
            var order_status_element = MochiKit.DOM.getElement("order_status");
            var all_row_elements = MochiKit.DOM.getElementsByTagAndClassName("tr", null, "pkpk_list_div");
            var img_element = MochiKit.DOM.getElement("order_status_img");
            var statuses = MochiKit.Base.map(getRowStatus, all_row_elements);
            var old_status = readInt(order_status_element);
            var new_status = order_status_element.innerHTML = calculateOrderStatus(statuses);
            var function_call_specification;

            if (old_status !== new_status) {
                // Change the order status image
                img_element.src = buildIconImagePath(new_status, "1");
            }

            if (post_comment) {
                if ((isGreen(new_status)) && (!isGreen(old_status))) {
                    // Moving from non-green to green status
                    if (pickpack.globals.orderNotesHandler) {
                        // There are order notes for this order. Show them now.
                        // After the notes dialog has been dismissed, we mark
                        // the order as complete.

                        // Bundle the function to be called in to an array.
                        function_call_specification = [
                            orderComplete
                        ];

                        // Here, we are telling the notes manager to queue up
                        // the call to the orderComplete function, and to run it
                        // after the notes dialog has been dismissed. With the
                        // 'end' paremter, we're telling the orderNotesHandler
                        // that we're at the end of the process.
                        pickpack.globals.orderNotesHandler.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed(
                            'end',
                            function_call_specification
                        );
                    }
                    else {
                        // There are no order notes. Mark the order as complete
                        // right now.
                        orderComplete();
                    }

                }
                else if ((!isGreen(new_status)) && (isGreen(old_status))) {
                    // We can't move from green to non-green status if we are
                    // posting results to the database. Application error.
                    pickpack.error.throwApplicationError("Can not move from green to non-green status.");
                }
            }

            if (isRed(new_status)) {
                // Play an error sound on red, even if we were red before.
                pickpack.globals.soundController.playErrorSound();
            }
        }

        function orderComplete() {
            // Write an "order complete" comment, and notify user.
            var order_number_and_generation = getOrderNumberAndGeneration();
            var current_order_number = order_number_and_generation[0];
            var current_order_generation = order_number_and_generation[1];
            var comment_text = "Scanned: complete.";
            var represent_special_keys;
            var serial_number_json;

            // If there is a non-empty log of special-key presses, append the
            // log to the comments.
            if (pickpack.globals.specialKeysLogger.log) {
                represent_special_keys = pickpack.globals.specialKeysLogger.specialKeysAsString();
                if (represent_special_keys !== "") {
                    comment_text = comment_text +
                                   " Special keys: " +
                                   represent_special_keys;
                }
            }

            // Send serial number data to the database along with the comment.
            serial_number_json = pickpack.globals.serializedItemContainer.serializedItemsAsJSON();

            pickpack.server.postOrderComplete(current_order_number,
                                              current_order_generation,
                                              comment_text,
                                              serial_number_json
                                             );
        }

        function calculateOrderStatus(statuses) {

            if (alertBoxIsActive()) {
                return pickpack.constants.STATUS_RED;
            }

            if (statuses.length === 0) {
                return pickpack.constants.STATUS_BLANK;
            }

            var allGreen = MochiKit.Iter.every(statuses, isGreen);
            if (allGreen) {
                return pickpack.constants.STATUS_GREEN;
            }

            var allBlank = MochiKit.Iter.every(statuses, isBlank);
            if (allBlank) {
                return pickpack.constants.STATUS_BLANK;
            }

            var someRed = MochiKit.Iter.some(statuses, isRed);
            if (someRed) {
                return pickpack.constants.STATUS_RED;
            }

            var noYellow = !(MochiKit.Iter.some(statuses, isYellow));
            var noRed = !someRed;
            var someGreen = MochiKit.Iter.some(statuses, isGreen);
            var someGray = MochiKit.Iter.some(statuses, isGray);
            var noError = noYellow && noRed;
            var someProgress = someGreen || someGray;
            if (noError && someProgress) {
                return pickpack.constants.STATUS_GRAY;
            }

            // We have not figured out the right status, punt.
            return pickpack.constants.STATUS_YELLOW;
        }

        function highlightRowAndUpdateStatusImg(row_element) {
            // Is there a row?
            if (!row_element) {
                return;
            }

            // Only change the row highlighting if we are not already
            // highlighted.
            if (!(MochiKit.DOM.hasElementClass(row_element, "highlight"))) {
                lowlightAllRows();
                common.ui.highlightElement(row_element);
            }

            // Bring the element into view on the screen, unless a box is
            // active.
            if (!serialNumberBoxIsActive()) {
                row_element.scrollIntoView();
            }

            // We use a different (bold) status image for the highlighted row,
            // so we need to update the row image when we change the
            // highlighting.
            updateRowStatusImg(row_element);
        }

        function lowlightAllRows() {
            // Clear all existing highlighting
            var currently_highlighted = MochiKit.DOM.getElementsByTagAndClassName("tr", "highlight");
            MochiKit.Iter.forEach(currently_highlighted, lowlightRowAndUpdateStatusImg);
        }

        function lowlightRowAndUpdateStatusImg(row_element) {
            common.ui.lowlightElement(row_element);
            // We use a different (bold) status image for the highlighted row,
            // so we need to update the row image when we change the
            // highlighting.
            updateRowStatusImg(row_element);
        }

        function switchToCardboardBoxLook(element) {
            common.ui.addAbsolutePositioning(element);
            MochiKit.DOM.swapElementClass(element, "pkpk_info", "pkpk_cardboard_box");
        }

        function switchToBlueInfoBoxLook(element) {
            common.ui.removeAbsolutePositioning(element);
            MochiKit.DOM.swapElementClass(element, "pkpk_cardboard_box", "pkpk_info");
        }

        function getRowItemNumber(row_element) {
            var item_element = MochiKit.DOM.getFirstElementByTagAndClassName("td", "pkpk_item", row_element);
            return item_element.innerHTML;
        }

        function getFieldIntValue(field, row) {
            return readInt(MochiKit.DOM.getFirstElementByTagAndClassName("td", field, row));
        }
        var getRowCurrentQuantity = MochiKit.Base.partial(getFieldIntValue, "pkpk_cur_qty");
        var getRowExpectedQuantity = MochiKit.Base.partial(getFieldIntValue, "pkpk_qty");
        var getRowStatus = MochiKit.Base.partial(getFieldIntValue, "pkpk_status");

        function doUpDown(direction) {
            // No changes allowed if the order is already complete, or if there
            // is an error or info box active.
            guardNoChangesAllowed();

            var current_row_element = getCurrentRowElement();
            var all_row_elements;
            var new_current_row_element;

            if (current_row_element) {
                // First we strip all highlighting. This makes comparison work.
                // Otherwise, the 'all_row_elements' array looks like this:
                // [tr#648484111959, tr#648484014687.highlight, tr#648484267946]
                lowlightAllRows();

                // Note to self: don't hoist this 'all_row_elements' assignment out of
                // the 'if' statement. If there is a current row, we need to
                // lowlight first.
                all_row_elements = MochiKit.DOM.getElementsByTagAndClassName("tr", null, "pkpk_list_div");
                var all_row_ids = MochiKit.Base.map(getElementId, all_row_elements);
                var current_position = MochiKit.Base.findIdentical(all_row_ids, current_row_element.id);

                var delta;
                if (direction === pickpack.constants.ARROW_UP) {
                    delta = -1;
                }
                else if (direction === pickpack.constants.ARROW_DOWN) {
                    delta = 1;
                }

                var new_position = common.utility_functions.pythonStyleMod((current_position + delta), all_row_elements.length);
                new_current_row_element = all_row_elements[new_position];
            }
            else {
                // No row highlighted yet. Choose one.
                var front_or_back;
                if (direction === pickpack.constants.ARROW_UP) {
                    front_or_back = 1;
                }
                else if (direction === pickpack.constants.ARROW_DOWN) {
                    front_or_back = 0;
                }
                all_row_elements = MochiKit.DOM.getElementsByTagAndClassName("tr", null, "pkpk_list_div");
                new_current_row_element = all_row_elements[((all_row_elements.length - 1) * front_or_back)];
            }

            highlightRowAndUpdateStatusImg(new_current_row_element);
        }

        function doUpArrow() {
            doUpDown(pickpack.constants.ARROW_UP);
        }

        function doDownArrow() {
            doUpDown(pickpack.constants.ARROW_DOWN);
        }

        function doRightLeft(direction) {
            // No changes allowed if the order is already complete, or if there
            // is an error or info box active.
            guardNoChangesAllowed();

            var current_row_element = getCurrentRowElement();
            var delta;
            if (current_row_element) {
                if (isSerializedItem(current_row_element)) {
                    pickpack.error.throwHandleableError("This is a serialized item. You can not " +
                                                        "use the arrow keys on a serialized item. " +
                                                        "You must scan each serial number.");
                }
                else {
                    if (direction === pickpack.constants.ARROW_RIGHT) {
                        delta = 1;
                    }
                    else if (direction === pickpack.constants.ARROW_LEFT) {
                        delta = -1;
                    }
                    pickpack.globals.specialKeysLogger.logSpecialKeyUsage(current_row_element, direction);
                    updateRowCountRelative(current_row_element, delta);
                }
            }
        }

        function doRightArrow() {
            doRightLeft(pickpack.constants.ARROW_RIGHT);
        }

        function doLeftArrow() {
            doRightLeft(pickpack.constants.ARROW_LEFT);
        }

        function doPlusMinus(key) {
            // No changes allowed if the order is already complete, or if there
            // is an error or info box active.
            guardNoChangesAllowed();

            var current_row_element = getCurrentRowElement();
            var status;
            if (key === pickpack.constants.PLUS_KEY) {
                status = pickpack.constants.STATUS_GREEN;
            }
            else if (key === pickpack.constants.F2_KEY) {
                status = pickpack.constants.STATUS_BLANK;
            }

            if (current_row_element) {
                if (isSerializedItem(current_row_element)) {
                    if (key === pickpack.constants.PLUS_KEY) {
                        pickpack.error.throwHandleableError("This is a serialized item. You can not " +
                                                            "use the Plus key on a serialized item. " +
                                                            "You must scan each serial number.");
                    }
                    else if (key === pickpack.constants.F2_KEY) {
                        // If serialized, delete log of serial numbers *for this row only*
                        pickpack.globals.serializedItemContainer.clearScannedSerialNumbers(current_row_element);
                    }
                }
                pickpack.globals.specialKeysLogger.logSpecialKeyUsage(current_row_element, key);
                updateRowStatus(current_row_element, status);
            }
        }

        function doPlus() {
            doPlusMinus(pickpack.constants.PLUS_KEY);
        }

        function doMinus() {
            doPlusMinus(pickpack.constants.F2_KEY);
        }

        function doEscape() {
            location.reload();
        }

        function dismissConfigPane() {
            var info_msg;

            if (!validateConfigPaneData()) {
                info_msg = pickpack.ui.getElementValue("user_id") + " is not a valid user id. Must be three characters or digits";
                pickpack.error.throwInfoException(info_msg);
            }

            // Hide configuration screen
            dismissModalPane(pickpack.constants.OPTIONS_PANE_ID);

            // Write the user preferences to a cookie.
            pickpack.globals.optionController.saveOptionValuesToCookie();

            // Update the user id display
            displayUserId();
        }

        function showConfigPane() {

            // Set up some options for the call to showModalPane.
            var additional_show_options = {
                // Run the fade-in in 0.3 seconds
                duration: 0.3,
                // We have to wait until the animation is done and the input box
                // is visible before we can set focus and select the current
                // contents.
                afterFinish: function () {
                    focusAndSelectUserId();
                }
            };

            // Show configuration screen
            showModalPane(pickpack.constants.OPTIONS_PANE_ID,
                          additional_show_options);

            // Load the stored values from the cookie into the form.
            pickpack.globals.optionController.loadOptionValuesFromCookie();
        }

        function focusAndSelectUserId() {
            // Focus and select the user id field
            var userIdElement = MochiKit.DOM.getElement("user_id");
            userIdElement.focus();
            userIdElement.select();
        }

        function validateConfigPaneData() {
            var user_id = pickpack.ui.getElementValue("user_id");
            if (!pickpack.regex.allowedUserId(user_id)) {
                return false;
            }
            return true;
        }

        function resetUserId() {
            // Get rid of the current user id.
            pickpack.globals.optionController.resetUserId();

            // Update the user id display
            displayUserId();
        }

        function validateUserId() {
            var info_msg;
            var cookie_user_id = pickpack.globals.optionController.userId;
            if (!pickpack.regex.allowedUserId(cookie_user_id)) {
                pickpack.globals.inputBuffer.reset();
                if (cookie_user_id === "***") {
                    info_msg = "Press F4 to set your user id.";
                }
                else {
                    info_msg = cookie_user_id + " is not a valid user id. Must be three characters or digits. Press F4 to set your user id.";
                }
                pickpack.error.throwInfoException(info_msg);
            }
        }



        function dismissHelpPane() {
            // Hide help screen
            dismissModalPane(pickpack.constants.HELP_PANE_ID);
        }

        function showHelpPane() {
            // Show help screen
            showModalPane(pickpack.constants.HELP_PANE_ID);
        }

        function dismissModalPane(pane_id) {
            common.ui.dismissModalPane(pane_id);

            // Reset the input buffer and prepare for input.
            pickpack.globals.inputBuffer.reset();
        }

        function showModalPane(pane_id,
                               additional_show_options  /* optional */ ) {
            guardModal("284");
            common.ui.showModalPane(pane_id,
                                           additional_show_options  /* optional */ );
        }

        function hideSerialNumberBox() {
            var serial_number_box = MochiKit.DOM.getElement(pickpack.constants.SERIAL_NO_BOX_ID);
            var serial_number_text_element = MochiKit.DOM.getElement(pickpack.constants.SERIAL_NO_TEXT_ID);
            common.ui.hideElement(serial_number_box);
            serial_number_text_element.innerHTML = "";

            // Reset the input buffer and prepare for input.
            pickpack.globals.inputBuffer.reset();
        }

        function showSerialNumberBox(item_number) {
            var message;

            // Throw an error if one of the modal panes is open.
            guardModal("271");

            var serial_number_box = MochiKit.DOM.getElement(pickpack.constants.SERIAL_NO_BOX_ID);
            var serial_number_text_element = MochiKit.DOM.getElement(pickpack.constants.SERIAL_NO_TEXT_ID);

            if (serialNumberBoxIsActive()) {
                pickpack.error.throwApplicationError("The serial number box is already active.");
            }

            message = "Please scan a serial number for item " + item_number;
            serial_number_text_element.innerHTML = message;
            common.ui.showElement(serial_number_box);

            // Reset the input buffer and prepare for input. The serial number
            // dialog relies on the same input box as the rest of the
            // application.
            pickpack.globals.inputBuffer.reset();
        }

        function hideInfoBox() {
            var info_box = MochiKit.DOM.getElement(pickpack.constants.INFO_BOX_ID);
            var info_body_element = MochiKit.DOM.getElement(pickpack.constants.INFO_BOX_BODY_ID);
            common.ui.hideElement(info_box);
            info_body_element.innerHTML = "";

            // The info box can have either position: fixed (does not move when
            // the user scrolls) or position: absolute (scrolls with the rest of
            // the page content).
            //
            // I use 'fixed' to show short plain-text information messages to
            // the user.
            //
            // I use 'absolute' to show the order information messages such as
            // battery label instructions. These can be long and involved, and I
            // want them to be scrollable. Rather than use two different info
            // boxes, I just toggle the positioning by adding and removing a
            // class (called 'absolute').
            //
            // Here, I reset the positioning to its default value, 'fixed', by
            // removing the 'absolute' class. I also set the pkpk_info class on
            // the box, to reset it to its default style.
            switchToBlueInfoBoxLook(info_box);

            // Reset the input buffer and prepare for input.
            pickpack.globals.inputBuffer.reset();

            // Tell the Item Notes manager (which also uses the info box) that
            // the info box has been dismissed. This will cause it to fire its
            // deferred, if it has one active.
            if (pickpack.globals.itemNotesHandler) {
                pickpack.globals.itemNotesHandler.infoBoxWasDismissed();
            }

            // Tell the Order Notes manager (which also uses the info box) that
            // the info box has been dismissed. This will cause it to fire its
            // deferred, if it has one active.
            if (pickpack.globals.orderNotesHandler) {
                pickpack.globals.orderNotesHandler.infoBoxWasDismissed();
            }

            // We do not update order status when the info box is dismissed.
        }

        function showInfoBox(info_msg) {
            var info_box = MochiKit.DOM.getElement(pickpack.constants.INFO_BOX_ID);
            var info_body_element = MochiKit.DOM.getElement(pickpack.constants.INFO_BOX_BODY_ID);
            if (infoBoxIsActive()) {
                // The info box alert is already active. Append.
                info_body_element.innerHTML = info_body_element.innerHTML + common.ui.htmlBreakTag() + info_msg;
            }
            else {
                // Here, I reset the info box to its default blue look and
                // positioning. See hideInfoBox for more information about the
                // positioning of info_box.
                //
                // This is just a safety; the info box's default look should
                // already have been reset by hideInfoBox.
                switchToBlueInfoBoxLook(info_box);

                info_body_element.innerHTML = info_msg;
                common.ui.showElement(info_box);
            }
            pickpack.globals.soundController.playErrorSound();
            // We do not update order status when the info box is shown.

            // On big info boxes (e.g.battery warnings) the bottom of the box
            // might be off the bottom of the screen.
            // Note: this only shows the top of the pkpk_info_body element, and
            // the rest, if it is long, is still out of view. However, that is
            // an uncommon occurence (the user repeatedly tries to do something
            // while the info box is active), so I'm not going to worry about
            // it. The user will at least see the first line of the content we
            // appended to pkpk_info_body.
            info_body_element.scrollIntoView();
        }

        function showInfoBoxWithDomElements(dom_elements,
                                            play_sound) {
            var info_box = MochiKit.DOM.getElement(pickpack.constants.INFO_BOX_ID);
            var info_body_element = MochiKit.DOM.getElement(pickpack.constants.INFO_BOX_BODY_ID);
            if (infoBoxIsActive()) {
                // The info box alert is already active. Append.
                info_body_element.innerHTML = info_body_element.innerHTML + common.ui.htmlBreakTag();
                MochiKit.DOM.appendChildNodes(info_body_element, dom_elements);
            }
            else {
                // Here, I set the positioning to 'absolute'. See hideInfoBox
                // for more information about the positioning of info_box.
                //
                // I also add the pkpk_cardboard_box class, to change the look
                // of the box.
                switchToCardboardBoxLook(info_box);

                MochiKit.DOM.replaceChildNodes(info_body_element, dom_elements);
                common.ui.showElement(info_box);

                // Scroll to the top of the page
                window.scroll(0,0);
            }
            if (play_sound) {
                pickpack.globals.soundController.playErrorSound();
            }
            // We do not update order status when the info box is shown.
        }

        function showOrderNotesOnDemand() {
            guardModal("281");
            if (pickpack.globals.orderNotesHandler) {
                pickpack.globals.orderNotesHandler.displayOrderNotes('on_demand');
            }
        }

        function clearAlert() {
            common.ui.clearAlert(pickpack.constants.ERROR_BOX_ID,
                                        pickpack.constants.ERROR_TEXT_ID);
            clearErrorDetail();

            // Update order status, and POST a comment to the database if needed
            updateOrderStatus(true);

            // Reset the input buffer and prepare for input.
            pickpack.globals.inputBuffer.reset();
        }

        function postAlert(message,
                           traceback /* optional */) {
            var error_box = MochiKit.DOM.getElement(pickpack.constants.ERROR_BOX_ID);
            var error_text_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TEXT_ID);

            if (alertBoxIsActive()) {
                // The alert box alert is already active. Append.
                error_text_element.innerHTML = error_text_element.innerHTML + common.ui.htmlBreakTag() + message;
            }
            else {
                error_text_element.innerHTML = message;
                common.ui.showElement(error_box);
                // Update order status, but don't POST a comment to the database
                updateOrderStatus(false);
            }

            if (traceback !== undefined) {
                populateErrorDetail(traceback);
            }
            else {
                clearErrorDetail();
            }

            pickpack.globals.soundController.playErrorSound();
        }

        function postAlertWithTraceback(message, traceback) {
            postAlert(message, traceback);
        }

        function populateErrorDetail(traceback) {
            var traceback_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TRACEBACK_ID);
            var toggle_div_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_DIV_ID);
            var toggle_text_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_TEXT_ID);
            common.ui.showElement(toggle_div_element);
            toggle_text_element.innerHTML = "Click here to show error details";
            MochiKit.Style.hideElement(traceback_element);
            traceback_element.innerHTML = traceback;
        }

        function clearErrorDetail() {
            var traceback_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TRACEBACK_ID);
            var toggle_div_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_DIV_ID);
            var toggle_text_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_TEXT_ID);
            common.ui.hideElement(toggle_div_element);
            toggle_text_element.innerHTML = "";
            MochiKit.Style.hideElement(traceback_element);
            traceback_element.innerHTML = "";
        }

        function toggleErrorDetail() {
            var traceback_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TRACEBACK_ID);
            var toggle_div_element = MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_DIV_ID);

            common.ui.showElement(toggle_div_element);

            var show_options = {duration: 0.6,
                                transition: MochiKit.Visual.Transitions.parabolic,
                                queue: "break",
                                afterFinish: function () {
                                                MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_TEXT_ID).innerHTML = "Click here to hide error details";
                                             }
                               };
            var hide_options = {duration: 0.6,
                                transition: MochiKit.Visual.Transitions.parabolic,
                                queue: "break",
                                afterFinish: function () {
                                                MochiKit.DOM.getElement(pickpack.constants.ERROR_TOGGLE_TEXT_ID).innerHTML = "Click here to show error details";
                                             }
                               };

            if (common.ui.isDisplayBlock(traceback_element)) {
                MochiKit.Visual.blindUp(traceback_element, hide_options);
            }
            else {
                MochiKit.Visual.blindDown(traceback_element, show_options);
            }
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
            else if ((elementTag === "input") && (elementType === "text")) {
                return common.utility_functions.trim(elementToRead.value);
            }
            else {
                pickpack.error.throwApplicationError("Incompatible element");

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
            else if ((elementTag === "input") && (elementType === "text")) {
                elementToWrite.value = common.utility_functions.trim(valueToSet);
            }
            else {
                pickpack.error.throwApplicationError("Incompatible element");
            }
        }

        function focusFirstInvalidRow() {
            // No changes allowed if the order is already complete, or if there
            // is an error or info box active.
            guardNoChangesAllowed();

            function rowIsNotGreen(row_element) {
                return (!(isGreen(getRowStatus(row_element))));
            }
            var all_row_elements = MochiKit.DOM.getElementsByTagAndClassName("tr", null, "pkpk_list_div");
            var non_green_row_elements = MochiKit.Base.filter(rowIsNotGreen, all_row_elements);

            if ((non_green_row_elements) &&  (non_green_row_elements.length > 0)) {
                highlightRowAndUpdateStatusImg(non_green_row_elements[0]);
            }
        }

        function clearBox() {
            // Clear the boxes in descending order of importance. If multiple
            // boxes are shown, it requires multiple calls to this function
            // (i.e. multiple presses of the space bar) to dismiss them.
            if (alertBoxIsActive()) {
                clearAlert();
                return;
            }

            if (infoBoxIsActive()) {
                hideInfoBox();
                return;
            }

            if (serialNumberBoxIsActive()) {
                hideSerialNumberBox();
                return;
            }
        }

        function aModalPaneIsActive() {
            return (optionsPaneIsActive() ||
                    helpPaneIsActive()
                   );
        }

        function noModalPane() {
            // No modal panes (e.g. the options pane) are active.
            return !aModalPaneIsActive();
        }

        function noModalPaneOrSerialNumberBox() {
            // No modal panes (e.g. the options pane) are active, and the serial
            // number box is not active.
            return !(aModalPaneIsActive() || serialNumberBoxIsActive());
        }

        function guardModal(error_no) {
            if (aModalPaneIsActive()) {
                pickpack.error.throwApplicationError(error_no);
            }
        }

        function guardNoChangesAllowed() {
            // The user is trying to make changes to the order, but the order is
            // not in an appropriate state to accept the changes.
            guardInfoBoxOrErrorBoxIsActive();
            guardGreen();
        }

        function guardInfoBoxOrErrorBoxIsActive() {
            // The user is trying to make changes to the order while there is an
            // active error or info box. Post an error message and disallow the
            // changes.
            var info_msg = "I can not proceed while this information box is visible. " +
                           "Please dismiss this box by pressing the space bar.";
            var error_msg = "I can not proceed while the red error box is visible. " +
                            "Please dismiss this box by pressing the space bar.";
            if (alertBoxIsActive()) {
                pickpack.error.throwHandleableError(error_msg);
            }
            else if (infoBoxIsActive()) {
                pickpack.error.throwInfoException(info_msg);
            }
        }

        function guardGreen() {
            // The user is trying to make changes to the order after the order
            // is complete (green). Post an information message and disallow the
            // changes.
            var info_msg = "This order is complete. You can no longer make changes to this order.";
            if (isOrderGreen()) {
                pickpack.error.throwInfoException(info_msg);
            }
        }

        function optionsPaneIsActive() {
            return common.ui.paneIsActive(pickpack.constants.OPTIONS_PANE_ID);
        }

        function helpPaneIsActive() {
            return common.ui.paneIsActive(pickpack.constants.HELP_PANE_ID);
        }

        function alertBoxIsActive() {
            return common.ui.boxIsActive(pickpack.constants.ERROR_BOX_ID);
        }

        function serialNumberBoxIsActive() {
            return common.ui.boxIsActive(pickpack.constants.SERIAL_NO_BOX_ID);
        }

        function infoBoxIsActive() {
            return common.ui.boxIsActive(pickpack.constants.INFO_BOX_ID);
        }

        function notifyOrderComplete() {
            // Chime
            pickpack.globals.soundController.playOrderCompleteSound();

            // Options for big green
            var fps;

            if (pickpack.globals.optionController.useFade) {
                fps = 25.0;
            }
            else {
                fps = 1.0;
            }

            // Flash big green
            var fade_out_options = {from: 0.75,
                                    to: 0.0,
                                    delay: 0.6,
                                    queue: "break",
                                    fps: fps,
                                    duration: 2.6};
            var fade_out = function () {
                MochiKit.Visual.fade("big_green", fade_out_options);
            };
            var fade_in_options = {from: 0.0,
                                   to: 0.75,
                                   duration: 0.4,
                                   delay: 0.4, // To sync with the sound
                                   queue: "break",
                                   fps: fps,
                                   transition: MochiKit.Visual.Transitions.parabolic,
                                   afterFinish: fade_out};
            MochiKit.Visual.appear("big_green", fade_in_options);
        }

        var isGreen = MochiKit.Base.partial(MochiKit.Base.operator.seq, pickpack.constants.STATUS_GREEN);
        var isYellow = MochiKit.Base.partial(MochiKit.Base.operator.seq, pickpack.constants.STATUS_YELLOW);
        var isRed = MochiKit.Base.partial(MochiKit.Base.operator.seq, pickpack.constants.STATUS_RED);
        var isGray = MochiKit.Base.partial(MochiKit.Base.operator.seq, pickpack.constants.STATUS_GRAY);
        var isBlank = MochiKit.Base.partial(MochiKit.Base.operator.seq, pickpack.constants.STATUS_BLANK);

        function getCurrentRowElement() {
            return MochiKit.DOM.getFirstElementByTagAndClassName("tr", "highlight", "pkpk_list_div");
        }

        function allowNextOrder() {
            var status = readInt(MochiKit.DOM.getElement("order_status"));
            return (isGreen(status) || isBlank(status));
        }

        function isOrderGreen() {
            var status = readInt(MochiKit.DOM.getElement("order_status"));
            return isGreen(status);
        }

        function isOrderBlank() {
            var status = readInt(MochiKit.DOM.getElement("order_status"));
            return isBlank(status);
        }

        function isSerializedItem(row_element) {
            var serialized = getFieldIntValue("pkpk_serialized", row_element);
            var is_serialized;

            if (serialized === pickpack.constants.DB_FALSE) {
                is_serialized = false;
            }
            else if (serialized === pickpack.constants.DB_TRUE) {
                is_serialized = true;
            }
            else {
                pickpack.error.throwApplicationError("System error 27900");
            }
            return is_serialized;
        }

        // These functions are the starting points of the asynchronous
        // processing and the callback chain.
        function processUserInput() {

            validateUserId();

            var userInput = pickpack.globals.inputBuffer.readAndReset();

            if (serialNumberBoxIsActive()) {
                processPossibleSerialNumber(userInput);
                return;
            }

            if (!userInput) {
                // Empty string, null, or undefined: we're done here.
                return;
            }

            // No changes allowed if there is an error or info box active.
            guardInfoBoxOrErrorBoxIsActive();

            // Decide if it's an item number, an order number, or a UPC.
            if (pickpack.regex.looksLikeUPC(userInput)) {
                // It's a UPC
                handleItemScan(userInput, pickpack.constants.INCREMENT_BY_UPC);
            }
            else if (!pickpack.regex.looksLikeOrderNumber(userInput)) {
                // It's not an order number; it must be an item number.
                //
                // Note: this case catches all Harper item scans. The
                // handleItemScan() function parses those Harper labels.
                handleItemScan(userInput, pickpack.constants.INCREMENT_BY_ITEM_NO);
            }
            else if (isOrderGreen()) {
                // It could be an order number or an item number. The
                // current order is complete (green), so assume it's an
                // order number.
                handleOrderIdScan(userInput);
            }
            else if (isOrderBlank()) {
                // It could be an order number or an item number. The
                // current order status is blank.
                if (countRowsByItem(userInput) === 0) {
                    // Currently, there are no rows with this item number.
                    // Assume it's an order number.
                    handleOrderIdScan(userInput);
                }
                else {
                    // The user input is an item number on the current
                    // order, so assume the user input is an item number.
                    handleItemScan(userInput, pickpack.constants.INCREMENT_BY_ITEM_NO);
                }
            }
            else {
                // It could be an order number or an item number. The
                // current order is not green or blank, so assume it's an
                // item number.
                handleItemScan(userInput, pickpack.constants.INCREMENT_BY_ITEM_NO);
            }
        }

        function processPossibleSerialNumber(userInput) {
            // No changes allowed if the order is already complete, or if there
            // is an error or info box active.
            guardNoChangesAllowed();

            pickpack.globals.serializedItemContainer.processPossibleSerialNumber(userInput);
        }

        // Export symbols to namespace
        var ns = pickpack.ui;
        ns.fillTable = fillTable;
        ns.handleOrderIdScan = handleOrderIdScan;
        ns.incrementRowCountByRowId = incrementRowCountByRowId;
        ns.getRowItemNumber = getRowItemNumber;
        ns.doEscape = doEscape;
        ns.resetUserId = resetUserId;
        ns.dismissConfigPane = dismissConfigPane;
        ns.showConfigPane = showConfigPane;
        ns.dismissHelpPane = dismissHelpPane;
        ns.showHelpPane = showHelpPane;
        ns.hideSerialNumberBox = hideSerialNumberBox;
        ns.showSerialNumberBox = showSerialNumberBox;
        ns.hideInfoBox = hideInfoBox;
        ns.showInfoBox = showInfoBox;
        ns.showInfoBoxWithDomElements = showInfoBoxWithDomElements;
        ns.showOrderNotesOnDemand = showOrderNotesOnDemand;
        ns.focusFirstInvalidRow = focusFirstInvalidRow;
        ns.getElementId = getElementId;
        ns.getElementValue = getElementValue;
        ns.setElementValue = setElementValue;
        ns.postAlert = postAlert;
        ns.postAlertWithTraceback = postAlertWithTraceback;
        ns.toggleErrorDetail = toggleErrorDetail;
        ns.clearBox = clearBox;
        ns.noModalPane = noModalPane;
        ns.noModalPaneOrSerialNumberBox = noModalPaneOrSerialNumberBox;
        ns.guardInfoBoxOrErrorBoxIsActive = guardInfoBoxOrErrorBoxIsActive;
        ns.optionsPaneIsActive = optionsPaneIsActive;
        ns.helpPaneIsActive = helpPaneIsActive;
        ns.alertBoxIsActive = alertBoxIsActive;
        ns.infoBoxIsActive = infoBoxIsActive;
        ns.notifyOrderComplete = notifyOrderComplete;
        ns.findRowsByItem = findRowsByItem;
        ns.processUserInput = processUserInput;
        ns.getRowCurrentQuantity = getRowCurrentQuantity;
        ns.getRowExpectedQuantity = getRowExpectedQuantity;
        ns.buildImagePath = buildImagePath;
        ns.formatOrderIdScanForDisplay = formatOrderIdScanForDisplay;
        ns.displayUserId = displayUserId;
        ns.doInitialPageRendering = doInitialPageRendering;
        ns.getOrderNumberAndGeneration = getOrderNumberAndGeneration;

        ns.doUpArrow = doUpArrow;
        ns.doDownArrow = doDownArrow;
        ns.doLeftArrow = doLeftArrow;
        ns.doRightArrow = doRightArrow;
        ns.doPlus = doPlus;
        ns.doMinus = doMinus;
        ns.isGreen = isGreen;
        //ns.isYellow = isYellow;
        //ns.isRed = isRed;
        //ns.isGray = isGray;
        //ns.isBlank = isBlank;
    }
()); // End of function (closure). Now invoke it.
