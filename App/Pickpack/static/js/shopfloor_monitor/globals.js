/*
 * globals.js: Globals for the client-side JavaScript for the Pick Pack
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

if (shopfloor_monitor.globals) {
    throw new Error("shopfloor_monitor.globals already exists");
}
else {
    shopfloor_monitor.globals = {};
}


(
    function () {
        'use strict';

        var ns = shopfloor_monitor.globals;

        function instantiateGlobalUtilityObjects() {
            ns.waitSpinnerController = shopfloor_monitor.utility_objects.waitSpinnerControllerFactory();
            ns.optionController = shopfloor_monitor.utility_objects.optionControllerFactory();
        }
        ns.instantiateGlobalUtilityObjects = instantiateGlobalUtilityObjects;
    }
()); // End of function (closure). Now invoke it.
