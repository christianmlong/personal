"""
shopfloor_monitor_data.py

Data access for the Shopfloor Monitor application


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import itertools

#from CML_Common.utility import utl_functions
from CML_Common.utility import utl_decorators

from CML_Pickpack.pickpack_modules import pickpack_common
from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_data
from CML_Pickpack.pickpack_modules import pickpack_errors
from CML_Pickpack.pickpack_modules import shopfloor_monitor_result_builders

from CML_Pickpack.pickpack_modules import shopfloor_monitor_classes


def jStatusOrdersData_deferred(shipping_station,
                               show_backorder,
                              ):
    """
    Start the process of reading order status data from the server. Return a
    deferred.
    """
    # Return mock data, if flag is set
    if pickpack_data.M_mock_data:
        from CML_Pickpack.pickpack_modules import shopfloor_monitor_data_mock
        return shopfloor_monitor_data_mock.jStatusOrdersData_deferred(shipping_station,
                                                                      show_backorder,
                                                                     )

    return pickpack_data.M_dbpool.runInteraction(jStatusOrdersData_transaction_wrapper,
                                                 shipping_station,
                                                 show_backorder,
                                                )

def jStatusOrdersData_transaction_wrapper(transaction_cursor,
                                          shipping_station,
                                          show_backorder,
                                         ):
    """
    A wrapper for all the transactional operations that need to happen when
    getting order status data from the server. Runs under the runInteraction
    transaction manager, from Twisted.adbapi.ConnectionPool. Returns order
    status data (not a deferred).
    """

    ## debug logging
    #ss_dict = {
    #    pickpack_constants.CONSUMABLES_SCALE    : "CONSUMABLES",
    #    pickpack_constants.SERVICE_PARTS_SCALE  : "SERVICE_PARTS",
    #    pickpack_constants.BOTH_SCALE           : "BOTH",
    #    pickpack_constants.ALL_SCALES           : "ALL",
    #}
    ##from twisted.python import log
    ### Note: for this twisted logging to work (in my current setup), you have
    ### to run start_pickpack with the --background option and the --log option.
    ##log.msg("============================")
    ##log.msg("Cache miss - Summary %s" % ss_dict[shipping_station])
    ##log.msg("============================")
    #print("============================")
    #print("Cache miss - Summary %s" % ss_dict[shipping_station])
    #print("============================")

    # transaction_cursor is a (lightly wrapped) instance of cx_oracle.cursor.
    # This will run in a thread; therefore, inside this function, we can use
    # blocking calls (e.g. cursor.execute) instead of dbpool.runOperation.

    if show_backorder:
        builder = shopfloor_monitor_result_builders.BackorderOrderStatusBuilder()

        (builder.today_sure_backorder_ready_to_print,
         builder.today_sure_backorder_pick_slip_printed,
         builder.today_sure_backorder_packed,
        ) = today_sure_backorder_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
        (builder.signature_service_backorder_ready_to_print,
         builder.signature_service_backorder_pick_slip_printed,
         builder.signature_service_backorder_packed,
        ) = signature_service_backorder_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
        (builder.service_files_backorder_ready_to_print,
         builder.service_files_backorder_pick_slip_printed,
         builder.service_files_backorder_packed,
        ) = service_files_backorder_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
        (builder.normal_backorder_ready_to_print,
         builder.normal_backorder_pick_slip_printed,
         builder.normal_backorder_packed,
        ) = normal_backorder_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
    else:
        builder = shopfloor_monitor_result_builders.OrdinaryOrderStatusBuilder()

        (builder.today_sure_can_ship_tomorrow_ready_to_print,
         builder.today_sure_can_ship_tomorrow_pick_slip_printed,
         builder.today_sure_can_ship_tomorrow_packed,
         builder.today_sure_should_ship_today_ready_to_print,
         builder.today_sure_should_ship_today_pick_slip_printed,
         builder.today_sure_should_ship_today_packed,
        ) = today_sure_ordinary_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
        (builder.signature_service_can_ship_tomorrow_ready_to_print,
         builder.signature_service_can_ship_tomorrow_pick_slip_printed,
         builder.signature_service_can_ship_tomorrow_packed,
         builder.signature_service_should_ship_today_ready_to_print,
         builder.signature_service_should_ship_today_pick_slip_printed,
         builder.signature_service_should_ship_today_packed,
        ) = signature_service_ordinary_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
        (builder.service_files_should_ship_today_ready_to_print,
         builder.service_files_should_ship_today_pick_slip_printed,
         builder.service_files_should_ship_today_packed,
        ) = service_files_ordinary_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )
        (builder.normal_can_ship_tomorrow_ready_to_print,
         builder.normal_can_ship_tomorrow_pick_slip_printed,
         builder.normal_can_ship_tomorrow_packed,
         builder.normal_should_ship_today_ready_to_print,
         builder.normal_should_ship_today_pick_slip_printed,
         builder.normal_should_ship_today_packed,
        ) = normal_ordinary_summary_provider.get_data(
            transaction_cursor,
            shipping_station,
        )

    return builder.render()

def jStatusOrderNumbersData_deferred(shipping_station,
                                     show_backorder,
                                     order_type,
                                    ):
    """
    Start the process of reading order number data from the server. Return a
    deferred.
    """
    # Return mock data, if flag is set
    if pickpack_data.M_mock_data:
        from CML_Pickpack.pickpack_modules import shopfloor_monitor_data_mock
        return shopfloor_monitor_data_mock.jStatusOrderNumbersData_deferred(shipping_station,
                                                                            show_backorder,
                                                                            order_type,
                                                                           )

    return pickpack_data.M_dbpool.runInteraction(jStatusOrderNumbersData_transaction_wrapper,
                                                 shipping_station,
                                                 show_backorder,
                                                 order_type,
                                                )

def jStatusOrderNumbersData_transaction_wrapper(transaction_cursor,
                                                shipping_station,
                                                show_backorder,
                                                order_type,
                                               ):
    """
    A wrapper for all the transactional operations that need to happen when
    getting order numbers data from the server. Runs under the runInteraction
    transaction manager, from Twisted.adbapi.ConnectionPool. Returns order
    status data (not a deferred).
    """

    ## debug logging
    #ss_dict = {
    #    pickpack_constants.CONSUMABLES_SCALE    : "CONSUMABLES",
    #    pickpack_constants.SERVICE_PARTS_SCALE  : "SERVICE_PARTS",
    #    pickpack_constants.BOTH_SCALE           : "BOTH",
    #    pickpack_constants.ALL_SCALES           : "ALL",
    #}
    ##from twisted.python import log
    ### Note: for this twisted logging to work (in my current setup), you have
    ### to run start_pickpack with the --background option and the --log option.
    ##log.msg("============================")
    ##log.msg("Cache miss - Detail %s %s" % (ss_dict[shipping_station], order_type))
    ##log.msg("============================")
    #print("============================")
    #print("Cache miss - Detail %s %s" % (ss_dict[shipping_station], order_type))
    #print("============================")

    if show_backorder:
        if order_type == pickpack_constants.TODAY_SURE:
            data_provider = today_sure_backorder_detail_data_provider
        elif order_type == pickpack_constants.SIGNATURE_SERVICE:
            data_provider = signature_service_backorder_detail_data_provider
        elif order_type == pickpack_constants.SERVICE_FILE:
            data_provider = service_files_backorder_detail_data_provider
        elif order_type == pickpack_constants.NORMAL:
            data_provider = normal_backorder_detail_data_provider
        else:
            raise pickpack_errors.ApplicationError("Unknown order type" % order_type)

        builder = shopfloor_monitor_result_builders.BackorderOrderNumberBuilder()
        (builder.backorder_ready_to_print,
         builder.backorder_pick_slip_printed,
         builder.backorder_packed,
        )= data_provider.get_data(transaction_cursor,
                                  shipping_station,
                                 )
    else:
        if order_type == pickpack_constants.TODAY_SURE:
            builder = shopfloor_monitor_result_builders.OrdinaryOrderNumberBuilder()
            data_provider = today_sure_ordinary_detail_data_provider
        elif order_type == pickpack_constants.SIGNATURE_SERVICE:
            builder = shopfloor_monitor_result_builders.OrdinaryOrderNumberBuilder()
            data_provider = signature_service_ordinary_detail_data_provider
        elif order_type == pickpack_constants.SERVICE_FILE:
            builder = shopfloor_monitor_result_builders.OrdinaryOrderNumberBuilderServiceFile()
            data_provider = service_files_ordinary_detail_data_provider
        elif order_type == pickpack_constants.NORMAL:
            builder = shopfloor_monitor_result_builders.OrdinaryOrderNumberBuilder()
            data_provider = normal_ordinary_detail_data_provider
        else:
            raise pickpack_errors.ApplicationError("Unknown order type" % order_type)

        order_number_data = data_provider.get_data(transaction_cursor,
                                                   shipping_station,
                                                  )

        if order_type == pickpack_constants.SERVICE_FILE:
            (builder.should_ship_today_ready_to_print,                          # pylint: disable=unbalanced-tuple-unpacking
             builder.should_ship_today_pick_slip_printed,
             builder.should_ship_today_packed,
            ) = order_number_data
        else:
            (builder.can_ship_tomorrow_ready_to_print,                          # pylint: disable=unbalanced-tuple-unpacking
             builder.can_ship_tomorrow_pick_slip_printed,
             builder.can_ship_tomorrow_packed,
             builder.should_ship_today_ready_to_print,
             builder.should_ship_today_pick_slip_printed,
             builder.should_ship_today_packed,
            ) = order_number_data

    # Get the last print data
    if order_type == pickpack_constants.TODAY_SURE:
        last_print_data_provider = today_sure_last_print_data_provider
    elif order_type == pickpack_constants.SIGNATURE_SERVICE:
        last_print_data_provider = signature_service_last_print_data_provider
    elif order_type == pickpack_constants.SERVICE_FILE:
        last_print_data_provider = service_files_last_print_data_provider
    elif order_type == pickpack_constants.NORMAL:
        last_print_data_provider = normal_last_print_data_provider
    else:
        raise pickpack_errors.ApplicationError("Unknown order type" % order_type)

    (builder.last_print_formatted_order_number,
     builder.entry_date_of_last_printed_order,
     builder.entry_time_of_last_printed_order,
     builder.last_print_date,
     builder.last_print_time,
    ) = last_print_data_provider.get_data(transaction_cursor,
                                          shipping_station,
                                         )

    return builder.render()

def orderNumberDetailData_deferred(order_number, order_generation):
    """
    Start the process of reading order number detail data from the server.
    Return a deferred.
    """
    # Return mock data, if flag is set
    if pickpack_data.M_mock_data:
        from CML_Pickpack.pickpack_modules import shopfloor_monitor_data_mock
        return shopfloor_monitor_data_mock.orderNumberDetailData_deferred(order_number, order_generation)

    return pickpack_data.M_dbpool.runInteraction(orderNumberDetailData_transaction_wrapper,
                                                 order_number,
                                                 order_generation,
                                                )

def orderNumberDetailData_transaction_wrapper(transaction_cursor,
                                              order_number,
                                              order_generation,
                                             ):
    """
    A wrapper for all the transactional operations that need to happen when
    getting order number detail data from the server. Runs under the
    runInteraction transaction manager, from Twisted.adbapi.ConnectionPool.
    Returns order status data (not a deferred).
    """
    builder = shopfloor_monitor_result_builders.OrderDataBuilder()
    (builder.customer_number,
     builder.order_number,
     builder.order_generation,
     builder.order_status_code,
     builder.customer_name,
     builder.entered_by,
     builder.backorder_code,
     builder.shipping_instructions,
     builder.carrier_code,
     builder.packer_id,
     builder.picker_id,
     builder.printer_id,
     builder.shipped_order_weight,
     builder.number_of_lines,
     builder.truck_team,
     builder.complete_ship_code,
     builder.service_level,
     builder.print_date,
     builder.print_time,
     builder.order_entry_date,
     builder.order_entry_time,
     builder.requested_ship_date,
     builder.order_notes,
    ) = order_number_detail_data_provider.get_data(transaction_cursor,
                                                   order_number,
                                                   order_generation,
                                                  )
    return builder.render()


class SQLBuilderUtility(object):
    """
    Some lowlevel utility methods
    """
    def __init__(self, *args, **kwargs):
        super(SQLBuilderUtility, self).__init__(*args, **kwargs)

    @staticmethod
    def makeColumnStructure(definition, name):
        """
        Makes a ColumnStructure object, holding a single Column object
        """
        return shopfloor_monitor_classes.make_column_structure(
            shopfloor_monitor_classes.Column(
                definition = definition,
                name = name,
            )
        )

    def addColumnToColumnStructure(self,
                                   column = None,
                                   column_definition = None,
                                   column_name = None,
                                  ):
        """
        At several points in the class hierarchy, we add columns to the
        column_structure. Each class adds its columns to self.column_structure.

        Callers can supply a Column object for the column argument. Or they can
        supply column_definition and column_name.
        """
        if column is None and column_definition is None and column_name is None:
            raise pickpack_errors.ApplicationError("Error: column, column_definition, and column_name can not all be None")
        elif column is None:
            additional_column = self.makeColumnStructure(
                definition = column_definition,
                name = column_name,
            )
        elif column_definition is None and column_name is None:
            # If a bare Column object was passed in, wrap it in a
            # ColumnStructure object.
            if isinstance(column, shopfloor_monitor_classes.Column):
                additional_column =shopfloor_monitor_classes.make_column_structure(column)
            else:
                additional_column = column
        else:
            raise pickpack_errors.ApplicationError("Error: column, column_definition, and column_name can not all be passed in.")

        if hasattr(self, 'column_structure'):
            # The column_structure attribute already exists for this object. Add
            # our column to it.
            self.column_structure += additional_column                          # pylint: disable=access-member-before-definition
        else:
            # No column_structure attribute found. Make a new column_structure
            # attribute, and add our column to it.
            self.column_structure = additional_column                           # pylint: disable=attribute-defined-outside-init


class SQLBuilderCommon(object):
    """
    Common functionality for the sql builders
    """
    def __init__(self, *args, **kwargs):
        super(SQLBuilderCommon, self).__init__(*args, **kwargs)

    def get_data(self,
                 transaction_cursor,
                 shipping_station,
                ):
        """
        Return the needed data, parsed and formatted.
        """
        # POSSIBLE IMPROVEMENT: Move build_sql to __init__. Save the built sql
        # in self.sql. Make shipping_station an argument to __init__. Or, split
        # them out in to their own classes. See notes at the bottom of the file
        # for more info.
        sql = self.build_sql(shipping_station)
        data = self.run_query(transaction_cursor, sql)
        return self.parse_query_results(data)                                   # pylint: disable=no-member

    def build_sql(self,
                  shipping_station,
                 ):
        """
        Build and return the appropriate sql query
        """
        formatting_data = self.build_formatting_data(shipping_station)          # pylint: disable=no-member
        sql = self.SQL_TEMPLATE.format(**formatting_data)                       # pylint: disable=no-member

        ## DE BUG
        #print "===================================================="
        #for line in sql.split('\n'):
        #    print line
        #print "===================================================="

        return sql

    def run_query(self,
                  transaction_cursor,
                  sql,
                  params = None,
                 ):
        """
        Query the database
        """
        # debug logging
        # Note: for this twisted logging to work (in my current setup), you have
        # to run start_pickpack with the --background option and the --log option.
        #from twisted.python import log
        #log.msg(self.category_name)
        #log.msg(sql)

        if params is None:
            transaction_cursor.execute(sql)
        else:
            transaction_cursor.execute(sql, params)
        data = transaction_cursor.fetchall()
        if data is None:
            raise pickpack_errors.ApplicationError("Error: %s select data returned None." % self.__class__.__name__)
        return data

    def build_common_sql(self,
                         shipping_station,
                        ):
        """
        Build and return the part of the sql query that is shared between the
        summary and detail queries.
        """
        common_template = """
            from orhed oh

            {shipping_station_join}

            where oh.ohorst in ('1', '2')   -- Status: ready or printed
            and oh.ohwhid = 'PW'            -- Parts Warehouse
            and oh.ohcono = 1               -- Company Number 1
            and oh.ohortp = 'O'             -- Order Type
            -- Some orders have requested ship date in the future: exclude them.
            -- Only return orders that have requested ship date of today or earlier.
            and oh.ohrsdt <= int(varchar_format(CURRENT_TIMESTAMP, 'YYMMDD'))

            {order_type_where_clause}

            {backorder_where_clause}

            {shipping_station_where_clause}

            {special_team_where_clause}
        """

        (shipping_station_where_clause,
         shipping_station_join,
         special_team_where_clause,
        ) = self.build_shipping_station_clauses(shipping_station)

        return common_template.format(
            shipping_station_join = shipping_station_join,
            order_type_where_clause = self.build_order_type_where_clause(),
            backorder_where_clause = self.build_backorder_where_clause(),       # pylint: disable=no-member
            shipping_station_where_clause = shipping_station_where_clause,
            special_team_where_clause = special_team_where_clause,
        )

    def build_order_type_where_clause(self):
        """
        Return the appropriate sql where clause for the order type
        """
        return "and trim(substr(oh.ohus15, 8, 2)) = '%s'" % self.ORDER_TYPE_DATABASE_VALUE      # pylint: disable=no-member

    @staticmethod
    def build_shipping_station_clauses(shipping_station):
        """
        Return the appropriate sql clauses for the shipping station
        """

        # Since APlus does not have the order source on orhed the way NDS did,
        # we have to calculate the order source for each open order, every time.
        # Here we have a sql snippet that we will add to the sql query for cases
        # when we want to filter by shipping station.
        #
        # Here's how it works.
        #
        # We look at all the line items on each order, and we read which APlus
        # business unit it belongs to. The APlus business units look like this B04,
        # B38, etc.
        #
        # Then, we map APlus business units to the conceptual business units. They
        # are Consumables, Helmets, Service Parts.
        #
        # Then we aggregate those conceptual business units in to a string for each
        # order. So, each order will have one of these strings: C, H, S, CH, CS, HS,
        # CHS.
        #
        # Then we map those strings to the shipping stations that will handle them.
        #    The Consumables scale handles C, H, and CH orders.
        #    The Service Parts scale handles S orders.
        #    The Both scale handles everything else.
        shipping_station_join_choose_scale = """
            -- Here we're joning from our main query to a temp table that holds
            -- business unit data. We use a temp table rather than a correlated
            -- subselect. A correlated subselect has to run the subquery for
            -- each row in the outer query, and we don't want that.
            join
            (
                -- This is the outer "group by". It takes all the busiess units for each order, and
                -- decides which scale should handle that order.
                select order_number
                     , order_generation
                     -- Here we're aggregating all the order's conceptual business units
                     -- (C, H, S) in to a concatenated string (e.g. C, S, HS, CHS). Then
                     -- we're mapping the aggregated conceptual business units to the
                     -- scales that handle them.
                     , case xmlserialize(xmlagg(xmltext(conceptual_business_unit) order by conceptual_business_unit) as varchar(100))
                       when 'C'     -- Only Consumables items: Consumables scale
                       then 'C'
                       when 'H'     -- Only helmets: Consumables scale
                       then 'C'
                       when 'S'     -- Only Service Parts items: Service Parts scale
                       then 'S'
                       when 'CH'    -- Consumables items and helmets: Consumables scale
                       then 'C'
                       when 'CS'    -- Consumables items and Service Parts items: Both scale
                       then 'B'
                       when 'HS'    -- Helmets and Service Parts items: Both scale
                       then 'B'
                       when 'CHS'   -- Consumables items, helmets and Service Parts items: Both scale
                       then 'B'
                       --else null
                       else 'C'     -- Any weird cases get grouped in with Consumables.
                       end which_scale
                from
                (
                    -- This is the inner "group by". It takes all the items on each order, and
                    -- groups them by business unit. The result is a series of rows for each order,
                    -- with each row representing a business unit whose items are on that order.
                    --
                    -- For example:
                    -- 6P626  0   C
                    -- 6P626  0   H
                    -- 6P626  0   S
                    -- 6P627  0   C
                    -- 6P627  0   S
                    -- 6P628  0   C
                    -- 6P629  0   C
                    --
                    -- Also, we use a sub-select here, to allow us to say "group by conceptual_business_unit"
                    -- instead of "group by case trim(im.imvnno) when 'B04' then 'C' . . . "
                    select order_number
                         , order_generation
                         , conceptual_business_unit
                    from
                    (
                        -- Select all the items on all the open orders
                        select oh2.ohorno                order_number
                             , oh2.ohorgn                order_generation
                             -- Here we're reducing APlus business units (B##) to one letter
                             -- abbreviations corresponding to conceptual business units:
                             -- C - Consumables, H - Helmets, S - Service Parts.
                             , case trim(im.imvnno)
                               when 'B04' then 'C'
                               when 'B13' then 'C'
                               when 'B15' then 'S'
                               when 'B35' then 'C'
                               when 'B38' then 'H'
                               else 'C'                 -- Treat unknown BUs as Consumables
                               end                      conceptual_business_unit
                        from orhed oh2
                        join ordet od
                        on oh2.ohcono = od.odcono
                        and oh2.ohorno = od.odorno
                        and oh2.ohorgn = od.odorgn
                        join itmst im
                        on od.oditno = im.imitno
                        where oh2.ohwhid = 'PW'        -- Warehouse ID
                        and oh2.ohcono = 1             -- Company Number
                        and oh2.ohortp = 'O'           -- Order Type - O is an order
                        and oh2.ohorst in ('1', '2')   -- Order Status Code
                        and od.odlitp = 'I'            -- Line Item Type - I is an item, M is a comment
                        and od.odqtsh > 0              -- Quantity shipped
                    ) as temp1
                    group by order_number
                           , order_generation
                           , conceptual_business_unit
                ) as temp2
                group by order_number
                       , order_generation
                order by order_number desc
                       , order_generation
            ) as temp3
            on oh.ohorno = temp3.order_number
            and oh.ohorgn = temp3.order_generation
        """
        shipping_station_join_all_scales = ""

        # The big join above (shipping_station_join_choose_scale) takes care of
        # excluding orders that have no non-zero detail lines. However, for the
        # "all scales" case, we don't include the big join in the sql statement.
        # So, we add this where clause, to take care of excluding empty orders.
        shipping_station_where_clause_all_scales = """
            -- Exclude orders that have no detail lines.
            and exists
            (
                select 1
                from ordet od
                where oh.ohcono = od.odcono
                and oh.ohorno = od.odorno
                and oh.ohorgn = od.odorgn
                and od.odlitp = 'I'            -- Line Item Type - I is an item, M is a comment
                and od.odqtsh > 0              -- Quantity shipped
            )
        """
        shipping_station_where_clause_consumables_scale = "and temp3.which_scale = 'C'"
        shipping_station_where_clause_service_parts_scale = "and temp3.which_scale = 'S'"
        shipping_station_where_clause_both_scale = "and temp3.which_scale = 'B'"

        # Special team orders
        #
        # The special team handles unusual orders and special cases:
        #   Truck orders: Large items that go out on a skid
        #   Canada backorders: Orders that are on hold waiting for an item
        #   Daily file orders: Orders that only go out once a week
        exclude_special_team_orders = """
            and oh.ohfl01 != 'T'
        """
        #all_team_orders = ""
        #only_special_team_orders = """
        #    and oh.ohfl01 = 'T'
        #"""

        shipping_station_dict = {
            pickpack_constants.CONSUMABLES_SCALE    : (shipping_station_where_clause_consumables_scale,
                                                       shipping_station_join_choose_scale,
                                                       exclude_special_team_orders,
                                                      ),
            pickpack_constants.SERVICE_PARTS_SCALE  : (shipping_station_where_clause_service_parts_scale,
                                                       shipping_station_join_choose_scale,
                                                       exclude_special_team_orders,
                                                      ),
            pickpack_constants.BOTH_SCALE           : (shipping_station_where_clause_both_scale,
                                                       shipping_station_join_choose_scale,
                                                       exclude_special_team_orders,
                                                      ),
            pickpack_constants.ALL_SCALES           : (shipping_station_where_clause_all_scales,
                                                       shipping_station_join_all_scales,
                                                       exclude_special_team_orders,
                                                      ),
            #pickpack_constants.SPECIAL_TEAM         : (shipping_station_where_clause_all_scales,
            #                                           shipping_station_join_all_scales,
            #                                           only_special_team_orders,
            #                                          ),
        }

        return shipping_station_dict[shipping_station]

    @staticmethod
    def build_formatted_order_number_definition(order_number_field,
                                                order_generation_field,
                                               ):
        """
        Build a sql column definition that provides a clean representation of
        order number and generation in AA001/00 format.
        """
        return "trim({order_number_field}) || '/' || right('00' || trim(char({order_generation_field})), 2)".format(
            order_number_field = order_number_field,
            order_generation_field = order_generation_field,
        )


@utl_decorators.add_constants_to_class({'OrderStatus'    : ('ReadyToPrint',
                                                            'PickSlipPrinted',
                                                            'Packed',
                                                            'Error',
                                                           ),
                                       },
                                       # Keep this small. That way we can return
                                       # smaller integers from the query.
                                       magic_number = 20,
                                      )
class SQLBuilderBase(SQLBuilderCommon, SQLBuilderUtility):
    """
    Base for data fetching classes
    """
    def __init__(self, *args, **kwargs):
        super(SQLBuilderBase, self).__init__(*args, **kwargs)
        self.addColumnToColumnStructure(column = self.build_order_status_column())

    def build_order_status_column(self):
        """
        Build the column for deciding if an order is in status "ready to print",
        "pick slip printed", or "packed".
        """
        template = """
            case

            when oh.ohorst = '1'
            then {ready_to_print}

            when oh.ohorst = '2'
            and trim(coalesce(oh.ohpacc, '')) = ''
            then {pick_slip_printed}

            when oh.ohorst = '2'
            and trim(coalesce(oh.ohpacc, '')) != ''
            then {packed}

            else {error}

            end
        """
        order_status_column_definition = template.format(
           ready_to_print = self.Constants.OrderStatus.ReadyToPrint,            # pylint: disable=no-member
           pick_slip_printed = self.Constants.OrderStatus.PickSlipPrinted,      # pylint: disable=no-member
           packed = self.Constants.OrderStatus.Packed,                          # pylint: disable=no-member
           error = self.Constants.OrderStatus.Error,                            # pylint: disable=no-member
        )
        return shopfloor_monitor_classes.Column(
            definition = order_status_column_definition,
            name = 'order_status',
        )

    def build_backorder_where_clause(self):
        """
        Return the appropriate sql where clause for selecting backorders.
        """
        if self.BACKORDER:                                                      # pylint: disable=no-member
            return "and oh.ohorgn > 0"
        else:
            return "and oh.ohorgn = 0"




# ====================================
# Last order printed
# ====================================

class LastPrint(SQLBuilderCommon):
    """
    Base for data fetching classes for last print data
    """
    SQL_TEMPLATE = """
        -- Our dates in APlus are stored as integers. O_o
        --
        -- Parsing them out is cumbersome
        select  {formatted_order_number}
             ,  trim(leading '0' from substr(temp1.order_entry_date_as_int_string, 5, 2 )) ||
                '/' ||
                trim(leading '0' from substr(temp1.order_entry_date_as_int_string, 7, 2 )) ||
                '/' ||
                trim(leading '0' from substr(temp1.order_entry_date_as_int_string, 1, 4 )) order_entry_date_as_string
                -- Round-trip through the DB2 time format, to make sure it
                -- is formatted consistently (AM, PM, etc.)
             ,  trim(leading '0' from char(time(
                    substr(temp1.order_entry_time_as_int_string, 1, 2 ) ||      -- Two hour characters
                    ':' ||                                                      -- ISO standard time separator
                    substr(temp1.order_entry_time_as_int_string, 3, 2 ) ||      -- Two minute characters
                    ':' ||                                                      -- ISO standard time separator
                    substr(temp1.order_entry_time_as_int_string, 5, 2 )         -- Two second characters
                ), USA)) order_entry_time_as_string
             ,  trim(leading '0' from substr(temp1.last_print_date_as_int_string, 5, 2 )) ||
                '/' ||
                trim(leading '0' from substr(temp1.last_print_date_as_int_string, 7, 2 )) ||
                '/' ||
                trim(leading '0' from substr(temp1.last_print_date_as_int_string, 1, 4 )) last_print_date_as_string
                -- Round-trip through the DB2 time format, to make sure it
                -- is formatted consistently (AM, PM, etc.)
             ,  trim(leading '0' from char(time(
                    substr(temp1.last_print_time_as_int_string, 1, 2 ) ||
                    ':' ||
                    substr(temp1.last_print_time_as_int_string, 3, 2 ) ||
                    ':' ||
                    substr(temp1.last_print_time_as_int_string, 5, 2 )
                ), USA)) last_print_time_as_string
        from (
            select  trim(char(oh.ohetcc)) ||                        -- Two century digits
                    right(                                          -- Left-zero-pad the string, to allow for single-digit years
                        repeat('0', 6) || trim(char(oh.ohetdt)),
                        6
                    ) order_entry_date_as_int_string
                 ,  right(                                          -- Left-zero-pad the string, to allow for single-digit hours
                        repeat('0', 6) || trim(char(oh.ohettm)),
                        6
                    ) order_entry_time_as_int_string
                 ,  trim(char(oh.ohppcc)) ||
                    right(
                        repeat('0', 6) || trim(char(oh.ohppdt)),
                        6
                    ) last_print_date_as_int_string
                 ,  right(
                        repeat('0', 6) || trim(char(oh.ohpptm)),
                        6
                    ) last_print_time_as_int_string
                 ,  oh.ohorno       order_number
                 ,  oh.ohorgn       order_generation

            {common_sql}

            and oh.ohppdt > 0
            and oh.ohpptm > 0
            -- Only get the most-recently printed order
            order by oh.ohppdt desc
                   , oh.ohpptm desc
            fetch first row only
        ) as temp1
    """
    def __init__(self, *args, **kwargs):
        super(LastPrint, self).__init__(*args, **kwargs)

    def build_formatting_data(self,
                              shipping_station,
                             ):
        """
        Build and return a dictionary with the data we need to render the sql
        template.
        """
        return {
            'common_sql'                : self.build_common_sql(shipping_station),
            'formatted_order_number'    : self.build_formatted_order_number_definition('temp1.order_number', 'temp1.order_generation'),
        }

    @staticmethod
    def build_backorder_where_clause():
        """
        For last print, we don't segregate backorders from normal orders.
        """
        return ""

    def parse_query_results(self,
                            data,
                           ):
        """
        The query returns formatted order number and generation, the date and
        time that order was entered, and the date and time of last print.
        """
        if data is None or len(data) == 0:
            formatted_order_number = pickpack_constants.NO_DATA_FOUND
            entry_date_of_last_printed_order = pickpack_constants.NO_DATA_FOUND
            entry_time_of_last_printed_order = pickpack_constants.NO_DATA_FOUND
            last_print_date = pickpack_constants.NO_DATA_FOUND
            last_print_time = pickpack_constants.NO_DATA_FOUND
        elif len(data) == 1:
            (formatted_order_number,
             entry_date_of_last_printed_order,
             entry_time_of_last_printed_order,
             last_print_date,
             last_print_time,
            ) = data[0]
            ## Our version of DB2 formats the date strings with leading zeros.
            ## Here we strip those off.
            #entry_date_of_last_printed_order = entry_date_of_last_printed_order.lstrip('0')
            #entry_time_of_last_printed_order = entry_time_of_last_printed_order.lstrip('0')
            #last_print_date = last_print_date.lstrip('0')
            #last_print_time = last_print_time.lstrip('0')
        else:
            raise pickpack_errors.ApplicationError("Error: %s select data returned more than one row. Data: %s" % (self.__class__.__name__, data))

        return (formatted_order_number,
                entry_date_of_last_printed_order,
                entry_time_of_last_printed_order,
                last_print_date,
                last_print_time,
               )


# ====================================
#  With cutoff or without
# ====================================

class WithCutoff(SQLBuilderUtility):
    """
    Mixin for queries that define a cutoff time.
    """
    def __init__(self, *args, **kwargs):
        super(WithCutoff, self).__init__(*args, **kwargs)

        self.addColumnToColumnStructure(
            column_definition = """
                case
                when oh.ohetdt >= int(varchar_format(CURRENT_TIMESTAMP, 'YYMMDD'))

                {cutoff_time_clause}

                then 'N'    -- After cutoff
                else 'Y'    -- Before cutoff
                end
            """.format(cutoff_time_clause = self.CUTOFF_TIME_CLAUSE),        # pylint: disable=no-member
            column_name = 'before_cutoff',
        )


class NoCutoff(object):
    """
    Mixin for queries that do not define a cutoff time.
    """
    def __init__(self, *args, **kwargs):
        super(NoCutoff, self).__init__(*args, **kwargs)










# ====================================
#  Summary vs Detail, with cutoff or without
# ====================================

class Summary(SQLBuilderBase):
    """
    Base for data fetching classes for summary (count) data
    """
    SQL_TEMPLATE = """
        {outer_select_clause}
        from (
            {inner_select_clause}
            {common_sql}
        ) as temp
        {group_by_clause}
    """
    def __init__(self, *args, **kwargs):
        super(Summary, self).__init__(*args, **kwargs)

        # After all the classes in the hierarchy have had a chance to call
        # __init__ and add their columns to self.column_structure, we build
        # another column structure based on self.column_structure. This new
        # column structure will give us the outer select statement.
        count_column_structure = self.makeColumnStructure('count(*)', 'count')
        if hasattr(self, 'column_structure'):
            # The column_structure attribute already exists for this object.
            # Build the outer select column structure based on the aliases of
            # self.column_structure.
            outer_column_structure = shopfloor_monitor_classes.make_column_structure(*
                (
                    shopfloor_monitor_classes.Column(
                        definition = inner_column_alias,
                        name = inner_column_alias,
                    )
                    for inner_column_alias
                    in self.column_structure._aliases                           # pylint: disable=protected-access
                )
            )
            outer_column_structure += count_column_structure
        else:
            # No self.column_structure attribute found. Just use the count
            # column as our outer_column_structure
            outer_column_structure = count_column_structure
        self.outer_column_structure = outer_column_structure

    def build_formatting_data(self,
                              shipping_station,
                             ):
        """
        Build and return a dictionary with the data we need to render the sql
        template.
        """
        return {
            'outer_select_clause'   : self.outer_column_structure._select_clause_just_definitions,          # pylint: disable=protected-access
            'inner_select_clause'   : self.column_structure._select_clause_definitions_and_aliases,         # pylint: disable=protected-access
            'common_sql'            : self.build_common_sql(shipping_station),
            'group_by_clause'       : self.column_structure._group_by_clause_aliases,                       # pylint: disable=protected-access
        }


class SummaryWithCutoff(Summary, WithCutoff):
    """
    Fetches summary data (counts) for service types that do have a cutoff
    """
    def __init__(self, *args, **kwargs):
        super(SummaryWithCutoff, self).__init__(*args, **kwargs)

    def parse_query_results(self,
                            data,
                           ):
        """
        The query for orders returns counts for orders in various statuses.

        This function parses that data from the database and sums it up in to
        count of orders in two different statuses:

           should_ship_today    - order date is before the cutoff.
           can_ship_tomorrow    - order date is after the cutoff.
        """

        if len(data) > 6:
            raise pickpack_errors.ApplicationError("Error: %s select data returned more than six rows. Data: %s" % (self.__class__.__name__, data))

        # Here's what the data looks like from the query
        #
        #  before_cutoff   order_status       count(*)
        #     N                 1                5
        #     N                 2               15
        #     N                 3                4
        #     Y                 1               29
        #     Y                 2                9
        #     Y                 3                7
        #
        # We parse it in this cumbersome way because some rows might be missing.

        can_ship_tomorrow_ready_to_print      = 0
        can_ship_tomorrow_pick_slip_printed   = 0
        can_ship_tomorrow_packed              = 0
        should_ship_today_ready_to_print      = 0
        should_ship_today_pick_slip_printed   = 0
        should_ship_today_packed              = 0

        for (before_cutoff,
             order_status,
             count,
            ) in data:
            if before_cutoff == 'N':
                if order_status == self.Constants.OrderStatus.ReadyToPrint:               # pylint: disable=no-member
                    can_ship_tomorrow_ready_to_print += count
                elif order_status == self.Constants.OrderStatus.PickSlipPrinted:          # pylint: disable=no-member
                    can_ship_tomorrow_pick_slip_printed += count
                elif order_status == self.Constants.OrderStatus.Packed:                   # pylint: disable=no-member
                    can_ship_tomorrow_packed += count
                else:
                    raise pickpack_errors.ApplicationError("Error: Invalid value %s for order_status Data: %s" % (order_status, data))
            elif before_cutoff == 'Y':
                if order_status == self.Constants.OrderStatus.ReadyToPrint:               # pylint: disable=no-member
                    should_ship_today_ready_to_print += count
                elif order_status == self.Constants.OrderStatus.PickSlipPrinted:          # pylint: disable=no-member
                    should_ship_today_pick_slip_printed += count
                elif order_status == self.Constants.OrderStatus.Packed:                   # pylint: disable=no-member
                    should_ship_today_packed += count
                else:
                    raise pickpack_errors.ApplicationError("Error: Invalid value %s for order_status Data: %s" % (order_status, data))
            else:
                raise pickpack_errors.ApplicationError("Error: Invalid value %s for before_cutoff Data: %s" % (before_cutoff, data))

        return (can_ship_tomorrow_ready_to_print,
                can_ship_tomorrow_pick_slip_printed,
                can_ship_tomorrow_packed,
                should_ship_today_ready_to_print,
                should_ship_today_pick_slip_printed,
                should_ship_today_packed,
               )


class SummaryNoCutoff(Summary, NoCutoff):
    """
    Fetches summary data (counts) for service types that don't have a cutoff
    """
    def __init__(self, *args, **kwargs):
        super(SummaryNoCutoff, self).__init__(*args, **kwargs)

    def parse_query_results(self,
                            data,
                           ):
        """
        The query for no-cutoff service types returns counts of orders grouped
        by order progress.
        """
        # Override base class' parsing

        if len(data) > 3:
            raise pickpack_errors.ApplicationError("Error: %s select data returned more than three rows. Data: %s" % (self.__class__.__name__, data))

        # Here's what the data looks like from the query
        #
        #   order_status       count(*)
        #        1                5
        #        2               15
        #        3                4
        #
        # We parse it in this cumbersome way because some rows might be missing.

        should_ship_today_ready_to_print      = 0
        should_ship_today_pick_slip_printed   = 0
        should_ship_today_packed              = 0

        for (order_status,
             count,
            ) in data:
            if order_status == self.Constants.OrderStatus.ReadyToPrint:               # pylint: disable=no-member
                should_ship_today_ready_to_print += count
            elif order_status == self.Constants.OrderStatus.PickSlipPrinted:          # pylint: disable=no-member
                should_ship_today_pick_slip_printed += count
            elif order_status == self.Constants.OrderStatus.Packed:                   # pylint: disable=no-member
                should_ship_today_packed += count
            else:
                raise pickpack_errors.ApplicationError("Error: Invalid value %s for order_status Data: %s" % (order_status, data))

        return (should_ship_today_ready_to_print,
                should_ship_today_pick_slip_printed,
                should_ship_today_packed,
               )


class Detail(SQLBuilderBase):
    """
    Base for data fetching classes for detail data (order numbers)
    """
    SQL_TEMPLATE = """
        {select_clause}
        {common_sql}
        {order_by_clause}
    """
    def __init__(self, *args, **kwargs):
        super(Detail, self).__init__(*args, **kwargs)

        self.addColumnToColumnStructure(
            column_definition = self.build_formatted_order_number_definition('oh.ohorno', 'oh.ohorgn'),
            column_name = 'formatted_order_number',
        )

    def build_formatting_data(self,
                              shipping_station,
                             ):
        """
        Build and return a dictionary with the data we need to render the sql
        template.
        """
        return {
            'select_clause'         : self.column_structure._select_clause_definitions_and_aliases,     # pylint: disable=protected-access
            'common_sql'            : self.build_common_sql(shipping_station),
            'order_by_clause'       : self.column_structure._order_by_clause_aliases,                   # pylint: disable=protected-access
        }

    @staticmethod
    def sort_and_truncate(order_numbers):
        """
        If the list of order numbers is longer than MAX_ORDER_NUMBERS, truncate
        the list and add an element indicating how many items were truncated.
        Also, sort the list.
        """
        # We have to sort first. Otherwise, the "... 388 More" trucation message
        # gets sorted to the top of the list. CPU and RAM are cheap, right?
        sorted_list = sorted(order_numbers)
        truncated_list = pickpack_common.truncateList(sorted_list, pickpack_constants.MAX_ORDER_NUMBERS)
        return truncated_list


class DetailWithCutoff(Detail, WithCutoff):
    """
    Fetches detail data (order numbers) for service types that do have a cutoff
    """
    def __init__(self, *args, **kwargs):
        super(DetailWithCutoff, self).__init__(*args, **kwargs)

    def parse_query_results(self,
                            data,
                           ):
        """
        The sql query returns a list of rows, one for each order number. The
        orders are ordered by cutoff and status. Here we split those rows in to
        groups, by cutoff and by status. If the groups are longer than
        pickpack_constants.MAX_ORDER_NUMBERS, the groups are truncated.
        """

        # We parse it in this cumbersome way because some groups might be
        # missing.
        can_ship_tomorrow_ready_to_print      = []
        can_ship_tomorrow_pick_slip_printed   = []
        can_ship_tomorrow_packed              = []
        should_ship_today_ready_to_print      = []
        should_ship_today_pick_slip_printed   = []
        should_ship_today_packed              = []

        index_of_order_no = self.column_structure._indexof('formatted_order_number')        # pylint: disable=protected-access
        index_of_before_cutoff = self.column_structure._indexof('before_cutoff')            # pylint: disable=protected-access
        index_of_order_status = self.column_structure._indexof('order_status')              # pylint: disable=protected-access
        for keys, rows in itertools.groupby(data, lambda row: (row[index_of_before_cutoff], row[index_of_order_status])):
            before_cutoff = keys[0]
            order_status = keys[1]
            if before_cutoff == 'N':
                if order_status == self.Constants.OrderStatus.ReadyToPrint:                 # pylint: disable=no-member
                    can_ship_tomorrow_ready_to_print.extend(row[index_of_order_no] for row in rows)
                elif order_status == self.Constants.OrderStatus.PickSlipPrinted:            # pylint: disable=no-member
                    can_ship_tomorrow_pick_slip_printed.extend(row[index_of_order_no] for row in rows)
                elif order_status == self.Constants.OrderStatus.Packed:                     # pylint: disable=no-member
                    can_ship_tomorrow_packed.extend(row[index_of_order_no] for row in rows)
                else:
                    raise pickpack_errors.ApplicationError("Error: Invalid value %s for order_status Data: %s" % (order_status, data))
            elif before_cutoff == 'Y':
                if order_status == self.Constants.OrderStatus.ReadyToPrint:                 # pylint: disable=no-member
                    should_ship_today_ready_to_print.extend(row[index_of_order_no] for row in rows)
                elif order_status == self.Constants.OrderStatus.PickSlipPrinted:            # pylint: disable=no-member
                    should_ship_today_pick_slip_printed.extend(row[index_of_order_no] for row in rows)
                elif order_status == self.Constants.OrderStatus.Packed:                     # pylint: disable=no-member
                    should_ship_today_packed.extend(row[index_of_order_no] for row in rows)
                else:
                    raise pickpack_errors.ApplicationError("Error: Invalid value %s for order_status Data: %s" % (order_status, data))
            else:
                raise pickpack_errors.ApplicationError("Error: Invalid value %s for before_cutoff Data: %s" % (before_cutoff, data))

        return (self.sort_and_truncate(can_ship_tomorrow_ready_to_print),
                self.sort_and_truncate(can_ship_tomorrow_pick_slip_printed),
                self.sort_and_truncate(can_ship_tomorrow_packed),
                self.sort_and_truncate(should_ship_today_ready_to_print),
                self.sort_and_truncate(should_ship_today_pick_slip_printed),
                self.sort_and_truncate(should_ship_today_packed),
               )


class DetailNoCutoff(Detail, NoCutoff):
    """
    Fetches detail data (order numbers) for service types that don't have a cutoff
    """
    def __init__(self, *args, **kwargs):
        super(DetailNoCutoff, self).__init__(*args, **kwargs)

    def parse_query_results(self,
                            data,
                           ):
        """
        The sql query returns a list of rows, one for each order number. The
        orders are ordered by status. Here we split those rows in to groups, by
        status. If the groups are longer than
        pickpack_constants.MAX_ORDER_NUMBERS, the groups are truncated.
        """

        # We parse it in this cumbersome way because some groups might be
        # missing.
        should_ship_today_ready_to_print      = []
        should_ship_today_pick_slip_printed   = []
        should_ship_today_packed              = []

        index_of_order_no = self.column_structure._indexof('formatted_order_number')    # pylint: disable=protected-access
        index_of_order_status = self.column_structure._indexof('order_status')          # pylint: disable=protected-access
        for key, rows in itertools.groupby(data, lambda row: row[index_of_order_status]):
            order_status = key
            if order_status == self.Constants.OrderStatus.ReadyToPrint:                 # pylint: disable=no-member
                should_ship_today_ready_to_print.extend(row[index_of_order_no] for row in rows)
            elif order_status == self.Constants.OrderStatus.PickSlipPrinted:            # pylint: disable=no-member
                should_ship_today_pick_slip_printed.extend(row[index_of_order_no] for row in rows)
            elif order_status == self.Constants.OrderStatus.Packed:                     # pylint: disable=no-member
                should_ship_today_packed.extend(row[index_of_order_no] for row in rows)
            else:
                raise pickpack_errors.ApplicationError("Error: Invalid value %s for order_status Data: %s" % (order_status, data))

        return (self.sort_and_truncate(should_ship_today_ready_to_print),
                self.sort_and_truncate(should_ship_today_pick_slip_printed),
                self.sort_and_truncate(should_ship_today_packed),
               )










# ====================================
#  Service Level
# ====================================

class TodaySure(object):
    """
    SQL for Today Sure orders
    """
    # Today Sure orders have a 4:30 pm cutoff. Here we express that as an
    # integer, 163000.
    CUTOFF_TIME_CLAUSE = "and oh.ohettm > 163000"
    ORDER_TYPE_DATABASE_VALUE = "T"
    def __init__(self, *args, **kwargs):
        super(TodaySure, self).__init__(*args, **kwargs)


class SignatureService(object):
    """
    SQL for Signature Service orders
    """
    # Signature Service orders have a 1 pm cutoff. Here we express that as as an
    # integer, 130000.
    CUTOFF_TIME_CLAUSE = "and oh.ohettm > 130000"
    ORDER_TYPE_DATABASE_VALUE = "SS"
    def __init__(self, *args, **kwargs):
        super(SignatureService, self).__init__(*args, **kwargs)


class ServiceFile(object):
    """
    SQL for Service File orders
    """
    ORDER_TYPE_DATABASE_VALUE = "S"
    def __init__(self, *args, **kwargs):
        super(ServiceFile, self).__init__(*args, **kwargs)


class Normal(object):
    """
    SQL for Normal orders
    """
    # Only Normal orders from today (or future) are after cutoff. Yesterday's
    # Normal orders are before cutoff. No time component, just yesterday and
    # today.
    CUTOFF_TIME_CLAUSE = ""
    ORDER_TYPE_DATABASE_VALUE = "N"
    def __init__(self, *args, **kwargs):
        super(Normal, self).__init__(*args, **kwargs)






# ====================================
#  Ordinary or Backorder
# ====================================

class Ordinary(object):
    """
    Mixin for ordinary (non-backordered) orders
    """
    BACKORDER = False
    def __init__(self, *args, **kwargs):
        super(Ordinary, self).__init__(*args, **kwargs)


class Backorder(object):
    """
    Mixin for backordered orders
    """
    BACKORDER = True
    def __init__(self, *args, **kwargs):
        super(Backorder, self).__init__(*args, **kwargs)







# ====================================
#  Ordinary Summary data
# ====================================

class TodaySureOrdinarySummary(SummaryWithCutoff, TodaySure, Ordinary):
    """
    Fetches summary data (counts) for ordinary Today Sure orders
    """
    def __init__(self, *args, **kwargs):
        super(TodaySureOrdinarySummary, self).__init__(*args, **kwargs)


class SignatureServiceOrdinarySummary(SummaryWithCutoff, SignatureService, Ordinary):
    """
    Fetches summary data (counts) for ordinary Signature Service orders
    """
    def __init__(self, *args, **kwargs):
        super(SignatureServiceOrdinarySummary, self).__init__(*args, **kwargs)


class ServiceFileOrdinarySummary(SummaryNoCutoff, ServiceFile, Ordinary):
    """
    Fetches summary data (counts) for ordinary Service File orders
    """
    def __init__(self, *args, **kwargs):
        super(ServiceFileOrdinarySummary, self).__init__(*args, **kwargs)


class NormalOrdinarySummary(SummaryWithCutoff, Normal, Ordinary):
    """
    Fetches summary data (counts) for ordinary Normal orders
    """
    def __init__(self, *args, **kwargs):
        super(NormalOrdinarySummary, self).__init__(*args, **kwargs)







# ====================================
#  Ordinary Detail data
# ====================================

class TodaySureOrdinaryDetail(DetailWithCutoff, TodaySure, Ordinary):
    """
    Fetches detail data (counts) for ordinary Today Sure orders
    """
    def __init__(self, *args, **kwargs):
        super(TodaySureOrdinaryDetail, self).__init__(*args, **kwargs)


class SignatureServiceOrdinaryDetail(DetailWithCutoff, SignatureService, Ordinary):
    """
    Fetches detail data (counts) for ordinary Signature Service orders
    """
    def __init__(self, *args, **kwargs):
        super(SignatureServiceOrdinaryDetail, self).__init__(*args, **kwargs)


class ServiceFileOrdinaryDetail(DetailNoCutoff, ServiceFile, Ordinary):
    """
    Fetches detail data (counts) for ordinary Service File orders
    """
    def __init__(self, *args, **kwargs):
        super(ServiceFileOrdinaryDetail, self).__init__(*args, **kwargs)


class NormalOrdinaryDetail(DetailWithCutoff, Normal, Ordinary):
    """
    Fetches detail data (counts) for ordinary Normal orders
    """
    def __init__(self, *args, **kwargs):
        super(NormalOrdinaryDetail, self).__init__(*args, **kwargs)














# ====================================
#  Backorder Summary data
# ====================================

class TodaySureBackorderSummary(SummaryNoCutoff, TodaySure, Backorder):
    """
    Fetches summary data (counts) for backordered Today Sure orders
    """
    def __init__(self, *args, **kwargs):
        super(TodaySureBackorderSummary, self).__init__(*args, **kwargs)


class SignatureServiceBackorderSummary(SummaryNoCutoff, SignatureService, Backorder):
    """
    Fetches summary data (counts) for backordered Signature Service orders
    """
    def __init__(self, *args, **kwargs):
        super(SignatureServiceBackorderSummary, self).__init__(*args, **kwargs)


class ServiceFileBackorderSummary(SummaryNoCutoff, ServiceFile, Backorder):
    """
    Fetches summary data (counts) for backordered Service File orders
    """
    def __init__(self, *args, **kwargs):
        super(ServiceFileBackorderSummary, self).__init__(*args, **kwargs)


class NormalBackorderSummary(SummaryNoCutoff, Normal, Backorder):
    """
    Fetches summary data (counts) for backordered Normal orders
    """
    def __init__(self, *args, **kwargs):
        super(NormalBackorderSummary, self).__init__(*args, **kwargs)













# ====================================
#  Backorder Detail data
# ====================================

class TodaySureBackorderDetail(DetailNoCutoff, TodaySure, Backorder):
    """
    Fetches detail data (counts) for backordered Today Sure orders
    """
    def __init__(self, *args, **kwargs):
        super(TodaySureBackorderDetail, self).__init__(*args, **kwargs)


class SignatureServiceBackorderDetail(DetailNoCutoff, SignatureService, Backorder):
    """
    Fetches detail data (counts) for backordered Signature Service orders
    """
    def __init__(self, *args, **kwargs):
        super(SignatureServiceBackorderDetail, self).__init__(*args, **kwargs)


class ServiceFileBackorderDetail(DetailNoCutoff, ServiceFile, Backorder):
    """
    Fetches detail data (counts) for backordered Service File orders
    """
    def __init__(self, *args, **kwargs):
        super(ServiceFileBackorderDetail, self).__init__(*args, **kwargs)


class NormalBackorderDetail(DetailNoCutoff, Normal, Backorder):
    """
    Fetches detail data (counts) for backordered Normal orders
    """
    def __init__(self, *args, **kwargs):
        super(NormalBackorderDetail, self).__init__(*args, **kwargs)









# ====================================
#  Last print data
# ====================================

class TodaySureLastPrint(LastPrint, TodaySure):
    """
    Fetches last print data for Today Sure orders
    """
    def __init__(self, *args, **kwargs):
        super(TodaySureLastPrint, self).__init__(*args, **kwargs)


class SignatureServiceLastPrint(LastPrint, SignatureService):
    """
    Fetches last print data for Signature Service orders
    """
    def __init__(self, *args, **kwargs):
        super(SignatureServiceLastPrint, self).__init__(*args, **kwargs)


class ServiceFileLastPrint(LastPrint, ServiceFile):
    """
    Fetches last print data for Service File orders
    """
    def __init__(self, *args, **kwargs):
        super(ServiceFileLastPrint, self).__init__(*args, **kwargs)


class NormalLastPrint(LastPrint, Normal):
    """
    Fetches last print data for Normal orders
    """
    def __init__(self, *args, **kwargs):
        super(NormalLastPrint, self).__init__(*args, **kwargs)














# ====================================
#  Order number detail data
# ====================================

class OrderNumberDetail(SQLBuilderCommon):
    """
    Data fetching class for order number detail data
    """
    SQL1 = """
        select oh.ohcsno        "Customer number"
             , oh.ohorno        "Order Number"
             , oh.ohorgn        "Order Generation"
             , oh.ohorst        "Order status code"
             , trim(oh.ohcsnm)  "customer name"
             , trim(oh.ohetus)  "Entered by"
             , trim(oh.ohbkcd)  "Backorder Code"
             , trim(oh.ohspin)  "Shipping Instructions"
             , trim(oh.ohcacd)  "Carrier Code"
             , trim(oh.ohpacc)  "Packer ID"
             , trim(oh.ohpicc)  "Picker ID"
             , trim(oh.ohppus)  "Printer ID"
             , oh.ohshwt        "Shipped Order Weight"
             , (select count(*)
                from ordet od
                join itmst im
                on od.oditno = im.imitno
                where od.odcono = oh.ohcono
                and od.odorno = oh.ohorno
                and od.odorgn = oh.ohorgn
                and od.odlitp = 'I'                     -- Line item type: I is for Items, C Charges, M Comments
                and od.odqtsh > 0                       -- Quantity shipped
               ) "Number of lines"
             , case
               when trim(oh.ohfl01) = 'T'
               then 'Truck'
               else ''
               end  "Truck Team"
             , case
               when trim(oh.ohcscd) = 'H'
               then 'Complete'
               else 'Partial'
               end  "Complete Ship Code"
             , case
               when trim(substr(oh.ohus15, 8, 2)) = 'T'
               then 'Today Sure'
               when trim(substr(oh.ohus15, 8, 2)) = 'SS'
               then 'Signature Service'
               when trim(substr(oh.ohus15, 8, 2)) = 'S'
               then 'Service File'
               when trim(substr(oh.ohus15, 8, 2)) = 'N'
               then 'Normal'
               else trim(substr(oh.ohus15, 8, 2))
               end "Service Level"

        from orhed oh
        where oh.ohwhid = 'PW'
        and oh.ohcono = 1
        and oh.ohortp = 'O'
        and oh.ohorno = ?
        and oh.ohorgn = ?
    """

    SQL2 = """
        select  case
                when temp1.print_date_as_int_string is null
                then null
                else trim(leading '0' from substr(temp1.print_date_as_int_string, 5, 2 )) ||
                     '/' ||
                     trim(leading '0' from substr(temp1.print_date_as_int_string, 7, 2 )) ||
                     '/' ||
                     trim(leading '0' from substr(temp1.print_date_as_int_string, 1, 4 ))
                end print_date_as_string
             ,  case
                when temp1.print_time_as_int_string is null
                then null
                -- Round-trip through the DB2 time format, to make sure it
                -- is formatted consistently (AM, PM, etc.)
                else trim(leading '0' from char(time(
                        substr(temp1.print_time_as_int_string, 1, 2 ) ||        -- Two hour characters
                        ':' ||                                                  -- ISO standard time separator
                        substr(temp1.print_time_as_int_string, 3, 2 ) ||        -- Two minute characters
                        ':' ||                                                  -- ISO standard time separator
                        substr(temp1.print_time_as_int_string, 5, 2 )           -- Two second characters
                    ), USA))
                end print_time_as_string
            , case
                when temp1.order_entry_date_as_int_string is null
                then null
                else trim(leading '0' from substr(temp1.order_entry_date_as_int_string, 5, 2 )) ||
                     '/' ||
                     trim(leading '0' from substr(temp1.order_entry_date_as_int_string, 7, 2 )) ||
                     '/' ||
                     trim(leading '0' from substr(temp1.order_entry_date_as_int_string, 1, 4 ))
                end order_entry_date_as_string
             ,  case
                when temp1.order_entry_time_as_int_string is null
                then null
                -- Round-trip through the DB2 time format, to make sure it
                -- is formatted consistently (AM, PM, etc.)
                else trim(leading '0' from char(time(
                         substr(temp1.order_entry_time_as_int_string, 1, 2 ) ||
                         ':' ||
                         substr(temp1.order_entry_time_as_int_string, 3, 2 ) ||
                         ':' ||
                         substr(temp1.order_entry_time_as_int_string, 5, 2 )
                    ), USA))
                end order_entry_time_as_string
            , case
                when temp1.requested_ship_date_as_int_string is null
                then null
                else trim(leading '0' from substr(temp1.requested_ship_date_as_int_string, 5, 2 )) ||
                     '/' ||
                     trim(leading '0' from substr(temp1.requested_ship_date_as_int_string, 7, 2 )) ||
                     '/' ||
                     trim(leading '0' from substr(temp1.requested_ship_date_as_int_string, 1, 4 ))
                end requested_ship_date_as_string
        from (
            select  case
                    when oh.ohppdt is null
                    then null
                    when oh.ohppdt = 0
                    then null
                    else trim(char(oh.ohppcc)) ||                    -- Two century digits
                         right(                                      -- Left-zero-pad the string, to allow for single-digit years
                             repeat('0', 6) || trim(char(oh.ohppdt)),
                             6
                         )
                    end print_date_as_int_string
                 ,  case
                    when oh.ohpptm is null
                    then null
                    when oh.ohpptm = 0
                    then null
                    else right(                                      -- Left-zero-pad the string, to allow for single-digit hours
                             repeat('0', 6) || trim(char(oh.ohpptm)),
                             6
                         )
                    end print_time_as_int_string
                 ,  case
                    when oh.ohetdt is null
                    then null
                    when oh.ohetdt = 0
                    then null
                    else trim(char(oh.ohetcc)) ||
                         right(
                             repeat('0', 6) || trim(char(oh.ohetdt)),
                             6
                         )
                    end order_entry_date_as_int_string
                 ,  case
                    when oh.ohettm is null
                    then null
                    when oh.ohettm = 0
                    then null
                    else right(
                             repeat('0', 6) || trim(char(oh.ohettm)),
                             6
                         )
                    end order_entry_time_as_int_string
                 ,  case
                    when oh.ohrsdt is null
                    then null
                    when oh.ohrsdt = 0
                    then null
                    else trim(char(oh.ohrscc)) ||
                         right(
                             repeat('0', 6) || trim(char(oh.ohrsdt)),
                             6
                         )
                    end requested_ship_date_as_int_string
            from orhed oh
            where oh.ohwhid = 'PW'
            and oh.ohcono = 1
            and oh.ohortp = 'O'
            and oh.ohorno = ?
            and oh.ohorgn = ?
        ) as temp1
    """

    SQL3 = """
        select trim(od.oditd1 || od.oditd2) note_text
        from ordet od
        where od.odlitp = 'M'
        and trim(od.oditno) not in ('/RS', '/RH', '/PR', '/ RS', '/ RH', '/ PR')
        and od.odorno = ?
        and od.odorgn = ?
        group by trim(od.oditd1 || od.oditd2)
        order by max(od.odorsq)
    """



    def __init__(self, *args, **kwargs):
        super(OrderNumberDetail, self).__init__(*args, **kwargs)

    def get_data(self,                                              # pylint: disable=arguments-differ
                 transaction_cursor,
                 order_number,
                 order_generation,
                ):
        """
        Return the needed data, parsed and formatted.
        """
        params = [order_number, order_generation]
        data1 = self.run_query(transaction_cursor, self.SQL1, params)
        data2 = self.run_query(transaction_cursor, self.SQL2, params)
        data3 = self.run_query(transaction_cursor, self.SQL3, params)
        return self.parse_query_results(pickpack_data.clean_the_data(data1),
                                        pickpack_data.clean_the_data(data2),
                                        pickpack_data.clean_the_data(data3),
                                       )

    def parse_query_results(self,
                            data1,
                            data2,
                            data3,
                           ):
        """
        The query returns formatted order number and generation, the date and
        time that order was entered, and the date and time of last print.
        """
        if data1 is None or len(data1) == 0:
            customer_number                 = pickpack_constants.NO_DATA_FOUND
            order_number                    = pickpack_constants.NO_DATA_FOUND
            order_generation                = pickpack_constants.NO_DATA_FOUND
            order_status_code               = pickpack_constants.NO_DATA_FOUND
            customer_name                   = pickpack_constants.NO_DATA_FOUND
            entered_by                      = pickpack_constants.NO_DATA_FOUND
            backorder_code                  = pickpack_constants.NO_DATA_FOUND
            shipping_instructions           = pickpack_constants.NO_DATA_FOUND
            carrier_code                    = pickpack_constants.NO_DATA_FOUND
            packer_id                       = pickpack_constants.NO_DATA_FOUND
            picker_id                       = pickpack_constants.NO_DATA_FOUND
            printer_id                      = pickpack_constants.NO_DATA_FOUND
            shipped_order_weight            = pickpack_constants.NO_DATA_FOUND
            number_of_lines                 = pickpack_constants.NO_DATA_FOUND
            truck_team                      = pickpack_constants.NO_DATA_FOUND
            complete_ship_code              = pickpack_constants.NO_DATA_FOUND
            service_level                   = pickpack_constants.NO_DATA_FOUND
        elif len(data1) == 1:
            (customer_number,
             order_number,
             order_generation,
             order_status_code,
             customer_name,
             entered_by,
             backorder_code,
             shipping_instructions,
             carrier_code,
             packer_id,
             picker_id,
             printer_id,
             shipped_order_weight,
             number_of_lines,
             truck_team,
             complete_ship_code,
             service_level,
            ) = data1[0]
        else:
            raise pickpack_errors.ApplicationError("Error: %s select data1 returned more than one row. Data1: %s" % (self.__class__.__name__, data1))

        if data2 is None or len(data2) == 0:
            print_date                      = pickpack_constants.NO_DATA_FOUND
            print_time                      = pickpack_constants.NO_DATA_FOUND
            order_entry_date                = pickpack_constants.NO_DATA_FOUND
            order_entry_time                = pickpack_constants.NO_DATA_FOUND
            requested_ship_date             = pickpack_constants.NO_DATA_FOUND
        elif len(data2) == 1:
            (print_date,
             print_time,
             order_entry_date,
             order_entry_time,
             requested_ship_date,
            ) = data2[0]
            if print_date is None:
                print_date = pickpack_constants.NO_DATA_FOUND
            if print_time is None:
                print_time = pickpack_constants.NO_DATA_FOUND
            if requested_ship_date is None:
                requested_ship_date = pickpack_constants.NO_DATA_FOUND
        else:
            raise pickpack_errors.ApplicationError("Error: %s select data2 returned more than one row. Data2: %s" % (self.__class__.__name__, data2))

        if data3 is None:
            raise pickpack_errors.ApplicationError("Error: %s select data3 returned None" % self.__class__.__name__)
        elif len(data3) == 0:
            order_notes = pickpack_constants.NO_DATA_FOUND
        else:
            order_notes = data3

        return (customer_number,
                order_number,
                order_generation,
                order_status_code,
                customer_name,
                entered_by,
                backorder_code,
                shipping_instructions,
                carrier_code,
                packer_id,
                picker_id,
                printer_id,
                shipped_order_weight,
                number_of_lines,
                truck_team,
                complete_ship_code,
                service_level,
                print_date,
                print_time,
                order_entry_date,
                order_entry_time,
                requested_ship_date,
                order_notes,
               )




# ====================================
# Persistent, module-level instances of our data classes
# ====================================

today_sure_ordinary_summary_provider = TodaySureOrdinarySummary()
signature_service_ordinary_summary_provider = SignatureServiceOrdinarySummary()
service_files_ordinary_summary_provider = ServiceFileOrdinarySummary()
normal_ordinary_summary_provider = NormalOrdinarySummary()

today_sure_backorder_summary_provider = TodaySureBackorderSummary()
signature_service_backorder_summary_provider = SignatureServiceBackorderSummary()
service_files_backorder_summary_provider = ServiceFileBackorderSummary()
normal_backorder_summary_provider = NormalBackorderSummary()

today_sure_ordinary_summary_provider = TodaySureOrdinarySummary()
signature_service_ordinary_summary_provider = SignatureServiceOrdinarySummary()
service_files_ordinary_summary_provider = ServiceFileOrdinarySummary()
normal_ordinary_summary_provider = NormalOrdinarySummary()

today_sure_backorder_summary_provider = TodaySureBackorderSummary()
signature_service_backorder_summary_provider = SignatureServiceBackorderSummary()
service_files_backorder_summary_provider = ServiceFileBackorderSummary()
normal_backorder_summary_provider = NormalBackorderSummary()

today_sure_ordinary_detail_data_provider = TodaySureOrdinaryDetail()
signature_service_ordinary_detail_data_provider = SignatureServiceOrdinaryDetail()
service_files_ordinary_detail_data_provider = ServiceFileOrdinaryDetail()
normal_ordinary_detail_data_provider = NormalOrdinaryDetail()

today_sure_backorder_detail_data_provider = TodaySureBackorderDetail()
signature_service_backorder_detail_data_provider = SignatureServiceBackorderDetail()
service_files_backorder_detail_data_provider = ServiceFileBackorderDetail()
normal_backorder_detail_data_provider = NormalBackorderDetail()

today_sure_last_print_data_provider = TodaySureLastPrint()
signature_service_last_print_data_provider = SignatureServiceLastPrint()
service_files_last_print_data_provider = ServiceFileLastPrint()
normal_last_print_data_provider = NormalLastPrint()

order_number_detail_data_provider = OrderNumberDetail()










#
#
#
#
#
## Notes
#
## A - alias
## D - def
#
#
## ColumnStructure
## before_cutoff:    outer A     inner DA    group A     order A
## order_status:     outer A     inner DA    group A     order A
## count:            outer D     inner       group       order
##
## Outer Select: before_cutoff, order_status, count(*)
## Inner Select: before_cutoff definition and alias, order_status definition and alias
## Group By: before_cutoff, order_status
## Order By: before_cutoff, order_status
#TodaySureOrdinarySummary
#SignatureServiceOrdinarySummary
#NormalOrdinarySummary
#
#
## ColumnStructure
## before_cutoff:    select DA   order A
## order_status:     select DA   order A
## order_number:     select DA   order A
##
## Select: before_cutoff definition and alias, order_status definition and alias, order_number definition and alias
## Order By: before_cutoff, order_status, order_number
#TodaySureOrdinaryDetail
#SignatureServiceOrdinaryDetail
#NormalOrdinaryDetail
#
#
## ColumnStructure
## order_status:     outer A     inner DA    group A     order A
## count:            outer D     inner       group       order
##
## Outer Select: order_status, count(*)
## Inner Select: order_status definition and alias
## Group By: order_status
## Order By: order_status
#ServiceFileOrdinarySummary
#TodaySureBackorderSummary
#SignatureServiceBackorderSummary
#ServiceFileBackorderSummary
#NormalBackorderSummary
#
#
## ColumnStructure
## order_status:     select DA   order A
## order_number:     select DA   order A
##
## Select: order_status definition and alias, order_number definition and alias
## Order By: order_status, order_number
#ServiceFileOrdinaryDetail
#TodaySureBackorderDetail
#SignatureServiceBackorderDetail
#ServiceFileBackorderDetail
#NormalBackorderDetail
#
##zzz
#
#SQLBuilderBase
## Adds order_status
#
#
#WithCutoff
## Adds before_cutoff
#
#NoCutoff
#
#Summary
## Adds count to a separate column structure that takes the inner select aliases as its starting point.
#
#
#SummaryWithCutoff
#
#SummaryNoCutoff
#
#
#Detail
## Adds order_number:
#
#DetailWithCutoff
#
#DetailNoCutoff
#
#TodaySure
#SignatureService
#ServiceFile
#Normal
#
#Backorder
#Ordinary
#
#
## ===================
#
#
#WithCutoff
## Adds before_cutoff to the front of self.column_structure
#
#NoCutoff
#
#Summary
## ColumnStructure
## order_status:     outer A     inner DA    group A     order A
## count:            outer D     inner       group       order
##
## Outer Select: order_status, count(*)
## Inner Select: order_status definition and alias
## Group By: order_status
## Order By: order_status
#
#
#SummaryWithCutoff
## before_cutoff:    outer A     inner DA    group A     order A
#
#SummaryNoCutoff
#
#
#Detail
## ColumnStructure
## order_status:     select DA   order A
## order_number:     select DA   order A
##
## Select: order_status definition and alias, order_number definition and alias
## Order By: order_status, order_number
#
#DetailWithCutoff
## before_cutoff:    select DA   order A

# ===================


# POSSIBLE IMPROVEMENT
# Provide a combinatoric matrix of classes, one for each case:
#
#  - backorder: yes, no
#  - shipping station: wcc, parts, etc.
#  - service type: normal, today sure, etc.
#
# Create one instance for each class. On creation, each object builds its very
# own, specific SQL string. That way we don't have to build the SQL each time we
# run the query.
#
# However, the string concatenation time is very small, so this won't present
# any real performance benefits. Especially since we cache the data resulting
# from the sql query, and thus we only run the query itself every thirty
# seconds.
#
# That said, it could lead to a conceptually cleaner structure for these classes,
# allowing us to eliminate the *args **kwargs in the co-operatively-called
# constructors.
#
# Or, go the opposite direction: define fewer classes, and have the object
# behavior modified by more arguments to the constructors.
#
# Either way, move the call to build_sql to the constructor, and save the result
# in self.sql.









# OLD code


    # Truncate (or do a top-n query in db2)
    #
    #    order by col1
    #    fetch first N row only
    #
    # In Oracle
    #
    #        SELECT val
    #        FROM   (SELECT val
    #                FROM   rownum_order_test
    #                ORDER BY val)
    #        WHERE rownum <= 5;
    #
    #       max_length = pickpack_constants.MAX_ORDER_NUMBERS
    #       pickpack_common.truncateList(bla, max_length)














# All the **kwargs in the classes above are needed because of super()
#
#   http://rhettinger.wordpress.com/2011/05/26/super-considered-super/
#   https://fuhm.net/super-harmful/
#
#        def f1(a, **kwargs):
#            print "a %s" % a
#            print "kwargs %s" % kwargs
#
#        # Errors
#        #f1(1, 3, 5)
#        #f1(1, 3, a=5)
#        #f1(1, b=3, a=5)
#
#        # These work
#        f1(1, b=3, g=5)
#        #   a 1
#        #   kwargs {'b': 3, 'g': 5}
#
#        f1(n=1, g=3, a=5)
#        #   a 5
#        #   kwargs {'g': 3, 'n': 1}
#
#        f1(a=1, g=3, h=5)
#        #   a 1
#        #   kwargs {'h': 5, 'g': 3}
#
#
#        def f2(a, *args, **kwargs):
#            print "a %s" % a
#            print "args %s" % str(args)
#            print "kwargs %s" % str(kwargs)
#
#        # Errors
#        #f2(1, 3, a=5)
#        #f2(1, b=3, a=5)
#
#        # These work
#        f2(1, 3, 5)
#        #   a 1
#        #   args (3, 5)
#        #   kwargs {}
#
#        f2(1, b=3, g=5)
#        #   a 1
#        #   args ()
#        #   kwargs {'b': 3, 'g': 5}
#
#        f2(n=1, g=3, a=5)
#        #   a 5
#        #   args ()
#        #   kwargs {'g': 3, 'n': 1}
#
#        f2(a=1, g=3, h=5)
#        #   a 1
#        #   args ()
#        #   kwargs {'h': 5, 'g': 3}





#
