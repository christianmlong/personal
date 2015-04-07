/*
 * utility_functions.js: Useful functions for the Shopfloor Monitor
 *
 */

/*
 * jshint declarations
 *
 */

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

if (shopfloor_monitor.utility_functions) {
    throw new Error("shopfloor_monitor.utility_functions already exists");
}
else {
    shopfloor_monitor.utility_functions = {};
}


(
    function () {
        'use strict';

        function getCurrentCaption() {
            return shopfloor_monitor.constants.WORKSTATION_CAPTIONS[shopfloor_monitor.globals.optionController.dataDisplay];
        }

        function omitDate(the_date, the_time) {
            // Combine the date and time in to one string. If the date is today,
            // omit it.

            var today_as_date = new Date();

            // Radix for parseInt
            var base_ten = 10;

            // getMonth is zero-based, and getDate is one-based o_O
            var today_as_string = (
                parseInt((today_as_date.getMonth() + 1), base_ten).toString() + "/" +
                parseInt(today_as_date.getDate(), base_ten).toString() + "/" +
                parseInt(today_as_date.getFullYear(), base_ten).toString()
            );

            if (the_date === today_as_string) {
                return the_time;
            }
            else {
                return the_date + common.constants.NBSP + the_time;
            }
        }

        //function testCancelDeferred() {
        //    // TO DO debug only
        //    var requestFields = ["scale",
        //                         "show_backorder"];
        //    var requestValues = ["wcc",
        //                         "true"];
        //    var deferred = MochiKit.Async.doSimpleXMLHttpRequest("/shopfloor_monitor/j_status_orders",
        //                                                     requestFields,
        //                                                     requestValues);
        //    deferred.addCallback(showAlert);
        //
        //    MochiKit.Async.callLater(2, MochiKit.Base.bind(deferred.cancel, deferred));
        //
        //    return deferred;
        //}
        //
        //function showAlert() {
        //    MochiKit.Logging.log("Callback called.");
        //    // shopfloor_monitor.utility_functions.testCancelDeferred()
        //}
        //
        //function showAlertCallback(alert_text, result_of_previous_callback) {
        //    MochiKit.Logging.log(alert_text);
        //    return result_of_previous_callback;
        //}

        // Export symbols to namespace
        var ns = shopfloor_monitor.utility_functions;
        ns.getCurrentCaption = getCurrentCaption;
        ns.omitDate = omitDate;
        //ns.testCancelDeferred = testCancelDeferred;
        //ns.showAlertCallback = showAlertCallback;
    }
()); // End of function (closure). Now invoke it.
