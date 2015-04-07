"""
shopfloor_monitor_result_builders.py

One central place for classes that build data structures that we return to the
client.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from Common.utility.utl_classes import Freezable


# Note: it may seem that these classes aren't doing enough to justify their
# existence. However, I added these *Builder classes to impose some structure
# and consistency on the data I was returning. For example, this ensures that
# the return value data formats are the same whether we are returning database
# data or mock data.



class OrdinaryOrderStatusBuilder(Freezable):
    """
    Structure for order status data for ordinary orders (not backorders).
    """
    def __init__(self):
        Freezable.__init__(self)
        self.unfreeze_attribute_creation()

        self.today_sure_should_ship_today_ready_to_print = None
        self.today_sure_should_ship_today_pick_slip_printed = None
        self.today_sure_should_ship_today_packed = None

        self.today_sure_can_ship_tomorrow_ready_to_print = None
        self.today_sure_can_ship_tomorrow_pick_slip_printed = None
        self.today_sure_can_ship_tomorrow_packed = None

        self.signature_service_should_ship_today_ready_to_print = None
        self.signature_service_should_ship_today_pick_slip_printed = None
        self.signature_service_should_ship_today_packed = None

        self.signature_service_can_ship_tomorrow_ready_to_print = None
        self.signature_service_can_ship_tomorrow_pick_slip_printed = None
        self.signature_service_can_ship_tomorrow_packed = None

        self.service_files_should_ship_today_ready_to_print = None
        self.service_files_should_ship_today_pick_slip_printed = None
        self.service_files_should_ship_today_packed = None

        self.normal_can_ship_tomorrow_ready_to_print = None
        self.normal_can_ship_tomorrow_pick_slip_printed = None
        self.normal_can_ship_tomorrow_packed = None

        self.normal_should_ship_today_ready_to_print = None
        self.normal_should_ship_today_pick_slip_printed = None
        self.normal_should_ship_today_packed = None

        self.freeze_attribute_creation()

    def render(self):
        """
        Builds the data structure in the right format.
        """
        return {"today_sure_should_ship_today_ready_to_print" : self.today_sure_should_ship_today_ready_to_print,
                "today_sure_should_ship_today_pick_slip_printed" : self.today_sure_should_ship_today_pick_slip_printed,
                "today_sure_should_ship_today_packed" : self.today_sure_should_ship_today_packed,

                "today_sure_can_ship_tomorrow_ready_to_print" : self.today_sure_can_ship_tomorrow_ready_to_print,
                "today_sure_can_ship_tomorrow_pick_slip_printed" : self.today_sure_can_ship_tomorrow_pick_slip_printed,
                "today_sure_can_ship_tomorrow_packed" : self.today_sure_can_ship_tomorrow_packed,

                "signature_service_should_ship_today_ready_to_print" : self.signature_service_should_ship_today_ready_to_print,
                "signature_service_should_ship_today_pick_slip_printed" : self.signature_service_should_ship_today_pick_slip_printed,
                "signature_service_should_ship_today_packed" : self.signature_service_should_ship_today_packed,

                "signature_service_can_ship_tomorrow_ready_to_print" : self.signature_service_can_ship_tomorrow_ready_to_print,
                "signature_service_can_ship_tomorrow_pick_slip_printed" : self.signature_service_can_ship_tomorrow_pick_slip_printed,
                "signature_service_can_ship_tomorrow_packed" : self.signature_service_can_ship_tomorrow_packed,

                "service_files_should_ship_today_ready_to_print" : self.service_files_should_ship_today_ready_to_print,
                "service_files_should_ship_today_pick_slip_printed" : self.service_files_should_ship_today_pick_slip_printed,
                "service_files_should_ship_today_packed" : self.service_files_should_ship_today_packed,

                "normal_can_ship_tomorrow_ready_to_print" : self.normal_can_ship_tomorrow_ready_to_print,
                "normal_can_ship_tomorrow_pick_slip_printed" : self.normal_can_ship_tomorrow_pick_slip_printed,
                "normal_can_ship_tomorrow_packed" : self.normal_can_ship_tomorrow_packed,

                "normal_should_ship_today_ready_to_print" : self.normal_should_ship_today_ready_to_print,
                "normal_should_ship_today_pick_slip_printed" : self.normal_should_ship_today_pick_slip_printed,
                "normal_should_ship_today_packed" : self.normal_should_ship_today_packed,
               }


class BackorderOrderStatusBuilder(Freezable):
    """
    Structure for order status data for backorders.
    """
    def __init__(self):
        Freezable.__init__(self)
        self.unfreeze_attribute_creation()

        self.today_sure_backorder_ready_to_print = None
        self.today_sure_backorder_pick_slip_printed = None
        self.today_sure_backorder_packed = None

        self.signature_service_backorder_ready_to_print = None
        self.signature_service_backorder_pick_slip_printed = None
        self.signature_service_backorder_packed = None

        self.service_files_backorder_ready_to_print = None
        self.service_files_backorder_pick_slip_printed = None
        self.service_files_backorder_packed = None

        self.normal_backorder_ready_to_print = None
        self.normal_backorder_pick_slip_printed = None
        self.normal_backorder_packed = None

        self.freeze_attribute_creation()

    def render(self):
        """
        Builds the data structure in the right format.
        """
        return {"today_sure_backorder_ready_to_print" : self.today_sure_backorder_ready_to_print,
                "today_sure_backorder_pick_slip_printed" : self.today_sure_backorder_pick_slip_printed,
                "today_sure_backorder_packed" : self.today_sure_backorder_packed,

                "signature_service_backorder_ready_to_print" : self.signature_service_backorder_ready_to_print,
                "signature_service_backorder_pick_slip_printed" : self.signature_service_backorder_pick_slip_printed,
                "signature_service_backorder_packed" : self.signature_service_backorder_packed,

                "service_files_backorder_ready_to_print" : self.service_files_backorder_ready_to_print,
                "service_files_backorder_pick_slip_printed" : self.service_files_backorder_pick_slip_printed,
                "service_files_backorder_packed" : self.service_files_backorder_packed,

                "normal_backorder_ready_to_print" : self.normal_backorder_ready_to_print,
                "normal_backorder_pick_slip_printed" : self.normal_backorder_pick_slip_printed,
                "normal_backorder_packed" : self.normal_backorder_packed,
               }


class OrderNumberBuilder(Freezable):
    """
    Structure for order number data.
    """
    def __init__(self):
        Freezable.__init__(self)
        self.unfreeze_attribute_creation()

        self.last_print_formatted_order_number      = None
        self.entry_date_of_last_printed_order       = None
        self.entry_time_of_last_printed_order       = None
        self.last_print_date                        = None
        self.last_print_time                        = None

        self.freeze_attribute_creation()


    def add_last_print_data(self, data_dict):
        """
        Adds last print data to the data_dict dictionary. This modifies the
        dictionary in-place.
        """
        data_dict['last_print_data'] = {"last_print_formatted_order_number"     : self.last_print_formatted_order_number,
                                        "entry_date_of_last_printed_order"      : self.entry_date_of_last_printed_order,
                                        "entry_time_of_last_printed_order"      : self.entry_time_of_last_printed_order,
                                        "last_print_date"                       : self.last_print_date,
                                        "last_print_time"                       : self.last_print_time,
                                       }


class OrdinaryOrderNumberBuilder(OrderNumberBuilder):
    """
    Structure for order number data.
    """
    def __init__(self):
        OrderNumberBuilder.__init__(self)
        self.unfreeze_attribute_creation()

        self.should_ship_today_ready_to_print       = None
        self.should_ship_today_pick_slip_printed    = None
        self.should_ship_today_packed               = None
        self.can_ship_tomorrow_ready_to_print       = None
        self.can_ship_tomorrow_pick_slip_printed    = None
        self.can_ship_tomorrow_packed               = None

        self.freeze_attribute_creation()

    def render(self):
        """
        Builds the data structure in the right format.
        """
        data_dict = {"should_ship_today" : {"ready_to_print"     : self.should_ship_today_ready_to_print,
                                            "pick_slip_printed"  : self.should_ship_today_pick_slip_printed,
                                            "packed"             : self.should_ship_today_packed,
                                           },
                     "can_ship_tomorrow" : {"ready_to_print"     : self.can_ship_tomorrow_ready_to_print,
                                            "pick_slip_printed"  : self.can_ship_tomorrow_pick_slip_printed,
                                            "packed"             : self.can_ship_tomorrow_packed,
                                           },
                    }
        self.add_last_print_data(data_dict)
        return data_dict


class OrdinaryOrderNumberBuilderServiceFile(OrderNumberBuilder):
    """
    Structure for order number data for Service File orders.
    """
    def __init__(self):
        OrderNumberBuilder.__init__(self)
        self.unfreeze_attribute_creation()

        self.should_ship_today_ready_to_print       = None
        self.should_ship_today_pick_slip_printed    = None
        self.should_ship_today_packed               = None

        self.freeze_attribute_creation()

    def render(self):
        """
        Builds the data structure in the right format.
        """
        data_dict = {"should_ship_today" : {"ready_to_print"     : self.should_ship_today_ready_to_print,
                                            "pick_slip_printed"  : self.should_ship_today_pick_slip_printed,
                                            "packed"             : self.should_ship_today_packed,
                                           },
                    }
        self.add_last_print_data(data_dict)
        return data_dict


class BackorderOrderNumberBuilder(OrderNumberBuilder):
    """
    Structure for order number data for backorders.
    """
    def __init__(self):
        OrderNumberBuilder.__init__(self)
        self.unfreeze_attribute_creation()

        self.backorder_ready_to_print               = None
        self.backorder_pick_slip_printed            = None
        self.backorder_packed                       = None

        self.freeze_attribute_creation()

    def render(self):
        """
        Builds the data structure in the right format.
        """
        data_dict = {"backorder" : {"ready_to_print"     : self.backorder_ready_to_print,
                                    "pick_slip_printed"  : self.backorder_pick_slip_printed,
                                    "packed"             : self.backorder_packed,
                                   },
                    }
        self.add_last_print_data(data_dict)
        return data_dict


class OrderDataBuilder(Freezable):
    """
    Structure for data about one individual order.
    """
    def __init__(self):
        Freezable.__init__(self)
        self.unfreeze_attribute_creation()

        self.customer_number                    = None
        self.order_number                       = None
        self.order_generation                   = None
        self.order_status_code                  = None
        self.customer_name                      = None
        self.entered_by                         = None
        self.backorder_code                     = None
        self.shipping_instructions              = None
        self.carrier_code                       = None
        self.packer_id                          = None
        self.picker_id                          = None
        self.printer_id                         = None
        self.shipped_order_weight               = None
        self.number_of_lines                    = None
        self.truck_team                         = None
        self.complete_ship_code                 = None
        self.service_level                      = None
        self.print_date                         = None
        self.print_time                         = None
        self.order_entry_date                   = None
        self.order_entry_time                   = None
        self.requested_ship_date                = None
        self.order_notes                        = None

        self.freeze_attribute_creation()

    def render(self):
        """
        Builds the data structure in the right format.
        """
        return {"customer_number"               : self.customer_number          ,
                "order_number"                  : self.order_number             ,
                "order_generation"              : self.order_generation         ,
                "order_status_code"             : self.order_status_code        ,
                "customer_name"                 : self.customer_name            ,
                "entered_by"                    : self.entered_by               ,
                "backorder_code"                : self.backorder_code           ,
                "shipping_instructions"         : self.shipping_instructions    ,
                "carrier_code"                  : self.carrier_code             ,
                "packer_id"                     : self.packer_id                ,
                "picker_id"                     : self.picker_id                ,
                "printer_id"                    : self.printer_id               ,
                "shipped_order_weight"          : self.shipped_order_weight     ,
                "number_of_lines"               : self.number_of_lines          ,
                "truck_team"                    : self.truck_team               ,
                "complete_ship_code"            : self.complete_ship_code       ,
                "service_level"                 : self.service_level            ,
                "print_date"                    : self.print_date               ,
                "print_time"                    : self.print_time               ,
                "order_entry_date"              : self.order_entry_date         ,
                "order_entry_time"              : self.order_entry_time         ,
                "requested_ship_date"           : self.requested_ship_date      ,
                "order_notes"                   : self.order_notes              ,
               }



#
# Useful regexes


#(today_sure|signature_service|service_files|normal)(_can_ship_tomorrow|_should_ship_today)?
#((?:today_sure|signature_service|service_files|normal)(?:_can_ship_tomorrow|_should_ship_today|_backorder)?)
# \1\2\3_ready_to_print\4\n\1\2\3_pick_slip_printed\4\n\1\2\3_packed\4\n

#(.+)(today_sure|signature_service|service_files|normal(?:_can_ship_tomorrow|_should_ship_today)?)(.+)\2(.+)
#\1\2_ready_to_print\3\2_ready_to_print\4\n\1\2_pick_slip_printed\3\2_pick_slip_printed\4\n\1\2_packed\3\2_packed\4\n


#(.+)((?:today_sure|signature_service|service_files|normal)_backorder)(.+)
# \1\2_ready_to_print\3\n\1\2_pick_slip_printed\3\n\1\2_packed\3\n

#(.+)((?:today_sure|signature_service|service_files|normal)_backorder)(.+)\2(.+)
#\1\2_ready_to_print\3\2_ready_to_print\4\n\1\2_pick_slip_printed\3\2_pick_slip_printed\4\n\1\2_packed\3\2_packed\4\n


#(.+)((?:today_sure|signature_service|service_files|normal)(?:_can_ship_tomorrow|_should_ship_today|_backorder))(.+)\n
# \1\2_ready_to_print\3\n\1\2_pick_slip_printed\3\n\1\2_packed\3\n
# \1\2_ready_to_print\3['ready_to_print']\n\1\2_pick_slip_printed\3['pick_slip_printed']\n\1\2_packed\3['packed']\n

# _(ready_to_print|pick_slip_printed|packed)_(can_ship_tomorrow|should_ship_today)
