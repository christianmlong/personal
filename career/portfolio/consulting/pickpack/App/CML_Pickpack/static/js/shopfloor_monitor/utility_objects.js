/*
 * utility_objects.js:Utility objects for the client-side JavaScript
 * for the Pick Pack application.
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit */
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
         strict: true,
         trailing: true,

         browser: true
*/

         //unused: strict,


// Create namespace if it does not yet exist
var shopfloor_monitor;

if (!shopfloor_monitor) {
    shopfloor_monitor = {};
}
else if (typeof shopfloor_monitor !== "object") {
    throw new Error("shopfloor_monitor already exists, and is not an object");
}

if (shopfloor_monitor.utility_objects) {
    throw new Error("shopfloor_monitor.utility_objects already exists");
}
else {
    shopfloor_monitor.utility_objects = {};
}


(
    function () {
        'use strict';

        // This object manages the options and user preferences.
        function OptionController() {
            // Using a path other than / didn't work for me in IE.
            this.dataStore = common.cookie.cookieFactory("sfmnOptions", "/");
            this.loadOptionValuesFromCookie();
        }

        OptionController.prototype.loadOptionValuesFromCookie = function () {
            // Go through each option available on the options pane. Read each
            // value from the cookie, and set the options pane to reflect the
            // cookie. If there is no cookie, make one based upon the options
            // pane defaults. Also, cache a local copy of the option value, so
            // that subsequent lookups of the value don't have to go through the
            // whole cookie parsing process - they just read the value from this
            // object.

            if (this.dataStore.hasOwnProperty("dataDisplay")) {
                shopfloor_monitor.ui.setElementValue("data_display", this.dataStore.dataDisplay);
                this.dataDisplay = this.dataStore.dataDisplay;
            }
            else {
                // No cookie value set, use default value from SELECT
                this.dataDisplay = shopfloor_monitor.ui.getElementValue("data_display");
            }

            //if (this.dataStore.hasOwnProperty("diagonalStripes")) {
            //    shopfloor_monitor.ui.setElementValue("diagonal_stripes", this.dataStore.diagonalStripes);
            //    this.diagonalStripes = common.utility_functions.smarterBooleanConversion(this.dataStore.diagonalStripes);
            //}
            //else {
            //    this.diagonalStripes = shopfloor_monitor.ui.getElementValue("diagonal_stripes");
            //}

            if (this.dataStore.hasOwnProperty("showUntil")) {
                shopfloor_monitor.ui.setElementValue("show_until", this.dataStore.showUntil);
                this.showUntil = this.dataStore.showUntil;
            }
            else {
                // No cookie value set, use default value from SELECT
                this.showUntil = shopfloor_monitor.ui.getElementValue("show_until");
            }

            if (this.dataStore.hasOwnProperty("showBackorder")) {
                shopfloor_monitor.ui.setElementValue("show_backorder", this.dataStore.showBackorder);
                this.showBackorder = common.utility_functions.smarterBooleanConversion(this.dataStore.showBackorder);
            }
            else {
                this.showBackorder = shopfloor_monitor.ui.getElementValue("show_backorder");
            }

            if (this.dataStore.hasOwnProperty("readyToPickHighlight")) {
                shopfloor_monitor.ui.setElementValue("ready_to_pick_highlight", this.dataStore.readyToPickHighlight);
                this.readyToPickHighlight = this.dataStore.readyToPickHighlight;
            }
            else {
                // No cookie value set, use default value from SELECT
                this.readyToPickHighlight = shopfloor_monitor.ui.getElementValue("ready_to_pick_highlight");
            }
        };

        OptionController.prototype.saveOptionValuesToCookie = function () {
            this.dataDisplay = this.dataStore.dataDisplay = shopfloor_monitor.ui.getElementValue("data_display");
            //this.diagonalStripes = this.dataStore.diagonalStripes = shopfloor_monitor.ui.getElementValue("diagonal_stripes");
            this.showUntil = this.dataStore.showUntil = shopfloor_monitor.ui.getElementValue("show_until");
            this.showBackorder = this.dataStore.showBackorder = shopfloor_monitor.ui.getElementValue("show_backorder");
            this.readyToPickHighlight = this.dataStore.readyToPickHighlight = shopfloor_monitor.ui.getElementValue("ready_to_pick_highlight");
            // Provide the current URL path, so that this cookie is specific to
            // this path.
            this.dataStore.storeForALongTime();
        };


        // This object manages the wait spinner.
        function WaitSpinnerController() {

            this.ui_timer = null;
            //this.pending_event = null;
            this.request_object = null;


            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are replacing each of the existing functions with a
            // new function that has "this" bound.
            //this.respondToUserInput = MochiKit.Base.bind(this.respondToUserInput, this);
            //this.startWaitingForAppXHR = MochiKit.Base.bind(this.startWaitingForAppXHR, this);
            //this.startWaitingForUserXHR = MochiKit.Base.bind(this.startWaitingForUserXHR, this);
            //this.isWaiting = MochiKit.Base.bind(this.isWaiting, this);
            this.doneWaiting = MochiKit.Base.bind(this.doneWaiting, this);
            //this.saveEventForLater = MochiKit.Base.bind(this.saveEventForLater, this);
            this._enterNotWaiting = MochiKit.Base.bind(this._enterNotWaiting, this);
            //this._enterWaitingInvisiblyAppXHR = MochiKit.Base.bind(this._enterWaitingInvisiblyAppXHR, this);
            this._enterWaitingInvisiblyUserXHR = MochiKit.Base.bind(this._enterWaitingInvisiblyUserXHR, this);
            this._enterWaitingVisibly = MochiKit.Base.bind(this._enterWaitingVisibly, this);
            this._startUiTimer = MochiKit.Base.bind(this._startUiTimer, this);
            this._cancelUiTimer = MochiKit.Base.bind(this._cancelUiTimer, this);

            // Waitspinner graphics, on an html5 canvas.
            this.waitspinner = common.waitspinner.waitspinnerFactory(
                shopfloor_monitor.constants.WAITSPINNER_CONTAINER_ID,
                {id : shopfloor_monitor.constants.WAITSPINNER_CANVAS_ID});
            this.waitspinner.setColor('#969696');
            this.waitspinner.setShape('roundRect');
            this.waitspinner.setDiameter(400);
            this.waitspinner.setDensity(12);
            this.waitspinner.setRange(0.9);
            this.waitspinner.setSpeed(1);
            this.waitspinner.setFPS(10);

            // State machine
            //
            // Events
            // app_xhr
            // user_xhr
            // user_input
            // ui_timer_ding
            // wait_over
            //
            // States
            // not_waiting
            // waiting_invisibly_app_xhr
            // waiting_invisibly_user_xhr
            // waiting_visibly
            this.fsm = common.state_machine.StateMachine.create({
                initial: 'not_waiting',
                //error: function(eventName, from, to, args, errorCode, errorMessage) {
                //    MochiKit.Logging.log('event ' + eventName + '\n' +
                //                         ' from ' + from + '\n' +
                //                         ' to ' + to + '\n' +
                //                         ' args ' + args + '\n' +
                //                         ' errorCode ' + errorCode + '\n' +
                //                         ' errorMessage :- ' + errorMessage);
                //},
                events: [
                    { name: 'wait_over',        from: 'waiting_invisibly_app_xhr',      to: 'not_waiting'                   },
                    { name: 'wait_over',        from: 'waiting_invisibly_user_xhr',     to: 'not_waiting'                   },
                    { name: 'wait_over',        from: 'waiting_visibly',                to: 'not_waiting'                   },
                    { name: 'wait_over',        from: 'not_waiting',                    to: 'not_waiting'                   }, // NO OP

                    { name: 'user_input',       from: 'waiting_invisibly_app_xhr',      to: 'waiting_invisibly_user_xhr'    },
                    { name: 'user_input',       from: 'waiting_invisibly_user_xhr',     to: 'waiting_visibly'               },
                    { name: 'user_input',       from: 'waiting_visibly',                to: 'waiting_visibly'               }, // NO OP
                    { name: 'user_input',       from: 'not_waiting',                    to: 'not_waiting'                   }, // NO OP

                    { name: 'ui_timer_ding',    from: 'waiting_invisibly_app_xhr',      to: 'waiting_invisibly_app_xhr'     }, // NO OP
                    { name: 'ui_timer_ding',    from: 'waiting_invisibly_user_xhr',     to: 'waiting_visibly'               },
                    { name: 'ui_timer_ding',    from: 'waiting_visibly',                to: 'waiting_visibly'               }, // NO OP
                    { name: 'ui_timer_ding',    from: 'not_waiting',                    to: 'not_waiting'                   }, // NO OP

                    { name: 'user_xhr',         from: 'waiting_invisibly_app_xhr',      to: 'waiting_invisibly_app_xhr'     }, // NO OP
                    { name: 'user_xhr',         from: 'waiting_invisibly_user_xhr',     to: 'waiting_invisibly_user_xhr'    }, // NO OP
                    { name: 'user_xhr',         from: 'waiting_visibly',                to: 'waiting_visibly'               }, // NO OP
                    { name: 'user_xhr',         from: 'not_waiting',                    to: 'waiting_invisibly_user_xhr'    },

                    { name: 'app_xhr',          from: 'waiting_invisibly_app_xhr',      to: 'waiting_invisibly_app_xhr'     }, // NO OP
                    { name: 'app_xhr',          from: 'waiting_invisibly_user_xhr',     to: 'waiting_invisibly_user_xhr'    }, // NO OP
                    { name: 'app_xhr',          from: 'waiting_visibly',                to: 'waiting_visibly'               }, // NO OP
                    { name: 'app_xhr',          from: 'not_waiting',                    to: 'waiting_invisibly_app_xhr'     }
                ],
                callbacks: {
                    // on enter state
                    onenternot_waiting:                     this._enterNotWaiting,
                    //onenterwaiting_invisibly_app_xhr:       this._enterWaitingInvisiblyAppXHR,
                    onenterwaiting_invisibly_user_xhr:      this._enterWaitingInvisiblyUserXHR,
                    onenterwaiting_visibly:                 this._enterWaitingVisibly
                }
            });

            // Explicitly bind "this" into all the methods that need it
            // (callbacks and errbacks that use "this.something"). See the
            // ServerRequestManager constructor for information.
            //
            // Here we are repacing each of the existing methods with a
            // new function that has "this" bound to the fsm object.
            this.fsm.ui_timer_ding = MochiKit.Base.bind(this.fsm.ui_timer_ding, this.fsm);
        }

        WaitSpinnerController.prototype.respondToUserInput = function (mkEvent) {
            var handle_user_input;

            if (this.fsm.is('waiting_invisibly_app_xhr')) {
                // The user made some input while we are waiting invisibly for a
                // scheduled data refresh. Cancel the pending xml http request,
                // and do what the user requested instead.
                this.cancelRequest();
                handle_user_input = true;
            }
            else if (this.fsm.is('waiting_visibly') ||
                     this.fsm.is('waiting_invisibly_user_xhr')) {
                // The user made some input while we are waiting invisibly for
                // another user reques, or while we are waiting visibly.
                // Continue waiting, and tell the calling function to ignore the
                // user input.
                handle_user_input = false;
            }
            else if (this.fsm.is('not_waiting')) {
                // The user made some input while we are not waiting. Tell the
                // calling function to ignore the user input.
                handle_user_input = true;
            }
            else {
                throw new Error("Invalid state in state machine " + this.fsm.bla);
            }

            // Fire the state machine event.
            this.fsm.user_input();

            // Return true if the user input event should be handled, or false
            // if the user input event should be ignored.
            return handle_user_input;
        };

        WaitSpinnerController.prototype.startWaitingForAppXHR = function (request_object) {
            // Start the wait spinner. We are waiting in response to an
            // application-triggered event (e.g. a timer).
            this.cancelRequest();
            this.request_object = request_object;
            this.fsm.app_xhr();
        };

        WaitSpinnerController.prototype.startWaitingForUserXHR = function (request_object) {
            // Start the wait spinner. We are waiting in response to a
            // user-triggered event such as a mouse click or a key press.
            this.cancelRequest();
            this.request_object = request_object;
            this.fsm.user_xhr();
        };

        WaitSpinnerController.prototype.doneWaiting = function (resultsOfLastCallback) {
            // *** Callback *** this method is used as a callback for a
            // deferred.
            //
            // This is what I call a "side-effects" callback. It does not
            // modify its input before passing it along the callback chain. It
            // just does stuff in response to the input, and passes the input
            // along unmodified.
            this.fsm.wait_over();
            return resultsOfLastCallback;
        };

        WaitSpinnerController.prototype.cancelRequest = function () {
            // Cancel any pending request object.
            if (this.request_object) {
                this.request_object.cancelXHRDeferred();
                //MochiKit.Logging.log("just called cancelXHRDeferred");
            }
            this.request_object = null;
        };

        WaitSpinnerController.prototype._enterNotWaiting = function(event, from, to) {
            //if (from === to) {
            //    MochiKit.Logging.log("NO OP not_waiting");
            //    return;
            //}
            //MochiKit.Logging.log("ENTER   STATE: not_waiting");
            this._cancelUiTimer();
            this.waitspinner.hide();
        };

        //WaitSpinnerController.prototype._enterWaitingInvisiblyAppXHR = function(event, from, to) {
        //    //if (from === to) {
        //    //    MochiKit.Logging.log("NO OP waiting_invisibly_app_xhr");
        //    //    return;
        //    //}
        //    MochiKit.Logging.log("ENTER   STATE: waiting_invisibly_app_xhr");
        //};

        WaitSpinnerController.prototype._enterWaitingInvisiblyUserXHR = function(event, from, to) {
            //if (from === to) {
            //    MochiKit.Logging.log("NO OP waiting_invisibly_user_xhr");
            //    return;
            //}
            //MochiKit.Logging.log("ENTER   STATE: waiting_invisibly_user_xhr");
            this._startUiTimer();
        };

        WaitSpinnerController.prototype._enterWaitingVisibly = function(event, from, to) {
            //if (from === to) {
            //    MochiKit.Logging.log("NO OP waiting_visibly");
            //    return;
            //}
            //MochiKit.Logging.log("ENTER   STATE: waiting_visibly");
            this._cancelUiTimer();
            this.waitspinner.show();
        };

        WaitSpinnerController.prototype._startUiTimer = function() {
            this._cancelUiTimer();
            this.ui_timer = MochiKit.Async.callLater(0.3,
                                                     this.fsm.ui_timer_ding);
        };

        WaitSpinnerController.prototype._cancelUiTimer = function() {
            if (this.ui_timer) {
                this.ui_timer.cancel();
            }
        };


        // These factory functions are exported to the namespace, instead of
        // exporting the constructors themselves. We use factory functions to
        // make sure the "new" keyword always gets called.
        function waitSpinnerControllerFactory() {
            return new WaitSpinnerController();
        }
        function optionControllerFactory() {
            return new OptionController();
        }


        // Export symbols to namespace
        var ns = shopfloor_monitor.utility_objects;
        ns.waitSpinnerControllerFactory = waitSpinnerControllerFactory;
        ns.optionControllerFactory = optionControllerFactory;
    }
()); // End of function (closure). Now invoke it.
