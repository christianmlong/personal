/*
 * server.js: Functions that deal with server requests for
 * the client-side JavaScript for the Shop Floor Monitor application.
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit */

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
         unused: strict,
         strict: true,
         trailing: true,

         browser: true,

         nonew: false
*/


// Create namespace if it does not yet exist
var shopfloor_monitor;

if (!shopfloor_monitor) {
    shopfloor_monitor = {};
}
else if (typeof shopfloor_monitor !== "object") {
    throw new Error("shopfloor_monitor already exists, and is not an object");
}

if (shopfloor_monitor.server) {
    throw new Error("shopfloor_monitor.server already exists");
}
else {
    shopfloor_monitor.server = {};
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

        ServerRequestManager.prototype.topLevelErrorHandler = function (err) {
            // *** Errback *** this method is used as an errback for a deferred.
            // It returns null, which causes execution to shift back to the
            // callback side of the chain if this function concludes normally.
            // If this function causes an error to be thrown, then the next
            // errback in the chain is invoked.

            // We post the alert directly (instead of just raising an error),
            // because these deferreds have a way of swallowing errors.

            if (! err instanceof MochiKit.Async.CancelledError) {
                shopfloor_monitor.error.handleError(err);
            }

            return null;
        };

        ServerRequestManager.prototype.handleFailure = function (err) {
            // *** Errback *** this method is used as an errback for a deferred.
            // It returns err, which causes execution to stay on the errback
            // side of the chain if this function concludes normally. Execution
            // will also stay on the errback side of the chain if this function
            // causes an error to be thrown.

            if (! err instanceof MochiKit.Async.CancelledError) {
                this.failure(err);
            }

            return err;
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
            var errorText = "System error 26800 while fetching order data" +
                            "<br /><br />Error message: " + err.message;

            // This is what we do if there was an error while requesting the
            // data from the server.
            if (err.req.responseText) {
                shopfloor_monitor.error.throwApplicationErrorWithTraceback(errorText,
                                                                           err.req.responseText);
            }
            else {
                shopfloor_monitor.error.throwApplicationError(errorText);
            }
        };

        GETRequestManager.prototype.noResponse = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if there is no data in the response object
            shopfloor_monitor.error.throwApplicationError("System error 26600 - No order data found.");
        };

        GETRequestManager.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // This is what we do if the server sent NO_DATA_FOUND. This gets
            // overridden by some descendant objects, to provide a friendlier
            // error message.
            shopfloor_monitor.error.throwApplicationError("System error 28300 - No order data found.");
        };

        GETRequestManager.prototype.makeRequest = function (url,
                                                            param_names,
                                                            param_values,
                                                            call_when_done) {
            // *** Regular method *** not intended for use as a callback/errback

            // Make a http GET request and create a deferred.

            // Wrap strings up in one-element arrays, if parameters were
            // supplied.
            if (param_names !== undefined &&
                !MochiKit.Base.isArrayLike(param_names)
               ) {
                param_names = [param_names];
            }
            if (param_values !== undefined &&
                !MochiKit.Base.isArrayLike(param_values)
               ) {
                param_values = [param_values];
            }

            if (param_names === undefined) {
                this.deferred = MochiKit.Async.doSimpleXMLHttpRequest(url);
            }
            else {
                this.deferred = MochiKit.Async.doSimpleXMLHttpRequest(url, param_names, param_values);
            }
            this.hookUpDeferred(call_when_done);
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
            return data;
        };

        GETRequestManager.prototype.cancelXHRDeferred = function () {
            // *** Regular method *** not intended for use as a callback/errback
            //MochiKit.Logging.log("before this.deferred.cancel()");
            this.deferred.cancel();
            //MochiKit.Logging.log("just called this.deferred.cancel()");
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
        JSONRequestManager.prototype.hookUpDeferred = function (call_when_done) {
            // *** Regular method *** not intended for use as a callback/errback

            // *** Override *** this method overrides
            // GETRequestManager.prototype.hookUpDeferred

            // Don't turn on the wait spinner here in the server code. Do that
            // in UI code instead.
            //this.switchOnWaitSpinner();

            // Add the callbacks to our deferred. this.deferred was created by
            // the makeRequest method.
            this.deferred.addCallbacks(this.validateResults, this.handleFailure);
            this.deferred.addCallback(this.decodeJSON);
            this.deferred.addCallback(this.handleResults);
            // To turn off the wait spinner when the results arrive, the UI code
            // passes in
            // shopfloor_monitor.globals.waitSpinnerController.doneWaiting as
            // the value of the call_when_done parameter
            this.deferred.addBoth(call_when_done);

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
                //json_results = MochiKit.Base.evalJSON(data);
                json_results = JSON.parse(data);
            }
            catch (ex) {
                shopfloor_monitor.error.throwApplicationError("Error parsing JSON (270) for order data " +
                                "<br />Data:  " + data +
                                "<br />Parser error message:  " + ex.message);
            }
            return json_results;
        };


        // This object manages requests for the summary order status data.
        function DataRequestObject() {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the getData function instead.

            // Call the constructor of the base object
            JSONRequestManager.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // None needed for this object
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        DataRequestObject.prototype = new JSONRequestManager();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        DataRequestObject.prototype.constructor = DataRequestObject;

        DataRequestObject.prototype.dataDisplayToRequest = function () {
            if (shopfloor_monitor.globals.optionController.dataDisplay === "4up_narrow") {
                return "4up";
            }
            else {
                return shopfloor_monitor.globals.optionController.dataDisplay;
            }
        };

        // This object manages requests for the summary order status data.
        function SummaryRequestObject(call_when_done) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the getOrderSummaryData function instead.

            // Call the constructor of the base object
            DataRequestObject.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // None needed for this object

            // Now make the request
            var requestFields = ["scale",
                                 "show_backorder"];
            var requestValues = [this.dataDisplayToRequest(),
                                 shopfloor_monitor.globals.optionController.showBackorder];
            this.makeRequest("/shopfloor_monitor/j_status_orders",
                             requestFields,
                             requestValues,
                             call_when_done);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        SummaryRequestObject.prototype = new DataRequestObject();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        SummaryRequestObject.prototype.constructor = SummaryRequestObject;

        // Ok, now we can get on with the show
        SummaryRequestObject.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // *** Override *** this method overrides
            // GETRequestManager.prototype.noDataFound

            // This is what we do if the server sent NO_DATA_FOUND
            shopfloor_monitor.error.throwApplicationError(" No order data found.");
        };

        SummaryRequestObject.prototype.handleResults = function (data) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.
            shopfloor_monitor.ui.displayGraph(data);
            return data;
        };


        // This object manages requests for the detailed order status data.
        function ListOfOrderNumbersRequestObject(bar_index, call_when_done) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the getListOfOrderNumbers function instead.

            // Call the constructor of the base object
            DataRequestObject.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing handleResults function with a
            // new function that has "this" bound.
            this.handleResults = MochiKit.Base.bind(this.handleResults, this);

            // Store away the bar index for later
            this.bar_index = bar_index;

            // Translate bar_index in to order_type
            var bar_index_lookup = {0 : "today_sure",
                                    1 : "signature_service",
                                    2 : "service_file",
                                    3 : "normal"};

            var order_type = bar_index_lookup[this.bar_index];

            if (order_type === undefined) {
                shopfloor_monitor.error.throwApplicationError("order_type is undefined.");
            }

            // Now make the request
            var requestFields = ["scale",
                                 "show_backorder",
                                 "order_type"];
            var requestValues = [this.dataDisplayToRequest(),
                                 shopfloor_monitor.globals.optionController.showBackorder,
                                 order_type];
            this.makeRequest("/shopfloor_monitor/j_status_order_numbers",
                             requestFields,
                             requestValues,
                             call_when_done);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        ListOfOrderNumbersRequestObject.prototype = new DataRequestObject();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        ListOfOrderNumbersRequestObject.prototype.constructor = ListOfOrderNumbersRequestObject;

        // Ok, now we can get on with the show
        ListOfOrderNumbersRequestObject.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // *** Override *** this method overrides
            // GETRequestManager.prototype.noDataFound

            // This is what we do if the server sent NO_DATA_FOUND
            shopfloor_monitor.error.throwApplicationError(" No order number data found.");
        };

        ListOfOrderNumbersRequestObject.prototype.handleResults = function (data) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.
            shopfloor_monitor.ui.displayOrderNumberList(data, this.bar_index);
            return data;
        };


        // This object manages requests for the detailed data for one order number.
        function OrderNumberDetailRequestObject(order_number, order_generation, call_when_done) {
            // We don't expose this constructor, because it is not intended to
            // be called directly. Call the getOrderNumberDetail function instead.

            // Call the constructor of the base object
            DataRequestObject.call(this);

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing the existing handleResults function with a
            // new function that has "this" bound.
            this.handleResults = MochiKit.Base.bind(this.handleResults, this);

            // Store away the bar index for later
            this.order_number = order_number;
            this.order_generation = order_generation;

            // Now make the request
            var requestFields = ["order_number", "order_generation"];
            var requestValues = [order_number, order_generation];
            this.makeRequest("/shopfloor_monitor/order_number_detail",
                             requestFields,
                             requestValues,
                             call_when_done);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        OrderNumberDetailRequestObject.prototype = new DataRequestObject();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        OrderNumberDetailRequestObject.prototype.constructor = OrderNumberDetailRequestObject;

        // Ok, now we can get on with the show
        OrderNumberDetailRequestObject.prototype.noDataFound = function () {
            // *** Regular method *** not intended for use as a callback/errback

            // *** Override *** this method overrides
            // GETRequestManager.prototype.noDataFound

            // This is what we do if the server sent NO_DATA_FOUND
            shopfloor_monitor.error.throwApplicationError(" No data found for order " + this.order_number + "/" + this.order_generation + ".");
        };

        OrderNumberDetailRequestObject.prototype.handleResults = function (data) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.
            shopfloor_monitor.ui.displayOrderDetails(data);
            return data;
        };


        // These functions creates and returns new server request objects. We
        // expose only these (factory) functions, so that we are sure to not
        // forget to use the "new" operator.
        function getOrderSummaryData(call_when_done) {
            return new SummaryRequestObject(call_when_done);
        }
        function getListOfOrderNumbers(bar_index, call_when_done) {
            return new ListOfOrderNumbersRequestObject(bar_index, call_when_done);
        }
        function getOrderNumberDetailData(order_number, order_generation, call_when_done) {
            return new OrderNumberDetailRequestObject(order_number, order_generation, call_when_done);
        }




        // Export symbols to namespace
        var ns = shopfloor_monitor.server;
        ns.getOrderSummaryData = getOrderSummaryData;
        ns.getListOfOrderNumbers = getListOfOrderNumbers;
        ns.getOrderNumberDetailData = getOrderNumberDetailData;

    }
()); // End of function (closure). Now invoke it.
