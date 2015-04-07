"""
utl_aplus.py

Utility clases and functions for the APlus database


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from CML_Common.error import error

class OrderIdParseError(error.InputError):
    """
    An error occurred when parsing the order id barcode scan value.
    """

class OrderIdentifier(object):
    """
    The canonical representation of an order identifier, and several
    pre-formatted representations.
    """

    def __init__(self):
        self.number = None
        self.generation = None
        self.padded_generation = None
        self.concatenated_for_database = None
        self.formatted_for_display = None

    def populate_from_barcode_scan(self,
                                   order_id_scan,
                                  ):
        """
        Populate the object based on a scanned barcode of the form '6P60800'.
        """
        if len(order_id_scan) != 7:
            raise OrderIdParseError("%s is not a valid order number scan. Order scans must be seven "
                                    "characters: order number and generation. For example 6P61800" % order_id_scan
                                   )

        self.populate_from_order_number_and_generation(order_id_scan[0:5],
                                                       order_id_scan[5:7],
                                                      )

        # Sanity check
        if order_id_scan != self.concatenated_for_database:
            raise OrderIdParseError(
                "Parse error: (%s) and (%s) do not match" % (order_id_scan,
                                                             self.concatenated_for_database,
                                                            )
            )

    def populate_from_order_representation_formatted_for_display(self,
                                                                 display_representation,
                                                                ):
        """
        Populate the object based on an order representation of the form '6P608/00'.
        """
        if len(display_representation) != 8:
            raise OrderIdParseError("%s is not a valid order representation of the form '6P608/00'." % display_representation)

        if display_representation[5] != '/':
            raise OrderIdParseError("%s is not a valid order representation of the form '6P608/00'." % display_representation)

        self.populate_from_order_number_and_generation(display_representation[0:5],
                                                       display_representation[6:8],
                                                      )

        # Sanity check
        if display_representation != self.formatted_for_display:
            raise OrderIdParseError(
                "Parse error: (%s) and (%s) do not match" % (display_representation,
                                                             self.formatted_for_display,
                                                            )
            )

    def populate_from_order_number_and_generation(self,
                                                  order_number,
                                                  order_generation,
                                                 ):
        """
        Populate the object based on order number and generation.
        """
        if order_number is None:
            raise OrderIdParseError("%s is not a valid order number." % order_number)
        if len(order_number) != 5:
            raise OrderIdParseError("%s is not a valid order number." % order_number)

        self.number = order_number

        # The canonical representation of order generation is an integer
        try:
            self.generation = int(order_generation)
        except ValueError:
            raise OrderIdParseError("%s is not a valid order generation" % order_generation)

        # Calculate derived fields

        # We also store a version of order generation that is zero-left-padded
        # to two characters.
        self.padded_generation = '{:0>2}'.format(self.generation)

        self.concatenated_for_database = "%s%s" % (self.number,
                                                   self.padded_generation,
                                                  )

        self.formatted_for_display = "%s/%s" % (self.number,
                                                self.padded_generation,
                                               )


# Factory functions
def order_id_from_barcode_scan(order_id_scan):
    """
    Takes an order id as it is encoded on a pick list barcode. E.g 6P60400.
    That's a five-character order number, and the order generation zero-left
    padded to two characters.

    Returns an instance of OrderIdentifier, which will serve as the canonical
    representation of the order. OrderIdentifier also provides some common
    pre-formatted representations of the order. E.g 6P604/00.
    """
    order_id = OrderIdentifier()
    order_id.populate_from_barcode_scan(order_id_scan)
    return order_id

def order_id_from_display_representation(display_representation):
    """
    Takes an order id as it is displayed on APlus screens. E.g 6P604/00. That's
    a five-character order number, then a forward slash, then the order
    generation zero-left padded to two characters.

    Returns an instance of OrderIdentifier, which will serve as the canonical
    representation of the order. OrderIdentifier also provides some common
    pre-formatted representations of the order. E.g 6P604/00.
    """
    order_id = OrderIdentifier()
    order_id.populate_from_order_representation_formatted_for_display(display_representation)
    return order_id

def order_id_from_order_number_and_generation(order_number,
                                              order_generation,
                                             ):
    """
    Takes a five-character order number, and the order generation as a string.

    Returns an instance of OrderIdentifier, which will serve as the canonical
    representation of the order. OrderIdentifier also provides some common
    pre-formatted representations of the order. E.g 6P604/00.
    """
    order_id = OrderIdentifier()
    order_id.populate_from_order_number_and_generation(order_number,
                                                       order_generation,
                                                      )
    return order_id
