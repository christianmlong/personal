/*
 * error.js: Named errors for the client-side JavaScript for the Shop Floor Monitor
 * application
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
var shopfloor_monitor;

if (!shopfloor_monitor) {
    shopfloor_monitor = {};
}
else if (typeof shopfloor_monitor !== "object") {
    throw new Error("shopfloor_monitor already exists, and is not an object");
}

if (shopfloor_monitor.error) {
    throw new Error("shopfloor_monitor.error already exists");
}
else {
    shopfloor_monitor.error = {};
}

(
    function () {
        'use strict';

        // New named errors and exceptions for our application
        function SFMException(message) {
            this.name = "shopfloor_monitor.error.SFMException";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        SFMException.prototype = new Error();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        SFMException.prototype.constructor = SFMException;


        function SFMError(message) {
            this.name = "shopfloor_monitor.error.SFMError";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        SFMError.prototype = new SFMException();
        SFMError.prototype.constructor = SFMError;


        function ApplicationError(message) {
            this.name = "shopfloor_monitor.error.ApplicationError";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        ApplicationError.prototype = new SFMError();
        ApplicationError.prototype.constructor = ApplicationError;


        function ApplicationErrorWithTraceback(message,
                                               traceback) {
            this.name = "shopfloor_monitor.error.ApplicationErrorWithTraceback";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
            this.traceback = traceback;
        }
        ApplicationErrorWithTraceback.prototype = new SFMError();
        ApplicationErrorWithTraceback.prototype.constructor = ApplicationErrorWithTraceback;





        function throwApplicationError(err_msg) {
            throw new ApplicationError(err_msg);
        }

        function throwApplicationErrorWithTraceback(err_msg, traceback) {
            throw new ApplicationErrorWithTraceback(err_msg, traceback);
        }


        function handleError(ex) {

            var error_text;

            if (ex instanceof ApplicationError) {
                // This shouldn't happen. Alert, using several means so that we
                // make sure we're notified even if an error gets swallowed
                // somewhere.
                error_text = "ApplicationError " + ex.name + ":<br />" + ex.message;
                javaScriptAlert(error_text);
                throw ex;
            }
            else if (ex instanceof ApplicationErrorWithTraceback) {
                // The server issued a traceback. Append it to the webpage for
                // inspection.
                error_text = "ApplicationErrorWithTraceback " + ex.name + ":<br />" + ex.message;
                javaScriptAlertWithTraceback(error_text, ex.traceback);
                throw ex;
            }
            else if (ex instanceof Error) {
                // This shouldn't happen. Alert, using several means so that we
                // make sure we're notified even if an error gets swallowed
                // somewhere.
                error_text = "JavaScript " + ex.name + ":<br />" + ex.message;
                javaScriptAlert(error_text);

                // throw ex not working even though ex is an error. The error we
                // throw is getting swallowed by the deferred?
                throw ex;
                //throw new Error(error_text);
            }
            else {
                // Bizarre case - ex is not an Error. Can this even happen?
                error_text = "An error occurred, but no error information was received. (289)";
                javaScriptAlert(error_text);
                throw new Error(error_text);
            }
        }

        function decorateWithErrorHandler(func) {
            // Takes a function and wraps it in a try/catch block.
            var new_func =
                function (args) {
                    try {
                        func(args);
                    }
                    catch (ex) {
                        handleError(ex);
                    }
                };
            return new_func;
        }

        function javaScriptAlert(error_text) {
            // Pop up a JavaScript alert box.
            window.alert(error_text);
        }

        function javaScriptAlertWithTraceback(error_text, traceback) {
            // Pop up a JavaScript alert box. Append the server traceback to the
            // web page
            MochiKit.DOM.getElement("sfmo_debug_info").innerHTML = traceback;
            window.alert(error_text);
        }



        // Export symbols to namespace
        var ns = shopfloor_monitor.error;
        ns.throwApplicationError = throwApplicationError;
        ns.throwApplicationErrorWithTraceback = throwApplicationErrorWithTraceback;
        ns.decorateWithErrorHandler = decorateWithErrorHandler;
        ns.handleError = handleError;
    }
()); // End of function (closure). Now invoke it.
