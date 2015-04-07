/*
 * startup.js: Startup code for the Client-side JavaScript for the Pick Pack
 * application
 *
 */

/*
 * jshint declarations
 *
 */

/*global MochiKit, pickpack */

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


// Connect our "handleOnLoad" function to the window load event
MochiKit.Signal.connect(window, "onload", pickpack.event_handlers.handleOnLoad);
