/*
 * error.js: Common error functions
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

         browser: true,
         laxcomma: true

*/


// Create namespace if it does not yet exist
var common;

if (!common) {
    common = {};
}
else if (typeof common !== "object") {
    throw new Error("common already exists, and is not an object");
}

if (common.error) {
    throw new Error("common.error already exists");
}
else {
    common.error = {};
}


(
    function () {
        'use strict';

        function throwError(err_msg) {
            throw new Error(err_msg);
        }

        // Export symbols to namespace
        var ns = common.error;
        ns.throwError = throwError;

    }
()); // End of function (closure). Now invoke it.
