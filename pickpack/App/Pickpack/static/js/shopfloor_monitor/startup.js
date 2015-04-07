/*
 * startup.js: Startup code for the Client-side JavaScript for the Shop Floor Monitor
 * application
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit, shopfloor_monitor */

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


// Connect our "handleOnLoad" function to the window load event
MochiKit.Signal.connect(window, "onload", shopfloor_monitor.event_handlers.handleOnLoad);
