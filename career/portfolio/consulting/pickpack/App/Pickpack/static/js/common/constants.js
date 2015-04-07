/*
 * constants.js: Common constants for the client-side JavaScript
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
var common;

if (!common) {
    common = {};
}
else if (typeof common !== "object") {
    throw new Error("common already exists, and is not an object");
}

if (common.constants) {
    throw new Error("common.constants already exists");
}
else {
    common.constants = {};
}

// Define module code inside this closure, then export the symbols we want into
// the common.constants namespace.
(
    function () {
        'use strict';

        var ns = common.constants;

        // These are named constants with values that correspond to the data
        // coming from the database, or to file paths on the server.
        ns.NO_DATA_FOUND = "NO_DATA_FOUND";
        ns.NBSP = "\u00a0";
        ns.BULLET_POINT = "\u2022";
    }
()); // End of function (closure). Now invoke it.
