"""
main.py

This module implements the logic needed to warn PickPack users about the
packaging and labelling requirements they need to follow. For example: battery
warning labels.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""
import collections

from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules import pickpack_lowlevel_common
from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules.warn import pkpk_warnings
from Pickpack.pickpack_modules.warn.utility_classes import CommonConstants
from Pickpack.pickpack_modules.warn.rulesets import get_item_rulesets
#from Pickpack.pickpack_modules.warn.rulesets import e_commerce_ruleset
from Pickpack.pickpack_modules.warn.inline_image import get_inline_image_calcualtor



class ShipmentWarningCalculator(CommonConstants):
    """
    Contains the math needed to calculate what kind of warning labels are needed
    on a shipment. Also calculates what weight and quantity restrictions
    apply, and returns some text explaining the restrictions.
    """

    def __init__(self):
        # Call base class' constructor
        CommonConstants.__init__(self)

    def calculate_item_warnings(self,
                                packing_list,
                                carrier_code,
                                ctx,
                               ):
        """
        Run the calculations for item-based warnings, and return a
        representation of the image and the warning text (if any) to be
        displayed to the user. Returns None if no notes are needed.

        ctx is a context object that can carry additional data from the web
        request. If no additional context is needed, ctx can be passed as None.

        Returns a list containing zero to many warnings to show to the user.
        The warnings are represented as instances of subclasses of class
        ShipmentWarning.
        """
        # Run through the list of items in the order, and store the quantities
        # of each type of item that needs a warning.
        #
        # The item type is a three-character code. The first two characters are
        # alpha, and indicate which category of warnable items this item belongs
        # to (PA = TRPR, HE = Helmet, BT = coin battery, etc.). The third
        # character is a digit, and indicates the sub-category. This allows us
        # to distinguish (for example) between two different types of coin
        # batteries, that follow similar rules, but not exactly the same (e.g.
        # one battery is heavier than another, and so the quantity per box is
        # lower, due to the weight restrictions).
        #
        # In addition to the category counter, we also accumulate a list that
        # tells which warning category each item belongs to. We will return this
        # list, which will be given to the client. The client uses this info to
        # display a battery warning image, as appropraite, next to each item in
        # the packing list.

        counter = collections.Counter()
        inline_warnings = []
        inline_image_calcualtor = get_inline_image_calcualtor(ctx)
        for item in packing_list:
            # Determine which shipment warning image we should use for this
            # item.
            inline_warnings.append(inline_image_calcualtor.calculate(item.category))

            if item.category is not None:
                # The item has a warning category. Add the quantity shipped to
                # that category's counter field.
                counter[item.category] += item.quantity

                # Note: for now, for multi-pack items, we count only the number
                # of packs when totalling up the quantities. If we want to count
                # the number of individual items in multi-packs, use the line
                # below.
                #counter[item.category] += (item.quantity * item.sales_um_conv)


        if len(counter) == 0:
            # Quit right now if there are no interesting items on the order.
            return None

        #if carrier_code in pickpack_constants.OTHER_SHIPPERS_DO_NOTHING:
        #    # Quit right now if this shipping method does not require labels.
        #    return None

        inline_image_calcualtor.assert_allowed_categories(counter)

        if pickpack_lowlevel_common.isAirCarrierCode(carrier_code):
            shipping_method = self.Constants.Shipping.Air                                                                   # pylint: disable=no-member
        elif pickpack_lowlevel_common.isGroundCarrierCode(carrier_code):
            shipping_method = self.Constants.Shipping.Ground                                                                # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Unknown carrier code %s." % carrier_code)

        # There are a number of independent warning systems. Each can throw a
        # warning. If, for example, five of the warning systems throw a warning,
        # then we show five different warnings to the user.
        #
        # Here we iterate over the item warning rulesets. For each item ruleset,
        # we pass in the counter object, which tells the ruleset how many items
        # of each warning category there are in this order.
        warnings = []
        for ruleset in get_item_rulesets(ctx):
            warning = ruleset.apply_rules(counter,
                                          shipping_method,
                                         )
            if warning is None:
                raise pickpack_errors.ApplicationError("Error: Warning is None")

            if isinstance(warning, pkpk_warnings.NoWarning):
                continue

            warnings.append(warning)

            # POSSIBLE IMPROVEMENT
            #
            # I might introduce a way for shipments to be cancelled at the scale
            # or stopped at the packing bench.
            #
            # In that case, each ruleset might also say that the shipment is not
            # allowed. Aggregate that data here. If any ruleset says the
            # shipment is not allowed, then set an attribute of the order
            # (order_alert_level) that tells the client that the shipment is not
            # allowed, and that gives an error message.
            #
            # See also pickpack_format.py, line 160

        return (warnings,
                inline_warnings,
                # A set of the warning categories that apply to this order. e.g.
                # frozenset(['HZ0', 'TH1', 'TH2'])
                frozenset(counter),
               )

# A single module-level object does all our calculations. The object is
# expensive to set up, but each operation it performs is relatively cheap.
warner = ShipmentWarningCalculator()

# This is the function that the client code calls.
def calculateShipmentWarnings(packing_list,
                              carrier_code,
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
    Given a list of items and a shipping method, this function calculates if any
    shipment warning messages are needed. If any are needed, it returns them in
    a dictionary, which contains warning text and the names of the warning
    images to show to the user. ctx is a context object that can carry
    additional data from the web request. If no additional context is needed,
    ctx can be passed as None.
    """
    all_warnings = []

    # warner is a module-level object. It is an instance of
    # ShipmentWarningCalculator
    result = warner.calculate_item_warnings(packing_list,
                                            carrier_code,
                                            ctx,
                                           )
    if result is None:
        inline_warnings = None
        warning_categories = None
    else:
        (item_warnings,                                                         # pylint: disable=unpacking-non-sequence
         inline_warnings,
         warning_categories,
        ) = result
        all_warnings.extend(item_warnings)


    # In addition to the item-based rulesets, we also have some special rulesets
    # that calculate warnings based on other criteria.
    #special_warning_1 = e_commerce_ruleset.apply_rules(customer_number,
    #                                                   order_entry_initials,
    #                                                  )
    #if special_warning_1 is None:
    #    raise pickpack_errors.ApplicationError("Error: Warning is None")
    #
    #if not isinstance(special_warning_1, pkpk_warnings.NoWarning):
    #    all_warnings.append(special_warning_1)


    # If there are three or more helmets, tell the user that the helmets must
    # go ground. Warn only if the order is allowed to be downgraded.
    number_of_helmets = 0
    for item in packing_list:
        if item.is_helmet == 1:
            # This item is a helmet, or a helmet multi-pack. Add the quantity
            # shipped to our accumulator. For multi-pack helmets, add the number
            # of helmets in the pack.
            #
            # Note that this is different from the way we count items for the
            # counter that we pass to the rulesets. There, a four-pack only
            # counts as one item. Here, a four-pack of helmets counts as four
            # helmets.
            number_of_helmets += (item.quantity * item.sales_um_conv)

    if (number_of_helmets >= 3
        and pickpack_lowlevel_common.isDowngradeToGroundAllowed(carrier_code,
                                                                service_level,
                                                                ship_to_state,
                                                                ship_to_country,
                                                               )
       ):
        all_warnings.append(pkpk_warnings.GroundHelmetWarning(number_of_helmets))


    # If the calculated order weight is more than 35 lbs, tell the user that it
    # must go ground. Warn only if the order is allowed to be downgraded.
    if not isinstance(calcualted_order_weight, int):
        raise pickpack_errors.ApplicationError("Error: Order weight is not an integer (%s %s)" %
                                               (calcualted_order_weight,
                                                type(calcualted_order_weight),
                                               )
                                              )
    if (calcualted_order_weight >= 35
        and pickpack_lowlevel_common.isDowngradeToGroundAllowed(carrier_code,
                                                                service_level,
                                                                ship_to_state,
                                                                ship_to_country,
                                                               )
       ):
        all_warnings.append(pkpk_warnings.HeavyOrderWarning(calcualted_order_weight))


    # International orders get a warning that tells the user to check the
    # destination
    if needsInternationalWarning(ship_to_country,
                                 customer_number,
                                 customer_sold_to_country,
                                ):
        all_warnings.append(pkpk_warnings.InternationalWarning())


    # Harper orders get a warning that tells the user to pack at the Harper
    # bench.
    if needsHarperWarning(customer_number):
        all_warnings.append(pkpk_warnings.HarperWarning())


    return (all_warnings,
            inline_warnings,
            warning_categories,
           )

def needsInternationalWarning(ship_to_country,
                              customer_number,
                              ignore_customer_sold_to_country,
                             ):
    """
    International orders get a warning that tells the user to check the
    destination.
    """
    needs_warning = False
    if pickpack_lowlevel_common.isUnitedStates(ship_to_country):
        # Some orders that are shipped to the USA will later be forwarded to
        # international destinations. Those orders need this warning.
        if customer_number == pickpack_constants.WCW_MEXICO_CUSTOMER_NUMBER:
            needs_warning = True
    elif pickpack_lowlevel_common.isCanada(ship_to_country):
        # No warning for Canada
        needs_warning = False
    else:
        # All non-Canada international destinations need the warning.
        needs_warning = True

    return needs_warning

def needsHarperWarning(customer_number):
    """
    Harper orders get a warning that tells the user to pack at the Harper
    bench.
    """
    return customer_number == pickpack_constants.HARPER_CUSTOMER_NUMBER
