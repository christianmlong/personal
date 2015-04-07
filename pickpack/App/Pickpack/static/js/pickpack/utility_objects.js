/*
 * utility_objects.js:Utility objects for the client-side JavaScript
 * for the Shopfloor Monitor.
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
         unused: true,
         strict: true,
         trailing: true,

         browser: true,
         laxcomma: true
*/


// Create namespace if it does not yet exist
var pickpack;

if (!pickpack) {
    pickpack = {};
}
else if (typeof pickpack !== "object") {
    throw new Error("pickpack already exists, and is not an object");
}

if (pickpack.utility_objects) {
    throw new Error("pickpack.utility_objects already exists");
}
else {
    pickpack.utility_objects = {};
}


(
    function () {
        'use strict';

        // This object manages the sound effects.
        function SoundController() {
        }

        // "Class" properties

        SoundController.BASE_URL = "/static/sounds/";
        SoundController.SOUNDFILE_EXT_MP3 = ".mp3";
        SoundController.SOUNDFILE_EXT_OGG = ".ogg";
        SoundController.SOUND_ELEMENT_ID = "pkpk_sound_element";

        SoundController.prototype.playOrderCompleteSound = function () {
            this.playSound(pickpack.globals.optionController.orderCompleteSound);
        };

        SoundController.prototype.playErrorSound = function () {
            this.playSound(pickpack.globals.optionController.errorSound);
        };

        SoundController.prototype.playScanBeep = function () {
            this.playSound(pickpack.globals.optionController.scanBeep);
        };

        SoundController.prototype.playSound = function (soundName) {
            var soundFileURLmp3;
            var soundFileURLogg;
            var soundObject;

            if (soundName !== "none") {
                this.stopSound();
                soundFileURLmp3 = SoundController.BASE_URL + soundName + SoundController.SOUNDFILE_EXT_MP3;
                soundFileURLogg = SoundController.BASE_URL + soundName + SoundController.SOUNDFILE_EXT_OGG;

                // This works on newer thin clients (t510) and on the older ones (t5535, t5525)
                soundObject = document.createElement('div');
                soundObject.setAttribute("id", SoundController.SOUND_ELEMENT_ID);
                soundObject.style.position = "absolute";
                soundObject.style.left = "-1000px";
                soundObject.style.top = "-1000px";
                // Note: the audio tag is an html5 tag, but the page body is xhtml 1
                // The browsers figure it out though :)
                soundObject.innerHTML = '<audio autoplay>' +
                                        '    <source src="' + soundFileURLmp3 + '" type="audio/mpeg">' +
                                        '    <source src="' + soundFileURLogg + '" type="audio/ogg">' +
                                        // Fallback for older browsers
                                        '    <embed src="' + soundFileURLmp3 + '" autostart="true" type="audio/mpeg" loop="false" />' +
                                        '</audio>';
                document.body.appendChild(soundObject);
                soundObject = null;
            }
        };

        SoundController.prototype.stopSound = function () {
            var soundObject = MochiKit.DOM.getElement(SoundController.SOUND_ELEMENT_ID);
            if (soundObject !== null) {
                document.body.removeChild(soundObject);
                soundObject = null;
            }
        };


        // This object manages the options and user preferences.
        function OptionController() {
            // Using a path other than / didn't work for me in IE.
            this.dataStore = common.cookie.cookieFactory("pkpkOptions", "/");
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

            if (this.dataStore.hasOwnProperty("orderCompleteSound")) {
                pickpack.ui.setElementValue("order_complete_sound", this.dataStore.orderCompleteSound);
                this.orderCompleteSound = this.dataStore.orderCompleteSound;
            }
            else {
                // No cookie value set, use default value from SELECT
                this.orderCompleteSound = pickpack.ui.getElementValue("order_complete_sound");
            }

            if (this.dataStore.hasOwnProperty("errorSound")) {
                pickpack.ui.setElementValue("error_sound", this.dataStore.errorSound);
                this.errorSound = this.dataStore.errorSound;
            }
            else {
                this.errorSound = pickpack.ui.getElementValue("error_sound");
            }

            if (this.dataStore.hasOwnProperty("scanBeep")) {
                pickpack.ui.setElementValue("scan_beep", this.dataStore.scanBeep);
                this.scanBeep = this.dataStore.scanBeep;
            }
            else {
                this.scanBeep = pickpack.ui.getElementValue("scan_beep");
            }

            if (this.dataStore.hasOwnProperty("useFade")) {
                pickpack.ui.setElementValue("use_fade", this.dataStore.useFade);
                this.useFade = this.dataStore.useFade;
            }
            else {
                this.useFade = pickpack.ui.getElementValue("use_fade");
            }

            var temp;
            if (this.dataStore.hasOwnProperty("userId")) {
                temp = this.dataStore.userId;
                if (!temp || temp.length === 0) {
                    temp = "***";
                }
                pickpack.ui.setElementValue("user_id", temp);
                this.userId = temp;
            }
            else {
                temp = pickpack.ui.getElementValue("user_id");
                if (!temp || temp.length === 0) {
                    temp = "***";
                    pickpack.ui.setElementValue("user_id", temp);
                    this.saveOptionValuesToCookie();
                }
                this.userId = temp;
            }
        };

        OptionController.prototype.saveOptionValuesToCookie = function () {
            this.orderCompleteSound = this.dataStore.orderCompleteSound = pickpack.ui.getElementValue("order_complete_sound");
            this.errorSound = this.dataStore.errorSound = pickpack.ui.getElementValue("error_sound");
            this.scanBeep = this.dataStore.scanBeep = pickpack.ui.getElementValue("scan_beep");
            this.useFade = this.dataStore.useFade = pickpack.ui.getElementValue("use_fade");

            var temp = common.utility_functions.trim(pickpack.ui.getElementValue("user_id").toUpperCase());
            if (!temp || temp.length === 0) {
                temp = "***";
            }
            this.userId = this.dataStore.userId = temp;

            this.dataStore.storeForALongTime();
        };

        OptionController.prototype.resetUserId = function () {
            this.userId = this.dataStore.userId = "***";
            this.dataStore.storeForALongTime();
        };

        // This object manages the logs of special keypresses made by the user.
        function SpecialKeysLogger() {
            // Make a new empty object to hold the objects that store the
            // special keys for each row.
            this.log = {};
        }

        SpecialKeysLogger.prototype.logSpecialKeyUsage = function (row_element, specialKey) {
            var item_number = pickpack.ui.getRowItemNumber(row_element);
            var row_id = row_element.id;
            var keyRepresentation;

            // We have to pay attention to the fact that there may be multiple
            // lines with the same item number. We index these logs by row id.
            // We leave out the row id when we output our string representation
            // of the logged special keys.

            if (specialKey === pickpack.constants.F2_KEY) {
                // If the user pressed the F2 key, then we reset the log.
                if (this.log.hasOwnProperty(row_id)) {
                    // An object exists for this row; delete it.
                    delete this.log[row_id];
                }
            }
            else {
                // If the user pressed a different special key, then we log it.
                switch (specialKey) {
                case pickpack.constants.ARROW_LEFT:
                    keyRepresentation = "<-";
                    break;
                case pickpack.constants.ARROW_RIGHT:
                    keyRepresentation = "->";
                    break;
                case pickpack.constants.PLUS_KEY:
                    keyRepresentation = "+";
                    break;
                default:
                    keyRepresentation = "Unknown key";
                    break;
                }
                if (this.log.hasOwnProperty(row_id)) {
                    // An object already exists for this row, append this
                    // special key to the object's specialKeys array.
                    this.log[row_id].specialKeys.push(keyRepresentation);

                    // Sanity check
                    common.utility_functions.assert(this.log[row_id].item_number === item_number, "Item number has changed");
                }
                else {
                    // Make a new object to store the item number and the
                    // special keys employed on this row.
                    this.log[row_id] = {};
                    this.log[row_id].item_number = item_number;
                    this.log[row_id].specialKeys = [keyRepresentation];
                }
            }
        };

        SpecialKeysLogger.prototype.specialKeysAsString = function () {
            var keysAsString;
            var keyLogToString;
            var keyLogs = MochiKit.Base.values(this.log);
            if (keyLogs.length === 0) {
                keysAsString = "";
            }
            else {
                keyLogToString = function (keyLog) {
                    return keyLog.item_number + ":[" + keyLog.specialKeys.join(" ") + "]";
                };
                // Sort the array in place. Useful for making sure the tests
                // always see the same result.
                keyLogs.sort();
                keysAsString = MochiKit.Base.map(keyLogToString, keyLogs).join("  ");
            }
            return keysAsString;
        };


        // This object contains and indexes the serial numbers.
        function SerializedItemContainer() {
            // Make a new empty object to hold the objects that hold the
            // serialNumber arrays.
            this.container = {};

            this.order_number = null;
            this.order_generation = null;
            this.active_row_id = null;
        }

        SerializedItemContainer.prototype.startSerialNumberEntry = function (row_element) {
            var item_number;
            var current_count;
            var expected_count;
            var already_scanned_serial_numbers_for_this_row;
            var order_number_and_generation;

            // Store order number and generation for later
            order_number_and_generation = pickpack.ui.getOrderNumberAndGeneration();
            this.order_number = order_number_and_generation[0];
            this.order_generation = order_number_and_generation[1];

            // Store this row's Id for future reference
            this.active_row_id = row_element.id;

            item_number = pickpack.ui.getRowItemNumber(row_element);
            current_count = pickpack.ui.getRowCurrentQuantity(row_element);
            expected_count = pickpack.ui.getRowExpectedQuantity(row_element);

            if (this.container.hasOwnProperty(this.active_row_id)) {
                // An object already exists for this row.
                //
                // Do a quick sanity check. Make sure the quantity of
                // already-scanned numbers equals the current count that we are
                // displaying. Also, make sure current count is less than or
                // equal to expected count.
                already_scanned_serial_numbers_for_this_row = this.container[this.active_row_id].serial_numbers;
                common.utility_functions.assert(already_scanned_serial_numbers_for_this_row.length === current_count, "Number of serial numbers scanned does not match current count.");
                common.utility_functions.assert(current_count <= expected_count, "Current count exceeds expected count.");
            }
            else {
                // No object exists. This must be the first time we are scanning
                // serial numbers for this row, or else F2 was pressed, and
                // deleted the previous object for this row. Create a new
                // storage object for the current row.
                this.container[this.active_row_id] = {};
                this.container[this.active_row_id].item_number = item_number;
                this.container[this.active_row_id].serial_numbers = [];
            }

            // Display dialog, and accept a serial number scan.
            pickpack.ui.showSerialNumberBox(item_number);
        };

        SerializedItemContainer.prototype.processPossibleSerialNumber = function (userInput) {
            // This gets called when the user scans something while the serial
            // number box is active.

            if (pickpack.regex.looksLikeSerialNumber(userInput)) {
                // It's a possible serial number. Check if it has been scanned
                // already.
                if (this.serialNumberHasBeenScannedAlready(userInput)) {
                    pickpack.error.throwHandleableError("Serial number " + userInput + " has already been scanned.");
                }
                else {
                    // Validate with the database.
                    pickpack.server.serialNumberRequest(this.container[this.active_row_id].item_number,
                                                        userInput);
                }
            }
            else {
                // Invalid input. This could be an item number, a UPC, an order
                // number, or just some garbled scan.
                pickpack.error.throwHandleableError(userInput + " is not a valid serial number. Please scan a serial number.");
            }
        };

        SerializedItemContainer.prototype.processValidSerialNumber = function (validated_item_number,
                                                                               validated_serial_number) {
            // This gets called once the database has determined that the serial
            // number is valid.
            //
            // Note that this does not get used as a callback. This is just a
            // regular function that gets called from inside a callback
            // function. So, we don't need to do the callback infrastructure
            // work (like binding the method, returning a return value, etc.)

            // Sanity check
            // Make sure we haven't changed item numbers somehow
            common.utility_functions.assert(validated_item_number === this.container[this.active_row_id].item_number, "Item number has changed");

            // Now we push the serial number on to the serialNumber array for
            // that row in this.container, and we increment the display of that
            // row in the HTML table.
            this.container[this.active_row_id].serial_numbers.push(validated_serial_number);
            pickpack.ui.incrementRowCountByRowId(this.active_row_id);

            // Reset our row reference.
            this.active_row_id = null;

            // Dismiss the serial number box.
            pickpack.ui.hideSerialNumberBox();
        };

        SerializedItemContainer.prototype.clearScannedSerialNumbers = function (row_element) {
            // This clears out the log of scanned serial numbers for this row.
            delete this.container[row_element.id];
        };

        SerializedItemContainer.prototype.serialNumberHasBeenScannedAlready = function (userInput) {
            var all_serial_numbers = this.allScannedSerialNumbersForAllRowsWithTheSameItemNumberAsTheCurrentRow();
            return (MochiKit.Base.findIdentical(all_serial_numbers, userInput) !== -1);
        };

        SerializedItemContainer.prototype.allScannedSerialNumbersForAllRowsWithTheSameItemNumberAsTheCurrentRow = function () {
            var row_ids = MochiKit.Base.map(pickpack.ui.getElementId, pickpack.ui.findRowsByItem(this.container[this.active_row_id].item_number));
            var row_id;
            var serial_numbers = [];
            var i;
            for (i = 0; i < row_ids.length; i += 1) {
                row_id = row_ids[i];
                if (this.container.hasOwnProperty(row_id)) {
                    serial_numbers = serial_numbers.concat(this.container[row_id].serial_numbers);
                }
            }
            return serial_numbers;
        };

        SerializedItemContainer.prototype.serializedItemsAsJSON = function () {
            // Here's an example of the serial numbers data
            //
            //{'1': {'item_number': '235671',
            //       'serial_numbers': ['20081050000000',
            //                          '20081050000001',
            //                          '20081050000002',
            //                          '20081050000003']},
            // '2': {'item_number': '235671',
            //       'serial_numbers': ['20081050000004',
            //                          '20081050000005',
            //                          '20081050000006',
            //                          '20081050000007']}}
            return MochiKit.Base.serializeJSON(this.container);
        };


        // This object manages the wait spinner.
        function WaitSpinnerController() {
            this.numberOfWaitRequests = 0;
        }

        WaitSpinnerController.prototype.waitForMe = function () {
            // Increment the counter that keeps track of whether we should show
            // the wait spinner.
            this.numberOfWaitRequests += 1;
            this.updateWaitSpinner();
        };

        WaitSpinnerController.prototype.iAmDone = function () {
            // Decrement the counter that keeps track of whether we should show
            // the wait spinner.
            //
            // Note that this does not get used as a callback (it gets called
            // from inside a callback function), so we don't need to do the
            // callback infrastructure work (like binding the method, returning
            // a return value, etc.)
            this.numberOfWaitRequests -= 1;
            this.updateWaitSpinner();
        };

        WaitSpinnerController.prototype.updateWaitSpinner = function () {
            if (this.numberOfWaitRequests > 0) {
                common.ui.showElement("wait_spinner");
            }
            else {
                common.ui.hideElement("wait_spinner");
            }
        };


        // This object manages the input buffer.
        function InputBuffer() {
            // These properties are defined and initialized inside the reset
            // function.
            //this.buffer = [];
            //this.scan_in_progress = false;
            //this.contains_space = false;

            this.reset();
        }

        InputBuffer.prototype.reset = function () {
            // Reset the buffer. Focus the window so it catches the next input.
            this.buffer = [];
            this.scan_in_progress = false;
            this.contains_space = false;
            window.focus();
        };

        InputBuffer.prototype.handleKeyPress = function (keyString) {
            // Add a single character to the buffer. If the keypress character
            // is the space character, then it disambiguates between a
            // spacebar-press by the user and a space character in a Harper
            // item label.
            var spacebar_keypress = false;

            if (keyString === " ") {
                if (this.scan_in_progress) {
                    // We found a space character in the middle of a scan. This
                    // must be a Harper label.
                    this.contains_space = true;
                }
                else {
                    // We're seeing a space keypress, but there is nothing in
                    // the buffer. This must be the result of the user pressing
                    // the space bar.
                    spacebar_keypress = true;
                }
            }

            if (!spacebar_keypress) {
                this.scan_in_progress = true;
                // Bust to upper case right away.
                this.buffer.push(String(keyString).toUpperCase());
            }

            return spacebar_keypress;
        };

        InputBuffer.prototype.readAndReset = function () {
            // Returns the contents of the buffer, as a string. Resets the
            // buffer.

            var contents = common.utility_functions.trim(this.buffer.join(""));

            if (this.contains_space) {
                // We saw a space character as we were filling the buffer, so
                // run the buffer contents through our Harper label process.
                //
                // Note: if the user scanned something that contains a space,
                // but is not a Harper label, the checkForHarperItemNumber
                // function will return the scan unchanged. It will error out as
                // an invalid scan later, as it should.
                contents = pickpack.regex.checkForHarperItemNumber(contents);
            }

            this.reset();

            return contents;
        };


        // Note: in some cases, it's ok to add an "ordinary function" to the
        // callback chain.
        //
        // By "ordinary function", I mean a function that has not been written
        // as a callback. Callback functions (i.e. functions that can
        // participate in a callback chain) follow certain conventions.
        //
        // 1) They have "result" as their last argument. This is where the data
        //    from the callback chain flows in to the function.
        //
        // 2) They return a result - the fruits of their processing of the input
        //    data. This result gets passed on down the callback chain to the
        //    next callback in line.
        //
        // However, it is possible to add plain functions to the callback chain,
        // even if that plain function does not confirm to the callback
        // conventions described above.
        //
        // (Note: this info is specific to MochiKit deferreds and their callback
        // chains. Twisted deferreds work a little differently, notably with
        // regard to the order of parameters. In Twisted, "result" is the first
        // parameter passed to the callback function. In MochiKit, "result" is
        // the last parameter passed to the callback function.)
        //
        // Here's why we can add a plain function to the MochiKit callback
        // chain. From the docs for MochiKit.Deferred:
        //
        //      If the initial callback value provided to the Deferred is
        //      omitted, an undefined value will be passed instead. This also
        //      happens if a callback or errback function does not return a
        //      value.
        //
        // and
        //
        //      A Deferred will be in the error state if one of the following
        //      conditions are met:
        //          1) The result given to callback or errback is "instanceof
        //             Error"
        //          2) The callback or errback threw an error while executing.
        //      Otherwise, the Deferred will be in the success state.
        //
        // So, even though the plain function does not return a value, the
        // callback chain stays on the callback side, and does not switch over
        // to the errback side.
        //
        // In addition, JavaScript allows you to pass any number of arguments to
        // a function, even though that function may not have the same number of
        // parameters defined. So, even though the deferred's callback-calling
        // mechanism is passing an extra "result" argument, we can safely use a
        // plain function (i.e. a function which does not have a "result"
        // parameter). JavaScript will simply ignore the extra argument.
        //
        // Note that this means that the plain function does not have access to
        // the deferred's data (data fetched asynchronously). What's more, any
        // callbacks added to the chain after the plain function will not
        // receive any deferred data either. This is a major limitation, which
        // relegates this technique to the quick-and-dirty-hacks category.
        //
        // However, it can be useful when you have (for example) a
        // user-interface function that you want to call both synchronously
        // (right now, in response to user action) and asynchronously (queue it
        // up to be called later).
        //
        // This is all relevant here, because I sometimes add "non-callback"
        // functions to the callback chain, by passing them in to e.g
        // ItemNotesHandler.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed.
        //
        // That method calls this.setUpDeferred. It passes in the function and
        // its arguments in an array I have named "function_call_specification".
        //
        // The function passed in might or might follow the "callback"
        // conventions I described above, but it should still work, given the
        // caveats I have described above.
        function NotesHandler() {
            this.deferred = null;
        }

        NotesHandler.prototype.setUpDeferred = function (function_call_specification) {
            // Create a new Deferred object, and add the function to its
            // callback chain.
            this.deferred = new MochiKit.Async.Deferred();

            // The "function_call_specification" parameter is an array to wrap
            // everything I need to create the callback.
            //
            // Here, I'm using "apply(null, function_call_specification)" to
            // spread that array out in my call to addCallback (like in python,
            // when you call a function and you use * in the arguments).
            //
            // So, if this function had been called like this:
            //
            //    function_call_specification = [
            //        functionToCallLater,
            //        arg1,
            //        arg2
            //    ];
            //    pickpack.globals.itemNotesHandler.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed(
            //        item_number,
            //        function_call_specification
            //    )
            //
            // then the line below would be equivalent to this:
            //
            //    this.deferred.addCallback(
            //        functionToCallLater,
            //        arg1,
            //        arg2
            //    )
            //
            // Another note: when addCallback is called with more than one
            // argument (as above), the excess arguments are bound to
            // functionToCallLater, using MochiKit.Base.partial.

            this.deferred.addCallback.apply(this.deferred, function_call_specification);

            // An explanation of JavaScript's apply() method.
            //
            // Every JavaScript function has an apply() method. It is easiest to
            // explain by example:
            //
            //            f.apply(o, [1, 2])
            //            // is the same as
            //            o.temp_method = f;
            //            o.temp_method(1, 2);
            //            delete o.temp_method;
            //
            // The first argument to apply() ('o' in the example above) becomes
            // the value of the 'this' keyword within the body of the function.
            //
            // Let's take a look at some more complex examples:
            //
            //            // f = deferred.addCallback
            //            // o = deferred
            //            deferred.addCallback.apply(deferred, function_call_specification);
            //            // is the same as
            //            deferred.temp_method = deferred.addCallback;
            //            deferred.temp_method(1, 2);
            //            delete deferred.temp_method;
            //
            //
            //            // f = deferred.addCallback
            //            // o = null
            //            deferred.addCallback.apply(null, function_call_specification);
            //            // is the same as
            //            null.temp_method = deferred.addCallback;
            //            null.temp_method(1, 2);
            //            delete null.temp_method;
            //
            //
            // These two lines are not equivalent.
            //
            //            deferred.addCallback.apply(deferred, function_call_specification);    // works
            //            deferred.addCallback.apply(null, function_call_specification);        // doesn't work
            //
            // In the second case, when the addCallback function runs, the
            // 'this' keyword evaluates to null inside the body of the
            // addCallback function.
            //
            // apply() can be used like Python's * operator, to spread an array
            // of arguments out in to individual positional arguments for a
            // function call.
        };

        NotesHandler.prototype.infoBoxWasDismissed = function () {
            // The user has dismissed the info box that was showing the notes.
            // Now we can set off the callback chain that was stored earlier.
            // This will run all of the callback functions in the callback
            // chain.
            if (this.deferred) {
                this.deferred.callback();
                this.deferred = null;
            }
        };


        // This object manages the notifications that inform the user about item
        // notes.
        function ItemNotesHandler(item_notes) {
            // Call the constructor of the base object
            NotesHandler.call(this);

            var item_number;
            this.item_notes = {};

            if (item_notes !== common.constants.NO_DATA_FOUND) {
                // After processing the JSON we received from the server,
                // item_notes contains a JavaScript object. The properties are
                // item numbers, and the property values contain the
                // concatenated text of all notes for that item.
                //
                // From that object, we build an object that will control the
                // behavior of notes notifications.
                for (item_number in item_notes) {
                    if (item_notes.hasOwnProperty(item_number)) {
                        this.item_notes[item_number] = {
                            'notes' : common.utility_functions.replaceNewlineWithBr(item_notes[item_number]),
                            'displayed' : false
                        };
                    }
                }
            }
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        ItemNotesHandler.prototype = new NotesHandler();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        ItemNotesHandler.prototype.constructor = ItemNotesHandler;

        // Ok, now we can get on with the show
        ItemNotesHandler.prototype.itemHasNotesToDisplay = function (item_number) {
            var return_value = false;
            if (this.item_notes.hasOwnProperty(item_number)) {
                if (!this.item_notes[item_number].displayed) {
                    return_value = true;
                }
            }
            return return_value;
        };

        ItemNotesHandler.prototype.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed = function (
            item_number,
            function_call_specification
        ) {
            // Note: I'd like to use JavaScript's "arguments" feature here
            // ("arguments" is an array-like object which holds all the
            // arguments that were passed in when this function was called, like
            // python's *args parameter) to pass all the arguments on to
            // setUpDeferred. However, I also need to have item_number here,
            // which should not be passed to setUpDeferred. So, I separate
            // item_number from the rest of the arguments, and I use the
            // function_call_specification array to hold all the other
            // arguments.
            if (!this.itemHasNotesToDisplay(item_number)) {
                pickpack.error.throwApplicationError("System error 29000 - No notes to show:  " + item_number);
            }

            // Create a new Deferred object, and add the function to its
            // callback chain.
            this.setUpDeferred(function_call_specification);

            // Now that we've scheduled some stuff to happen once the notes have
            // been dismissed, we can show the notes dialog.
            pickpack.ui.showInfoBox(this.item_notes[item_number].notes);
            this.item_notes[item_number].displayed = true;
        };

        function OrderNotesHandler(order_notes) {
            // Call the constructor of the base object
            NotesHandler.call(this);

            if (order_notes === common.constants.NO_DATA_FOUND) {
                pickpack.error.throwApplicationError("System error 29100 - No notes to show for this order");
            }

            // After processing the JSON we received from the server,
            // order_notes contains a JavaScript object.
            //
            // Here is the format for the order_notes component
            //  order_notes
            //      |
            //      - popup_time: 'beginning', 'end', 'beginning_and_end'
            //      |
            //      - components {0,3}
            //          |
            //          - type: 'text', 'image', 'text_and_image'
            //          |
            //          - content: note_text, image_names, (note_text, image_names)
            this.order_notes = order_notes;

            // Generate the dom elements for the html we will display to the user.
            this.order_notes_dom_elements = this.buildDomElementsForNotes(order_notes);
        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        OrderNotesHandler.prototype = new NotesHandler();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        OrderNotesHandler.prototype.constructor = OrderNotesHandler;

        // Ok, now we can get on with the show
        OrderNotesHandler.prototype.showNotesAndRunThisAfterTheNotesDialogHasBeenDismissed = function (
            call_time,
            function_call_specification
        ) {
            var function_to_call;
            var function_arguments;

            if (this.itsAnAppropriateTimeForOrderNotes(call_time)) {
                // Create a new Deferred object, and add the function to its
                // callback chain.
                this.setUpDeferred(function_call_specification);

                // Now that we've scheduled some stuff to happen once the notes
                // have been dismissed, we can show the notes dialog.
                this.displayOrderNotes(call_time);
            }
            else {
                // No order notes needed at this time, so no need to set up a
                // deferred. Just call the function_call_specification right
                // now.
                function_to_call = function_call_specification[0];
                function_arguments = function_call_specification.slice(1);
                function_to_call.apply(null, function_arguments);
            }
        };

        OrderNotesHandler.prototype.displayOrderNotes = function (call_time) {
            var play_sound;
            if (call_time === 'on_demand') {
                play_sound = false;
            }
            else {
                play_sound = true;
            }

            if (this.itsAnAppropriateTimeForOrderNotes(call_time)) {
                pickpack.ui.showInfoBoxWithDomElements(this.order_notes_dom_elements,
                                                       play_sound);
            }
        };

        OrderNotesHandler.prototype.itsAnAppropriateTimeForOrderNotes = function (call_time) {
            return ((this.order_notes.popup_time === 'beginning_and_end') ||
                    (call_time === 'on_demand') ||
                    (this.order_notes.popup_time === call_time)
                   );
        };

        OrderNotesHandler.prototype.buildDomElementsForNotes = function (order_notes) {
            var components = order_notes.components;
            var number_of_components = components.length;
            var image_name_suffix;

            if (number_of_components === 1) {
                image_name_suffix = '_large';
            }
            else if (number_of_components === 2) {
                image_name_suffix = '_large';
            }
            else if (number_of_components === 3) {
                image_name_suffix = '_medium';
            }
            else if (number_of_components === 4) {
                image_name_suffix = '_small';
            }
            else if (number_of_components === 5) {
                image_name_suffix = '_small';
            }
            else if (number_of_components === 6) {
                image_name_suffix = '_small';
            }
            else if (number_of_components === 7) {
                image_name_suffix = '_small';
            }
            else if (number_of_components === 8) {
                image_name_suffix = '_small';
            }
            else if (number_of_components === 9) {
                image_name_suffix = '_small';
            }
            else {
                pickpack.error.throwApplicationError("System error 29200 - Invalid number of components:  " + number_of_components);
            }

            // We need to use bind() here instead of partial().
            // This:
            //
            //      bind(method, this, arg1, arg2)
            //
            // is equivalent to this:
            //
            //      partial(bind(method, this), arg1, arg2)
            //
            // If we don't use bind(), the value of "this" is lost. If, while
            // debugging, you notice "this" is the window object rather than the
            // object it should be, then you need to use bind().
            //
            // See the definition of server.ServerRequestManager for more info.
            var dom_builder_function = MochiKit.Base.bind(this.buildDomForComponent,
                                                          this,
                                                          image_name_suffix);

            // Convenient local binding for the MochiKit.DOM namespace
            var d = MochiKit.DOM;

            // Build up the element using MochiKit.DOM.createDOM. This syntax is
            // based on Nevow's Stan.
            return d.DIV(null,
                         d.TABLE({'id' : pickpack.constants.ORDER_NOTES_TABLE_ID},
                                 d.TBODY(null,
                                         MochiKit.Base.map(dom_builder_function, components)
                                        )
                                )
                        );
        };

        OrderNotesHandler.prototype.buildDomForComponent = function (image_name_suffix,
                                                                     order_note_component) {
            var return_value;
            var note_text;

            if (order_note_component.type === 'text') {
                note_text = order_note_component.content;
                return_value = MochiKit.DOM.TR(null,
                                               this.buildImageCell(),
                                               this.buildTextCell(note_text)
                                              );
            }
            else if (order_note_component.type === 'image') {
                return_value = MochiKit.DOM.TR(null,
                                               this.buildImageCell(order_note_component.content,
                                                                   image_name_suffix),
                                               this.buildTextCell()
                                              );
            }
            else if (order_note_component.type === 'text_and_image') {
                note_text = order_note_component.content[0];
                return_value = MochiKit.DOM.TR(null,
                                               this.buildImageCell(order_note_component.content[1],
                                                                   image_name_suffix),
                                               this.buildTextCell(note_text)
                                              );
            }
            else {
                pickpack.error.throwApplicationError("System error 29300 - Unknown comment format:  " + order_note_component.type);
            }

            // I use return_value, because it shuts up Komodo's simple
            // JavaScript linter. Otherwise it complains about "strict warning:
            // anonymous function does not always return a value"
            return return_value;
        };

        OrderNotesHandler.prototype.buildImageCell = function (image_names,
                                                               image_name_suffix) {
            var buildSPAN = function (image_name_suffix,
                                      image_name) {
                var image_file_path = pickpack.ui.buildImagePath(image_name + image_name_suffix);
                return MochiKit.DOM.SPAN(null,
                                         MochiKit.DOM.IMG({"src" : image_file_path})
                                        );
            };
            // buildSPAN could probably just refer to image_name_suffix
            // directly, from its nested scope. However, I'm just binding it in
            // explicitly using partial().
            var builder_function = MochiKit.Base.partial(buildSPAN,
                                                         image_name_suffix);

            return this.buildCell(image_names,
                                  builder_function,
                                  "pkpk_order_note_image"
                                 );
        };

        OrderNotesHandler.prototype.buildTextCell = function (note_text) {
            var buildSPAN = function (line_text) {
                return MochiKit.DOM.SPAN(null,
                                         line_text,
                                         MochiKit.DOM.BR(null)
                                        );
            };
            return this.buildCell(note_text,
                                  buildSPAN,
                                  "pkpk_order_note_text"
                                 );
        };

        OrderNotesHandler.prototype.buildCell = function (contents,
                                                          build_function,
                                                          html_class) {
            var cell_contents;

            if (contents) {
                // contents might be a string, or it might be an array of
                // strings. Here we wrap it, using wrapScalarValue, so we can
                // handle it in a consistent way.
                cell_contents = MochiKit.Base.map(build_function,
                                                  common.utility_functions.wrapScalarValue(contents)
                                                 );
            }
            else {
                // Build a blank cell
                cell_contents = MochiKit.DOM.NBSP;
            }

            return MochiKit.DOM.TD({"class" : html_class},
                                   cell_contents
                                  );
        };





        // These factory functions are exported to the namespace, instead of
        // exporting the constructors themselves. We use factory functions to
        // make sure the "new" keyword always gets called.
        function soundControllerFactory() {
            return new SoundController();
        }
        function optionControllerFactory() {
            return new OptionController();
        }
        function specialKeysLoggerFactory() {
            return new SpecialKeysLogger();
        }
        function serializedItemContainerFactory() {
            return new SerializedItemContainer();
        }
        function waitSpinnerControllerFactory() {
            return new WaitSpinnerController();
        }
        function inputBufferFactory() {
            return new InputBuffer();
        }
        function itemNotesHandlerFactory(item_notes) {
            return new ItemNotesHandler(item_notes);
        }
        function orderNotesHandlerFactory(order_notes) {
            return new OrderNotesHandler(order_notes);
        }

        // Export symbols to namespace
        var ns = pickpack.utility_objects;
        ns.soundControllerFactory = soundControllerFactory;
        ns.optionControllerFactory = optionControllerFactory;
        ns.specialKeysLoggerFactory = specialKeysLoggerFactory;
        ns.serializedItemContainerFactory = serializedItemContainerFactory;
        ns.waitSpinnerControllerFactory = waitSpinnerControllerFactory;
        ns.inputBufferFactory = inputBufferFactory;
        ns.itemNotesHandlerFactory = itemNotesHandlerFactory;
        ns.orderNotesHandlerFactory = orderNotesHandlerFactory;
    }
()); // End of function (closure). Now invoke it.
