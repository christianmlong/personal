/*
 * ui.js: Functions that deal with manipulating the user interface for
 * the client-side JavaScript.
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
         laxcomma: true

*/


// Create namespace if it does not yet exist
var common;

if (!common) {
    common = {};
}
else if (typeof common !== "object") {
    throw new Error("common already exists, and is not an object");
}

if (common.ui) {
    throw new Error("common.ui already exists");
}
else {
    common.ui = {};
}


(
    function () {
        'use strict';

        function highlightElement(element) {
            MochiKit.DOM.addElementClass(element, "highlight");
        }

        function lowlightElement(element) {
            MochiKit.DOM.removeElementClass(element, "highlight");
        }

        function hideElement(element) {
            MochiKit.DOM.addElementClass(element, "invisible");
        }

        function showElement(element) {
            MochiKit.DOM.removeElementClass(element, "invisible");
        }

        function addAbsolutePositioning(element) {
            MochiKit.DOM.addElementClass(element, "absolute");
        }

        function removeAbsolutePositioning(element) {
            MochiKit.DOM.removeElementClass(element, "absolute");
        }

        function dismissModalPane(pane_id) {
            var fade_options = {duration: 0.7,
                                queue: "break"
                               };
            MochiKit.Visual.fade(pane_id, fade_options);
        }

        function showModalPane(pane_id,
                               additional_show_options  /* optional */ ) {
            var show_options = {duration: 0.7,
                                queue: "break"
                               };
            if (additional_show_options !== undefined) {
                MochiKit.Base.update(show_options, additional_show_options);
            }
            MochiKit.Visual.appear(pane_id, show_options);
        }

        function clearAlert(error_box_id, error_text_id) {
            var error_box = MochiKit.DOM.getElement(error_box_id);
            var error_text_element = MochiKit.DOM.getElement(error_text_id);
            common.ui.hideElement(error_box);
            error_text_element.innerHTML = "";
        }

        function postAlert(message, error_box_id, error_text_id) {
            var error_box = MochiKit.DOM.getElement(error_box_id);
            var error_text_element = MochiKit.DOM.getElement(error_text_id);
            if (boxIsActive(error_box_id)) {
                // The alert box alert is already active. Append.
                error_text_element.innerHTML = error_text_element.innerHTML + htmlBreakTag() + message;
            }
            else {
                error_text_element.innerHTML = message;
                common.ui.showElement(error_box);
            }
        }

        function showTraceback(traceback, debug_info_id) {
            MochiKit.DOM.getElement(debug_info_id).innerHTML = traceback;
        }

        function paneIsActive(pane_id) {
            return isDisplayBlock(pane_id);
        }

        function boxIsActive(box_id) {
            return isVisible(box_id);
        }

        function isVisible(theElement) {
            return (!(MochiKit.DOM.hasElementClass(theElement, "invisible")));
        }

        function isDisplayBlock(element_id) {
            return MochiKit.DOM.getElement(element_id).style.display === "block";
        }

        //function addHtmlLinebreak(original_string,
        //                          number_of_linebreaks  /* optional, default 1 */ ) {
        //    if (number_of_linebreaks === undefined) {
        //        number_of_linebreaks = 1;
        //    }
        //    var one_linebreak = htmlBreakTag();
        //    var linebreaks = one_linebreak;
        //
        //    /* jshint plusplus: false */
        //    for (var i = 1; i < number_of_linebreaks; i++) {
        //        linebreaks = linebreaks + one_linebreak;
        //    }
        //    return original_string + linebreaks;
        //}

        function htmlBreakTag() {
            return "<br />";
        }

        // Export symbols to namespace
        var ns = common.ui;
        ns.highlightElement = highlightElement;
        ns.lowlightElement = lowlightElement;
        ns.hideElement = hideElement;
        ns.showElement = showElement;
        ns.addAbsolutePositioning = addAbsolutePositioning;
        ns.removeAbsolutePositioning = removeAbsolutePositioning;
        ns.dismissModalPane = dismissModalPane;
        ns.showModalPane = showModalPane;
        ns.clearAlert = clearAlert;
        ns.postAlert = postAlert;
        ns.showTraceback = showTraceback;
        ns.paneIsActive = paneIsActive;
        ns.boxIsActive = boxIsActive;
        ns.isDisplayBlock = isDisplayBlock;
        //ns.addHtmlLinebreak = addHtmlLinebreak;
        ns.htmlBreakTag = htmlBreakTag;

    }
()); // End of function (closure). Now invoke it.
