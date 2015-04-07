"""
pickpack_common.py

Common, shared functions for the Pick Pack server


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""
import cgi, json

from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import pickpack_lowlevel_common
from Pickpack.pickpack_modules import pickpack_result_builders
from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules.warn.main import calculateShipmentWarnings

def getOrderNotesAndWarningCategories(carrier_code,
                                      packing_list,
                                      customer_number,
                                      #order_entry_initials,
                                      calcualted_order_weight,
                                      service_level,
                                      ship_to_state,
                                      ship_to_country,
                                      customer_sold_to_country,
                                      ctx = None,
                                     ):
    """
    Calculates what warning labels are required for the order (order notes).
    And, provides a list of the warning categories (TH0, CB0, SB1, etc.).

    ctx is an optional context object that can carry additional data from the
    web request.
    """
    (order_notes,
     ignore_inline_images,
     warning_categories,
    ) = _get_warning_info(carrier_code,
                          packing_list,
                          customer_number,
                          #order_entry_initials,
                          calcualted_order_weight,
                          service_level,
                          ship_to_state,
                          ship_to_country,
                          customer_sold_to_country,
                          ctx,
                         )

    return (order_notes,
            warning_categories,
           )

def getOrderNotesAndInlineImages(carrier_code,
                                 packing_list,
                                 customer_number,
                                 #order_entry_initials,
                                 calcualted_order_weight,
                                 service_level,
                                 ship_to_state,
                                 ship_to_country,
                                 customer_sold_to_country,
                                 ctx,
                                ):
    """
    Calculates and returns the warnings that the client should display to the
    user. Also returns inline image info for each row.
    """
    (order_notes,
     inline_images,
     ignore_warning_categories,
    ) = _get_warning_info(carrier_code,
                          packing_list,
                          customer_number,
                          #order_entry_initials,
                          calcualted_order_weight,
                          service_level,
                          ship_to_state,
                          ship_to_country,
                          customer_sold_to_country,
                          ctx,
                         )

    return (order_notes,
            inline_images,
           )

def _get_warning_info(carrier_code,
                      packing_list,
                      customer_number,
                      #order_entry_initials,
                      calcualted_order_weight,
                      service_level,
                      ship_to_state,
                      ship_to_country,
                      customer_sold_to_country,
                      ctx,
                     ):
    """
    Shared functionality
    """
    order_notes_components = []

    result = calculateShipmentWarnings(packing_list,
                                       carrier_code,
                                       customer_number,
                                       #order_entry_initials,
                                       calcualted_order_weight,
                                       service_level,
                                       ship_to_state,
                                       ship_to_country,
                                       customer_sold_to_country,
                                       ctx,
                                      )
    if result is not None:
        (warnings,
         inline_images,
         warning_categories
        ) = result

    for warning in warnings:
        if (warning.note_text is not None
            and warning.image_names is not None
           ):
            # Note: note_text might be a string, or it might be a tuple of
            # strings representing multiple lines of text.
            # image_names might be a string, or it might be a tuple of
            # strings containing the names of multiple images.
            order_notes_components.append(
                {'type' : 'text_and_image',
                 'content' : (warning.note_text,
                              warning.image_names,
                             ),
                }
            )
        elif warning.note_text is not None:
            order_notes_components.append(
                {'type' : 'text',
                 'content' : warning.note_text,
                }
            )
        elif warning.image_names is not None:
            order_notes_components.append(
                {'type' : 'image',
                 'content' : warning.image_names,
                }
            )
        else:
            raise pickpack_errors.ApplicationError("Error: Text and image both None.")

    if len(order_notes_components) == 0:
        order_notes = pickpack_constants.NO_DATA_FOUND

        # This order has no warnings, so no inline images are needed. Return a
        # list of all zeros to indicate that no inline images are needed.
        inline_images = (0, ) * len(packing_list)

        warning_categories = pickpack_constants.NO_DATA_FOUND
    else:
        builder = pickpack_result_builders.OrderNotesBuilder()
        builder.popup_time = 'beginning_and_end'
        #builder.popup_time = 'beginning'
        #builder.popup_time = 'end'
        builder.components = order_notes_components
        order_notes = builder.render()

        if inline_images is None:
            # We have order notes (e.g. an ecommerce order), but no warning
            # images to add to the packing list. Return a list of all zeros to
            # indicate that no inline images are needed.
            inline_images = (0, ) * len(packing_list)

    return (order_notes,
            inline_images,
            warning_categories,
           )

def validate_order(is_on_wm_hold,
                   order_status,
                   order_id,
                   service_level,
                   carrier_code,
                  ):
    """
    Generate error messages for various invalid order conditions.
    """

    if is_on_wm_hold:
        # Return WM hold error to client
        raise pickpack_errors.HandleableServerError("Order %s is on Warehouse Hold. Do not ship." % order_id.formatted_for_display)

    if order_status == '1':
        # Return order status error to client
        raise pickpack_errors.HandleableServerError("Order %s has not yet been picked." % order_id.formatted_for_display)

    if order_status == '3':
        # Return order status error to client
        raise pickpack_errors.HandleableServerError("Order %s has already been shipped." % order_id.formatted_for_display)

    if order_status == '9':
        # Return order status error to client
        raise pickpack_errors.HandleableServerError("Order %s is on hold. Do not ship." % order_id.formatted_for_display)

    if order_status != '2':
        # Return order status error to client
        raise pickpack_errors.HandleableServerError("Order %s has an invalid status: %s."  % (order_id.formatted_for_display, order_status))

    if service_level not in ('T', 'SS', 'S', 'N'):
        # Return service level error to client
        raise pickpack_errors.HandleableServerError("Order %s has an invalid service level: %s. Should be T, SS, S or N."  % (order_id.formatted_for_display, service_level))

    if not pickpack_lowlevel_common.isValidCarrierCode(carrier_code):
        # Return carrier code error to client
        raise pickpack_errors.HandleableServerError("Order %s has an invalid carrier code: %s."  % (order_id.formatted_for_display, carrier_code))

def truncateList(original_list,
                 max_size,
                 add_notification = True,
                ):
    """
    Truncate the list to max_size. If the list is truncated and add_notification
    is True, then append a string to the end of the list, that says how many
    more items there are in the original list.
    """
    if len(original_list) <= max_size:
        # Already smaller than or equal to the maximum. Return as-is.
        return original_list

    how_many_left_over = len(original_list) - max_size

    new_list = original_list[:max_size]

    if add_notification:
        new_list.append("... %s more" % how_many_left_over)

    return new_list

def getItemNotes(list_of_items,
                 function_to_call,
                 additional_keyword_arguments = None,
                ):
    """
    Returns a list of item notes, if any exist for any of the items passed in.
    """
    item_notes = {}
    for item in list_of_items:
        # POSSIBLE IMPROVEMENT Fetch item notes from the database instead.

        #if item.has_item_note == 0:
        #    continue
        #if item.has_item_note != 1:
        #    raise pickpack_errors.ApplicationError("Error: Invalid value for item.has_item_note. %s" % item.has_item_note)

        if additional_keyword_arguments is None:
            data = function_to_call(item.item_no)
        else:
            data = function_to_call(item.item_no,
                                    **additional_keyword_arguments      # No trailing comma allowed after **
                                   )
        if len(data) > 0:
            item_notes[item.item_no] = generateItemNote(item.item_no,
                                                        data,
                                                       )

    if len(item_notes) == 0:
        return pickpack_constants.NO_DATA_FOUND
    else:
        return item_notes

def generateItemNote(item_no,
                     data,
                    ):
    """
    Builds the item note text, html escaped.
    """
    # Pre-populate the note list with an informative header.
    note_list = ['Item Notes for %s' % item_no,
                 '',       # Blank line
                ]

    # The results of this note-building function will be inserted in to the web
    # page, using some JavaScript like this:
    #
    #   dom_element.inner_html = note_text_we_got_from_the_server
    #
    # I don't want unsafe characters in the notes to blow up my page, so I
    # escape any HTML-unfriendly characters using cgi.escape.
    note_list.extend(cgi.escape(note_row[0]) for note_row in data)
    return '\n'.join(note_list)


def dumpToJSON(data):
    """
    Formats the data as JSON.
    """
    if data is None:
        raise pickpack_errors.ApplicationError("Error: data is None.")
    return json.dumps(data)





#
#def executeQuery(transaction_cursor,
#                 sql,
#                 params = None,
#                ):
#    """
#    Execute a query operation on the cursor. If the operation fails, reconnect
#    to the database and retry a few times before raising an error.
#    """
#
#    try:
#        if params is None:
#            transaction_cursor.execute(sql)
#        else:
#            transaction_cursor.execute(sql, params)
#    except pyodbc.Error:
#        # POSSIBLE IMPROVEMENT -  reconnect
#
#
#
#    # pyodbc.Error: ('08S01', '[08S01] [IBM][iSeries Access ODBC Driver]Communication
#    # link failure. comm rc=8405 - CWBCO1047 - The iSeries server application
#    # disconnected the connection (8405) (SQLExecDirectW)')
#


# Another possible solution, if cp_reconnect = True doesn't work
#
# Question, if we use ReconnectingConnectionPool, should we still set
# cp_reconnect = True, or False, or doesn't matter?

# From here
# https://gist.github.com/powdahound/174056
#
#class ReconnectingConnectionPool(adbapi.ConnectionPool):
#    """Reconnecting adbapi connection pool for MySQL.
#
#    This class improves on the solution posted at
#    http://www.gelens.org/2008/09/12/reinitializing-twisted-connectionpool/
#    by checking exceptions by error code and only disconnecting the current
#    connection instead of all of them.
#
#    Also see:
#    http://twistedmatrix.com/pipermail/twisted-python/2009-July/020007.html
#
#    """
#    def _runInteraction(self, interaction, *args, **kw):
#        try:
#            return adbapi.ConnectionPool._runInteraction(self, interaction, *args, **kw)
#        #except MySQLdb.OperationalError, e:
#        except pyodbc.SomeOdbcError as e:
#            if e[0] not in (2006, 2013):
#                raise
#            #log.msg("RCP: got error %s, retrying operation" %(e))
#            conn = self.connections.get(self.threadID())
#            self.disconnect(conn)
#            # try the interaction again
#            return adbapi.ConnectionPool._runInteraction(self, interaction, *args, **kw)
#
#
#
#
# For now, I just set a cron job to restart the twisted server process every day
# at 4:01 am.













#
