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

if (pickpack.globals) {
    throw new Error("pickpack.globals already exists");
}
else {
    pickpack.globals = {};
}


(
    function () {
        'use strict';

        var ns = pickpack.globals;

        function instantiateGlobalUtilityObjects() {
            ns.inputBuffer = pickpack.utility_objects.inputBufferFactory();
            ns.waitSpinnerController = pickpack.utility_objects.waitSpinnerControllerFactory();
            ns.soundController = pickpack.utility_objects.soundControllerFactory();
            ns.optionController = pickpack.utility_objects.optionControllerFactory();
            ns.specialKeysLogger = null;
            ns.serializedItemContainer = null;
            ns.itemNotesHandler = null;
            ns.orderNotesHandler = null;
        }
        ns.instantiateGlobalUtilityObjects = instantiateGlobalUtilityObjects;
    }
()); // End of function (closure). Now invoke it.
