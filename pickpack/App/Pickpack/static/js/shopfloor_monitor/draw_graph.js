/*
 * draw_graph.js:Utility functions for
 * the client-side JavaScript for the Shop Floor Monitor application.
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
         unused: strict,
         strict: true,
         trailing: true,

         browser: true

*/


// Create namespace if it does not yet exist
var shopfloor_monitor;

if (!shopfloor_monitor) {
    shopfloor_monitor = {};
}
else if (typeof shopfloor_monitor !== "object") {
    throw new Error("shopfloor_monitor already exists, and is not an object");
}

if (shopfloor_monitor.draw_graph) {
    throw new Error("shopfloor_monitor.draw_graph already exists");
}
else {
    shopfloor_monitor.draw_graph = {};
}


(
    function () {
        'use strict';

        function drawOneUp(data, backorder) {
            if (backorder) {
                one_up_backorder_renderer.renderChart(data);
            }
            else {
                one_up_ordinary_renderer.renderChart(data);
            }
        }

        function drawFourUp(data, backorder, narrow) {
            var wcc_renderer;
            var parts_renderer;
            var both_renderer;
            var all_renderer;

            if (narrow) {
                if (backorder) {
                    wcc_renderer = narrow_wcc_backorder_renderer;
                    parts_renderer = narrow_parts_backorder_renderer;
                    both_renderer = narrow_both_backorder_renderer;
                    all_renderer = narrow_all_backorder_renderer;
                }
                else {
                    wcc_renderer = narrow_wcc_ordinary_renderer;
                    parts_renderer = narrow_parts_ordinary_renderer;
                    both_renderer = narrow_both_ordinary_renderer;
                    all_renderer = narrow_all_ordinary_renderer;
                }
            }
            else {
                if (backorder) {
                    wcc_renderer = small_wcc_backorder_renderer;
                    parts_renderer = small_parts_backorder_renderer;
                    both_renderer = small_both_backorder_renderer;
                    all_renderer = small_all_backorder_renderer;
                }
                else {
                    wcc_renderer = small_wcc_ordinary_renderer;
                    parts_renderer = small_parts_ordinary_renderer;
                    both_renderer = small_both_ordinary_renderer;
                    all_renderer = small_all_ordinary_renderer;
                }
            }

            wcc_renderer.renderChart(data.wcc);
            parts_renderer.renderChart(data.parts);
            both_renderer.renderChart(data.both);
            all_renderer.renderChart(data.all);
        }

        // This is a base object from which other objects can inherit.
        function ChartRenderer(backorder) {

            this.backorder = backorder;

            // Factors
            //this.SHADOW_SKEW_FACTOR = 0.6;
            //this.SHADOW_SCALE_FACTOR = 0.2;

            // Constants
            this.ALIGN_RIGHT = "right";

            // Bright theme
            // See bottom of file for other color variants
            this.PURPLE          = "#671fed";
            this.DARK_PURPLE     = "#27026b";
            this.LIGHT_PURPLE    = "#c3aded";
            this.ORANGE          = "#ed671f";
            this.DARK_ORANGE     = "#9c3803";
            this.LIGHT_ORANGE    = "#eda57e";
            this.GREEN           = "#a5ed1f";
            this.DARK_GREEN      = "#669c03";
            this.LIGHT_GREEN     = "#d7edad";
            this.BLUE            = "#1fa5ed";
            this.DARK_BLUE       = "#444478";
            this.LIGHT_BLUE      = "#add7ed";
            this.WHITE           = "#ffffff";
            this.TEXT_COLOR      = "#606060";  // dark gray
            //this.SHADOW_COLOR    = "rgba(85%, 85%, 85%, 0.5)";
            this.TEXT_FONT1      = "bold ";              // First part of our font specifier string.
            this.TEXT_FONT2      = "pt sans-serif";      // Second part of our font specifier string.
                                                         // Later, we will build a font specifier string
                                                         // by concatenating these two strings along with
                                                         // an integer specifying font size in points.
        }

        ChartRenderer.prototype.renderChart = function (data, caption) {
            if (this.backorder) {
                this.renderBackorderChart(data, caption);
            }
            else {
                this.renderOrdinaryChart(data, caption);
            }
        };

        ChartRenderer.prototype.renderOrdinaryChart = function (data, caption) {
            var canvas = MochiKit.DOM.getElement(this.canvas_id);
            var context = canvas.getContext("2d");
            this.clear_canvas(canvas, context, false);

            // Flip the grid upside down, so it matches the cartesian
            // coordiantes I'm used to.
            context.translate(0, canvas.height - this.BAR_BOTTOM);
            context.scale(1, -1);

            // Build a css-style font specifier string
            var font_specifier = this.TEXT_FONT1 + this.FONT_SIZE + this.TEXT_FONT2;

            var today_sure_can_ship_tomorrow =          data.today_sure_can_ship_tomorrow_ready_to_print +
                                                        data.today_sure_can_ship_tomorrow_pick_slip_printed;
            var today_sure_should_ship_today =          data.today_sure_should_ship_today_ready_to_print +
                                                        data.today_sure_should_ship_today_pick_slip_printed;
            var signature_service_can_ship_tomorrow =   data.signature_service_can_ship_tomorrow_ready_to_print +
                                                        data.signature_service_can_ship_tomorrow_pick_slip_printed;
            var signature_service_should_ship_today =   data.signature_service_should_ship_today_ready_to_print +
                                                        data.signature_service_should_ship_today_pick_slip_printed;
            var service_files_should_ship_today =       data.service_files_should_ship_today_ready_to_print +
                                                        data.service_files_should_ship_today_pick_slip_printed;
            var normal_can_ship_tomorrow =              data.normal_can_ship_tomorrow_ready_to_print +
                                                        data.normal_can_ship_tomorrow_pick_slip_printed;
            var normal_should_ship_today =              data.normal_should_ship_today_ready_to_print +
                                                        data.normal_should_ship_today_pick_slip_printed;

            if (shopfloor_monitor.globals.optionController.showUntil === shopfloor_monitor.constants.SHOW_UNTIL_SCALE) {
                today_sure_can_ship_tomorrow +=         data.today_sure_can_ship_tomorrow_packed;
                today_sure_should_ship_today +=         data.today_sure_should_ship_today_packed;
                signature_service_can_ship_tomorrow +=  data.signature_service_can_ship_tomorrow_packed;
                signature_service_should_ship_today +=  data.signature_service_should_ship_today_packed;
                service_files_should_ship_today +=      data.service_files_should_ship_today_packed;
                normal_can_ship_tomorrow +=             data.normal_can_ship_tomorrow_packed;
                normal_should_ship_today +=             data.normal_should_ship_today_packed;
            }

            // Scale the dimensions
            var t_ghost_bar_height = Math.round(today_sure_can_ship_tomorrow * this.BAR_HEIGHT_FACTOR);
            var t_solid_bar_height = Math.round(today_sure_should_ship_today * this.BAR_HEIGHT_FACTOR);
            var ss_ghost_bar_height = Math.round(signature_service_can_ship_tomorrow * this.BAR_HEIGHT_FACTOR);
            var ss_solid_bar_height = Math.round(signature_service_should_ship_today * this.BAR_HEIGHT_FACTOR);
            var s_solid_bar_height = Math.round(service_files_should_ship_today * this.BAR_HEIGHT_FACTOR);
            var n_ghost_bar_height = Math.round(normal_can_ship_tomorrow * this.BAR_HEIGHT_FACTOR);
            var n_solid_bar_height = Math.round(normal_should_ship_today * this.BAR_HEIGHT_FACTOR);
            var t_bug_height = Math.round(data.today_sure_should_ship_today_ready_to_print * this.BAR_HEIGHT_FACTOR);
            var ss_bug_height = Math.round(data.signature_service_should_ship_today_ready_to_print * this.BAR_HEIGHT_FACTOR);
            var s_bug_height = Math.round(data.service_files_should_ship_today_ready_to_print * this.BAR_HEIGHT_FACTOR);
            var n_bug_height = Math.round(data.normal_should_ship_today_ready_to_print * this.BAR_HEIGHT_FACTOR);

            // Draw the bars
            // Today Sure
            var t_top = this.draw_bar(context, t_solid_bar_height, 0, this.PURPLE);
            this.draw_ghost_bar(context, t_ghost_bar_height, 0, this.PURPLE, t_top);
            // Signature Service
            var ss_top = this.draw_bar(context, ss_solid_bar_height, 1, this.ORANGE);
            this.draw_ghost_bar(context, ss_ghost_bar_height, 1, this.ORANGE, ss_top);
            // Service Files
            this.draw_bar(context, s_solid_bar_height, 2, this.GREEN);
            // Normal
            var n_top = this.draw_bar(context, n_solid_bar_height, 3, this.BLUE);
            this.draw_ghost_bar(context, n_ghost_bar_height, 3, this.BLUE, n_top);

            if (shopfloor_monitor.globals.optionController.readyToPickHighlight === shopfloor_monitor.constants.READY_HIGHLIGHT_BUG) {
                // We draw "bugs" (little triangle indicators) on the side of
                // the bars, to show how many of the items in that bar are
                // waiting to be printed.
                this.draw_print_status_bug(context, t_bug_height, 0);
                this.draw_print_status_bug(context, ss_bug_height, 1);
                this.draw_print_status_bug(context, s_bug_height, 2);
                this.draw_print_status_bug(context, n_bug_height, 3);
            }
            else if (shopfloor_monitor.globals.optionController.readyToPickHighlight === shopfloor_monitor.constants.READY_HIGHLIGHT_STRIPE) {
                // We draw stripes on top of the bars, to show how many of the
                // items in that bar are waiting to be printed.
                this.draw_highlighted_bar(context, t_bug_height, 0, this.PURPLE, this.LIGHT_PURPLE, false);
                this.draw_highlighted_bar(context, ss_bug_height, 1, this.ORANGE, this.DARK_ORANGE, false);
                this.draw_highlighted_bar(context, s_bug_height, 2, this.GREEN, this.DARK_GREEN, false);
                this.draw_highlighted_bar(context, n_bug_height, 3, this.BLUE, this.DARK_BLUE, false);
            }

            // These white triangles will be visible on top of the solid bars if
            // they extend past the top of the canvas. Ghost bars are not
            // affected.
            var t_total_solid_bar_height = t_solid_bar_height;
            var ss_total_solid_bar_height = ss_solid_bar_height;
            var s_total_solid_bar_height = s_solid_bar_height;
            var n_total_solid_bar_height = n_solid_bar_height;
            var maximum_bar_height = canvas.height - this.BAR_BOTTOM;
            if (t_total_solid_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 0);
            }
            if (ss_total_solid_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 1);
            }
            if (s_total_solid_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 2);
            }
            if (n_total_solid_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 3);
            }

            // Draw the text labels
            // Go back to ordinary transform (y=0 at top). Text will be flipped
            // if we use the current flipped transform. However, translate the
            // transform downwards, so the labels are below the bars.
            context.save();
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.translate(0, canvas.height - this.LABEL_Y_POSITION);
            context.fillStyle = this.TEXT_COLOR;
            context.font = font_specifier;
            this.draw_label("T",                                    context, 0, 1);
            this.draw_label(today_sure_can_ship_tomorrow,           context, 0, 0, this.ALIGN_RIGHT);
            this.draw_label(today_sure_should_ship_today,           context, 0, 1, this.ALIGN_RIGHT);
            this.draw_label("SS",                                   context, 1, 1);
            this.draw_label(signature_service_can_ship_tomorrow,    context, 1, 0, this.ALIGN_RIGHT);
            this.draw_label(signature_service_should_ship_today,    context, 1, 1, this.ALIGN_RIGHT);
            this.draw_label("S",                                    context, 2, 1);
            this.draw_label(service_files_should_ship_today,        context, 2, 1, this.ALIGN_RIGHT);
            this.draw_label("N",                                    context, 3, 1);
            this.draw_label(normal_can_ship_tomorrow,               context, 3, 0, this.ALIGN_RIGHT);
            this.draw_label(normal_should_ship_today,               context, 3, 1, this.ALIGN_RIGHT);
            context.restore();

            // Draw the workstation type caption
            // Go back to ordinary transform (y=0 at top). Text will be flipped
            // if we use the current flipped transform. Translate the transform
            // upwards, so the caption will be above the bars.
            context.save();
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.translate(0, this.LABEL_Y_POSITION);
            context.fillStyle = this.TEXT_COLOR;
            context.font = font_specifier;
            context.fillText(caption, 0, 0);
            context.restore();
        };

        ChartRenderer.prototype.renderBackorderChart = function (data, caption) {
            var canvas = MochiKit.DOM.getElement(this.canvas_id);
            var context = canvas.getContext("2d");
            this.clear_canvas(canvas, context, false);

            // Flip the grid upside down, so it matches the cartesian
            // coordiantes I'm used to.
            context.translate(0, canvas.height - this.BAR_BOTTOM);
            context.scale(1, -1);

            // Build a css-style font specifier string
            var font_specifier = this.TEXT_FONT1 + this.FONT_SIZE + this.TEXT_FONT2;

            //{"normal_backorder_packed": 0,
            // "signature_service_backorder_pick_slip_printed": 16,
            // "today_sure_backorder_packed": 0,
            // "today_sure_backorder_ready_to_print": 5,
            // "service_files_backorder_ready_to_print": 6,
            // "normal_backorder_pick_slip_printed": 1,
            // "normal_backorder_ready_to_print": 4,
            // "service_files_backorder_pick_slip_printed": 14,
            // "service_files_backorder_packed": 1,
            // "signature_service_backorder_packed": 3,
            // "signature_service_backorder_ready_to_print": 57,
            // "today_sure_backorder_pick_slip_printed": 1}


            var today_sure_backorder =          data.today_sure_backorder_ready_to_print +
                                                data.today_sure_backorder_pick_slip_printed;
            var signature_service_backorder =   data.signature_service_backorder_ready_to_print +
                                                data.signature_service_backorder_pick_slip_printed;
            var service_files_backorder =       data.service_files_backorder_ready_to_print +
                                                data.service_files_backorder_pick_slip_printed;
            var normal_backorder =              data.normal_backorder_ready_to_print +
                                                data.normal_backorder_pick_slip_printed;

            if (shopfloor_monitor.globals.optionController.showUntil === shopfloor_monitor.constants.SHOW_UNTIL_SCALE) {
                today_sure_backorder +=         data.today_sure_backorder_packed;
                signature_service_backorder +=  data.signature_service_backorder_packed;
                service_files_backorder +=      data.service_files_backorder_packed;
                normal_backorder +=             data.normal_backorder_packed;
            }

            // Scale the dimensions
            var t_stripe_bar_height = Math.round(today_sure_backorder * this.BAR_HEIGHT_FACTOR);
            var ss_stripe_bar_height = Math.round(signature_service_backorder * this.BAR_HEIGHT_FACTOR);
            var s_stripe_bar_height = Math.round(service_files_backorder * this.BAR_HEIGHT_FACTOR);
            var n_stripe_bar_height = Math.round(normal_backorder * this.BAR_HEIGHT_FACTOR);

            // Draw the bars
            this.draw_highlighted_bar(context, t_stripe_bar_height, 0, this.PURPLE, this.LIGHT_PURPLE, true);
            this.draw_highlighted_bar(context, ss_stripe_bar_height, 1, this.ORANGE, this.DARK_ORANGE, true);
            this.draw_highlighted_bar(context, s_stripe_bar_height, 2, this.GREEN, this.DARK_GREEN, true);
            this.draw_highlighted_bar(context, n_stripe_bar_height, 3, this.BLUE, this.DARK_BLUE, true);

            // These white triangles will be visible on top of the stripe bars
            // if they extend past the top of the canvas.
            var maximum_bar_height = canvas.height - this.BAR_BOTTOM;
            if (t_stripe_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 0);
            }
            if (ss_stripe_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 1);
            }
            if (s_stripe_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 2);
            }
            if (n_stripe_bar_height > maximum_bar_height) {
                this.draw_white_triangles(context, 3);
            }

            // Draw the text labels
            // Go back to ordinary transform (y=0 at top). Text will be flipped
            // if we use the current flipped transform. However, translate the
            // transform downwards, so the labels are below the bars.
            context.save();
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.translate(0, canvas.height - this.LABEL_Y_POSITION);
            context.fillStyle = this.TEXT_COLOR;
            context.font = font_specifier;
            this.draw_label("T",                                        context, 0, 0);
            this.draw_label(today_sure_backorder,                  context, 0, 0, this.ALIGN_RIGHT);
            this.draw_label("SS",                                       context, 1, 0);
            this.draw_label(signature_service_backorder,           context, 1, 0, this.ALIGN_RIGHT);
            this.draw_label("S",                                        context, 2, 0);
            this.draw_label(service_files_backorder,               context, 2, 0, this.ALIGN_RIGHT);
            this.draw_label("N",                                        context, 3, 0);
            this.draw_label(normal_backorder,                      context, 3, 0, this.ALIGN_RIGHT);
            context.restore();

            // Draw the workstation type caption
            // Go back to ordinary transform (y=0 at top). Text will be flipped
            // if we use the current flipped transform. Translate the transform
            // upwards, so the caption will be above the bars.
            context.save();
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.translate(0, this.LABEL_Y_POSITION);
            context.fillStyle = this.TEXT_COLOR;
            context.font = font_specifier;
            context.fillText(caption + ' - Backorder', 0, 0);
            context.restore();
        };

        ChartRenderer.prototype.draw_bar = function (context,
                                                     bar_height,
                                                     x_index,
                                                     fill_style,
                                                     y_index  /* optional, default 0 */) {
            if (y_index === undefined) {
                y_index = 0;
            }

            context.save();
            context.translate(this.x_pos_from_x_index(x_index), y_index);
            context.fillStyle = fill_style;
            context.fillRect(0,
                             0,
                             this.BAR_WIDTH,
                             bar_height
                            );

            context.restore();
            // Return the position of the top of the bar.
            return y_index + bar_height;
        };

        ChartRenderer.prototype.draw_ghost_bar = function (context,
                                                           bar_height,
                                                           x_index,
                                                           color,
                                                           y_index) {
            // Change the rendering of the ghost box at small numbers. This
            // keeps it from being confused with a regular box. Otherwise, at
            // height less than seven, the ghost box closes up and looks just
            // like a regular box.
            if (bar_height <= (this.GHOST_LINE_WIDTH * 2)) {
                // Draw a regular (closed-up) bar instead. Draw it in a lighter color
                this.draw_bar(context,
                              bar_height,
                              x_index,
                              this.lighten_color(color),
                              y_index + this.GHOST_VERTICAL_OFFSET);
            }
            else {
                context.strokeStyle = color;
                context.lineWidth = this.GHOST_LINE_WIDTH;
                context.strokeRect((this.x_pos_from_x_index(x_index)) + (context.lineWidth / 2),
                                   y_index + this.GHOST_VERTICAL_OFFSET + (context.lineWidth / 2),
                                   this.BAR_WIDTH - context.lineWidth,
                                   bar_height - context.lineWidth
                                  );
            }
        };

        ChartRenderer.prototype.draw_highlighted_bar = function (context,
                                                                 bar_height,
                                                                 x_index,
                                                                 background_color,
                                                                 stripe_color,
                                                                 diagonal_stripes,
                                                                 y_index /* optional, default 0 */) {
            if (y_index === undefined) {
                y_index = 0;
            }
            var fill_style = this.stripe_fill_from_color(context,
                                                         background_color,
                                                         stripe_color,
                                                         diagonal_stripes);
            return this.draw_bar(context,
                                 bar_height,
                                 x_index,
                                 fill_style,
                                 y_index);
        };

        ChartRenderer.prototype.lighten_color = function (color) {
            // Returns the light version of the supplied color
            if (color === this.PURPLE) {
                return this.LIGHT_PURPLE;
            }
            else if (color === this.ORANGE) {
                return this.LIGHT_ORANGE;
            }
            else if (color === this.BLUE) {
                return this.LIGHT_BLUE;
            }
            //else if (color === this.SHADOW_COLOR) {
            //    return this.SHADOW_COLOR;
            //}
            else {
                throw new Error("Can't lighten this color " + color);
            }
        };

        ChartRenderer.prototype.stripe_fill_from_color = function (main_context,
                                                                   background_color,
                                                                   stripe_color,
                                                                   diagonal_stripes) {
            // Returns a CanvasPattern object representing a striped version of
            // the supplied color.

            var stripe_width;
            var offscreen_size;

            if (diagonal_stripes) {
                stripe_width = this.DIAGONAL_STRIPE_WIDTH;
            }
            else {
                stripe_width = this.VERTICAL_STRIPE_WIDTH;
            }

            offscreen_size = stripe_width * 2;

            // Make an invisible html canvas where we can build up the pattern.
            var offscreen = document.createElement("canvas");
            offscreen.width = offscreen.height = offscreen_size;
            var offscreen_context = offscreen.getContext("2d");
            offscreen_context.fillStyle = background_color;

            if (diagonal_stripes) {
                // Slant the stripes
                offscreen_context.translate(stripe_width, 0);
                offscreen_context.transform(1, 0, -1, 1, 0, 0);

                // Draw the pattern on our invisible canvas.
                offscreen_context.fillRect(0, 0, stripe_width, offscreen_size);
                offscreen_context.fillRect(stripe_width * 2, 0, stripe_width, offscreen_size);
                offscreen_context.fillStyle = stripe_color;
                offscreen_context.fillRect(-stripe_width, 0, stripe_width, offscreen_size);
                offscreen_context.fillRect(stripe_width, 0, stripe_width, offscreen_size);
            }
            else {
                // Draw the pattern on our invisible canvas.
                offscreen_context.fillRect(0, 0, stripe_width, offscreen_size);
                offscreen_context.fillStyle = stripe_color;
                offscreen_context.fillRect(stripe_width, 0, stripe_width, offscreen_size);
            }

            // Use the main context to create a CanvasPattern object. Return the
            // new CanvasPattern object.
            return main_context.createPattern(offscreen, "repeat");
        };

        ChartRenderer.prototype.draw_label = function (text,
                                                       context,
                                                       x_index,
                                                       line_index,
                                                       h_align) {

            var x_origin_shift;
            if (h_align === this.ALIGN_RIGHT) {
                x_origin_shift = this.BAR_WIDTH - context.measureText(text).width;
            } else {
                x_origin_shift = 0;
            }

            var y_offset = line_index * this.LABEL_LINE_HEIGHT;

            context.fillText(text,
                             (this.x_pos_from_x_index(x_index)) + x_origin_shift,
                             y_offset);
        };

        ChartRenderer.prototype.draw_white_triangles = function (context,
                                                                 x_index) {
            var x_pos = this.x_pos_from_x_index(x_index);
            var number_of_triangles;
            //if (shopfloor_monitor.globals.optionController.diagonalStripes) {
            //    // A slightly larger triangle looks better against the fatter
            //    // diagonal stripes.
            //    number_of_triangles = 4;
            //}
            //else {
            //    number_of_triangles = 5;
            //}
            number_of_triangles = 5;
            var triangle_size = this.BAR_WIDTH / number_of_triangles;

            context.save();
            context.setTransform(1, 0, 0, 1, 0, 0);

            /* jshint plusplus: false */
            for (var i = 0; i < number_of_triangles; i++) {
                this.draw_white_triangle(context,
                                         x_pos,
                                         0,
                                         triangle_size);
                x_pos += triangle_size;
            }

            context.restore();
        };

        ChartRenderer.prototype.draw_white_triangle = function (context,
                                                                x_pos,
                                                                y_pos,
                                                                triangle_size) {
            context.fillStyle = this.WHITE;
            context.beginPath();
            context.moveTo(x_pos, y_pos);
            context.lineTo(x_pos + triangle_size, y_pos);
            context.lineTo(x_pos + Math.round(triangle_size / 2), y_pos + Math.round(triangle_size / 2));
            context.lineTo(x_pos, y_pos);
            context.fill();
        };

        ChartRenderer.prototype.draw_dark_triangle = function (context,
                                                               x_pos,
                                                               y_pos,
                                                               triangle_size) {
            context.fillStyle = this.TEXT_COLOR;
            context.beginPath();
            context.moveTo(x_pos, y_pos);
            context.lineTo(x_pos + Math.round(triangle_size / 2), y_pos + Math.round(triangle_size / 2));
            context.lineTo(x_pos + Math.round(triangle_size / 2), y_pos - Math.round(triangle_size / 2));
            context.lineTo(x_pos, y_pos);
            context.fill();
        };

        ChartRenderer.prototype.draw_print_status_bug = function (context,
                                                                  bug_height,
                                                                  x_index) {
            var x_pos = this.x_pos_from_x_index(x_index) + this.BAR_WIDTH;
            this.draw_dark_triangle(context,
                                    x_pos,
                                    bug_height,
                                    this.BUG_SIZE);
        };

        ChartRenderer.prototype.x_pos_from_x_index = function (x_index) {
            return (this.BAR_WIDTH + this.BAR_GAP) * x_index;
        };

        ChartRenderer.prototype.clear_canvas = function (canvas,
                                                         context,
                                                         preserve_transform) {
            // Clear the canvas

            if (preserve_transform) {
                // Store the current transformation matrix
                context.save();
            }

            // Use the identity matrix while clearing the canvas
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.clearRect(0, 0, canvas.width, canvas.height);

            if (preserve_transform) {
                // Restore the saved transformation matrix
                context.restore();
            }
        };


        function OneUpChartRenderer(backorder) {
            // Call the constructor of the base object
            ChartRenderer.call(this, backorder);
            this.canvas_id = "sfmo_canvas_1up";

            // Factors
            this.BAR_HEIGHT_FACTOR = 1;

            // Pixel and point dimensions
            this.BAR_BOTTOM = 120;
            this.BAR_WIDTH = shopfloor_monitor.constants.ONE_UP_BAR_WIDTH;
            this.VERTICAL_STRIPE_WIDTH = 15;
            this.DIAGONAL_STRIPE_WIDTH = 36;
            this.BAR_GAP = shopfloor_monitor.constants.ONE_UP_BAR_GAP;
            this.BAR_GAP = 110;
            this.GHOST_VERTICAL_OFFSET = 2;
            this.GHOST_LINE_WIDTH = 3;
            this.LABEL_Y_POSITION = 70;
            this.LABEL_LINE_HEIGHT = 46;
            this.FONT_SIZE = "30";         // in points
            this.BUG_SIZE = 20;

        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript. POSSIBLE IMPROVEMENT get rid of inheritance, structure this some other
        // way.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        OneUpChartRenderer.prototype = new ChartRenderer();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        OneUpChartRenderer.prototype.constructor = OneUpChartRenderer;

        OneUpChartRenderer.prototype.renderChart = function (data) {
            // Delegate to the base class
            var caption = shopfloor_monitor.utility_functions.getCurrentCaption();
            ChartRenderer.prototype.renderChart.call(this, data, caption);
        };


        function FourUpChartRenderer(workstation, narrow, backorder) {
            // Call the constructor of the base object
            ChartRenderer.call(this, backorder);
            var canvas_number;
            var wide_narrow;

            if (narrow) {
                wide_narrow = "narrow_";

                // Factors
                this.BAR_HEIGHT_FACTOR = 0.44;

                // Pixel and point dimensions
                this.BAR_BOTTOM = 53;
                this.BAR_WIDTH = 70;
                this.VERTICAL_STRIPE_WIDTH = 7;
                this.DIAGONAL_STRIPE_WIDTH = 16;
                this.BAR_GAP = 39;
                this.GHOST_VERTICAL_OFFSET = 2;
                this.GHOST_LINE_WIDTH = 2;
                this.LABEL_Y_POSITION = 30;
                this.LABEL_LINE_HEIGHT = 20;
                this.FONT_SIZE = "13";         // in points
                this.BUG_SIZE = 10;
            }
            else {
                wide_narrow = "";

                // Factors
                this.BAR_HEIGHT_FACTOR = 0.66;

                // Pixel and point dimensions
                this.BAR_BOTTOM = 80;
                this.BAR_WIDTH = 100;
                this.VERTICAL_STRIPE_WIDTH = 10;
                this.DIAGONAL_STRIPE_WIDTH = 24;
                this.BAR_GAP = 68;
                this.GHOST_VERTICAL_OFFSET = 2;
                this.GHOST_LINE_WIDTH = 2;
                this.LABEL_Y_POSITION = 46;
                this.LABEL_LINE_HEIGHT = 30;
                this.FONT_SIZE = "20";         // in points
                this.BUG_SIZE = 14;
            }

            switch (workstation) {
                case shopfloor_monitor.constants.WORKSTATIONS.wcc:
                    canvas_number = "1";
                    this.caption = shopfloor_monitor.constants.WORKSTATION_CAPTIONS.wcc;
                    break;
                case shopfloor_monitor.constants.WORKSTATIONS.parts:
                    canvas_number = "2";
                    this.caption = shopfloor_monitor.constants.WORKSTATION_CAPTIONS.parts;
                    break;
                case shopfloor_monitor.constants.WORKSTATIONS.both:
                    canvas_number = "3";
                    this.caption = shopfloor_monitor.constants.WORKSTATION_CAPTIONS.both;
                    break;
                case shopfloor_monitor.constants.WORKSTATIONS.all:
                    canvas_number = "4";
                    this.caption = shopfloor_monitor.constants.WORKSTATION_CAPTIONS.all;
                    break;
            }

            this.canvas_id = "sfmo_canvas_4up_" + wide_narrow + canvas_number;

        }
        // Crazy extra stuff we need to do to make classical inheritance work in
        // JavaScript. POSSIBLE IMPROVEMENT get rid of inheritance, structure this some other
        // way.

        // Explicitly create our prototype, and make our prototype be the base
        // object. Otherwise, we get Object.prototype as our prototype.
        FourUpChartRenderer.prototype = new ChartRenderer();

        // Also, we have to manually assign the prototype.constructor property
        // to be the derived object's constructor, not the base object's
        // constructor.
        FourUpChartRenderer.prototype.constructor = FourUpChartRenderer;

        FourUpChartRenderer.prototype.renderChart = function (data) {
            // Delegate to the base class
            ChartRenderer.prototype.renderChart.call(this, data, this.caption);
        };



        // Here we create all of the objects we need. We only create the objects
        // once.
        var one_up_ordinary_renderer = new OneUpChartRenderer(false);
        var small_wcc_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.wcc,
                                                                  false,
                                                                  false);
        var small_parts_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.parts,
                                                                    false,
                                                                    false);
        var small_both_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.both,
                                                                   false,
                                                                   false);
        var small_all_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.all,
                                                                  false,
                                                                  false);
        var narrow_wcc_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.wcc,
                                                                   true,
                                                                   false);
        var narrow_parts_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.parts,
                                                                     true,
                                                                     false);
        var narrow_both_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.both,
                                                                    true,
                                                                    false);
        var narrow_all_ordinary_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.all,
                                                                   true,
                                                                   false);
        var one_up_backorder_renderer = new OneUpChartRenderer(true);
        var small_wcc_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.wcc,
                                                                   false,
                                                                   true);
        var small_parts_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.parts,
                                                                     false,
                                                                     true);
        var small_both_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.both,
                                                                    false,
                                                                    true);
        var small_all_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.all,
                                                                   false,
                                                                   true);
        var narrow_wcc_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.wcc,
                                                                    true,
                                                                    true);
        var narrow_parts_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.parts,
                                                                      true,
                                                                      true);
        var narrow_both_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.both,
                                                                     true,
                                                                     true);
        var narrow_all_backorder_renderer = new FourUpChartRenderer(shopfloor_monitor.constants.WORKSTATIONS.all,
                                                                    true,
                                                                    true);

        // Export symbols to namespace
        var ns = shopfloor_monitor.draw_graph;
        ns.drawOneUp = drawOneUp;
        ns.drawFourUp = drawFourUp;

    }
()); // End of function (closure). Now invoke it.







// Mixins
// from http://javascriptweblog.wordpress.com/2011/05/31/a-fresh-look-at-javascript-mixins/
//
//      var asCircle = function() {
//        this.area = function() {
//          return Math.PI * this.radius * this.radius;
//        };
//        this.grow = function() {
//          this.radius++;
//        };
//        this.shrink = function() {
//          this.radius--;
//        };
//        return this;
//      };
//
//      var Circle = function(radius) {
//          this.radius = radius;
//      };
//      asCircle.call(Circle.prototype);
//      var circle1 = new Circle(5);
//      circle1.area(); //78.54






// Color notes
//
//purple
//8020E0 - Chihuly fluorine purple (609030 or 406020 are greens 180 degrees away from this purple)
//         or 80E020
//
//
//orange
//EE6A1E
//D16E19
//C06000 burnt pure orange (0060C0 opposite blue)
//
//
//green
//406020 - priiiimary
//
//blue
//143A6A - needs to be lighter
//
//
//
//
//
//My Colourlovers palettes
//
//Dark theme
//purple 4a1847
//orange 993400
//green 006605
//blue 005f9d
//charcoal blue/black, for text 16161f
//
//
//Bright theme
//purple 671fed
//orange ed671f
//green a5ed1f
//blue 1fa5ed
//charcoal blue/black, for text 16161f
//
