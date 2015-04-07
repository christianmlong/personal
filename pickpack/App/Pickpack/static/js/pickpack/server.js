/*
 * server.js: Functions that deal with server requests for
 * the client-side JavaScript for the Pick Pack application.
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit */
/*global common */

// We have the jshint "nonew" directive set to false here,
// because we do have some constructor functions in this
// file that call new().
//
// In other files in this project, "nonew" is set to true.


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
         plusplus: true,
         undef: true,
         unused: true,
         strict: true,
         trailing: true,

         browser: true,
         laxcomma: true,

         nonew: false
*/


// Create namespace if it does not yet exist
var pickpack;

if (!pickpack) {
    pickpack = {};
}
else if (typeof pickpack !== "object") {
    throw new Error("pickpack already exists, and is not an object");
}

if (pickpack.server) {
    throw new Error("pickpack.server already exists");
}
else {
    pickpack.server = {};
}


(
    function () {
        'use strict';

        // This object manages sending requests to, and receiving data from, the
        // server. This is a base object from which other objects can inherit.
        function ServerRequestManager() {
            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something").
            //
            // Quote from Bob Ippolito on MochiKit Google group (Search for
            // "callback scope")
            //
            //      Yeah, JavaScript doesn't have bound methods, so you lose the
            //      "this" pointer when you store away the callbacks. At the
            //      bottom of <your constructor>, add bindMethods(this), which
            //      will wrap all of the function calls with a closure that
            //      maintains "this".
            //
            //
            // Here we are repacing the existing handleFailure function with a
            // new function that has "this" bound.
            this.handleFailure = MochiKit.Base.bind(this.handleFailure, this);
        }

        ServerRequestManager.prototype.handleTimeout = function (err) {
            // *** Regular method *** not intended for use as a callback/errback

            // Possible enhancement: investigate
            // Note: I don't think I have any timeout checks. Does
            // MochiKit.Async.doSimpleXMLHttpRequest provide a timeout
            // automatically?

            if (err instanceof MochiKit.Async.CancelledError) {
                pickpack.error.throwHandleableError("Timeout while accessing database for " + this.requestValueAsString + " Please try again.");
                return true;
            }
            else {
                return false;
            }
        };

        ServerRequestManager.prototype.switchOffWaitSpinner = function (resultsOfLastCallback) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.

            pickpack.globals.waitSpinnerController.iAmDone();
            return resultsOfLastCallback;
        };

        ServerRequestManager.prototype.topLevelErrorHandler = function (err) {
            // *** Errback *** this method is used as an errback for a deferred.
            // It returns null, which causes execution to shift back to the
            // callback side of the chain if this function concludes normally.
            // If this function causes an error to be thrown, then the next
            // errback in the chain is invoked.

            // We post the alert directly (instead of just raising an error),
            // because these deferreds have a way of swallowing errors.

            pickpack.error.handleError(err);

            return null;
        };

        ServerRequestManager.prototype.handleFailure = function (err) {
            // *** Errback *** this method is used as an errback for a deferred.
            // It returns null, which causes execution to shift back to the
            // callback side of the chain if this function concludes normally.
            // If this function causes an error to be thrown, then the next
            // errback in the chain is invoked.

            if (!this.handleTimeout(err)) {
                this.failure(err);
            }
            return null;
        };

        function GETRequestManager() {
            // Call the constructor of the base object
            ServerRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing validateResults function with a
            // new function that has "this" bound.
            this.validateResults = MochiKit.Base.bind(this.validateResults, this);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        GETRequestManager.prototype = new ServerRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        GETRequestManager.prototype.constructor = GETRequestManager;

        // Ok, now we can get on with the show
        GETRequestManager.prototype.failure = function (err) {
            // *** Regular method *** not intended for use as a callback/errback
            var errorText = "System error 26800 while working on " + this.requestValueAsString +
                            "<br /><br />Error message: " + err.message;

            // This is what we do if there was an error while requesting the
            // data from the server.
            if (err.req.responseText) {
                pickpack.error.throwApplicationErrorWithTraceback(errorText,
                                                                  err.req.responseText);
            }
            else {
                pickpack.error.throwApplicationError(errorText);
            }
        };

        GETRequestManager.prototype.noResponse = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if there is no data in the response object
            pickpack.error.throwApplicationError("System error 26600 - No data for:  " + this.requestValueAsString);
        };

        GETRequestManager.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if the server sent NO_DATA_FOUND. This gets
            // overridden by some descendant objects, to provide a friendlier
            // error message.
            pickpack.error.throwApplicationError("System error 28300 - No data  found for:  " + this.requestValueAsString);
        };

        GETRequestManager.prototype.hookUpDeferred = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // Set the wait spinner. This gets overridden by some descendant
            // objects, if they want to hook up a different chain of deferreds.
            pickpack.globals.waitSpinnerController.waitForMe();

            // Add the callbacks to our deferred. this.deferred was created by
            // the makeRequest method.
            this.deferred.addCallbacks(this.validateResults, this.handleFailure);
            this.deferred.addCallback(this.handleResults);
            this.deferred.addBoth(this.switchOffWaitSpinner);

            // We're adding this errback at the end of the chain, so it should
            // catch any unhandled exceptions in the chain.
            this.deferred.addErrback(this.topLevelErrorHandler);
        };

        GETRequestManager.prototype.makeRequest = function (url, paramNames, paramValues) {
            // *** Regular method *** not intended for use as a callback/errback

            // Make a http GET request and create a deferred.

            // Wrap strings up in one-element arrays
            if (!MochiKit.Base.isArrayLike(paramNames)) {
                paramNames = [paramNames];
            }
            if (!MochiKit.Base.isArrayLike(paramValues)) {
                paramValues = [paramValues];
            }

            this.deferred = MochiKit.Async.doSimpleXMLHttpRequest(url, paramNames, paramValues);
            this.hookUpDeferred();

            // Store the last GET request as a object property. This makes it
            // easier to test.
            GETRequestManager.lastGET = MochiKit.Base.queryString(paramNames, paramValues);
        };

        GETRequestManager.prototype.validateResults = function (request) {
            // *** Callback *** this method is used as an callback for a
            // deferred.
            //
            // This is what I call a "processing" callback. It returns a
            // different value than the value that was passed in. It modifies
            // its input before passing it along the callback chain.

            // We got a response back from the server. Validate the response. If
            // there are problems, call the appropriate function. The
            // "noResponse" and "noDataFound" functions are not defined here.
            // Instead, they are defined by the objects that inherit from
            // this base object.
            var data = request.responseText;
            if ((!data) || (data === "")) {
                this.noResponse();
            }
            else if (data === common.constants.NO_DATA_FOUND) {
                this.noDataFound();
            }
            return data;
        };

        function POSTRequestManager() {
            // Call the constructor of the base object
            ServerRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing validateResults function with a
            // new function that has "this" bound.
            this.validateResults = MochiKit.Base.bind(this.validateResults, this);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        POSTRequestManager.prototype = new ServerRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        POSTRequestManager.prototype.constructor = POSTRequestManager;

        // Ok, now we can get on with the show
        POSTRequestManager.prototype.failure = function (err) {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if there was an error while writing the data
            // to the server.

            var errorText =  "Error while writing to the database for order number " +
                             common.utility_functions.formatOrderNumberAndGenerationForDisplay(this.order_number,
                                                                                                      this.order_generation) +
                             ".<br /><br />Press the space bar to try resending the data.";

            // err might be an instance of MochiKit.Async.XMLHttpRequestError.
            // If so, we can extract the server error message from the request
            // object and present the traceback in a nicely-formatted way.
            if (err.req && err.req.responseText) {
                pickpack.error.throwApplicationErrorWithTraceback(errorText,
                                                                  err.req.responseText);
            }
            else {
                // No traceback, so just print the error message.
                errorText = errorText + "<br /><br />Error message: " + err.message;
                pickpack.error.throwApplicationError(errorText);
            }
        };

        POSTRequestManager.prototype.hookUpDeferred = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // Set the wait spinner
            pickpack.globals.waitSpinnerController.waitForMe();

            // Add the callbacks to our deferred. this.deferred was created by
            // the makeRequest method.
            this.deferred.addCallbacks(this.validateResults, this.handleFailure);
            this.deferred.addCallback(this.handleResults);
            this.deferred.addBoth(this.switchOffWaitSpinner);

            // We're adding this errback at the end of the chain, so it should
            // catch any unhandled exceptions in the chain.
            this.deferred.addErrback(this.topLevelErrorHandler);
        };

        POSTRequestManager.prototype.makeRequest = function (url, formFields, formValues) {
            // *** Regular method *** not intended for use as a callback/errback

            // Make a http POST request and create a deferred.
            var headers = {"Content-Type": "application/x-www-form-urlencoded"};
            var urlencoded_content = MochiKit.Base.queryString(formFields, formValues);
            var options = {"method": "POST",
                          "headers": headers,
                          "sendContent": urlencoded_content};
            this.deferred = MochiKit.Async.doXHR(url, options);
            this.hookUpDeferred();

            // Store the contents of the last POST request as a object property.
            // This makes it easier to test.
            POSTRequestManager.lastPOST = urlencoded_content;
        };

        POSTRequestManager.prototype.validateResults = function (request) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "processing" callback. It returns a
            // different value than the value that was passed in. It modifies
            // its input before passing it along the callback chain.

            var data = request.responseText;
            // Post an error if we get anything other than an empty string back.
            if (data !== "") {
                pickpack.error.throwApplicationError("System error 26300 - Unexpected return value:  " + data);
            }
            return data;
        };

        function JSONRequestManager() {
            // Call the constructor of the base object
            GETRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing decodeJSON function with a
            // new function that has "this" bound.
            this.decodeJSON = MochiKit.Base.bind(this.decodeJSON, this);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        JSONRequestManager.prototype = new GETRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        JSONRequestManager.prototype.constructor = JSONRequestManager;

        // Ok, now we can get on with the show
        JSONRequestManager.prototype.hookUpDeferred = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // *** Override *** this method overrides
            // GETRequestManager.prototype.hookUpDeferred

            // Set the wait spinner
            pickpack.globals.waitSpinnerController.waitForMe();

            // Add the callbacks to our deferred. this.deferred was created by
            // the makeRequest method.
            this.deferred.addCallbacks(this.validateResults, this.handleFailure);
            this.deferred.addCallback(this.decodeJSON);
            this.deferred.addCallback(this.handleResults);
            this.deferred.addBoth(this.switchOffWaitSpinner);

            // We're adding this errback at the end of the chain, so it should
            // catch any unhandled exceptions in the chain.
            this.deferred.addErrback(this.topLevelErrorHandler);
        };

        JSONRequestManager.prototype.decodeJSON = function (data) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "processing" callback. It returns a
            // different value than the value that was passed in. It modifies
            // its input before passing it along the callback chain.

            // We got packing list data from the server in JSON format. Now we
            // eval that JSON, check for errors and pass the JSON results on to
            // the next callback.
            var json_results;
            try {
                // Decode JSON. Note: this returns an object, not an array.
                // It should work just like an array, but it shows up
                // as an object when you inspect with Firebug. Arrays are
                // objects in JavaScript anyway.
                json_results = MochiKit.Base.evalJSON(data);
            }
            catch (ex) {
                pickpack.error.throwApplicationError("Error parsing JSON (270) for: " + this.requestValueAsString +
                                "<br />Data:  " + data +
                                "<br />Parser error message:  " + ex.message);
            }
            return json_results;
        };

        // This object manages order number requests
        function PackingListRequestObject(requestValue) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the packingListRequest function instead.
            // By calling the packingListRequest function, we make sure we don't
            // forget to use the "new" operator. If we do forget to use the
            // "new" operator, the prototype doesn't get set properly. No need
            // to keep a reference to the new object in a variable: the
            // constructor does all the needed work, hooking up the deferreds.

            // Call the constructor of the base object
            JSONRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing handleResults function with a
            // new function that has "this" bound.
            this.handleResults = MochiKit.Base.bind(this.handleResults, this);

            // Store the order number for later (error messages, etc.)
            this.requestValueAsString = requestValue;

            // Now make the request
            this.makeRequest("/packinglist", "order_id_scan", requestValue);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        PackingListRequestObject.prototype = new JSONRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        PackingListRequestObject.prototype.constructor = PackingListRequestObject;

        // Ok, now we can get on with the show
        PackingListRequestObject.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if the server sent NO_DATA_FOUND
            //
            // Note: I'm intentionally not trying to format requestValueAsString
            // as an order number (AA001/00) before this point. Let the other
            // error handling mechanisms already in place handle bad scans, rather
            // than throw up an error when trying to parse a bad scan in to
            // a format suitable for display.
            var display = pickpack.ui.formatOrderIdScanForDisplay(this.requestValueAsString,
                                                                  /* error_on_fail */ false);
            if (display === null) {
                display = this.requestValueAsString;
            }
            pickpack.error.throwHandleableError("Order number  " + display + " not found.");
        };

        PackingListRequestObject.prototype.handleHandleableServerError = function (err_msg) {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if the server sent a handleable error
            pickpack.error.throwHandleableError(err_msg);
        };

        PackingListRequestObject.prototype.handleResults = function (json_results) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.

            // We got the packing list data. Now we can prepare the environment
            // for a new order, and display the new order to the user.

            // Check if the server threw an error we can handle.
            if (json_results.server_error !== undefined) {
                this.handleHandleableServerError(json_results.server_error);
            }

            // Do some further validation of the results. Look for NO_DATA_FOUND
            // in the packing_list_array property of the json_results object.
            if (json_results.packing_list_array === common.constants.NO_DATA_FOUND) {
                this.noDataFound();
            }

            // Make new global key logger object for this order
            pickpack.globals.specialKeysLogger = pickpack.utility_objects.specialKeysLoggerFactory();

            // Make new global serial number object for this order
            pickpack.globals.serializedItemContainer = pickpack.utility_objects.serializedItemContainerFactory();

            // Make new item notes handler object for this order.
            pickpack.globals.itemNotesHandler = pickpack.utility_objects.itemNotesHandlerFactory(json_results.item_notes);

            // Make new order notes handler object for this order, if needed.
            if (json_results.order_notes === common.constants.NO_DATA_FOUND) {
                pickpack.globals.orderNotesHandler = null;
            }
            else {
                pickpack.globals.orderNotesHandler = pickpack.utility_objects.orderNotesHandlerFactory(json_results.order_notes);
            }

            // Display data to user
            pickpack.ui.fillTable(json_results);

            // Display any order notes, if needed. Note: there is an attribute
            // of the order notes that says whether the notes should be
            // displayed at the start of the order or at the end, or both. We
            // call displayOrderNotes() both at the beginning and the end of the
            // order scanning process, and it figures out if a note should be
            // displayed.
            if (pickpack.globals.orderNotesHandler) {
                // Call displayOrderNotes, and tell it we're at the beginning of
                // the process.
                pickpack.globals.orderNotesHandler.displayOrderNotes('beginning');
            }

            return json_results;
        };

        // This object manages order number requests
        function SerialNumberRequestObject(item_number,
                                           serial_number) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the SerialNumberRequest function
            // instead. See the PackingListRequestObject constructor for
            // information.

            // Call the constructor of the base object
            JSONRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing handleResults function with a
            // new function that has "this" bound.
            this.handleResults = MochiKit.Base.bind(this.handleResults, this);

            // Store the request values for later (error messages, etc.)
            this.requestValueAsString = "Item number: " + item_number +
                                        " Serial number: " + serial_number;
            this.item_number = item_number;
            this.serial_number = serial_number;


            // Now make the request
            var requestFields = ["item_number", "serial_number"];
            var requestValues = [item_number, serial_number];
            this.makeRequest("/validateserialnumber", requestFields, requestValues);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        SerialNumberRequestObject.prototype = new JSONRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        SerialNumberRequestObject.prototype.constructor = SerialNumberRequestObject;

        // Ok, now we can get on with the show
        SerialNumberRequestObject.prototype.handleResults = function (json_results) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.

            // We got the server's reply indicating if this is a valid serial
            // number for this item number.
            if (json_results.is_valid === pickpack.constants.DB_TRUE) {
                // It's a valid serial number.
                pickpack.globals.serializedItemContainer.processValidSerialNumber(this.item_number,
                                                                                  this.serial_number);
            }
            else {
                // It's not a valid serial number; show error to user
                pickpack.error.throwHandleableError(json_results.err_msg);
            }
            return json_results;
        };

        // This object manages requests for the item number corresponding to the
        // given UPC.
        function GetItemNumberByUPCRequestObject(requestValue) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the getItemNumberByUPC function instead.
            // See the PackingListRequestObject constructor for information.

            // Call the constructor of the base object
            GETRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // None needed for this object

            // Store the upc for later (error messages, etc.)
            this.requestValueAsString = requestValue;

            // Now make the request
            this.makeRequest("/itembyupc", "upc", requestValue);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        GetItemNumberByUPCRequestObject.prototype = new GETRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        GetItemNumberByUPCRequestObject.prototype.constructor = GetItemNumberByUPCRequestObject;

        // Ok, now we can get on with the show
        GetItemNumberByUPCRequestObject.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // *** Override *** this method overrides
            // GETRequestManager.prototype.noDataFound

            // This is what we do if the server sent NO_DATA_FOUND
            pickpack.error.throwHandleableError(" No item number is associated with this UPC " +
                            this.requestValueAsString +
                            ".");
        };

        GetItemNumberByUPCRequestObject.prototype.handleResults = function (data) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.

            // All we're doing here is appending the item number to the end
            // of an alert that is already visible on the screen.
            pickpack.ui.postAlert(" Item #: " + data);
            return data;
        };

        // This object manages writing comments
        function PostOrderCompleteObject(currentOrderNumber, currentOrderGeneration, commentText, serialNumberJSON) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the postOrderComplete function instead.
            // See the PackingListRequestObject constructor for information.

            // Call the constructor of the base object
            POSTRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // None needed for this object

            // Now make the request
            this.order_number = currentOrderNumber;
            this.order_generation = currentOrderGeneration;
            //this.comment_text = commentText;
            var formFields = ["order_number", "order_generation", "comment_text", "serial_numbers", "user_id"];
            var formValues = [currentOrderNumber, currentOrderGeneration, commentText, serialNumberJSON, pickpack.globals.optionController.userId];
            this.makeRequest("/ordercomplete", formFields, formValues);
        }

        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        PostOrderCompleteObject.prototype = new POSTRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        PostOrderCompleteObject.prototype.constructor = PostOrderCompleteObject;

        // Ok, now we can get on with the show
        PostOrderCompleteObject.prototype.handleResults = function (post_results) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.

            // We posted the data to the database. Now we display a notification
            // to the user. We call pickpack.ui.notifyOrderComplete() from here
            // so that it only happens if the callback chain has happened
            // without errors.

            // Notify user that the order has been completed successfully
            pickpack.ui.notifyOrderComplete();

            return post_results;
        };


        // These functions creates new server request objects. No need to
        // return the new object: the constructor does all the needed work,
        // hooking up the deferreds. We expose only these (factory) functions,
        // so that we are sure to not forget to use the "new" operator.
        function packingListRequest(requestValue) {
            new PackingListRequestObject(requestValue);
        }
        function getItemNumberByUPC(requestValue) {
            new GetItemNumberByUPCRequestObject(requestValue);
        }
        function postOrderComplete(currentOrderNumber, currentOrderGeneration, commentText, serialNumberJSON) {
            new PostOrderCompleteObject(currentOrderNumber, currentOrderGeneration, commentText, serialNumberJSON);
        }
        function serialNumberRequest(item_number,
                                     serial_number) {
            new SerialNumberRequestObject(item_number,
                                          serial_number);
        }

        // This function returns the last GET for the given parameter. Used for
        // testing.
        function lastGET() {
            return GETRequestManager.lastGET;
        }

        // This function returns the last POST.  Used for testing.
        function lastPOST() {
            return POSTRequestManager.lastPOST;
        }

        // Export symbols to namespace
        var ns = pickpack.server;
        ns.packingListRequest = packingListRequest;
        ns.getItemNumberByUPC = getItemNumberByUPC;
        ns.postOrderComplete = postOrderComplete;
        ns.serialNumberRequest = serialNumberRequest;
        ns.lastGET = lastGET;
        ns.lastPOST  = lastPOST;
    }
()); // End of function (closure). Now invoke it.
