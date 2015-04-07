/*
 * cookie.js: Functions that deal with cookies for
 * the client-side JavaScript for the Pick Pack application.
 *
 */

/*
 * jshint declarations
 *
 */

/*jshint bitwise: true,
         curly: true,
         eqeqeq: true,
         forin: false,
         immed: true,
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
var common;

if (!common) {
    common = {};
}
else if (typeof common !== "object") {
    throw new Error("common already exists, and is not an object");
}

if (common.cookie) {
    throw new Error("common.cookie already exists");
}
else {
    common.cookie = {};
}


(
    function () {
        'use strict';

        // This object manages cookies.
        function Cookie(name, path) {
            /**
             * This is the Cookie() constructor function.
             *
             * This constructor looks for a cookie with the specified name for
             * the current document. If one exists, it parses its value into a
             * set of name/value pairs and stores those values as properties of
             * the newly created object.
             *
             * To store new data in the cookie, simply set properties of the
             * Cookie object. Avoid properties named "store" and "remove" since
             * these are reserved as method names.
             *
             * To save cookie data in the web browser's local store, call
             * store(). To remove cookie data from the browser's store, call
             * remove().
             *
             */

            var i;

            // Remember the name of this cookie
            this.$name = name;

            // Remember the path of this cookie
            this.$path = path;

            // First, get a list of all cookies that pertain to this document We
            // do this by reading the magic Document.cookie property If there
            // are no cookies, we don't have anything to do
            var allcookies = document.cookie;
            if (allcookies === "") {
                return;
            }

            // Break the string of all cookies into individual cookie strings.
            // Then loop through the cookie strings, looking for our name
            var cookies = allcookies.split(';');
            var trimmedCookie = null;
            var cookieValue = null;
            for (i = 0; i < cookies.length; i += 1) {
                trimmedCookie = common.utility_functions.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (trimmedCookie.substring(0, name.length + 1) === (name + "=")) {
                    // The cookie value is the part after the equals sign
                    cookieValue = trimmedCookie.substring(name.length + 1);
                    break;
                }
            }

            // If we didn't find a matching cookie, quit now
            if (cookieValue === null) {
                return;
            }

            // Now that we've extracted the value of the named cookie, we must
            // break that value down into individual state variable names and
            // values. The name/value pairs are separated from each other by
            // ampersands, and the individual names and values are separated
            // from each other by colons. We use the split() method to parse
            // everything.

            // Break it into an array of name/value pairs
            var a = cookieValue.split('&');
            for (i = 0; i < a.length; i += 1)  {
                // Break each pair into an array
                a[i] = a[i].split(':');
            }

            // Now that we've parsed the cookie value, set all the names and
            // values as properties of this Cookie object. Note that we decode
            // the property value because the store() method encodes it
            for (i = 0; i < a.length; i += 1) {
                this[a[i][0]] = decodeURIComponent(a[i][1]);
            }
        }


        //  This function is the store() method of the Cookie object.
        //
        //  Arguments:
        //
        //    daysToLive: the lifetime of the cookie, in days. If you set this
        //      to zero, the cookie will be deleted. If you set it to null, or
        //      omit this argument, the cookie will be a session cookie and will
        //      not be retained when the browser exits. This argument is used to
        //      set the max-age attribute of the cookie.
        //    path: the value of the path attribute of the cookie
        //    domain: the value of the domain attribute of the cookie
        //    secure: if true, the secure attribute of the cookie will be set

        Cookie.prototype.store = function (daysToLive, /* optional */ path, domain, secure) {
            // First, loop through the properties of the Cookie object and put
            // together the value of the cookie. Since cookies use the equals
            // sign and semicolons as separators, we'll use colons and
            // ampersands for the individual state variables we store within a
            // single cookie value. Note that we encode the value of each
            // property in case it contains punctuation or other illegal
            // characters.
            var cookieval = "";
            var prop;

            for (prop in this) {
                // Ignore properties with names that begin with '$' and also
                // methods
                if ((prop.charAt(0) === '$') ||
                    ((typeof this[prop]) === 'function')) {
                    continue;
                }
                if (cookieval !== "") {
                    cookieval += '&';
                }
                cookieval += prop + ':' + encodeURIComponent(this[prop]);
            }

            // Now that we have the value of the cookie, put together the
            // complete cookie string, which includes the name and the various
            // attributes specified when the Cookie object was created
            var cookie = this.$name + '=' + cookieval;
            if (daysToLive || daysToLive === 0) {
                // IE only accepts "expires" not "max-age"
                var date = new Date();
                date.setTime(date.getTime() + (daysToLive * 24 * 60 * 60 * 1000));
                cookie += "; expires=" + date.toGMTString();
                cookie += "; max-age=" + (daysToLive * 24 * 60 * 60);
            }

            if (path) {
                cookie += "; path=" + path;
            }
            else {
                cookie += "; path=" + this.$path;
            }
            if (domain) {
                cookie += "; domain=" + domain;
            }
            if (secure) {
                cookie += "; secure";
            }

            // Now store the cookie by setting the magic Document.cookie
            // property
            document.cookie = cookie;
        };

        Cookie.prototype.storeForALongTime = function () {
            this.store(365 * 100);
        };


        /**
         * This function is the remove() method of the Cookie object; it deletes
         * the properties of the object and removes the cookie from the browser's
         * local store.
         *
         * The arguments to this function are all optional, but to remove a
         * cookie you must pass the same values you passed to store().
         */
        Cookie.prototype.remove = function (path, domain, secure) {
            var prop;

            // Delete the properties of the cookie
            for (prop in this) {
                if ((prop.charAt(0) !== '$') &&
                    (typeof this[prop] !== 'function')) {
                    delete this[prop];
                }
            }

            // Then, store the cookie with a lifetime of 0
            this.store(0, path, domain, secure);
        };


        // This factory function is exported to the namespace, instead of
        // exporting the constructor itself. We use a factory function to make
        // sure the "new" keyword always gets called.
        function cookieFactory(name, path) {
            return new Cookie(name, path);
        }

        // Export symbols to namespace
        var ns = common.cookie;
        ns.cookieFactory = cookieFactory;

    }
()); // End of function (closure). Now invoke it.
