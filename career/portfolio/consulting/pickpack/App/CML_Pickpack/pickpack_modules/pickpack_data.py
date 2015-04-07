"""
pickpack_data.py

Data access for the Pick Pack server


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""


import decimal

from twisted.internet import defer
from twisted.enterprise import adbapi

from CML_Common.utility import utl_aplus

from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_common
from CML_Pickpack.pickpack_modules import pickpack_result_builders
from CML_Pickpack.pickpack_modules import pickpack_errors
from CML_Pickpack.pickpack_modules import pickpack_utility_classes

# Module-level variables
M_mock_data = None
M_dbpool = None
M_dbpool_for_update = None
M_custom_library = None
M_procedure_library = None

def connectToData(con_string,
                  con_string_for_update,
                  use_which_data,
                  custom_library,
                  procedure_library,
                 ):
    """
    Connects the twisted.adbapi.ConnectionPool object to the proper database.
    Also sets the M_mock_data flag.
    """
    global M_mock_data                  # pylint: disable=W0603
    global M_dbpool                     # pylint: disable=W0603
    global M_dbpool_for_update          # pylint: disable=W0603
    global M_custom_library      # pylint: disable=W0603
    global M_procedure_library   # pylint: disable=W0603
    if use_which_data == pickpack_constants.MOCK_DATA:
        M_mock_data = True
        M_dbpool = None
        M_dbpool_for_update = None
        M_custom_library = None
        M_procedure_library = None
    else:
        M_mock_data = False
        M_dbpool = adbapi.ConnectionPool("pyodbc",
                                         con_string,
                                         cp_reconnect = True,
                                        )
        M_dbpool_for_update = adbapi.ConnectionPool("pyodbc",
                                                    con_string_for_update,
                                                    cp_reconnect = True,
                                                   )
        M_custom_library = custom_library
        M_procedure_library = procedure_library

def getPackingList_deferred(order_id,
                            ctx,
                           ):
    """
    Start the process of reading packing list data from the server. Return a
    deferred.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.getPackingList_deferred(order_id,
                                                          ctx,
                                                         )

    return M_dbpool.runInteraction(getPackingList_transaction_wrapper,
                                   order_id,
                                   M_custom_library,
                                   ctx,
                                  )

def getPackingList_transaction_wrapper(transaction_cursor,
                                       order_id,
                                       custom_library,
                                       ctx,
                                      ):
    """
    A wrapper for all the transactional operations that need to happen when
    getting packing list data from the server. Runs under the runInteraction
    transaction manager, from Twisted.adbapi.ConnectionPool. Returns packing
    list data (not a deferred).
    """
    # transaction_cursor is a (lightly wrapped) instance of pyodbc.cursor. This
    # will run in a thread; therefore, inside this function, we can use blocking
    # calls (e.g. cursor.execute) instead of M_dbpool.runOperation.

    builder = pickpack_result_builders.PackingListBuilder()
    builder.order_number = order_id.number
    builder.order_generation = order_id.generation

    order_head_data = getOrderHeadData(transaction_cursor,
                                       order_id,
                                      )
    if order_head_data is None:
        builder.packing_list_for_client = pickpack_constants.NO_DATA_FOUND
        builder.item_notes = pickpack_constants.NO_DATA_FOUND
        builder.order_notes = pickpack_constants.NO_DATA_FOUND
        return builder.render()
        #------ End ----------

    (customer_number,                                                           # pylint: disable=unpacking-non-sequence
     carrier_code,
     #order_entry_initials,
     is_on_wm_hold,
     order_status,
     calcualted_order_weight,
     service_level,
     ship_to_state,
     ship_to_country,
     customer_sold_to_country,
    ) = order_head_data

    try:
        pickpack_common.validate_order(is_on_wm_hold,
                                       order_status,
                                       order_id,
                                       service_level,
                                       carrier_code,
                                      )
    except pickpack_errors.HandleableServerError as err:
        builder.server_error = err.message
        return builder.render()
        #------ End ----------

    packing_list = getPackingList(transaction_cursor,
                                  order_id,
                                  # POSSIBLE IMPROVEMENT
                                  # add support for the allow_shipped query
                                  # parameter.
                                  False,
                                  custom_library,
                                 )

    if len(packing_list) == 0:
        builder.packing_list_for_client = pickpack_constants.NO_DATA_FOUND
        builder.item_notes = pickpack_constants.NO_DATA_FOUND
        builder.order_notes = pickpack_constants.NO_DATA_FOUND
        return builder.render()
        #------ End ----------

    if len(packing_list.items_not_picked) > 0:
        # Return "items not picked" error to client
        builder.server_error = ("Order %s has one or more items that have "
                                "not been picked. Items: %s."
                                % (order_id.formatted_for_display,
                                   ", ".join(packing_list.items_not_picked),
                                  )
                               )
        return builder.render()
        #------ End ----------

    builder.item_notes = pickpack_common.getItemNotes(packing_list,
                                                      getItemNoteText,
                                                      additional_keyword_arguments =
                                                        {'transaction_cursor' : transaction_cursor,
                                                        }
                                                     )

    (builder.order_notes,
     inline_images,
    ) = pickpack_common.getOrderNotesAndInlineImages(carrier_code,
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

    # Add the inline images to our packing list container object
    packing_list.add_inline_images(inline_images)

    builder.packing_list_for_client = packing_list.client_data()
    return builder.render()

def getItemNoteText(item_no,
                    transaction_cursor,                                         # pylint: disable=unused-argument
                   ):
    """
    Queries the server for the text of an item note. This function is passed in
    as an argument when calling pickpack_common.getItemNotes.
    """

    # POSSIBLE IMPROVEMENT Fetch from the database instead.
    # Returns item notes, hardcoded here, instead of fetching them from the
    # database.
    item_notes_dict = {
        '231703' : [("IMPORTANT: SOLD AS 4 PACK ONLY. DO NOT BREAK CARTON.", ), ],
        '235626' : [("IMPORTANT: SOLD AS 6 PACK ONLY. DO NOT BREAK CARTON.", ), ],
    }
    data = item_notes_dict.get(item_no, [])

    #sql = """
    #      -- This is what the sql might look like, if the item notes are stored
    #      -- in APlus. We do it this way because there may be multiple item
    #      -- notes for one item.
    #      --
    #      -- select ic.iccmtx
    #      -- from itcmnt ic
    #      -- where ic.icctyp = 'PACK'
    #      -- and ic.icitno = ?
    #      -- order by ic.icsqno
    #      """
    #transaction_cursor.execute(sql, item_no)
    #
    #data = transaction_cursor.fetchall()
    #if data is None:
    #    raise pickpack_errors.ApplicationError("Error:Select item notes data returned None.")
    #if len(data) == 0:
    #    raise pickpack_errors.ApplicationError("Error: Select item notes data returned no rows.")

    return clean_the_data(data)

def isValidItemNumberData_deferred(item_number):
    """
    Start the process of reading item number data from the server. Return a
    deferred.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.isValidItemNumberData_deferred(item_number)

    sql = """
          select   1
          from     itmst
          where    imitno = ?
          """
    params = [item_number]

    # M_dbpool.runQuery returns a deferred
    return M_dbpool.runQuery(sql, params)

def isValidOrderNumberData_deferred(possible_order_id_scan):
    """
    Start the process of reading order number data from the server. Return a
    deferred.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.isValidOrderNumberData_deferred(possible_order_id_scan)

    try:
        order_id = utl_aplus.order_id_from_barcode_scan(possible_order_id_scan)
    except utl_aplus.OrderIdParseError:
        # Could not parse the input as an order number. Return a Deferred
        # object, already called back, with the value of None.
        return defer.succeed(None)

    sql = """
          select    1
          from      orhed oh
          where     oh.ohorno = ?
          and       oh.ohorgn = ?
          and       oh.ohorst = '2'
          """
    params = [order_id.number, order_id.generation]

    # M_dbpool.runQuery returns a deferred
    return M_dbpool.runQuery(sql, params)

def itemByUPCData_deferred(upc):
    """
    Reads item number from the server. Returns a deferred.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.itemByUPCData_deferred(upc)

    sql = """
          select   trim(upitno) item_number
          from     itupc
          where    upbrit = ?
          """
    params = [upc]

    # M_dbpool.runQuery returns a deferred
    return M_dbpool.runQuery(sql, params)

def writeOrderCompleteData_deferred(order_id,
                                    comment_text,
                                    serial_numbers,
                                    user_id,
                                   ):
    """
    Write "order complete" data to the server.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.writeOrderCompleteData_deferred(order_id,
                                                                  comment_text,
                                                                  serial_numbers,
                                                                  user_id,
                                                                 )

    return M_dbpool_for_update.runInteraction(writeOrderComplete_transaction_wrapper,
                                              order_id,
                                              comment_text,
                                              serial_numbers,
                                              user_id,
                                              M_procedure_library,
                                             )

def writeOrderComplete_transaction_wrapper(transaction_cursor,
                                           order_id,
                                           ignore_comment_text,
                                           all_serial_numbers,
                                           user_id,
                                           procedure_library,
                                          ):
    """
    A wrapper for all the transactional operations that need to happen when
    writing "order complete" data to the server. Runs under the runInteraction
    transaction manager, from Twisted.adbapi.ConnectionPool.
    """
    # transaction_cursor is a (lightly wrapped) instance of pyodbc.cursor. This
    # will run in a thread, so we can use blocking calls in here (e.g.
    # cursor.execute) instead of using M_dbpool_for_update.runOperation.

    # Note: the M_dbpool_for_update ConnectionPool object is configured to use
    # transactions. In the connection string for that ConnectionPool, I pass
    # CommitMode 2, which means CommitMode CHG, aka Read Uncomitted).
    #
    # The ConnectionPool.runInteraction method that runs this function
    # automatically calls cursor.commit() if this function returns a value, and
    # it automatically calls cursor.rollback() if this function raises an error.


    # Update the user
    sql = """
          update orhed oh
          set oh.ohpacc = ?               -- Packer ID
          where oh.ohorno = ?
          and oh.ohorgn = ?
          and oh.ohwhid = 'PW'            -- Parts Warehouse
          and oh.ohcono = 1               -- Company Number
          and oh.ohortp = 'O'             -- Order Type
          """
    params = [user_id[:3],
              order_id.number,
              order_id.generation,
             ]
    transaction_cursor.execute(sql, params)

    ## POSSIBLE IMPROVEMENT
    ## Add comments to APlus ordet table
    #sql = """
    #      insert into ordet
    #      (     odcono
    #          , odorno
    #          , odorgn
    #          , odwhid
    #          , odortp
    #          , odorst
    #          , odohld
    #          , oditno                  -- Item Number
    #          , odlitp                  -- Line Item Type
    #          , oditd1                  -- Item Description 1
    #          , oditd2                  -- Item Description 2
    #      )
    #      select
    #      (     od.odcono
    #          , oh.ohorno
    #          , oh.ohorgn
    #          , oh.ohwhid
    #          , oh.ohortp
    #          , oh.ohorst
    #          , oh.ohohld
    #          , '/X'
    #          , 'M'
    #          , ?
    #          , ?
    #      )
    #      from orhed oh
    #      where oh.ohorno = ?
    #      and oh.ohorgn = ?
    #      and oh.ohwhid = 'PW'            -- Parts Warehouse
    #      and oh.ohcono = 1               -- Company Number
    #      and oh.ohortp = 'O'             -- Order Type
    #      """


    # Here's an example of the serial number data
    #
    # {'1': {'item_number': '235671',
    #        'serial_numbers': ['20081050000000',
    #                           '20081050000001',
    #                           '20081050000002',
    #                           '20081050000003',
    #                          ],
    #       },
    #  '2': {'item_number': '235671',
    #        'serial_numbers': ['20081050000004',
    #                           '20081050000005',
    #                           '20081050000006',
    #                           '20081050000007',
    #                          ],
    #       },
    # }

    # Record the serial numbers

    # Info from Dave
    #
    # The stored procedure is ready for you to test! The program name is
    # ZSRLUPSP, and the version for the MT test environment is in library
    # APLUS83MMN.
    #
    # This stored procedure takes 10 parameters - the first 9 are input
    # parameters containing the key fields for the WMRSV file, including the new
    # Serial # to be added. The 10th parameter is an output parameter to return
    # an error message - if it is blank there were no errors. As usual the
    # numeric key field values should be sent in character format with leading
    # zeros.
    #
    # The parameters are defined as:
    #
    # &APID      - Application ID ('OE' for Order Entry)         (2 A/N)
    # &CONO      - Company Number ('01' or '02')                 (2 A/N)
    # &GID6      - Group ID (For 'OE' = Order Number)            (6 A/N)
    # &ORGN      - Order Generation Number                       (2 A/N)
    # &SQ05      - Order Sequence (Line) Number                  (5 A/N)
    # &BMSQ      - BOM Sequence Number                           (4 A/N)
    # &LOCA      - W/M Location                                 (12 A/N)
    # &COFO      - Country Of Origin                             (3 A/N)
    # &SRLN      - New Serial Number                            (20 A/N)
    # &MESG      - Error Message Returned                       (80 A/N)
    #
    # Additional Notes:
    # The Group ID is a 6 character field, and the 5 character Order #
    # should be left justified in this parameter.
    #
    # The BOM Sequence # is usually (but not always) zero.
    #
    # Currently I expect the Location value to be in file format, with
    # no slash separators, but if necessary I have a routine for
    # converting to file format. For your application however, I think
    # all of the order reservations that are being updated would
    # theoretically be at the loading dock location '555555555'.
    #
    # The Country of Origin is currently always blank.
    #
    # Let me know if you have any questions or problems!
    #
    #
    #
    #
    #------------------------------------------
    #
    #
    # Hi Dave,
    #
    # I'm calling the stored procedure
    #
    # CALL APLUS83MMN/ZSRLUPSP PARM('OE' '01' '6Q161 ' '00' '00003' '0' '555555555' '' '20081015000000')
    #
    # and I'm getting this error:
    #  Decimal-data error occurred (C G D F).
    #  CEE9901 received by procedure ZSRLUPSP. (C D I R)
    # Thanks for your help.
    #
    #
    # Hi Christian,
    #
    # This happened because the 6th parameter (BOM Sequence #) is not a valid 4
    # digit number with leading zeros - it needs to be '0000' not '0'. The alpha
    # parameters can have trailing blanks truncated but the numeric parameters
    # must be the exact length. The correct call is:
    #
    # CALL APLUS83MMN/ZSRLUPSP PARM('OE' '01' '6Q161 ' '00' '00003' '0000' '555555555' '' '20081015000000')


    # Note: For the ODBC call, the three spaces for parameter 8 are required. A zero-length string
    # causes an error.
    #
    # ODBC call example:
    # {call aplus83mmn.zsrlupsp('OE','01','6Q174 ','00','00001','0000','555555555','   ','20081015000005')}
    stored_procedure_call_template = "{call %s('OE','01','%-6s','%s','%05i','0000','555555555','   ','%s')}"

    stored_procedure_name = "%s.zsrlupsp" % procedure_library

    for row_num, row_dict in all_serial_numbers.items():
        for serial_number in row_dict['serial_numbers']:
            stored_procedure_call = stored_procedure_call_template % (stored_procedure_name,
                                                                      order_id.number,
                                                                      order_id.padded_generation,
                                                                      # This int() call is required here, to avoid
                                                                      # TypeError: %d format: a number is required, not unicode
                                                                      int(row_num),
                                                                      serial_number,
                                                                     )
            transaction_cursor.execute(stored_procedure_call)

    # Must return a value from this function, to satisfy the callback chain.
    # Also, by returning a value, we tell adbapi.runInteraction to commit the
    # changes to the database.
    return True

def getClippershipWarningsData_deferred(order_id,
                                        allow_shipped,
                                       ):
    """
    Start the process of reading Clippership order warning data from the server.
    Return a deferred.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.getClippershipWarningsData_deferred(order_id)

    return M_dbpool.runInteraction(getClippershipWarnings_transaction_wrapper,
                                   order_id,
                                   allow_shipped,
                                   M_custom_library,
                                  )

def getClippershipWarnings_transaction_wrapper(transaction_cursor,
                                               order_id,
                                               allow_shipped,
                                               custom_library,
                                              ):
    """
    A wrapper for all the transactional operations that need to happen when
    getting Clippership order warning data from the server. Runs under the
    runInteraction transaction manager, from Twisted.adbapi.ConnectionPool.
    Returns order warning data (not a deferred).
    """
    # transaction_cursor is a (lightly wrapped) instance of pyodbc.cursor. This
    # will run in a thread; therefore, inside this function, we can use blocking
    # calls (e.g. cursor.execute) instead of M_dbpool.runOperation.

    builder = pickpack_result_builders.ClippershipWarningsBuilderInternal()
    builder.order_number = order_id.number
    builder.order_generation = order_id.generation

    order_head_data = getOrderHeadData(transaction_cursor,
                                       order_id,
                                      )
    if order_head_data is None:
        # POSSIBLE IMPROVEMENT
        # Enable Clippership to cancel shipping a package if there is a server
        # error. Add server_error to the Clippership builder internal and
        # external. Return an error here, instead of NO_DATA_FOUND.
        #builder.server_error = "Error: Order %s not found" % order_id.formatted_for_display

        builder.order_notes = pickpack_constants.NO_DATA_FOUND
        builder.warning_categories = pickpack_constants.NO_DATA_FOUND
        return builder.render()
        #------ End ----------

    (customer_number,                                                           # pylint: disable=unpacking-non-sequence
     carrier_code,
     #order_entry_initials,
     is_on_wm_hold,
     order_status,
     calcualted_order_weight,
     service_level,
     ship_to_state,
     ship_to_country,
     customer_sold_to_country,
    ) = order_head_data

    try:
        pickpack_common.validate_order(is_on_wm_hold,
                                       order_status,
                                       order_id,
                                       service_level,
                                       carrier_code,
                                      )
    except pickpack_errors.HandleableServerError as ignore_err:
    #except pickpack_errors.HandleableServerError as err:
        # POSSIBLE IMPROVEMENT
        # Enable Clippership to cancel shipping a package if there is a server
        # error. Add server_error to the Clippership builder internal and
        # external. Return an error here, instead of NO_DATA_FOUND.
        #builder.server_error = err.message

        # The order has a status error. Return NO_DATA_FOUND to Clippership.
        builder.order_notes = pickpack_constants.NO_DATA_FOUND
        builder.warning_categories = pickpack_constants.NO_DATA_FOUND
        return builder.render()
        #------ End ----------

    packing_list = getPackingList(transaction_cursor,
                                  order_id,
                                  allow_shipped,
                                  custom_library,
                                 )

    if len(packing_list) == 0:
        # POSSIBLE IMPROVEMENT
        # Enable Clippership to cancel shipping a package if there is a server
        # error. Add server_error to the Clippership builder internal and
        # external. Return an error here, instead of NO_DATA_FOUND.
        #builder.server_error = "Error: No shippable line items on order %s" % order_id.formatted_for_display

        builder.order_notes = pickpack_constants.NO_DATA_FOUND
        builder.warning_categories = pickpack_constants.NO_DATA_FOUND
        return builder.render()
        #------ End ----------

    (builder.order_notes,
     builder.warning_categories,
    ) = pickpack_common.getOrderNotesAndWarningCategories(carrier_code,
                                                          packing_list,
                                                          customer_number,
                                                          #order_entry_initials,
                                                          calcualted_order_weight,
                                                          service_level,
                                                          ship_to_state,
                                                          ship_to_country,
                                                          customer_sold_to_country,
                                                         )
    return builder.render()

def getOrderHeadData(transaction_cursor,
                     order_id,
                    ):
    """
    Return the customer number, the carrier code, and the entry initials for
    this order.
    """
    sql = """
          select oh.ohcsno          customer_number
               , trim(oh.ohcacd)    carrier_code
               -- , trim(oh.ohetus)    user_initials
               , trim(oh.ohhlcd)    hold_code
               , oh.ohorst          order_status
               , oh.ohshwt          calcualted_order_weight
               , trim(substr(oh.ohus15, 8, 2))  service_level
               , case when trim(coalesce(oh.ohshst, '')) = ''
                      then trim(oh.ohblst)
                      else trim(coalesce(oh.ohshst, ''))
                 end                        ship_to_state
               , trim(oh.ohshci)    ship_to_country
               , trim(cm.cmctid)    customer_sold_to_country
          from orhed oh
          join cusms cm                 -- Customer master
          on oh.ohcono = cm.cmcono
          and oh.ohcsno = cm.cmcsno
          where oh.ohwhid = 'PW'        -- Warehouse
          and oh.ohcono = 1             -- Company number
          and oh.ohortp = 'O'           -- Order type
          and oh.ohorno = ?
          and oh.ohorgn = ?
          """
    params = [order_id.number,
              order_id.generation,
             ]
    transaction_cursor.execute(sql, params)

    data = transaction_cursor.fetchall()

    if data is None:
        raise pickpack_errors.ApplicationError("Error: select data from orhed returned None.")
    if len(data) == 0:
        return None
        #------ End ----------

    if len(data) > 1:
        raise pickpack_errors.ApplicationError("Error: select data from orhed returned more than one row.")

    cleaned_data = clean_the_data(data)

    (customer_number,
     carrier_code,
     #order_entry_initials,
     hold_code,
     order_status,
     calcualted_order_weight,
     service_level,
     ship_to_state,
     ship_to_country,
     customer_sold_to_country,
    ) = cleaned_data[0]

    if calcualted_order_weight is None:
        calcualted_order_weight = 0
    calcualted_order_weight = int(calcualted_order_weight)

    error_if_no_data(customer_number)
    error_if_no_data(carrier_code)

    # Per Doug: When an order goes on WM hold, the ORHED.OHHLCD (hold code) will
    # be set to WM and the ORHED.OHORST (order status) will be set to 9 meaning
    # the order in on hold.
    if (hold_code == 'WM'
        or order_status == '9'
       ):
        is_on_wm_hold = True
    else:
        is_on_wm_hold = False

    return (customer_number,
            carrier_code,
            #order_entry_initials,
            is_on_wm_hold,
            order_status,
            calcualted_order_weight,
            service_level,
            ship_to_state,
            ship_to_country,
            customer_sold_to_country,
           )

def clean_the_data(data):
    """
    Given a data set, cleans and strips leading and trailing whitespace from
    each field in each row. Converts Decimal to int, truncating any fractional
    part. Returns a cleaned copy of the dataset.
    """
    def _clean_item(item):
        """
        Given an item of scalar data, cleans and strips leading and trailing
        whitespace from each field in each row. Converts Decimal to int,
        truncating any fractional part. Returns a cleaned copy of the item.
        """
        if item is None:
            return None

        try:
            return item.strip()
        except AttributeError:
            pass

        if isinstance(item, decimal.Decimal):
            return int(item)

        return item

    def _clean_row(row):
        """
        Clean one row
        """
        return tuple(_clean_item(item) for item in row)

    # Note: I had a fancier list comprehension here, but it flattened out the
    # data. So, I made the operations more explicit, with nested functions.
    return [_clean_row(row) for row in data]

def error_if_no_data(item):
    """
    Raises an error if an item is None or is a zero-length string.
    """
    if item is None:
        raise pickpack_errors.ApplicationError("Error: data is null.")
    try:
        length = len(item)
    except TypeError:
        pass
    else:
        if length == 0:
            raise pickpack_errors.ApplicationError("Error: data is zero-length.")

def getPackingList(transaction_cursor,
                   order_id,
                   allow_shipped,
                   custom_library,
                  ):
    """
    Runs an SQL query and returns PackingListContainer object containing packing
    list data (not a deferred).

    If the client request was specified with allow_shipped = True, we return
    rows where oh.ohorst is 2 (pick list printed) or 3 (ready to invoice).
    """

    if allow_shipped:
        allowed_statuses = "'2', '3'"
    else:
        allowed_statuses = "'2'"

    sql = """
          select od.odorsq                  line_number
               , trim(iu.upbrit)            upc
               , trim(od.oditno)            item_number
               , case when iu.upbrit is null
                      then 3
                      else 0
                 end                        status              -- No nvl2 on db2 for iSeries
               , od.odqtsh                  qty_shipped
               , trim(od.odunms)            sales_um
               , coalesce(od.odprcn, 1)     sales_um_conv
               , case when im.imwmcd = 'T'
                      then 1
                      else 0
                 end                        is_serialized
               -- This is what has_note might look like, if the item notes are
               -- stored in APlus. We do it this way because there may be
               -- multiple item notes for one item. We will fetch them later.
               --
               -- , case when exists (
               --       select 'Y'
               --       from itcmnt ic
               --       where ic.icctyp = 'PACK'
               --       and ic.icitno = od.oditno
               --   )
               --        then 1
               --        else 0
               --   end                        has_note
               , 0                          has_note            -- No item notes now
               , trim(pw.pwitcg)            item_category       -- Item warning category (HZ0, SB1, etc.)
               , coalesce(wm.wvpick, '')    item_pick_status
               , case when locate('HELMET,', im.imitd1) = 1
                      then 1
                      else 0
                 end                        is_helmet
          from orhed oh
          join ordet od
          on oh.ohcono = od.odcono
          and oh.ohorno = od.odorno
          and oh.ohorgn = od.odorgn
          join itmst im
          on od.oditno = im.imitno
          left join wmrsv wm
          on oh.ohcono = wm.wvcono          -- Company number
          and oh.ohwhid = wm.wvwhid         -- Warehouse
          and oh.ohorno = wm.wvgid6         -- Order number
          and oh.ohorgn = wm.wvorgn         -- Order generation
          and od.odorsq = wm.wvsq05         -- Line item sequence number
          and od.oditno = wm.wvitno         -- Item number
          left join itupc iu
          on od.oditno = iu.upitno
          left join %s.pwarn pw
          on od.oditno = pw.pwitno
          where oh.ohwhid = 'PW'            -- Warehouse
          and oh.ohcono = 1                 -- Company number
          and oh.ohortp = 'O'               -- Order type
          and od.odlitp = 'I'               -- Line item type: I is for Items, C Charges, M Comments
          and oh.ohorst in (%s)             -- Order status
          and od.odqtsh > 0                 -- Quantity shipped
          and oh.ohorno = ?
          and oh.ohorgn = ?
          order by trim(od.oditno)
                 , od.odorsq
          """ % (custom_library,
                 allowed_statuses,
                )
    params = [order_id.number,
              order_id.generation,
             ]
    transaction_cursor.execute(sql, params)

    data = transaction_cursor.fetchall()
    if data is None:
        raise pickpack_errors.ApplicationError("Error: Select packing list data returned None.")
    if len(data) == 0:
        raise pickpack_errors.ApplicationError("Error: Select packing list data returned no rows.")

    cleaned_data = clean_the_data(data)

    # Some of the packing list data we query from the database gets returned to
    # the client as-is. Other data elements are used to calculate aggregate or
    # otherwise digested values. Here we use the data from the query to populate
    # a container of objects. This container will hold and transport the packing
    # list data during processing.
    return pickpack_utility_classes.PackingListContainer(cleaned_data)

def isValidSerialNumberData_deferred(item_number,
                                     serial_number,
                                    ):
    """
    Start the process of reading serial number data from the server. Return a
    deferred.
    """
    # Return mock data, if flag is set
    if M_mock_data:
        from CML_Pickpack.pickpack_modules import pickpack_data_mock
        return pickpack_data_mock.isValidSerialNumberData_deferred(item_number,
                                                                   serial_number,
                                                                  )

    return M_dbpool.runInteraction(isValidSerialNumber_transaction_wrapper,
                                   item_number,
                                   serial_number,
                                  )

def isValidSerialNumber_transaction_wrapper(transaction_cursor,
                                            item_number,
                                            serial_number,
                                           ):
    """
    A wrapper for all the transactional operations that need to happen when
    getting serial number data from the server. Runs under the runInteraction
    transaction manager, from Twisted.adbapi.ConnectionPool. Returns serial
    number data (not a deferred).
    """
    # transaction_cursor is a (lightly wrapped) instance of pyodbc.cursor. This
    # will run in a thread; therefore, inside this function, we can use blocking
    # calls (e.g. cursor.execute) instead of M_dbpool.runOperation.

    # Make sure this serial number has not been used before.
    sql = """
          select count(*)
          from wmrsv wm
          where wm.wvwhid = 'PW'        -- Parts warehouse
          and wm.wvcono = 1             -- Company number
          and wm.wvitno = ?
          and wm.wvltsr = ?
          """

    params = [item_number,
              serial_number,
             ]
    transaction_cursor.execute(sql, params)

    data = transaction_cursor.fetchall()
    if data is None:
        raise pickpack_errors.ApplicationError("Error: Select serial number data returned None.")

    cleaned_data = clean_the_data(data)
    count = cleaned_data[0][0]

    builder = pickpack_result_builders.IsValidSerialNumberBuilder()

    if count == 0:
        # Not already used: ok
        builder.is_valid = pickpack_constants.DB_TRUE
        builder.err_msg = None
    else:
        # Already used: error
        builder.is_valid = pickpack_constants.DB_FALSE

        # Find our where this serial number has been used before.
        sql = """
              select wm.wvgid6              -- Order number
                   , wm.wvorgn              -- Order generation
              from wmrsv wm
              where wm.wvwhid = 'PW'        -- Parts warehouse
              and wm.wvcono = 1             -- Company number
              and wm.wvitno = ?
              and wm.wvltsr = ?
              """
        params = [item_number,
                  serial_number,
                 ]
        transaction_cursor.execute(sql, params)
        data = transaction_cursor.fetchall()
        if data is None:
            raise pickpack_errors.ApplicationError("Error: Select serial number previous order returned None.")

        cleaned_data = clean_the_data(data)
        if len(cleaned_data) == 1:
            these_orders_string = "Order %s/%s" % cleaned_data[0]
        else:
            these_orders = ["Orders",]
            for row in cleaned_data:
                these_orders.append("%s/%s" % row)
            these_orders_string = " ".join(these_orders)
        builder.err_msg = "Serial number %s has already been used. %s" % (serial_number,
                                                                          these_orders_string,
                                                                         )
    return builder.render()
