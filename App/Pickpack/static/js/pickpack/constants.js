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
         unused: true,
         strict: true,
         trailing: true,

         browser: true

*/


// Create namespace if it does not yet exist
var pickpack;

if (!pickpack) {
    pickpack = {};
}
else if (typeof pickpack !== "object") {
    throw new Error("pickpack already exists, and is not an object");
}

if (pickpack.constants) {
    throw new Error("pickpack.constants already exists");
}
else {
    pickpack.constants = {};
}

// Define module code inside this closure, then export the symbols we want into
// the pickpack.constants namespace.
(
    function () {
        'use strict';

        var ns = pickpack.constants;

        // These are named constants with values that correspond to the data
        // coming from the database, or to file paths on the server.
        ns.STATUS_BLANK = 0;
        ns.STATUS_GRAY = 1;
        ns.STATUS_RED = 2;
        ns.STATUS_YELLOW = 3;
        ns.STATUS_GREEN = 4;
        ns.DB_FALSE = 0;
        ns.DB_TRUE = 1;
        ns.PATH_TO_IMG = "/static/img/";
        ns.IMG_EXT = ".png";
        ns.ITEMS_TABLE_ID = "table_of_items";
        ns.ORDER_NOTES_TABLE_ID = "table_of_order_notes";
        ns.OPTIONS_PANE_ID = "pkpk_options_pane";
        ns.HELP_PANE_ID = "pkpk_help_pane";
        ns.ERROR_BOX_ID = "pkpk_error_box";
        ns.ERROR_TEXT_ID = "pkpk_error_text";
        ns.ERROR_TRACEBACK_ID = "pkpk_error_traceback";
        ns.ERROR_TOGGLE_DIV_ID = "pkpk_error_toggle_div";
        ns.ERROR_TOGGLE_TEXT_ID = "pkpk_error_toggle_text";
        ns.SERIAL_NO_BOX_ID = "pkpk_serial_no_box";
        ns.SERIAL_NO_TEXT_ID = "pkpk_serial_no_text";
        ns.INFO_BOX_ID = "pkpk_info_box";
        ns.INFO_BOX_BODY_ID = "pkpk_info_body";

        // These are named constants with arbitrary unique values.
        ns.ARROW_UP = 210;
        ns.ARROW_DOWN = 211;
        ns.ARROW_LEFT = 212;
        ns.ARROW_RIGHT = 213;
        ns.F2_KEY = 214;
        ns.PLUS_KEY = 215;

        ns.ITS_AN_ITEM = 230;
        ns.ITS_AN_ORDER = 231;

        ns.INCREMENT_BY_ITEM_NO = 232;
        ns.INCREMENT_BY_UPC = 233;
    }
()); // End of function (closure). Now invoke it.
