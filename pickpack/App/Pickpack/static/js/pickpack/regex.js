/*
 * regex.js: Functions that deal with regular expressions for
 * the client-side JavaScript for the Pick Pack application.
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

if (pickpack.regex) {
    throw new Error("pickpack.regex already exists");
}
else {
    pickpack.regex = {};
}


(
    function () {
        'use strict';

        function looksLikeUPC(input) {
            var UPCPattern = /^(?:648484|582839|720949|190993|379222|118082)\d{6}$/;
            var inputStr = String(input);
            return UPCPattern.test(inputStr);
        }

        function looksLikeOrderNumber(input) {
            var OrderNumberPattern = /^[A-Za-z0-9]{5}[0-9]{2}$/;
            var inputStr = String(input);
            return OrderNumberPattern.test(inputStr);
        }

        function looksLikeSerialNumber(input) {
            // Any alpha-numeric, with dashes and underscores
            // 10-30 characters long
            var SerialNumberPattern = /^[A-Za-z0-9_-]{10,30}$/;
            var inputStr = String(input);
            return SerialNumberPattern.test(inputStr);
        }

        function checkForHarperItemNumber(input) {
            // Checks if value looks like a scan of a barcode off of a Harper
            // item number label. Those Harper item label barcodes look like
            // this: "1 10N022". They have an item quantity, then a space, then
            // the Harper item number.
            //
            // If a Harper label is found, we strip off the leading quantity
            // digits, and return just the item number. If not, we return the
            // value unchanged.
            var HarperItemNumberPattern = /^[1-9]\d{0,2} ([A-Z0-9\-]{4,10})$/;
            var inputStr = String(input);
            var matchResult = HarperItemNumberPattern.exec(inputStr);

            if (matchResult === null) {
                // If we didn't find the pattern, return the original value
                // (busted to a string).
                return inputStr;
            }
            else {
                // We found a Harper item label. Return just the item number.
                return matchResult[1];
            }
        }

        function allowedLabelCharacter(input) {
            var LabelCharacterPattern = /^[A-Za-z0-9_\- ]$/;
            var inputStr = String(input);
            return LabelCharacterPattern.test(inputStr);
        }

        function allowedUserId(input) {
            var UserIdPattern = /^\w{3}$/;
            var inputStr = String(input);

            if (inputStr === "") {
                // We allow blank user id.
                return true;
            }
            else {
                return UserIdPattern.test(inputStr);
            }
        }

        // Export symbols to namespace
        var ns = pickpack.regex;
        ns.looksLikeUPC = looksLikeUPC;
        ns.looksLikeOrderNumber = looksLikeOrderNumber;
        ns.looksLikeSerialNumber = looksLikeSerialNumber;
        ns.checkForHarperItemNumber = checkForHarperItemNumber;
        ns.allowedLabelCharacter = allowedLabelCharacter;
        ns.allowedUserId = allowedUserId;
    }
()); // End of function (closure). Now invoke it.
