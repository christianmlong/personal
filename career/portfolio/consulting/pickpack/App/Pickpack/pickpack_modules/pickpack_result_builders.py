"""
pickpack_result_builders.py

One central place for classes that build data structures that we return to the
client.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import os

from nevow import flat, tags, entities

from CML_Common.utility import utl_functions

from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_errors

# Note: it may seem that these classes aren't doing enough to justify their
# existence. However, I added these *Builder classes to impose some structure
# and consistency on the data I was returning. For example, this ensures that
# the return value data formats are the same whether we are returning database
# data or mock data.


class PackingListBuilder(object):
    """
    Used when responding to packing list requests. Builds the data structure
    that we will return.
    """
    def __init__(self):
        self.order_number = None
        self.order_generation = None
        self.packing_list_for_client = None
        self.item_notes = None
        self.order_notes = None
        self.server_error = None

    def render(self):
        """
        Builds the data structure in the right format.
        """
        if self.server_error is None:
            return {"order_number" : self.order_number,
                    "order_generation" : self.order_generation,
                    "packing_list_array" : self.packing_list_for_client,
                    "item_notes" : self.item_notes,
                    "order_notes" : self.order_notes,
                   }
        else:
            return {"order_number" : self.order_number,
                    "order_generation" : self.order_generation,
                    "server_error" : self.server_error,
                   }


class ClippershipWarningsBuilderInternal(object):
    """
    Used when responding to requests for order warnings for Clippership. This
    data structure is used as the internal representation of the data we return
    to Clippership. This structure is used to move the data internally. At the
    end of the process the data is used to populate a data structure (built by
    ClippershipWarningsBuilderExternal) that we return to the client.

    Here are some examples:

    {'order_notes' : 'NO_DATA_FOUND',
     'order_number' : 'AA10300',
     'order_generation' : 0,
     'warning_categories' : frozenset(['HZ0', 'TH1', 'TH2'])
    }

    {'order_notes' : ({'components' : [{'content' : ('Helmet lenses get two Metal labels',
                                                     'metal2',
                                                    ),
                                        'type' : 'text_and_image',
                                       },
                                      ],
                       'popup_time' : 'beginning_and_end',
                      },
                      [1],
                     ),
     'order_number' : 'AA10400',
     'order_generation' : 0,
     'warning_categories' : frozenset(['HZ0', 'TH1', 'TH2'])
    }
    """
    def __init__(self):
        self.order_number = None
        self.order_generation = None
        self.order_notes = None
        self.warning_categories = None

    def render(self):
        """
        Builds the data structure in the right format.
        """
        return {"order_number" : self.order_number,
                "order_generation" : self.order_generation,
                "order_notes" : self.order_notes,
                "warning_categories" : self.warning_categories,
               }


class WarningsFormatter(object):
    """
    Base class for classes that format warning data
    """
    def _build_stan_for_one_component(self,
                                      image_name_suffix,
                                      component,
                                     ):
        if component['type'] == 'text':
            note_text = component['content']
            return tags.tr[                                                            # pylint: disable=no-member
                self._buildImageCell(),
                self._buildTextCell(note_text),
            ]
        elif component['type'] == 'image':
            return tags.tr[                                                            # pylint: disable=no-member
                self._buildImageCell(component['content'],
                                     image_name_suffix,
                                    ),
                self._buildTextCell(),
            ]
        elif component['type'] == 'text_and_image':
            note_text = component['content'][0]
            return tags.tr[                                                            # pylint: disable=no-member
                self._buildImageCell(component['content'][1],
                                     image_name_suffix,
                                    ),
                self._buildTextCell(note_text),
            ]
        else:
            raise pickpack_errors.ApplicationError("Error: Unknown comment format: %s" % component['type'])

    def _buildImageCell(self,
                        image_names = None,
                        image_name_suffix = None,
                       ):
        def _buildSPAN(image_name):
            # This function picks image_name_suffix up from its contining scope
            image_file_path = self._buildImagePath(image_name, image_name_suffix)
            return (        # Parentheses for line-continuation
                tags.span[                                                             # pylint: disable=no-member
                    tags.img(src = image_file_path)                                    # pylint: disable=no-member
                ]
            )
        return self._buildCell(image_names,
                               _buildSPAN,
                               "pkpk_order_note_image",
                              )

    def _buildTextCell(self,
                       note_text = None,
                      ):
        def _buildSPAN(line_text):
            return (        # Parentheses for line-continuation
                tags.span[                                                             # pylint: disable=no-member
                    line_text,
                    tags.br,                                                           # pylint: disable=no-member
                ]
            )
        return self._buildCell(note_text,
                               _buildSPAN,
                               "pkpk_order_note_text",
                              )

    @staticmethod
    def _buildCell(contents,
                   build_function,
                   html_class,
                  ):
        if contents is None:
            # Build a blank cell
            cell_contents = entities.nbsp                                              # pylint: disable=no-member
        else:
            # contents might be a string, or it might be an array of strings.
            # Here we wrap it, using wrapScalarValue, so we can handle it in a
            # consistent way.
            cell_contents = (build_function(item) for item in utl_functions.wrapScalarValue(contents))

        return (        # Parentheses for line-continuation
            tags.td(class_ = html_class)[                                              # pylint: disable=no-member
                cell_contents,
            ]
        )

    @staticmethod
    def _buildImagePath(image_name, image_name_suffix):
        filename = "%s%s%s" % (image_name,
                               image_name_suffix,
                               pickpack_constants.IMG_EXT,
                              )
        return os.path.join(pickpack_constants.IMG_URL_PATH,
                            filename,
                           )

    def build_stan(self,
                   order_notes,
                  ):
        """
        Build the document structure, using Nevow's STAN.
        """
        if order_notes == pickpack_constants.NO_DATA_FOUND:
            stan_dom = (
                tags.div[                                                              # pylint: disable=no-member
                    tags.p["No warning labels needed."]                                # pylint: disable=no-member
                ]
            )
        else:
            components = order_notes['components']
            number_of_components = len(components)

            if number_of_components == 1 or number_of_components == 2:
                image_name_suffix = '_large'
            elif number_of_components == 3:
                image_name_suffix = '_medium'
            elif number_of_components >= 4 and number_of_components <= 9:
                image_name_suffix = '_small'
            else:
                raise pickpack_errors.ApplicationError("Error: Invalid number of components: %s" % number_of_components)

            stan_dom = (
                tags.div[                                                              # pylint: disable=no-member
                    tags.table[                                                        # pylint: disable=no-member
                        tags.tbody[                                                    # pylint: disable=no-member
                            (self._build_stan_for_one_component(image_name_suffix,
                                                                component,
                                                               )
                             for component in components
                            )
                        ]
                    ]
                ]
            )
        return stan_dom

    def build_html(self,
                   order_notes,
                  ):
        """
        Build the HTML that we will display to the user.
        """
        return flat.flatten(self.build_stan(order_notes))


class ClippershipWarningsBuilderExternal(WarningsFormatter):
    """
    Used to build the data structure that we return to Clippership.
    """
    def __init__(self,
                 clippership_warning_data_internal,
                ):
        WarningsFormatter.__init__(self)
        self.order_notes = clippership_warning_data_internal['order_notes']
        self.warning_categories = clippership_warning_data_internal['warning_categories']

    def render(self):
        """
        Build the data structure that we return to Clippership.
        """
        if self.order_notes == pickpack_constants.NO_DATA_FOUND:
            warnings_needed = 0
            warning_categories = []
        else:
            warnings_needed = 1
            if self.warning_categories is None:
                # There are cases where we warn the user, but there is no item
                # warning category. For example, a Gas Rebate form might be
                # needed, but there are no warned items on the order. So, in
                # that case, there are order notes, but no warning categories.
                warning_categories = []
            else:
                # We must convert the frozenset to a list, so it can be
                # jsonified.
                warning_categories = list(self.warning_categories)

        return {'warnings_needed' : warnings_needed,
                'warnings_html' : self.build_html(self.order_notes),
                'warning_categories' : warning_categories,
               }


class OrderNotesBuilder(object):
    """
    Used to build an order notes structure.
    """
    def __init__(self):
        self.popup_time = None
        self.components = None

    def render(self):
        """
        Builds the data structure in the right format.
        """
        return {"popup_time" : self.popup_time,
                "components" : self.components,
               }


class IsValidSerialNumberBuilder(object):
    """
    Structure for serial number validation data.
    """
    def __init__(self):
        self.is_valid = None
        self.err_msg = None

    def render(self):
        """
        Builds the data structure in the right format.
        """
        return {"is_valid" : self.is_valid,
                "err_msg" : self.err_msg,
               }











#
