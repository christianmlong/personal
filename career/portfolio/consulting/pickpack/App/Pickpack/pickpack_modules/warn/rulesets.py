"""
rulesets.py

This module implements the logic needed to warn PickPack users about the battery
packaging and labelling requirements they need to follow. The logic is
implemented in classes I call rulesets.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

#import datetime

from Common.utility import utl_decorators

from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules.warn import pkpk_warnings
from Pickpack.pickpack_modules.warn.utility_classes import (MultiDict,
                                                                   ItemRuleset,
                                                                   #SpecialRuleset,
                                                                  )


@utl_decorators.add_constants_to_class({'MetalCoinBattery'   : ('Zero',
                                                                'OneOrMore',
                                                               ),
                                       },
                                       magic_number = 110000,
                                      )
class MetalRuleset(ItemRuleset):
    """
    Represents rules for lithium metal battery warnings
    """
    def __init__(self):
        # Call base class' constructor
        ItemRuleset.__init__(self)

        # "Constants" was added by the "add_constants_to_class" decorator.
        c = self.Constants                                                                                                        # pylint: disable=no-member
        self.ruleset = {
            (c.Shipping.Ground,     c.MetalCoinBattery.Zero)        : pkpk_warnings.NoWarning,
            (c.Shipping.Ground,     c.MetalCoinBattery.OneOrMore)   : pkpk_warnings.GroundCoinBatteryWarning,
            (c.Shipping.Air,        c.MetalCoinBattery.Zero)        : pkpk_warnings.NoWarning,
            (c.Shipping.Air,        c.MetalCoinBattery.OneOrMore)   : pkpk_warnings.AirCoinBatteryWarning,
        }

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        # We calculate metal warnings based on two factors:
        #    shipping method : air or ground
        #    Coin battery qty: 0 or 1+

        coin_battery_qty = counter[self.Constants.Codes.MetalCoinBattery]                                                        # pylint: disable=no-member
        if coin_battery_qty == 0:
            coin_battery_factor = self.Constants.MetalCoinBattery.Zero                                                           # pylint: disable=no-member
        elif coin_battery_qty > 0:
            coin_battery_factor = self.Constants.MetalCoinBattery.OneOrMore                                                      # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid coin battery quantity %s." % coin_battery_qty)

        decisive_factors = (shipping_method,
                            coin_battery_factor,
                           )
        return decisive_factors


@utl_decorators.add_constants_to_class({'MetalAndIonPackageKit'   : ('Zero',
                                                                     'OneOrMore',
                                                                    ),
                                       },
                                       magic_number = 120000,
                                      )
class MetalAndIonOtherRuleset(ItemRuleset):
    """
    Represents rules for battery warnings for kits which contain both metal and
    ion batteries. We do not need to warn about the metal batteries, just the
    ion. So, such kits get just ion labels.
    """
    def __init__(self):
        # Call base class' constructor
        ItemRuleset.__init__(self)

        # "Constants" was added by the "add_constants_to_class" decorator.
        c = self.Constants                                                                                                      # pylint: disable=no-member
        self.ruleset = {
            (c.Shipping.Ground,     c.MetalAndIonPackageKit.Zero)       : pkpk_warnings.NoWarning,
            (c.Shipping.Ground,     c.MetalAndIonPackageKit.OneOrMore)  : pkpk_warnings.GroundHelmetAndSmartBandBeltKitWarning,
            (c.Shipping.Air,        c.MetalAndIonPackageKit.Zero)       : pkpk_warnings.NoWarning,
            (c.Shipping.Air,        c.MetalAndIonPackageKit.OneOrMore)  : pkpk_warnings.AirHelmetAndSmartBandBeltKitWarning,
        }

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        # We calculate warnings for MetalAndIonOtherRuleset based on two factors:
        #    shipping method : air or ground
        #    Metal and Ion kit qty: 0 or 1+
        metal_ion_other_qty = counter[self.Constants.Codes.MetalAndIonPackageKit]                                                    # pylint: disable=no-member
        if metal_ion_other_qty == 0:
            metal_ion_other_factor = self.Constants.MetalAndIonPackageKit.Zero                                                       # pylint: disable=no-member
        elif metal_ion_other_qty > 0:
            metal_ion_other_factor = self.Constants.MetalAndIonPackageKit.OneOrMore                                                  # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid MetalAndIonPackageKit quantity %s." % metal_ion_other_qty)

        decisive_factors = (shipping_method,
                            metal_ion_other_factor,
                           )
        return decisive_factors


@utl_decorators.add_constants_to_class({'TRPR'   : ('Zero',
                                                    'OneOrMore',
                                                   ),
                                       },
                                       magic_number = 130000,
                                      )
class GeneralTrprRuleset(ItemRuleset):
    """
    Represents rules for lithium ion battery warnings for all TRPRs. Complete
    TRPR kits contain both lithium ion and lithium metal batteries. Ion-only
    TRPR kits contain only ion batteries. However, we do not need to warn about
    the metal batteries, just the ion. So we treat "complete" and "ion-only" the
    same.

    TRPRs come in large boxes that ship individually.
    """
    def __init__(self):
        # Call base class' constructor
        ItemRuleset.__init__(self)

        # "Constants" was added by the "add_constants_to_class" decorator.
        c = self.Constants                                                                                                  # pylint: disable=no-member
        self.ruleset = {
            (c.Shipping.Ground,     c.TRPR.Zero)        : pkpk_warnings.NoWarning,
            (c.Shipping.Ground,     c.TRPR.OneOrMore)   : pkpk_warnings.GroundTrprWarning,
            (c.Shipping.Air,        c.TRPR.Zero)        : pkpk_warnings.NoWarning,
            (c.Shipping.Air,        c.TRPR.OneOrMore)   : pkpk_warnings.AirTrprWarning,
        }

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        # We calculate warnings for IonTrprRuleset based on two factors:
        #    shipping method : air or ground
        #    The quantity of "ion-only trprs" PLUS "ion-and-metal trprs"
        ion_trpr_qty = counter[self.Constants.Codes.TRPRWithoutLens]                                                        # pylint: disable=no-member
        if ion_trpr_qty < 0:
            raise pickpack_errors.ApplicationError("Error: Invalid TRPR quantity %s." % ion_trpr_qty)

        metal_ion_trpr_qty = counter[self.Constants.Codes.CompleteTRPR]                                                     # pylint: disable=no-member
        if metal_ion_trpr_qty < 0:
            raise pickpack_errors.ApplicationError("Error: Invalid TRPR quantity %s." % metal_ion_trpr_qty)

        general_trpr_qty = ion_trpr_qty + metal_ion_trpr_qty
        if general_trpr_qty == 0:
            general_trpr_factor = self.Constants.TRPR.Zero                                                                  # pylint: disable=no-member
        elif general_trpr_qty > 0:
            general_trpr_factor = self.Constants.TRPR.OneOrMore                                                             # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid TRPR quantity %s." % general_trpr_qty)

        decisive_factors = (shipping_method,
                            general_trpr_factor,
                           )
        return decisive_factors


@utl_decorators.add_constants_to_class({'SmartBand'    : ('Zero',
                                                         'One',
                                                         'Two',
                                                         'ThreeOrMore',
                                                        ),
                                        'SmartBelt'    : ('Zero',
                                                         'One',
                                                         'Two',
                                                         'ThreeOrMore',
                                                        ),
                                        'TRPRBattery'   : ('Zero',
                                                           'OneOrMore',
                                                          ),
                                        'SmartBandBattery'   : ('Zero',
                                                               'OneOrMore',
                                                              ),
                                        'SmartBeltBattery'   : ('Zero',
                                                               'OneOrMore',
                                                              ),
                                       },
                                       magic_number = 150000,
                                      )
class IonRuleset(ItemRuleset):
    """
    Represents rules for lithium ion battery warnings.
    """
    def __init__(self):
        # Call base class' constructor
        ItemRuleset.__init__(self)

        # "Constants" was added by the "add_constants_to_class" decorator.

        # Some shortcuts
        _S = self.Constants.Shipping                                                                                              # pylint: disable=no-member
        _B = self.Constants.SmartBand                                                                                              # pylint: disable=no-member
        _T = self.Constants.SmartBelt                                                                                              # pylint: disable=no-member
        _P = self.Constants.TRPRBattery                                                                                           # pylint: disable=no-member
        _Y = self.Constants.SmartBandBattery                                                                                       # pylint: disable=no-member
        _R = self.Constants.SmartBeltBattery                                                                                       # pylint: disable=no-member

        # We use frozenset to represent multiple possible values. Frozensets are
        # immutable, thus hashable. We need all the elements of the tuple to be
        # hashable, since it will be used as a dictionary key.
        _S.Any = frozenset((_S.Ground,
                            _S.Air,
                           )
                          )
        _B.Any = frozenset((_B.Zero,
                            _B.One,
                            _B.Two,
                            _B.ThreeOrMore,
                           )
                          )
        _B.OneOrTwo = frozenset((_B.One,
                                 _B.Two,
                                )
                               )
        _B.OneOrMore = frozenset((_B.One,
                                  _B.Two,
                                  _B.ThreeOrMore,
                                 )
                                )
        _B.TwoOrMore = frozenset((_B.Two,
                                  _B.ThreeOrMore,
                                 )
                                )
        _T.Any = frozenset((_T.Zero,
                            _T.One,
                            _T.Two,
                            _T.ThreeOrMore,
                           )
                          )
        _T.OneOrTwo = frozenset((_T.One,
                                 _T.Two,
                                )
                               )
        _T.OneOrMore = frozenset((_T.One,
                                  _T.Two,
                                  _T.ThreeOrMore,
                                 )
                                )
        _T.TwoOrMore = frozenset((_T.Two,
                                  _T.ThreeOrMore,
                                 )
                                )
        _P.Any = frozenset((_P.Zero,
                            _P.OneOrMore,
                           )
                          )
        _Y.Any = frozenset((_Y.Zero,
                            _Y.OneOrMore,
                           )
                          )
        _R.Any = frozenset((_R.Zero,
                            _R.OneOrMore,
                           )
                          )

        self.ruleset = MultiDict(
            ruleset = {
                #                                                                       SmartBand        SmartBelt
                # Shipping      SmartBand            SmartBelt            TRPR battery    battery         battery         BatteryWarning class
                (_S.Any,        _B.Zero,            _T.Zero,            _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.NoWarning,
                (_S.Ground,     _B.Any,             _T.Any,             _P.Zero,        _Y.Any,         _R.OneOrMore)   : pkpk_warnings.GroundSmartBeltBatteryWarning,
                (_S.Ground,     _B.Any,             _T.Any,             _P.Zero,        _Y.OneOrMore,   _R.Zero)        : pkpk_warnings.GroundSmartBandBatteryWarning,
                (_S.Ground,     _B.Any,             _T.Any,             _P.OneOrMore,   _Y.Any,         _R.Any)         : pkpk_warnings.GroundTrprBatteryWarning,
                (_S.Ground,     _B.Zero,            _T.OneOrTwo,        _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundFewSmartBandSmartBeltWarning,
                (_S.Ground,     _B.OneOrTwo,        _T.Zero,            _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundFewSmartBandSmartBeltWarning,
                (_S.Ground,     _B.One,             _T.One,             _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundFewSmartBandSmartBeltWarning,
                (_S.Ground,     _B.Zero,            _T.ThreeOrMore,     _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundManySmartBandSmartBeltWarning,
                (_S.Ground,     _B.One,             _T.TwoOrMore,       _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundManySmartBandSmartBeltWarning,
                (_S.Ground,     _B.TwoOrMore,       _T.OneOrMore,       _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundManySmartBandSmartBeltWarning,
                (_S.Ground,     _B.ThreeOrMore,     _T.Zero,            _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.GroundManySmartBandSmartBeltWarning,
                (_S.Air,        _B.Zero,            _T.Zero,            _P.Zero,        _Y.Any,         _R.OneOrMore)   : pkpk_warnings.AirIonBatteryWarning,
                (_S.Air,        _B.Zero,            _T.Zero,            _P.Zero,        _Y.OneOrMore,   _R.Zero)        : pkpk_warnings.AirIonBatteryWarning,
                (_S.Air,        _B.Zero,            _T.Zero,            _P.OneOrMore,   _Y.Any,         _R.Any)         : pkpk_warnings.AirIonBatteryWarning,
                (_S.Air,        _B.Zero,            _T.OneOrTwo,        _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirFewSmartBandSmartBeltWarning,
                (_S.Air,        _B.One,             _T.One,             _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirFewSmartBandSmartBeltWarning,
                (_S.Air,        _B.OneOrTwo,        _T.Zero,            _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirFewSmartBandSmartBeltWarning,
                (_S.Air,        _B.Zero,            _T.ThreeOrMore,     _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirManySmartBandSmartBeltWarning,
                (_S.Air,        _B.One,             _T.TwoOrMore,       _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirManySmartBandSmartBeltWarning,
                (_S.Air,        _B.TwoOrMore,       _T.OneOrMore,       _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirManySmartBandSmartBeltWarning,
                (_S.Air,        _B.ThreeOrMore,     _T.Zero,            _P.Zero,        _Y.Zero,        _R.Zero)        : pkpk_warnings.AirManySmartBandSmartBeltWarning,
                (_S.Air,        _B.OneOrMore,       _T.Any,             _P.Zero,        _Y.Any,         _R.OneOrMore)   : pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
                (_S.Air,        _B.OneOrMore,       _T.Any,             _P.Zero,        _Y.OneOrMore,   _R.Zero)        : pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
                (_S.Air,        _B.OneOrMore,       _T.Any,             _P.OneOrMore,   _Y.Any,         _R.Any)         : pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
                (_S.Air,        _B.Zero,            _T.OneOrMore,       _P.Zero,        _Y.Any,         _R.OneOrMore)   : pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
                (_S.Air,        _B.Zero,            _T.OneOrMore,       _P.Zero,        _Y.OneOrMore,   _R.Zero)        : pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
                (_S.Air,        _B.Zero,            _T.OneOrMore,       _P.OneOrMore,   _Y.Any,         _R.Any)         : pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
            },
            # This argument is used only for testing
            combinatorial_dimensions = (_S.Any, _B.Any, _T.Any, _P.Any, _Y.Any, _R.Any)
        )


            # Combinatorially, this is unwieldy. It is not amenable to setting
            # up a plain rules table, as was done in MetalRuleset. There would
            # be a lot of combinations.
            #
            #   air/ground
            #   smart band 0, 1, 2, 3+
            #   smart belt 0, 1, 2, 3+
            #   trpr battery 0, 1+
            #   smart band battery 0, 1+
            #   smart belt battery 0, 1+
            #
            # That's 2*4*4*2*2*2 = 256 possibilities

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        # We calculate ion warnings based on six factors:
        #    shipping method : air or ground
        #    SmartBand : 0, 1, 2, or 3+
        #    SmartBelt : 0, 1, 2, or 3+
        #    TRPR battery qty: 0 or 1+
        #    SmartBand battery qty: 0 or 1+
        #    SmartBelt battery qty: 0 or 1+

        smartband_qty = counter[self.Constants.Codes.SmartBand]                                                                    # pylint: disable=no-member
        if smartband_qty == 0:
            smartband_factor = self.Constants.SmartBand.Zero                                                                       # pylint: disable=no-member
        elif smartband_qty == 1:
            smartband_factor = self.Constants.SmartBand.One                                                                        # pylint: disable=no-member
        elif smartband_qty == 2:
            smartband_factor = self.Constants.SmartBand.Two                                                                        # pylint: disable=no-member
        elif smartband_qty > 2:
            smartband_factor = self.Constants.SmartBand.ThreeOrMore                                                                # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid SmartBand quantity %s." % smartband_qty)

        smartbelt_qty = counter[self.Constants.Codes.SmartBelt]                                                                    # pylint: disable=no-member
        if smartbelt_qty == 0:
            smartbelt_factor = self.Constants.SmartBelt.Zero                                                                       # pylint: disable=no-member
        elif smartbelt_qty == 1:
            smartbelt_factor = self.Constants.SmartBelt.One                                                                        # pylint: disable=no-member
        elif smartbelt_qty == 2:
            smartbelt_factor = self.Constants.SmartBelt.Two                                                                        # pylint: disable=no-member
        elif smartbelt_qty > 2:
            smartbelt_factor = self.Constants.SmartBelt.ThreeOrMore                                                                # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid SmartBelt quantity %s." % smartbelt_qty)

        trpr_battery_qty = counter[self.Constants.Codes.TRPRBattery]                                                             # pylint: disable=no-member
        if trpr_battery_qty == 0:
            trpr_battery_factor = self.Constants.TRPRBattery.Zero                                                                # pylint: disable=no-member
        elif trpr_battery_qty > 0:
            trpr_battery_factor = self.Constants.TRPRBattery.OneOrMore                                                           # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid TRPR Battery quantity %s." % trpr_battery_qty)

        smartband_battery_qty = counter[self.Constants.Codes.SmartBandBattery]                                                     # pylint: disable=no-member
        if smartband_battery_qty == 0:
            smartband_battery_factor = self.Constants.SmartBandBattery.Zero                                                        # pylint: disable=no-member
        elif smartband_battery_qty > 0:
            smartband_battery_factor = self.Constants.SmartBandBattery.OneOrMore                                                   # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid SmartBand battery quantity %s." % smartband_battery_qty)

        smartbelt_battery_qty = counter[self.Constants.Codes.SmartBeltBattery]                                                     # pylint: disable=no-member
        if smartbelt_battery_qty == 0:
            smartbelt_battery_factor = self.Constants.SmartBeltBattery.Zero                                                        # pylint: disable=no-member
        elif smartbelt_battery_qty > 0:
            smartbelt_battery_factor = self.Constants.SmartBeltBattery.OneOrMore                                                   # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid SmartBelt battery quantity %s." % smartbelt_battery_qty)

        decisive_factors = (shipping_method,
                            smartband_factor,
                            smartbelt_factor,
                            trpr_battery_factor,
                            smartband_battery_factor,
                            smartbelt_battery_factor,
                           )
        return decisive_factors


@utl_decorators.add_constants_to_class({'LightThoriumRods'   : ('Zero',
                                                                'Normal',
                                                                'BoxInBox',
                                                                'MultiPack',
                                                               ),
                                        'HeavyThoriumRods'   : ('Zero',
                                                                'Normal',
                                                                'BoxInBox',
                                                                'MultiPack',
                                                               ),
                                        'OtherThoriumItem'   : ('Zero',
                                                                'OneOrMore',
                                                               ),
                                       },
                                       magic_number = 160000,
                                      )
class ThoriumRodsRuleset(ItemRuleset):
    """
    Represents rules for thorium welding rod warnings, for heavyweight, large
    diameter thorium rods.
    """
    def __init__(self):
        # Call base class' constructor
        ItemRuleset.__init__(self)

        # Here's a summary of the thorium rules. There are three thorium
        # classes. All thorium shipments must be labelled.
        #
        # Class 1
        #   skinny, lightweight welding rods
        #   Items           Max qty without             Max qty inside                  Over 100
        #   WT040x7         other shielding             a nested box                    Use multiple packages
        #   WT116x7         40                          100 (no data on this, so I'm
        #                                                    conservatively using half
        #                                                    of the 5x multiplier that
        #                                                    the other class exhibits)
        #
        # Class 2
        #   heavier welding rods
        #   Items           Max qty without             Max qty inside                  Over 20
        #   WT332x7         other shielding             a nested box                    Use multiple packages
        #   WT018x7         4                           20
        #   WT532x7
        #
        # Class 3
        #   everything else, pack as normal, no limit, label required


        # "Constants" was added by the "add_constants_to_class" decorator.
        c = self.Constants                                                                                                          # pylint: disable=no-member
        self.ruleset = {
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Zero,       c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.NoWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Zero,       c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Zero,       c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Zero,       c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Normal,     c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Normal,     c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Normal,     c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.Normal,     c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.Zero,       c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Zero,       c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Zero,       c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Zero,       c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Zero,       c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Normal,     c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Normal,     c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909Warning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Normal,     c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.Normal,     c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909WithExtraBoxWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.BoxInBox,   c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.Zero,     )       : pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.Normal,   )       : pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.BoxInBox, )       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            (c.OtherThoriumItem.OneOrMore,  c.LightThoriumRods.MultiPack,  c.HeavyThoriumRods.MultiPack,)       : pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        }

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        # This factor is calculated based on the quantity of small-diameter
        # thorium rods. Note: the sales unit of measure is 10PK
        light_rods_qty = counter[self.Constants.Codes.ThoriatedTungstenRodsLight]                                                   # pylint: disable=no-member
        if light_rods_qty == 0:
            light_rods_factor = self.Constants.LightThoriumRods.Zero                                                                # pylint: disable=no-member
        elif 0 < light_rods_qty <= 40:
            light_rods_factor = self.Constants.LightThoriumRods.Normal                                                              # pylint: disable=no-member
        elif 40 < light_rods_qty <= 100:
            light_rods_factor = self.Constants.LightThoriumRods.BoxInBox                                                            # pylint: disable=no-member
        elif light_rods_qty > 100:
            light_rods_factor = self.Constants.LightThoriumRods.MultiPack                                                           # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid thorium rod quantity %s." % light_rods_qty)

        # This factor is calculated based on the quantity of large-diameter
        # thorium rods. Note: the sales unit of measure is 10PK
        heavy_rods_qty = counter[self.Constants.Codes.ThoriatedTungstenRodsHeavy]                                                   # pylint: disable=no-member
        if heavy_rods_qty == 0:
            heavy_rods_factor = self.Constants.HeavyThoriumRods.Zero                                                                # pylint: disable=no-member
        elif 0 < heavy_rods_qty <= 4:
            heavy_rods_factor = self.Constants.HeavyThoriumRods.Normal                                                              # pylint: disable=no-member
        elif 4 < heavy_rods_qty <= 20:
            heavy_rods_factor = self.Constants.HeavyThoriumRods.BoxInBox                                                            # pylint: disable=no-member
        elif heavy_rods_qty > 20:
            heavy_rods_factor = self.Constants.HeavyThoriumRods.MultiPack                                                           # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid thorium rod quantity %s." % heavy_rods_qty)

        # This factor is calculated based on the quantity of other thorium
        # items. This includes other kinds of thorium rods, and, principally,
        # Weldcraft TIG welding kits, that contain TIG consumables, such as a
        # nozzle and a few welding rods.
        other_thorium_qty = (counter[self.Constants.Codes.ThoriatedTungsten] +                                                      # pylint: disable=no-member
                             counter[self.Constants.Codes.ThoriatedTungstenKit] +                                                   # pylint: disable=no-member
                             counter[self.Constants.Codes.ThoriatedTungstenAccessoryKit]                                            # pylint: disable=no-member
                            )
        if other_thorium_qty == 0:
            other_thorium_factor = self.Constants.OtherThoriumItem.Zero                                                             # pylint: disable=no-member
        elif other_thorium_qty > 0:
            other_thorium_factor = self.Constants.OtherThoriumItem.OneOrMore                                                        # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid quantity of thorium items %s." % other_thorium_qty)

        decisive_factors = (other_thorium_factor,
                            light_rods_factor,
                            heavy_rods_factor,
                           )
        return decisive_factors


@utl_decorators.add_constants_to_class({'ORMD'   : ('Zero',
                                                    'OneOrMore',
                                                   ),
                                       },
                                       magic_number = 170000,
                                      )
class ORMDRuleset(ItemRuleset):
    """
    Represents rules for warnings for ORM-D items. ORM-D items must ship via
    ground.
    """
    def __init__(self):
        # Call base class' constructor
        ItemRuleset.__init__(self)

        # "Constants" was added by the "add_constants_to_class" decorator.
        c = self.Constants                                                                                                  # pylint: disable=no-member
        self.ruleset = {
            (c.Shipping.Ground,     c.ORMD.Zero)        : pkpk_warnings.NoWarning,
            (c.Shipping.Ground,     c.ORMD.OneOrMore)   : pkpk_warnings.GroundORMDWarning,
            (c.Shipping.Air,        c.ORMD.Zero)        : pkpk_warnings.NoWarning,
            (c.Shipping.Air,        c.ORMD.OneOrMore)   : pkpk_warnings.AirORMDWarning,
        }

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        # We calculate warnings for ORMDRuleset based on two factors:
        #    shipping method : air or ground
        #    The quantity of ORM-D items
        ormd_qty = counter[self.Constants.Codes.ORM_D]                                                                      # pylint: disable=no-member
        if ormd_qty == 0:
            ormd_factor = self.Constants.ORMD.Zero                                                                          # pylint: disable=no-member
        elif ormd_qty > 0:
            ormd_factor = self.Constants.ORMD.OneOrMore                                                                     # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Error: Invalid ORM-D quantity %s." % ormd_qty)

        decisive_factors = (shipping_method,
                            ormd_factor,
                           )
        return decisive_factors


#@utl_decorators.add_constants_to_class({'Config' : {'EcommerceCustomer' : '040598',
#                                                  },
#                                       },
#                                      )
#class ECommerceRuleset(SpecialRuleset):
#    """
#    Rules for e-commmerce shipments.
#    """
#    def __init__(self,
#                ):
#        # Call base class' constructor
#        SpecialRuleset.__init__(self)
#
#    def apply_rules(self,
#                    customer_number,
#                    in_store_pickup,
#                   ):
#        """
#        Looks at the customer number, the in_store_pickup value (T or F), and
#        the current date. Determines whether we need a Gas Rebate form. The
#        return value is an instance of a subclass of ShipmentWarning.
#
#        If no warning is needed, returns an instance of the NoWarning class.
#        """
#        this_year = datetime.date.year()
#        next_year = this_year + 1
#        start_date = datetime.date(this_year, 11, 25)
#        end_date = datetime.date(next_year, 1, 31)
#
#        # Online Order - In store pick u
#        # p - Please add special label
#
#        # I'm not doing anything with initials now, because that is used for
#        # calculating a different sticker. That sticker is currently being
#        # applied at the Clippership scale. The Clippership automation code
#        # throws up a warning.
#
#        if (customer_number == self.Constants.Config.EcommerceCustomer                                                      # pylint: disable=no-member
#            and start_date <= datetime.date.today() <= end_date):
#            return pkpk_warnings.ECommerceWarning()
#        else:
#            return pkpk_warnings.NoWarning()


# We instantiate these potentially large static objects only once, and we store
# them here in these variables.
normal_item_ruleset_package = (MetalRuleset(),
                               MetalAndIonOtherRuleset(),
                               GeneralTrprRuleset(),
                               IonRuleset(),
                               ThoriumRodsRuleset(),
                               ORMDRuleset(),
                              )
#e_commerce_ruleset = ECommerceRuleset()

def get_item_rulesets(ctx):
    """
    This supplies the appropriate ruleset package depending on what the context
    object says.
    """
    if ctx is None:
        return normal_item_ruleset_package
    elif ctx.flavor == ctx.Constants.Flavor.Normal:                             # pylint: disable=no-member
        return normal_item_ruleset_package
    else:
        raise pickpack_errors.ApplicationError("Error: Invalid context object flavor value %s." % ctx.flavor)





















# OLD code







# Cacheing
#
# http://code.activestate.com/recipes/576532/
# http://en.wikipedia.org/wiki/Adaptive_replacement_cache
#
#class Cache(object):
#    """
#    >>> dec_cache = Cache(10)
#    >>> @dec_cache
#    ... def identity(f):
#    ...     return f
#    >>> dummy = [identity(x) for x in range(20) + range(11,15) + range(20) +
#    ... range(11,40) + [39, 38, 37, 36, 35, 34, 33, 32, 16, 17, 11, 41]]
#    >>> dec_cache.t1
#    deque([(41,)])
#    >>> dec_cache.t2
#    deque([(11,), (17,), (16,), (32,), (33,), (34,), (35,), (36,), (37,)])
#    >>> dec_cache.b1
#    deque([(31,), (30,)])
#    >>> dec_cache.b2
#    deque([(38,), (39,), (19,), (18,), (15,), (14,), (13,), (12,)])
#    >>> dec_cache.p
#    5
#    """
#    def __init__(self, size):
#        self.cached = {}
#        self.c = size
#        self.p = 0
#        self.t1 = deque()
#        self.t2 = deque()
#        self.b1 = deque()
#        self.b2 = deque()
#
#    def replace(self, args):
#        if self.t1 and (
#            (args in self.b2 and len(self.t1) == self.p) or
#            (len(self.t1) > self.p)):
#            old = self.t1.pop()
#            self.b1.appendleft(old)
#        else:
#            old = self.t2.pop()
#            self.b2.appendleft(old)
#        del(self.cached[old])
#
#    def __call__(self, func):
#        def wrapper(*orig_args):
#            """decorator function wrapper"""
#            args = orig_args[:]
#            if args in self.t1:
#                self.t1.remove(args)
#                self.t2.appendleft(args)
#                return self.cached[args]
#            if args in self.t2:
#                self.t2.remove(args)
#                self.t2.appendleft(args)
#                return self.cached[args]
#            result = func(*orig_args)
#            self.cached[args] = result
#            if args in self.b1:
#                self.p = min(
#                    self.c, self.p + max(len(self.b2) / len(self.b1) , 1))
#                self.replace(args)
#                self.b1.remove(args)
#                self.t2.appendleft(args)
#                #print "%s:: t1:%s b1:%s t2:%s b2:%s p:%s" % (
#                #    repr(func)[10:30], len(self.t1),len(self.b1),len(self.t2),
#                #    len(self.b2), self.p)
#                return result
#            if args in self.b2:
#                self.p = max(0, self.p - max(len(self.b1)/len(self.b2) , 1))
#                self.replace(args)
#                self.b2.remove(args)
#                self.t2.appendleft(args)
#                #print "%s:: t1:%s b1:%s t2:%s b2:%s p:%s" % (
#                #   repr(func)[10:30], len(self.t1),len(self.b1),len(self.t2),
#                #   len(self.b2), self.p)
#                return result
#            if len(self.t1) + len(self.b1) == self.c:
#                if len(self.t1) < self.c:
#                    self.b1.pop()
#                    self.replace(args)
#                else:
#                    del(self.cached[self.t1.pop()])
#            else:
#                total = len(self.t1) + len(self.b1) + len(
#                    self.t2) + len(self.b2)
#                if total >= self.c:
#                    if total == (2 * self.c):
#                        self.b2.pop()
#                    self.replace(args)
#            self.t1.appendleft(args)
#            return result
#        return wrapper
#
#
#
#
# In the comments on this recipe, Raymond Hettinger says this:
#
#
# Thanks for the nice, clean translation of the spec in the patent application.
#
# As presented, the recipe uses collections.deque() which is efficient for the
# all of the operations except remove() and __contains__() which are both O(n)
# operations.
#
# Instead of collections.deque(), it would be better to use an alternate deque
# implementation that supports fast searching and removal. This can easily be
# expressed using collections.OrderedDict() which appeared in Py2.7 and Py3.1
# and has an ASPN recipe for earlier versions. In the recipe above, just
# substitute Deque for deque and define it as:
#
#class Deque:
#    'Fast searchable queue'
#    def __init__(self):
#        self.od = OrderedDict()
#    def appendleft(self, k):
#        od = self.od
#        if k in od:
#            del od[k]
#        od[k] = None
#    def pop(self):
#        return self.od.popitem(0)[0]
#    def remove(self, k):
#        del self.od[k]
#    def __len__(self):
#        return len(self.od)
#    def __contains__(self, k):
#        return k in self.od
#    def __iter__(self):
#        return reversed(self.od)
#    def __repr__(self):
#        return 'Deque(%r)' % (list(self),)
