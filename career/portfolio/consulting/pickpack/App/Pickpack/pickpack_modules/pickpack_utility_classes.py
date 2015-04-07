"""
pickpack_utility_classes.py

Utility classes


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import itertools

class PackingListItem(object):
    """
    A carrier for the data for one line item on a packing list.
    """
    def __init__(self, item_data):
        (self.line_no,
         self.barcode,
         self.item_no,
         self.status,
         quantity,
         self.sales_um,
         sales_um_conv,
         self.serialized,
         self.has_item_note,
         self.category,
         self.pick_status,
         self.is_helmet,
        ) = item_data

        # Convert to integer, since item quantities are floats in the database.
        self.quantity = int(quantity)
        self.sales_um_conv = int(sales_um_conv)

        # This gets added later
        self.inline_image = None


class PackingListContainer(object):
    """
    A container object that holds the data for a packing list.
    """
    def __init__(self, raw_data):
        self.items = [PackingListItem(row) for row in raw_data]
        self.items_not_picked = None
        self._calculate_items_not_picked()

    def get_column(self, column_name):
        """
        Returns a list of the values of this attribute for all objects in
        self.items. i.e. it returns a single "column" of data.
        """
        return [getattr(item, column_name) for item in self.items]

    def set_column(self, column_name, list_of_values):
        """
        For each item in self.items, sets that item's attribute to the
        corresponding value in list_of_values. i.e. it sets a single "column" of
        data.
        """
        for (item, value) in itertools.izip(self.items, list_of_values):
            setattr(item, column_name, value)

    def add_inline_images(self, inline_images):
        """
        In the process of calculating warnings for orders, we also calculate
        inline images that go with each row of data. This function adds those
        inline images to each row.
        """
        self.set_column('inline_image', inline_images)

    def client_data(self):
        """
        This returns just the data that we want to send to the client.
        """
        return [(item.line_no,
                 item.barcode,
                 item.item_no,
                 item.status,
                 item.quantity,
                 item.sales_um,
                 item.serialized,
                 item.has_item_note,
                 item.inline_image,
                )
                for item
                in self.items
               ]

    def __len__(self):
        """
        This returns the length of the underlying data set (number of rows of
        data).
        """
        return len(self.items)

    def __iter__(self):
        """
        This is generator function (because it contains 'yield') that iterates
        over the underlying data set.
        """
        for item in self.items:
            yield item

        ## Or, using a genexp
        #return (item for item in self.items)

    def _calculate_items_not_picked(self):
        """
        Any item where the pick status is blank has not been picked.
        """
        self.items_not_picked = [item.item_no
                                 for item
                                 in self.items
                                 if (item.pick_status == ''           # Not picked yet
                                     or item.pick_status == '1'       # Picking in progress (released to a gun)
                                    )
                                ]




# OLD code
#
#def addDataToPackingList(packing_list,
#                         data_to_add,
#                        ):
#    """
#    The packing_list argument is a list of lists. The data_to_add argument is a
#    list of lists or a list of scalar values (int, str, etc.). This function
#    removes the last "column" of data from packing_list, and appends the
#    data_to_add as a new column or columns. It returns a modified copy of the
#    packing list. it dows not modify the packing list in place.
#    """
#    if len(packing_list) != len(data_to_add):
#        raise pickpack_errors.ApplicationError("Error: the two lists are not the same length.")
#
#    modified_packing_list = []
#
#    for (row, add_this) in itertools.izip(packing_list,
#                                          data_to_add,
#                                         ):
#        new_row = list(row)
#        new_row.pop()
#        new_row.extend(utl_functions.wrapScalarValue(add_this))
#        modified_packing_list.append(new_row)
#
#    return modified_packing_list
#
