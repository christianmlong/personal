/*
 * utility_functions.js:Utility functions for
 * the client-side JavaScript for the Pick Pack application.
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit */

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
var common;

if (!common) {
    common = {};
}
else if (typeof common !== "object") {
    throw new Error("common already exists, and is not an object");
}

if (common.utility_functions) {
    throw new Error("common.utility_functions already exists");
}
else {
    common.utility_functions = {};
}


(
    function () {
        'use strict';

        function pythonStyleMod(a, b) {
            // Implements modulus division the way Python does it: -1%5 === 4.
            // In JavaScript, -1%5 === -1.
            if (b === 0) {
                return NaN;
            }
            var mod = a % b;
            if (mod < 0) {
                // Negative result? Add the divisor.
                // (-1%5)+5=4   Just like Python, ahhhh
                mod += b;
            }
            return mod;
        }

        function integerInRange(value, low, high) {
            if (typeof value !== "number") {
                common.error.throwApplicationError("Invalid number: " + value);
            }
            if ((value >= low) && (value <= high)) {
                return true;
            }
            else {
                return false;
            }
        }

        function trim(str) {
            // trim() is only supported on Firefox 3.5 and later. Some of our
            // older thin clients are running Firefox 2 (IceWeasel)
            return str.replace(/^\s+|\s+$/g, "");
            //return str.replace(/^\s\s*/, "").replace(/\s\s*$/, "");
        }

        function smarterBooleanConversion(valueToConvert) {
            var returnValue;
            if (typeof valueToConvert === "string") {
                if (valueToConvert === "true") {
                    returnValue = true;
                }
                else if (valueToConvert === "false") {
                    returnValue = false;
                }
                else {
                    common.error.throwApplicationError("Invalid string: " + valueToConvert);
                }
            }
            else if (typeof valueToConvert === "number") {
                if (valueToConvert === 1) {
                    returnValue = true;
                }
                else if (valueToConvert === 0) {
                    returnValue = false;
                }
                else {
                    common.error.throwApplicationError("Invalid number: " + valueToConvert);
                }
            }
            else if (typeof valueToConvert === "boolean") {
                returnValue = valueToConvert;
            }
            else {
                common.error.throwApplicationError("Invalid object of type: " + typeof valueToConvert);
            }
            return returnValue;
        }

        function failIf(assertion, msg) {
            if (assertion !== false) {
                common.error.throwApplicationError(msg);
            }
        }

        function assert(assertion, msg) {
            if (assertion !== true) {
                common.error.throwApplicationError(msg);
            }
        }

        function replaceBrWithNewline(input) {
            // Replace XHTML <br /> tags with regular newlines (\n). Used when
            // displaying an HTML error message in a JavaScript alert box.
            return input.replace(/<br \/>/g, "\n");
        }

        function replaceNewlineWithBr(input) {
            // Replace newlines (\n and \r\n) with XHTML <br /> tags. Used when
            // displaying multi-line notes on an XHTML page.
            return input.replace(/\r?\n/g, common.ui.htmlBreakTag());
        }

        function wrapScalarValue(input) {
            // Sometimes we handle input that can be scalar (interger, string,
            // etc.) or vector (array). This function wraps scalar values up
            // inside an array.
            if (typeof input === "boolean" ||
                typeof input === "number" ||
                typeof input === "string") {
                return [input];
            }
            else {
                return input;
            }
        }

        function arrayContainsElement(arr, possible_element) {
            // Returns true if the array contains the element. Returns false
            // otherwise.
            return MochiKit.Base.findValue(arr, possible_element) !== -1;
        }

        function startsWith(targetString, searchString) {
            // Returns true if targetString begins with searchString. False
            // otherwise.
            return targetString.lastIndexOf(searchString, 0) === 0;
        }

        function parseOrderNumberAndGenerationFromDisplay(formatted_data) {
            // Get order number and generation back out of the display format.
            //
            // POSSIBLE IMPROVEMENT
            // Use a global variable instead of using the DOM for data storage.
            var formatted_elements = formatted_data.split("/");
            var order_number = formatted_elements[0];
            var order_generation = formatted_elements[1];

            if (typeof order_generation !== "string") {
                common.error.throwError("System error 29600 - order generation is not a string. " + typeof order_generation);
            }

            var parsed_elements = [];
            parsed_elements[0] = order_number;
            parsed_elements[1] = parseInt(order_generation);
            return parsed_elements;
        }

        function parseOrderNumberAndGenerationFromScan(order_id_scan) {
            // Get order number and generation back out of the scanned barcode format.
            //
            // POSSIBLE IMPROVEMENT
            // Make an order_id object to group all this parsing and formatting.

            if (typeof order_id_scan !== "string") {
                common.error.throwError("System error 29605 - order_id_scan is not a string. " + typeof order_id_scan);
            }

            order_id_scan = common.utility_functions.trim(order_id_scan);

            if (order_id_scan.length !== 7) {
                common.error.throwError("System error 29610 - " + order_id_scan + " is not a valid input. ");
            }

            var parsed_elements = [];
            parsed_elements[0] = order_id_scan.substring(0, 5);
            parsed_elements[1] = parseInt(order_id_scan.substring(5, 7));
            return parsed_elements;
        }

        function formatOrderNumberAndGenerationForDisplay(order_number, order_generation) {
            var text_order_generation;

            if (typeof order_generation !== "number") {
                common.error.throwError("System error 29400 - order generation is not a number. " + typeof order_generation);
            }

            if (order_generation >= 0 &&
                order_generation < 10) {
                text_order_generation = "0" + order_generation.toString();
            }
            else {
                text_order_generation = order_generation.toString();
            }

            if (text_order_generation.length !== 2) {
                common.error.throwError("System error 29500 - order generation is not two characters long. " + text_order_generation);
            }

            return order_number + "/" + text_order_generation;
        }

        // Export symbols to namespace
        var ns = common.utility_functions;
        ns.pythonStyleMod = pythonStyleMod;
        ns.integerInRange = integerInRange;
        ns.trim = trim;
        ns.smarterBooleanConversion = smarterBooleanConversion;
        ns.failIf = failIf;
        ns.assert = assert;
        ns.replaceBrWithNewline = replaceBrWithNewline;
        ns.replaceNewlineWithBr = replaceNewlineWithBr;
        ns.wrapScalarValue = wrapScalarValue;
        ns.arrayContainsElement = arrayContainsElement;
        ns.startsWith = startsWith;
        ns.parseOrderNumberAndGenerationFromDisplay = parseOrderNumberAndGenerationFromDisplay;
        ns.parseOrderNumberAndGenerationFromScan = parseOrderNumberAndGenerationFromScan;
        ns.formatOrderNumberAndGenerationForDisplay = formatOrderNumberAndGenerationForDisplay;

    }
()); // End of function (closure). Now invoke it.
