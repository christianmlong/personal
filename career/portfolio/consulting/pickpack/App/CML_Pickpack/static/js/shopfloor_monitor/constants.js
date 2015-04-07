/*
 * constants.js: Constants for the client-side JavaScript for the Pick Pack
 * application
 *
 */

/*
 * jshint declarations
 *
 */

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

if (shopfloor_monitor.constants) {
    throw new Error("shopfloor_monitor.constants already exists");
}
else {
    shopfloor_monitor.constants = {};
}

// Define module code inside this closure, then export the symbols we want into
// the shopfloor_monitor.constants namespace.
(
    function () {
        'use strict';

        var ns = shopfloor_monitor.constants;

        ns.OPTIONS_PANE_ID = "sfmo_options_pane";
        ns.HELP_PANE_ID = "sfmo_help_pane";
        ns.ERROR_BOX_ID = "sfmo_error_box";
        ns.ERROR_TEXT_ID = "sfmo_error_text";
        ns.INFO_BOX_ID = "sfmo_info_box";
        ns.INFO_BOX_BODY_ID = "sfmo_info_body";
        ns.ORDER_DETAIL_BOX_ID = "sfmo_order_detail_box";
        ns.ORDER_DETAIL_BOX_BODY_ID = "sfmo_order_detail_body";
        ns.ORDER_DETAIL_TABLE_ID = "order_detail_table";
        ns.WAITSPINNER_CONTAINER_ID = "waitspinner_container";
        ns.WAITSPINNER_CANVAS_ID = "waitspinner_canvas";
        ns.ONE_UP_CANVAS_ID = "sfmo_canvas_1up";
        ns.PATH_TO_IMG = "/static/img/shopfloor_monitor";
        ns.IMG_EXT = ".png";
        ns.LABEL_TODAY = "Ship Today";
        ns.LABEL_TOMORROW = "Ship Tomorrow";
        ns.LABEL_HOLD = "On Hold";
        ns.LABEL_BACKORDER = "Backorders";
        ns.LABEL_READY_TO_PRINT = "Ready To Print";
        ns.LABEL_PICKSLIP_PRINTED = "Pick Slip Printed";
        ns.LABEL_PACKED = "Packed - On track";
        ns.TODAY_SURE = "Today Sure";
        ns.SIGNATURE_SERVICE = "Signature Service";
        ns.SERVICE_FILE = "Service File";
        ns.NORMAL = "Normal";
        ns.SHOW_UNTIL_PACKING_BENCH = "packing_bench";
        ns.SHOW_UNTIL_SCALE = "scale";
        ns.READY_HIGHLIGHT_NONE = "no_highlight";
        ns.READY_HIGHLIGHT_BUG = "bug";
        ns.READY_HIGHLIGHT_STRIPE = "stripe";

        ns.ONE_UP_BAR_WIDTH = 150;
        ns.ONE_UP_BAR_GAP = 110;

        // TO DO debug only
        ns.REFRESH_RATE = 15;   // Seconds
        //ns.REFRESH_RATE = 1500;   // Seconds

        ns.WORKSTATIONS = {
            wcc : 1000,
            parts : 1001,
            both : 1002,
            all : 1003
        };

        ns.WORKSTATION_CAPTIONS = {
            "wcc" : "CN",
            "parts" : "SV",
            "both" : "AP",
            "all" : "All"
        };





    }
()); // End of function (closure). Now invoke it.
