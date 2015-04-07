"""
    inline_image.py

    used to decide which inline warning image to display
"""

from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules.warn.utility_classes import CommonConstants

class InlineImageCalculator(CommonConstants):
    """
    Contains the categories into which we group items, for the purposes of
    showing the inline image
    """
    def __init__(self):
        # Call base class' constructor
        CommonConstants.__init__(self)

        self.no_warning_categories = frozenset()
        # We are not giving any warnings about helmets or helmet lenses.
        self.metal_categories = frozenset((self.Constants.Codes.MetalCoinBattery,                                               # pylint: disable=no-member
                                          )
                                         )
        self.metal_ion_categories = frozenset((self.Constants.Codes.MetalAndIonPackageKit,                                      # pylint: disable=no-member
                                               self.Constants.Codes.CompleteTRPR,                                               # pylint: disable=no-member
                                              )
                                             )
        self.ion_categories = frozenset((self.Constants.Codes.SmartBand,                                                         # pylint: disable=no-member
                                         self.Constants.Codes.SmartBelt,                                                         # pylint: disable=no-member
                                         self.Constants.Codes.TRPRBattery,                                                      # pylint: disable=no-member
                                         self.Constants.Codes.SmartBandBattery,                                                  # pylint: disable=no-member
                                         self.Constants.Codes.SmartBeltBattery,                                                  # pylint: disable=no-member
                                         self.Constants.Codes.TRPRWithoutLens,                                                  # pylint: disable=no-member
                                        )
                                       )
        self.thoriated_categories = frozenset((self.Constants.Codes.ThoriatedTungsten,                                          # pylint: disable=no-member
                                               self.Constants.Codes.ThoriatedTungstenKit,                                       # pylint: disable=no-member
                                               self.Constants.Codes.ThoriatedTungstenRodsLight,                                 # pylint: disable=no-member
                                               self.Constants.Codes.ThoriatedTungstenRodsHeavy,                                 # pylint: disable=no-member
                                               self.Constants.Codes.ThoriatedTungstenAccessoryKit,                              # pylint: disable=no-member
                                              )
                                             )
        self.orm_d_categories = frozenset((self.Constants.Codes.ORM_D,                                                    # pylint: disable=no-member
                                          )
                                         )

        # Build a set of all allowed categories, by unioning all the subcategories.
        self.allowed_categories = frozenset(
            self.no_warning_categories.union(self.metal_categories,
                                             self.metal_ion_categories,
                                             self.ion_categories,
                                             self.thoriated_categories,
                                             self.orm_d_categories,
                                            )
        )

    def assert_allowed_categories(self,
                                  counter,
                                 ):
        """
        Raise an error if counter has any unknown categories.
        """
        seen_categories = frozenset(counter)
        if not seen_categories.issubset(self.allowed_categories):
            raise pickpack_errors.ApplicationError("Error: Unknown category or categories %s." % seen_categories.difference(self.allowed_categories))

    def calculate(self,
                  item_category,
                 ):
        """
        Determine which shipment warning image we should use for this item.
        """
        if item_category is None:
            return self.Constants.InlineWarningImage.Blank                                                                              # pylint: disable=no-member
        elif item_category in self.no_warning_categories:
            return self.Constants.InlineWarningImage.Blank                                                                              # pylint: disable=no-member
        elif item_category in self.metal_categories:
            return self.Constants.InlineWarningImage.Metal                                                                              # pylint: disable=no-member
        elif item_category in self.metal_ion_categories:
            # These kit items contain a helmet complete with lens, and also an
            # item that has an ion battery (e.g. TRPR, SmartBand). However, we
            # are not putting labels on helmets or helmet lenses. So, these
            # items get just an ion label.
            return self.Constants.InlineWarningImage.Ion                                                                                # pylint: disable=no-member
        elif item_category in self.ion_categories:
            return self.Constants.InlineWarningImage.Ion                                                                                # pylint: disable=no-member
        elif item_category in self.thoriated_categories:
            return self.Constants.InlineWarningImage.Thorium                                                                            # pylint: disable=no-member
        elif item_category in self.orm_d_categories:
            return self.Constants.InlineWarningImage.ORM_D                                                                              # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Unknown category %s." % item_category)


# Instantiate only once, and store in this module-level variable.
normal_inline_image_calcualtor = InlineImageCalculator()

def get_inline_image_calcualtor(ctx):
    """
    This supplies the appropriate inline image calculator depending on what the
    context object says.
    """
    if ctx is None:
        return normal_inline_image_calcualtor
    elif ctx.flavor == ctx.Constants.Flavor.Normal:                             # pylint: disable=no-member
        return normal_inline_image_calcualtor
    else:
        raise pickpack_errors.ApplicationError("Error: Invalid context object flavor value %s." % ctx.flavor)
