"""
pkpk_warnings.py

This module contains are all the possible warnings that we can output.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from Common.utility import utl_decorators

from Pickpack.pickpack_modules.warn.utility_classes import PackingInstructionConstants

class ShipmentWarning(object):
    """
    Represents a warning we return to the user. The warning informs the user
    about what kind of special treatment this shipment should receive. For
    example: battery warning labels.


    The interesting properties are:
        note_text        - String, or tuple of strings
        image_names      - String, or tuple of strings indicating which image to
                           display
    """
    def __init__(self):
        self.note_text = None
        self.image_names = None

class LithiumBatteryWarning(ShipmentWarning, PackingInstructionConstants):
    """
    Base class for warinings about all lithium batteries.
    """
    def __init__(self):
        ShipmentWarning.__init__(self)


@utl_decorators.add_constants_to_class({'Image' : {'OneLabel' : 'metal1',
                                                   'TwoLabels' : 'metal2',
                                                  },
                                       },
                                      )
class MetalWarning(LithiumBatteryWarning):
    """
    Base class for warinings about lithium metal batteries.
    """
    def __init__(self):
        LithiumBatteryWarning.__init__(self)


@utl_decorators.add_constants_to_class({'Image' : {'OneLabel' : 'ion1',
                                                   'TwoLabels' : 'ion2',
                                                  },
                                       },
                                      )
class IonWarning(LithiumBatteryWarning):
    """
    Base class for warinings about lithium ion batteries.
    """
    def __init__(self):
        LithiumBatteryWarning.__init__(self)


@utl_decorators.add_constants_to_class({'Image' : {'MetalLabel' : 'metal1',
                                                   'IonLabel' : 'ion1',
                                                  },
                                       },
                                      )
class MetalAndIonWarning(LithiumBatteryWarning):
    """
    Base class for warinings about items that contain both metal and ion
    batteries.
    """
    def __init__(self):
        LithiumBatteryWarning.__init__(self)


@utl_decorators.add_constants_to_class({'Image' : {'UN2909' : 'un_2909',
                                                   'ExtraPackaging' : 'boxes',
                                                  },
                                       },
                                      )
class ThoriumWarning(ShipmentWarning):
    """
    Base class for warinings about items that contain thoriated welding rods.
    """
    def __init__(self):
        ShipmentWarning.__init__(self)


class ORMDWarning(ShipmentWarning):
    """
    Base class for warinings about items that contain ORM-D HazMat.
    """
    def __init__(self):
        ShipmentWarning.__init__(self)


#@utl_decorators.add_constants_to_class({'Image' : {'Overpack' : 'overpack',
#                                                  },
#                                       },
#                                      )
#class OverpackWarning(ShipmentWarning):
#    """
#    Base class for warinings to the Truck team about orders that contain items
#    that don't require a warning when shipped singly, but do require an
#    "Overpack" label when aggregated.
#    """
#    def __init__(self):
#        ShipmentWarning.__init__(self)


class NoWarning(ShipmentWarning):
    """
    Class for use when no warning is needed.
    """
    def __init__(self):
        ShipmentWarning.__init__(self)


class GroundCoinBatteryWarning(MetalWarning):
    """
    Used when any number of coin batteries go by ground.
    """
    def __init__(self):
        MetalWarning.__init__(self)
        self.note_text = 'Pack coin batteries with other items'
        self.image_names = self.Constants.Image.TwoLabels                                                                           # pylint: disable=no-member


class GroundSmartBandBatteryWarning(IonWarning):
    """
    Used when any number of spare SmartBand batteries go by ground. Pre-empts
    GroundFewSmartBandSmartBeltWarning and GroundManySmartBandSmartBeltWarning.
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = 'Pack SmartBand batteries with other items, max 75 per box'
        self.image_names = self.Constants.Image.TwoLabels                                                                           # pylint: disable=no-member


class GroundSmartBeltBatteryWarning(IonWarning):
    """
    Used when any number of spare SmartBelt batteries go by ground. Pre-empts
    GroundSmartBandBatteryWarning, GroundFewSmartBandSmartBeltWarning and
    GroundManySmartBandSmartBeltWarning.
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = 'Pack SmartBelt batteries with other items, max 40 per box'
        self.image_names = self.Constants.Image.TwoLabels                                                                           # pylint: disable=no-member


class GroundTrprBatteryWarning(IonWarning):
    """
    Used when any number of TRPR batteries go by ground. Pre-empts
    GroundSmartBeltBatteryWarning, GroundFewSmartBandSmartBeltWarning and
    GroundManySmartBandSmartBeltWarning.
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = 'Pack TRPR batteries with other items, max 20 per box'
        self.image_names = self.Constants.Image.TwoLabels                                                                           # pylint: disable=no-member


class GroundFewSmartBandSmartBeltWarning(IonWarning):
    """
    Used when a total of 1 or 2 SmartBands and/or SmartBelts go by ground.
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = 'SmartBands/SmartBelts get Ion label'
        self.image_names = self.Constants.Image.OneLabel                                                                            # pylint: disable=no-member


class GroundManySmartBandSmartBeltWarning(IonWarning):
    """
    Used when any number of SmartBands and/or SmartBelts go by ground.
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = 'SmartBands/SmartBelts get Ion label'
        self.image_names = self.Constants.Image.TwoLabels                                                                           # pylint: disable=no-member


class GroundTrprWarning(MetalAndIonWarning):
    """
    Used when any number of TRPR kits go by ground. Complete TRPR kits
    contain both lithium ion and lithium metal batteries. Ion-only TRPR kits
    contain only ion batteries. However, we do not need to warn about the metal
    batteries, just the ion. So we treat "complete" and "ion-only" the same.

    TRPR kits come in a large box, and they ship individually in their own
    packaging.
    """
    def __init__(self):
        MetalAndIonWarning.__init__(self)
        self.note_text = 'Label each TRPR box with Ion label'
        self.image_names = self.Constants.Image.IonLabel                                                                            # pylint: disable=no-member


class GroundHelmetAndSmartBandBeltKitWarning(MetalAndIonWarning):
    """
    Used when any number of "both" items go by ground. Some items we ship are
    kits that contain both lithium ion and lithium metal batteries (e.g. a
    Helmet and a SmartBand in the same package). We do not need to warn about the
    metal batteries, just the ion. So, such kits get just ion labels.
    """
    def __init__(self):
        MetalAndIonWarning.__init__(self)
        self.note_text = 'Label each Helmet + SmartBand/SmartBelt kit with Ion label'
        self.image_names = self.Constants.Image.IonLabel                                                                            # pylint: disable=no-member


class AirCoinBatteryWarning(MetalWarning):
    """
    Used when any number of coin batteries go by air.
    """
    def __init__(self):
        MetalWarning.__init__(self)
        self.note_text = ('Pack coin batteries in a separate box',
                          'Mark "Metal, Batteries Only" on document',
                         )
        self.image_names = (self.Constants.Image.TwoLabels,                                                                         # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction968,                                                             # pylint: disable=no-member
                           )


class AirSmartBandSmartBeltWithBatteryWarning(IonWarning):
    """
    Used when one or more SmartBands/SmartBelts goes by air, with spare ion
    batteries
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = ('Max 2 SmartBands/SmartBelts per box',
                          'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                          '------------------',
                          'Package Ion batteries in a separate box, max 2 per box',
                          'Mark "Ion, Batteries Only" on the document for the battery box',
                         )
        self.image_names = (self.Constants.Image.TwoLabels,                                                                         # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction966And965,                                                       # pylint: disable=no-member
                           )


class AirIonBatteryWarning(IonWarning):
    """
    Used when any number of TRPR batteries, SmartBand batteries, or SmartBelt
    batteries go by air, without any TRPR, SmartBand or SmartBelt.
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = ('Package Ion batteries in a separate box, max 2 per box',
                          'Mark "Ion, Batteries Only" on document',
                         )
        self.image_names = (self.Constants.Image.TwoLabels,                                                                         # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction965,                                                             # pylint: disable=no-member
                           )


class AirFewSmartBandSmartBeltWarning(IonWarning):
    """
    Used when a total of 1 or 2 SmartBands and/or SmartBelts go by air, without
    spare batteries
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = ('SmartBands/SmartBelts get Ion label',
                          'Mark "Ion, With Equipment" on document',
                         )
        self.image_names = (self.Constants.Image.OneLabel,                                                                          # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction966,                                                             # pylint: disable=no-member
                           )


class AirManySmartBandSmartBeltWarning(IonWarning):
    """
    Used when more than two total SmartBands and/or SmartBelts go by air, without
    spare batteries
    """
    def __init__(self):
        IonWarning.__init__(self)
        self.note_text = ('Max 2 SmartBands/SmartBelts per box',
                          'SmartBands/SmartBelts get Ion label',
                          'Mark "Ion, With Equipment" on document',
                         )
        self.image_names = (self.Constants.Image.TwoLabels,                                                                         # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction966,                                                             # pylint: disable=no-member
                           )


class AirTrprWarning(MetalAndIonWarning):
    """
    Used when any number of TRPR kits go by air. Complete TRPR kits
    contain both lithium ion and lithium metal batteries. Ion-only TRPR kits
    contain only ion batteries. However, we do not need to warn about the metal
    batteries, just the ion. So we treat "complete" and "ion-only" the same.

    TRPR kits come in a large box, and they ship individually in their own
    packaging.
    """
    def __init__(self):
        MetalAndIonWarning.__init__(self)
        self.note_text = ('Label each TRPR box with Ion label',
                          'Mark "Ion, With Equipment" on document',
                         )
        self.image_names = (self.Constants.Image.IonLabel,                                                                          # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction966,                                                             # pylint: disable=no-member
                           )


class AirHelmetAndSmartBandBeltKitWarning(MetalAndIonWarning):
    """
    Used when any number of "both" items go by air. Some items we ship are kits
    that contain both lithium ion and lithium metal batteries (e.g. a Helmet and
    a SmartBand in the same package). We do not need to warn about the metal
    batteries, just the ion. So, such kits get just ion labels.
    """
    def __init__(self):
        MetalAndIonWarning.__init__(self)
        self.note_text = ('Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                          'Mark "Ion, With Equipment" on document',
                         )
        self.image_names = (self.Constants.Image.IonLabel,                                                                          # pylint: disable=no-member
                            self.Constants.Image.PackingInstruction966,                                                             # pylint: disable=no-member
                           )


class UN2909Warning(ThoriumWarning):
    """
    Used when a small number of thoriated welding rods (or kits containing such
    rods) go by ground or air.
    """
    def __init__(self):
        ThoriumWarning.__init__(self)
        self.note_text = 'Label shipping carton with UN 2909 label'
        self.image_names = self.Constants.Image.UN2909                                                                              # pylint: disable=no-member


class UN2909WithExtraBoxWarning(ThoriumWarning):
    """
    Used when a larger number of thoriated welding rods go by ground or air.
    """
    def __init__(self):
        ThoriumWarning.__init__(self)

        self.note_text = ('Wrap thoriated rods in a small box inside shipping carton',
                          'Label shipping carton with UN 2909 label',
                         )
        self.image_names = (self.Constants.Image.UN2909,                                                                            # pylint: disable=no-member
                            self.Constants.Image.ExtraPackaging,                                                                    # pylint: disable=no-member
                           )


class UN2909MultiplePackagesLightRodsWarning(ThoriumWarning):
    """
    Used when shipping more lightweight thoriated rods than are allowed in a
    single packge. Tells the user to split the order in to several shipping
    cartons.
    """
    def __init__(self):
        ThoriumWarning.__init__(self)

        self.note_text = ('Ship in multiple packages',
                          'Max 100 packs of rods per package',
                          'Wrap thoriated rods in a small box inside each shipping carton',
                          'Label shipping cartons with UN 2909 label',
                         )
        self.image_names = (self.Constants.Image.UN2909,                                                                            # pylint: disable=no-member
                            self.Constants.Image.ExtraPackaging,                                                                    # pylint: disable=no-member
                           )


class UN2909MultiplePackagesHeavyRodsWarning(ThoriumWarning):
    """
    Used when shipping more heavyweight thoriated rods than are allowed in a
    single packge. Tells the user to split the order in to several shipping
    cartons.
    """
    def __init__(self):
        ThoriumWarning.__init__(self)

        self.note_text = ('Ship in multiple packages',
                          'Max 20 packs of rods per package',
                          'Wrap thoriated rods in a small box inside each shipping carton',
                          'Label shipping cartons with UN 2909 label',
                         )
        self.image_names = (self.Constants.Image.UN2909,                                                                            # pylint: disable=no-member
                            self.Constants.Image.ExtraPackaging,                                                                    # pylint: disable=no-member
                           )


@utl_decorators.add_constants_to_class({'Image' : {'ORM_D' : 'ormd',
                                                   'BoxRating' : 'box_rating',
                                                  },
                                       },
                                      )
class GroundORMDWarning(ORMDWarning):
    """
    Used when ORM-D hazmat items go by ground.
    """
    def __init__(self):
        ORMDWarning.__init__(self)
        self.note_text = ('Label ORM-D. Make sure the box rating is visible',
                          'Must ship by Ground',
                         )
        self.image_names = (self.Constants.Image.ORM_D,                                                                             # pylint: disable=no-member
                            self.Constants.Image.BoxRating,                                                                         # pylint: disable=no-member
                           )


@utl_decorators.add_constants_to_class({'Image' : {'DoNotShip' : 'red_x',
                                                  },
                                       },
                                      )
class AirORMDWarning(ORMDWarning):
    """
    Used when ORM-D hazmat items are on an order going by air. This throws up a
    big warnining stating that ORM-D must go by ground.
    """
    def __init__(self):
        ORMDWarning.__init__(self)
        self.note_text = ('STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.',
                          'Label ORM-D. Make sure the box rating is visible',
                         )
        self.image_names = self.Constants.Image.DoNotShip                                                                           # pylint: disable=no-member


@utl_decorators.add_constants_to_class({'Image' : {'DollarSign' : 'dollar_sign',
                                                  },
                                       },
                                      )
class ECommerceWarning(ShipmentWarning):
    """
    Used for e-commerce orders
    """
    def __init__(self):
        ShipmentWarning.__init__(self)
        self.note_text = 'Include Gas Purchase Mail-In Rebate Form.'
        self.image_names = self.Constants.Image.DollarSign                                                                          # pylint: disable=no-member


@utl_decorators.add_constants_to_class({'Image' : {'Helmet' : 'helmet',
                                                  },
                                       },
                                      )
class GroundHelmetWarning(ShipmentWarning):
    """
    Used for cases when we ship three or more helmets.
    """
    def __init__(self, number_of_helmets):
        ShipmentWarning.__init__(self)
        self.note_text = 'This order has %s helmets. The helmets must go Ground' % number_of_helmets
        self.image_names = self.Constants.Image.Helmet                                                                         # pylint: disable=no-member


@utl_decorators.add_constants_to_class({'Image' : {'HeavyWeight' : 'heavy_weight',
                                                  },
                                       },
                                      )
class HeavyOrderWarning(ShipmentWarning):
    """
    Used for orders over 35 lb.
    """
    def __init__(self, calcualted_order_weight):
        ShipmentWarning.__init__(self)
        self.note_text = 'This order weighs %s lbs. Orders over 35 lbs. must go Ground. Apply the yellow Ground sticker.' % int(calcualted_order_weight)
        self.image_names = self.Constants.Image.HeavyWeight                                                                     # pylint: disable=no-member


@utl_decorators.add_constants_to_class({'Image' : {'P' : 'p',
                                                  },
                                       },
                                      )
class InternationalWarning(ShipmentWarning):
    """
    Used for international orders.
    """
    def __init__(self):
        ShipmentWarning.__init__(self)
        self.note_text = 'International order. Check destination.'
        self.image_names = self.Constants.Image.P                                                                               # pylint: disable=no-member


@utl_decorators.add_constants_to_class({'Image' : {'Harper' : 'harper',
                                                  },
                                       },
                                      )
class HarperWarning(ShipmentWarning):
    """
    Used for Harper orders.
    """
    def __init__(self):
        ShipmentWarning.__init__(self)
        self.note_text = 'Harper order. Bring to Harper bench.'
        self.image_names = self.Constants.Image.Harper                                                                        # pylint: disable=no-member
