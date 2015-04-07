/*
 * event_handlers.js: Event handlers for the client-side JavaScript for the
 * Pick Pack application.
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
         unused: true,
         strict: true,
         trailing: true,

         browser: true,
         onecase: true

*/


// Create namespace if it does not yet exist
var pickpack;

if (!pickpack) {
    pickpack = {};
}
else if (typeof pickpack !== "object") {
    throw new Error("pickpack already exists, and is not an object");
}

if (pickpack.event_handlers) {
    throw new Error("pickpack.event_handlers already exists");
}
else {
    pickpack.event_handlers = {};
}


(
    function () {
        'use strict';

        function _onLoad(mkEvent) {

            // Silence the "'mkEvent' is defined but never used." warning
            /* jshint unused: false */

            // Now that the page has been loaded, connect our other event
            // handlers
            MochiKit.Signal.connect(window, "onclick", handleWindowOnClick);
            MochiKit.Signal.connect(document, "onkeydown", handleOnKeyDown);
            MochiKit.Signal.connect(document, "onkeypress", handleOnKeyPress);
            MochiKit.Signal.connect(document, "onkeyup", handleOnKeyUp);
            MochiKit.Signal.connect("order_complete_sound", "onchange", handleSelectChange);
            MochiKit.Signal.connect("error_sound", "onchange", handleSelectChange);
            MochiKit.Signal.connect("scan_beep", "onchange", handleSelectChange);
            MochiKit.Signal.connect("order_complete_sound", "onkeyup", handleSelectKeyUp);
            MochiKit.Signal.connect("error_sound", "onkeyup", handleSelectKeyUp);
            MochiKit.Signal.connect("scan_beep", "onkeyup", handleSelectKeyUp);
            MochiKit.Signal.connect(pickpack.constants.ERROR_BOX_ID, "onclick", handleErrorBoxOnClick);
            pickpack.globals.instantiateGlobalUtilityObjects();
            //pickpack.globals.inputBuffer.reset(); // Happens inside constructor

            pickpack.ui.doInitialPageRendering();
        }

        function _onKeyDown(mkEvent) {
            var key_string = mkEvent.key().string;
            if (aModifierWasPressed(mkEvent)) {
                return;
            }
            if (pickpack.ui.optionsPaneIsActive()) {
                switch (key_string) {
                case "KEY_F4":
                    mkEvent.stop();
                    pickpack.ui.dismissConfigPane();
                    //break;
                    // No need to run the next switch statememnt
                    return;
                case "KEY_ENTER":
                    mkEvent.stop();
                    pickpack.ui.dismissConfigPane();
                    //break;
                    // No need to run the next switch statememnt
                    return;
                }
            }
            else if (pickpack.ui.helpPaneIsActive()) {
                switch (key_string) {
                case "KEY_F1":
                    mkEvent.stop();
                    pickpack.ui.dismissHelpPane();
                    //break;
                    // No need to run the next switch statememnt
                    return;
                case "KEY_ENTER":
                    mkEvent.stop();
                    pickpack.ui.dismissHelpPane();
                    //break;
                    // No need to run the next switch statememnt
                    return;
                }
            }
            else if (pickpack.ui.noModalPaneOrSerialNumberBox()) {
                switch (key_string) {
                case "KEY_ARROW_LEFT":
                    mkEvent.stop();
                    pickpack.ui.doLeftArrow();
                    break;
                case "KEY_ARROW_UP":
                    mkEvent.stop();
                    pickpack.ui.doUpArrow();
                    break;
                case "KEY_ARROW_RIGHT":
                    mkEvent.stop();
                    pickpack.ui.doRightArrow();
                    break;
                case "KEY_ARROW_DOWN":
                    mkEvent.stop();
                    pickpack.ui.doDownArrow();
                    break;
                case "KEY_F1":
                    mkEvent.stop();
                    pickpack.ui.showHelpPane();
                    break;
                case "KEY_F2":
                    mkEvent.stop();
                    pickpack.ui.doMinus();
                    break;
                case "KEY_F3":
                    mkEvent.stop();
                    pickpack.ui.focusFirstInvalidRow();
                    break;
                case "KEY_F4":
                    mkEvent.stop();
                    pickpack.ui.showConfigPane();
                    break;
                case "KEY_F6":
                    mkEvent.stop();
                    //Toggle
                    if (pickpack.ui.infoBoxIsActive()) {
                        pickpack.ui.hideInfoBox();
                    }
                    else {
                        pickpack.ui.showOrderNotesOnDemand();
                    }
                    break;
                case "KEY_F12":
                    mkEvent.stop();
                    pickpack.ui.resetUserId();
                    break;
                }
            }
        }

        function _onKeyPress(mkEvent) {
            var key_string = mkEvent.key().string;
            //var key_code = mkEvent.key().code;
            var user_pressed_space;

            if (pickpack.ui.noModalPaneOrSerialNumberBox()) {
                switch (key_string) {
                case "+":
                    mkEvent.stop();
                    pickpack.ui.doPlus();
                    //break;
                    // No need to run the next tests
                    return;
                }
            }

            if (pickpack.ui.optionsPaneIsActive()) {
                switch (key_string) {
                case " ":
                    mkEvent.stop();
                    pickpack.ui.clearBox();
                    //break;
                    // No need to run the next tests
                    return;
                default:
                    pickpack.ui.guardInfoBoxOrErrorBoxIsActive();
                }
            }
            else {
                if (pickpack.regex.allowedLabelCharacter(key_string)) {
                    mkEvent.stop();
                    user_pressed_space = pickpack.globals.inputBuffer.handleKeyPress(key_string);
                    if (user_pressed_space) {
                        pickpack.ui.clearBox();
                    }
                }
            }
        }

        function _onKeyUp(mkEvent) {
            var key_string = mkEvent.key().string;
            if (aModifierWasPressed(mkEvent)) {
                return;
            }
            switch (key_string) {
            case "KEY_ESCAPE":
                mkEvent.stop();
                pickpack.ui.doEscape();
                //break;
                // No need to run the next switch statememnt
                return;
            }
            if (pickpack.ui.noModalPane()) {
                switch (key_string) {
                case "KEY_TAB":
                    mkEvent.stop();
                    pickpack.ui.processUserInput();
                    break;
                case "KEY_ENTER":
                    mkEvent.stop();
                    pickpack.ui.processUserInput();
                    break;
                }
            }
        }

        function _selectChange(mkEvent) {
            if (pickpack.ui.optionsPaneIsActive()) {
                pickpack.globals.soundController.playSound(pickpack.ui.getElementValue(mkEvent.src()));
            }
        }

        function _selectKeyUp(mkEvent) {
            var key_string = mkEvent.key().string;
            if (pickpack.ui.optionsPaneIsActive()) {
                if ((key_string === "KEY_ARROW_UP") ||
                    (key_string === "KEY_ARROW_DOWN") ||
                    (key_string === "KEY_ARROW_RIGHT") ||
                    (key_string === "KEY_ARROW_LEFT")) {
                    MochiKit.Signal.signal(mkEvent.src(), "onchange");
                }
            }
        }

        function _windowOnClick(mkEvent) {
            if (!pickpack.ui.optionsPaneIsActive()) {
                mkEvent.stop();
                pickpack.globals.inputBuffer.reset();
            }
        }

        function _errorBoxOnClick(mkEvent) {
            if (pickpack.ui.alertBoxIsActive()) {
                mkEvent.stop();
                pickpack.ui.toggleErrorDetail();
            }
        }

        var handleOnKeyDown = pickpack.error.decorateWithErrorHandler(_onKeyDown);
        var handleOnKeyPress = pickpack.error.decorateWithErrorHandler(_onKeyPress);
        var handleOnKeyUp = pickpack.error.decorateWithErrorHandler(_onKeyUp);
        var handleSelectChange = pickpack.error.decorateWithErrorHandler(_selectChange);
        var handleSelectKeyUp = pickpack.error.decorateWithErrorHandler(_selectKeyUp);
        var handleWindowOnClick = pickpack.error.decorateWithErrorHandler(_windowOnClick);
        var handleErrorBoxOnClick = pickpack.error.decorateWithErrorHandler(_errorBoxOnClick);

        // This doesn't work
        //handleOnKeyDown: pickpack.error.decorateWithErrorHandler(_onKeyDown);

        function aModifierWasPressed(mkEvent) {
            var modifiers = mkEvent.modifier();
            if (modifiers.any) {
                return true;
            }
            else {
                return false;
            }
        }

        // Export symbols to namespace
        var ns = pickpack.event_handlers;
        ns.handleOnLoad = pickpack.error.decorateWithErrorHandler(_onLoad);
    }
()); // End of function (closure). Now invoke it.
