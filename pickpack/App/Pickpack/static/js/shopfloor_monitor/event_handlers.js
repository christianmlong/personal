/*
 * event_handlers.js: Event handlers for the client-side JavaScript for the
 * Shop Floor Monitor application.
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

if (shopfloor_monitor.event_handlers) {
    throw new Error("shopfloor_monitor.event_handlers already exists");
}
else {
    shopfloor_monitor.event_handlers = {};
}


(
    function () {
        'use strict';

        function _onLoad(mkEvent) {
            // Silence the "'mkEvent' is defined but never used." warning
            /* jshint unused: false */

            // Now that the page has been loaded, connect our other event
            // handlers.
            MochiKit.Signal.connect(window, "onhelp", handleWindowOnHelp);
            MochiKit.Signal.connect(document, "onkeydown", handleOnKeyDown);
            MochiKit.Signal.connect(document, "onkeypress", handleOnKeyPress);
            MochiKit.Signal.connect("data_display", "onchange", handleOptionChange);
            MochiKit.Signal.connect("data_display", "onkeyup", handleSelectKeyUp);
            MochiKit.Signal.connect("show_until", "onchange", handleOptionChange);
            MochiKit.Signal.connect("show_backorder", "onchange", handleOptionChange);
            MochiKit.Signal.connect("ready_to_pick_highlight", "onchange", handleOptionChange);
            MochiKit.Signal.connect(shopfloor_monitor.constants.ONE_UP_CANVAS_ID, "onclick", handleCanvasOnClick);

            // Create global objects
            shopfloor_monitor.globals.instantiateGlobalUtilityObjects();

            // Fetch initial data
            getOrderSummaryDataInResponseToApplicationEvent();

            // Create a random additional padding so that different clients
            // refresh at slightly different rates.
            var random_padding = Math.round(Math.random() * 4000);

            // Refresh the data every few seconds. Note that the server caches
            // data for thirty seconds, so not every data refresh will get new
            // data. I leave the refresh here at fifteen seconds so that the
            // total delay from database to display will not exceed 45 seconds.
            setInterval(getOrderSummaryDataInResponseToApplicationEvent,
                        (shopfloor_monitor.constants.REFRESH_RATE * 1000) + random_padding);
        }

        function _windowOnHelp(mkEvent) {
            // Stop IE from popping up its own help screen.
            // http://stackoverflow.com/questions/3405412/internet-explorer-or-any-browser-f1-keypress-displays-your-own-help
            mkEvent.stop();
            return false;
        }

        function _onKeyDown(mkEvent) {
            var key_string = mkEvent.key().string;
            if (aModifierWasPressed(mkEvent)) {
                return;
            }
            if (!shopfloor_monitor.globals.waitSpinnerController.respondToUserInput()) {
                // Let keyDown events like F5 continue bubbling up, so the
                // browser can get them. Don't call mkEvent.stop() here.
                return;
            }
            if (shopfloor_monitor.ui.optionsPaneIsActive()) {
                switch (key_string) {
                case "KEY_F4":
                    mkEvent.stop();
                    shopfloor_monitor.ui.dismissConfigPane();
                    // No need to run the next switch statememnt
                    return;
                }
            }
            else if (shopfloor_monitor.ui.helpPaneIsActive()) {
                switch (key_string) {
                case "KEY_F1":
                    mkEvent.stop();
                    shopfloor_monitor.ui.dismissHelpPane();
                    // No need to run the next switch statememnt
                    return;
                }
            }
            else if (shopfloor_monitor.ui.noModalPane()) {
                switch (key_string) {
                case "KEY_F1":
                    mkEvent.stop();
                    shopfloor_monitor.ui.showHelpPane();
                    break;
                case "KEY_F4":
                    mkEvent.stop();
                    shopfloor_monitor.ui.showConfigPane();
                    break;
                }
            }
        }

        function _onKeyPress(mkEvent) {
            var key_string = mkEvent.key().string;
            var key_upper;
            var key_array;
            if (!shopfloor_monitor.globals.waitSpinnerController.respondToUserInput()) {
                mkEvent.stop();
                return;
            }
            if (shopfloor_monitor.ui.aBoxIsActive()) {
                switch (key_string) {
                case " ":
                    mkEvent.stop();
                    shopfloor_monitor.ui.clearBox();
                    //break;
                    // No need to run the next tests
                    return;
                }
            }
            else {
                key_array = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "S", "B"];
                key_upper = key_string.toUpperCase();
                if (common.utility_functions.arrayContainsElement(key_array, key_upper)) {
                    mkEvent.stop();
                    // Set the options
                    shopfloor_monitor.ui.setOptionsByShortcut(key_upper);
                    // Refresh the data
                    getOrderSummaryDataInResponseToUserInput();
                }
            }
        }

        function _optionChange(mkEvent) {
            // Silence the "'mkEvent' is defined but never used." warning
            /* jshint unused: false */

            if (!shopfloor_monitor.globals.waitSpinnerController.respondToUserInput()) {
                mkEvent.stop();
                return;
            }
            if (shopfloor_monitor.ui.optionsPaneIsActive()) {
                // Write the user preferences to a cookie.
                shopfloor_monitor.globals.optionController.saveOptionValuesToCookie();
                // Refresh the data
                getOrderSummaryDataInResponseToUserInput();
            }
        }

        function _canvasOnClick(mkEvent) {
            if (!shopfloor_monitor.globals.waitSpinnerController.respondToUserInput()) {
                mkEvent.stop();
                return;
            }
            if (shopfloor_monitor.ui.aBoxIsActive()) {
                // No need to run the next tests
                return;
            }

            //MochiKit.Logging.log("Click handled");

            var client_coordinates = mkEvent.mouse().client;
            var rect = MochiKit.DOM.getElement(shopfloor_monitor.constants.ONE_UP_CANVAS_ID).getBoundingClientRect();
            var canvas_x = client_coordinates.x - rect.left;
            //var canvas_y = client_coordinates.y - rect.top;

            var t_min = 0;
            var t_max = t_min + shopfloor_monitor.constants.ONE_UP_BAR_WIDTH;
            var ss_min = t_max + shopfloor_monitor.constants.ONE_UP_BAR_GAP;
            var ss_max = ss_min + shopfloor_monitor.constants.ONE_UP_BAR_WIDTH;
            var s_min = ss_max + shopfloor_monitor.constants.ONE_UP_BAR_GAP;
            var s_max = s_min + shopfloor_monitor.constants.ONE_UP_BAR_WIDTH;
            var n_min = s_max + shopfloor_monitor.constants.ONE_UP_BAR_GAP;
            var n_max = n_min + shopfloor_monitor.constants.ONE_UP_BAR_WIDTH;

            var bar_index;

            if (canvas_x > t_min && canvas_x < t_max) {
                bar_index = 0;
            }
            else if (canvas_x > ss_min && canvas_x < ss_max) {
                bar_index = 1;
            }
            else if (canvas_x > s_min && canvas_x < s_max) {
                bar_index = 2;
            }
            else if (canvas_x > n_min && canvas_x < n_max) {
                bar_index = 3;
            }

            if (bar_index !== undefined) {
                // Show the order info to the user
                //MochiKit.Logging.log("Bar " + bar_index + " clicked");
                getListOfOrderNumbers(bar_index);
            }

        }

        function _orderNumberSpanOnClick(mkEvent) {
            if (!shopfloor_monitor.globals.waitSpinnerController.respondToUserInput()) {
                mkEvent.stop();
                return;
            }

            var order_number_display;
            var order_number_and_generation;
            var order_number;
            var order_generation;
            order_number_display = MochiKit.DOM.getElement(mkEvent.src()).innerHTML;

            if (order_number_display !== undefined) {
                order_number_and_generation = common.utility_functions.parseOrderNumberAndGenerationFromDisplay(order_number_display);
                order_number = order_number_and_generation[0];
                order_generation = order_number_and_generation[1];
                getOrderNumberDetailData(order_number,
                                         order_generation);
            }

        }

        function _selectKeyUp(mkEvent) {
            var key_string = mkEvent.key().string;
            if (shopfloor_monitor.ui.optionsPaneIsActive()) {
                if ((key_string === "KEY_ARROW_UP") ||
                    (key_string === "KEY_ARROW_DOWN") ||
                    (key_string === "KEY_ARROW_RIGHT") ||
                    (key_string === "KEY_ARROW_LEFT")) {
                    MochiKit.Signal.signal(mkEvent.src(), "onchange");
                }
            }
        }

        function aModifierWasPressed(mkEvent) {
            var modifiers = mkEvent.modifier();
            if (modifiers.any) {
                return true;
            }
            else {
                return false;
            }
        }

        function getOrderSummaryDataInResponseToApplicationEvent() {
            // When the application requests data, we don't show the wait
            // spinner.
            var request_object = shopfloor_monitor.server.getOrderSummaryData(shopfloor_monitor.globals.waitSpinnerController.doneWaiting);
            shopfloor_monitor.globals.waitSpinnerController.startWaitingForAppXHR(request_object);
        }

        function getOrderSummaryDataInResponseToUserInput() {
            // When the user requests data, we do show the wait spinner, after a
            // 500 ms delay.
            var request_object = shopfloor_monitor.server.getOrderSummaryData(shopfloor_monitor.globals.waitSpinnerController.doneWaiting);
            shopfloor_monitor.globals.waitSpinnerController.startWaitingForUserXHR(request_object);
        }

        function getListOfOrderNumbers(bar_index) {
            var request_object = shopfloor_monitor.server.getListOfOrderNumbers(bar_index,
                                                                                shopfloor_monitor.globals.waitSpinnerController.doneWaiting);
            shopfloor_monitor.globals.waitSpinnerController.startWaitingForUserXHR(request_object);
        }

        function getOrderNumberDetailData(order_number, order_generation) {
            var request_object = shopfloor_monitor.server.getOrderNumberDetailData(order_number,
                                                                                   order_generation,
                                                                                   shopfloor_monitor.globals.waitSpinnerController.doneWaiting);
            shopfloor_monitor.globals.waitSpinnerController.startWaitingForUserXHR(request_object);
        }



        var handleOnKeyDown = shopfloor_monitor.error.decorateWithErrorHandler(_onKeyDown);
        var handleOnKeyPress = shopfloor_monitor.error.decorateWithErrorHandler(_onKeyPress);
        var handleOptionChange = shopfloor_monitor.error.decorateWithErrorHandler(_optionChange);
        var handleSelectKeyUp = shopfloor_monitor.error.decorateWithErrorHandler(_selectKeyUp);
        //var handleWindowOnClick = shopfloor_monitor.error.decorateWithErrorHandler(_windowOnClick);
        var handleWindowOnHelp = shopfloor_monitor.error.decorateWithErrorHandler(_windowOnHelp);
        var handleCanvasOnClick = shopfloor_monitor.error.decorateWithErrorHandler(_canvasOnClick);

        // Export symbols to namespace
        var ns = shopfloor_monitor.event_handlers;
        ns.handleOnLoad = shopfloor_monitor.error.decorateWithErrorHandler(_onLoad);
        ns.handleOrderNumberSpanOnClick = shopfloor_monitor.error.decorateWithErrorHandler(_orderNumberSpanOnClick);
    }
()); // End of function (closure). Now invoke it.
