/*
 * error.js: Named errors for the client-side JavaScript for the Pick Pack
 * application
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

if (pickpack.error) {
    throw new Error("pickpack.error already exists");
}
else {
    pickpack.error = {};
}

(
    function () {
        'use strict';

        // New named errors and exceptions for our application
        function PickPackException(message) {
            this.name = "pickpack.error.PickPackException";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        PickPackException.prototype = new Error();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        PickPackException.prototype.constructor = PickPackException;


        function PickPackError(message) {
            this.name = "pickpack.error.PickPackError";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        PickPackError.prototype = new PickPackException();
        PickPackError.prototype.constructor = PickPackError;


        function HandleableError(message) {
            this.name = "pickpack.error.HandleableError";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        HandleableError.prototype = new PickPackError();
        HandleableError.prototype.constructor = HandleableError;


        function ApplicationError(message) {
            this.name = "pickpack.error.ApplicationError";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        ApplicationError.prototype = new PickPackError();
        ApplicationError.prototype.constructor = ApplicationError;


        function ApplicationErrorWithTraceback(message,
                                               traceback) {
            this.name = "pickpack.error.ApplicationErrorWithTraceback";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
            this.traceback = traceback;
        }
        ApplicationErrorWithTraceback.prototype = new PickPackError();
        ApplicationErrorWithTraceback.prototype.constructor = ApplicationErrorWithTraceback;


        function InfoException(message) {
            this.name = "pickpack.error.InfoException";
            if (!message) {
                message = "No error message";
            }
            this.message = message;
        }
        InfoException.prototype = new PickPackException();
        InfoException.prototype.constructor = InfoException;



        function throwHandleableError(err_msg) {
            throw new HandleableError(err_msg);
        }

        function throwApplicationError(err_msg) {
            throw new ApplicationError(err_msg);
        }

        function throwApplicationErrorWithTraceback(err_msg, traceback) {
            throw new ApplicationErrorWithTraceback(err_msg, traceback);
        }

        function throwInfoException(err_msg) {
            throw new InfoException(err_msg);
        }

        function handleError(ex) {

            var error_text;

            if (ex instanceof InfoException) {
                // Post alert using the in-application info panel
                pickpack.ui.showInfoBox(ex.message);
            }
            else if (ex instanceof HandleableError) {
                // Post alert using the in-application alert panel
                pickpack.ui.postAlert(ex.message);
            }
            else if (ex instanceof ApplicationError) {
                // This shouldn't happen. Alert, using several means so that we
                // make sure we're notified even if an error gets swallowed
                // somewhere.
                error_text = ex.name + ":<br />" + ex.message;
                javaScriptAlert(error_text);
                throw ex;
            }
            else if (ex instanceof ApplicationErrorWithTraceback) {
                // The server issued a traceback. Append it to the webpage for
                // inspection.
                pickpack.ui.postAlertWithTraceback(ex.message, ex.traceback);
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
            pickpack.ui.postAlert(error_text);
            window.alert(common.utility_functions.replaceBrWithNewline(error_text));
        }

        // Export symbols to namespace
        var ns = pickpack.error;
        ns.throwApplicationError = throwApplicationError;
        ns.throwApplicationErrorWithTraceback = throwApplicationErrorWithTraceback;
        ns.throwHandleableError = throwHandleableError;
        ns.throwInfoException = throwInfoException;
        ns.decorateWithErrorHandler = decorateWithErrorHandler;
        ns.handleError = handleError;
    }
()); // End of function (closure). Now invoke it.


// Another way to define custom errors that inherit from Error
//StopIteration = function () {};
//StopIteration.prototype = new Error();
//StopIteration.name = 'StopIteration';
//StopIteration.message = 'StopIteration';
