"""
Tests for the classes in the warn.rulesets.py module
"""
# pylint: disable=too-many-public-methods

import collections

from CML_Pickpack.pickpack_modules.warn import rulesets, pkpk_warnings
from CML_Pickpack.pickpack_modules.test.utility_classes_for_testing import BaseItemRulesetTester, MultiDictBackedRuleset

class TestMetalRuleset(BaseItemRulesetTester):
    """
    Test the MetalRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.MetalRuleset()

    def __init__(self):
        BaseItemRulesetTester.__init__(self)

    def test_no_thorium(self):
        """
        Thorium generates no warning
        """
        self._run_apply_rules(
            counter = collections.Counter({'TH3' : 13,
                                           'TH4' : 14,
                                           'TH5' : 15,
                                           'TH1' : 16,
                                           'TH2' : 12,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test3(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                           'HZ0' : 2,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test4(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test5(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test7(self):
        self._run_apply_rules(
            counter = collections.Counter({'SB0' : 6,
                                           'BT0' : 300,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirCoinBatteryWarning,
            expected_result_ground = pkpk_warnings.GroundCoinBatteryWarning,
        )


class TestMetalAndIonOtherRuleset(BaseItemRulesetTester):
    """
    Test the MetalAndIonOtherRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.MetalAndIonOtherRuleset()

    def __init__(self):
        BaseItemRulesetTester.__init__(self)

    def test_no_thorium(self):
        """
        Thorium generates no warning
        """
        self._run_apply_rules(
            counter = collections.Counter({'TH3' : 13,
                                           'TH4' : 14,
                                           'TH5' : 15,
                                           'TH1' : 16,
                                           'TH2' : 12,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test3(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                           'HZ0' : 2,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test4(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test5(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test7(self):
        self._run_apply_rules(
            counter = collections.Counter({'SB0' : 6,
                                           'BT0' : 300,
                                           'HZ0' : 2,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )


class TestGeneralTrprRuleset(BaseItemRulesetTester):
    """
    Test the GeneralTrprRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.GeneralTrprRuleset()

    def __init__(self):
        BaseItemRulesetTester.__init__(self)

    def test_no_thorium(self):
        """
        Thorium generates no warning
        """
        self._run_apply_rules(
            counter = collections.Counter({'TH3' : 13,
                                           'TH4' : 14,
                                           'TH5' : 15,
                                           'TH1' : 16,
                                           'TH2' : 12,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test3(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirTrprWarning,
            expected_result_ground = pkpk_warnings.GroundTrprWarning,
        )

    def test4(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirTrprWarning,
            expected_result_ground = pkpk_warnings.GroundTrprWarning,
        )

    def test5(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )


class TestIonRuleset(MultiDictBackedRuleset):
    """
    Test the IonRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.IonRuleset()

    def __init__(self):
        MultiDictBackedRuleset.__init__(self)

    def test3(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test4(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 1,
                                           'HZ0' : 2,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test5(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test7(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test8(self):
        self._run_apply_rules(
            counter = collections.Counter({'SB1' : 1,
                                           'SB2' : 30,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirIonBatteryWarning,
            expected_result_ground = pkpk_warnings.GroundSmartBeltBatteryWarning,
        )

    def test9(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 2,
                                           'SB1' : 1,
                                           'SB2' : 30,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirSmartBandSmartBeltWithBatteryWarning,
            expected_result_ground = pkpk_warnings.GroundSmartBeltBatteryWarning,
        )

    def test10(self):
        expected_result_air = pkpk_warnings.AirFewSmartBandSmartBeltWarning,
        expected_result_ground = pkpk_warnings.GroundFewSmartBandSmartBeltWarning,

        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 1}),
            expected_result_air = expected_result_air,
            expected_result_ground = expected_result_ground,
        )
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 2}),
            expected_result_air = expected_result_air,
            expected_result_ground = expected_result_ground,
        )
        self._run_apply_rules(
            counter = collections.Counter({'CT0' : 1}),
            expected_result_air = expected_result_air,
            expected_result_ground = expected_result_ground,
        )
        self._run_apply_rules(
            counter = collections.Counter({'CT0' : 2}),
            expected_result_air = expected_result_air,
            expected_result_ground = expected_result_ground,
        )
        self._run_apply_rules(
            counter = collections.Counter({'CT0' : 1, 'CB0' : 1}),
            expected_result_air = expected_result_air,
            expected_result_ground = expected_result_ground,
        )

    def test11(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 3}),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test12(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 20}),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test13(self):
        self._run_apply_rules(
            counter = collections.Counter({'CT0' : 4}),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test14(self):
        self._run_apply_rules(
            counter = collections.Counter({'CT0' : 330}),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test15(self):
        self._run_apply_rules(
            counter = collections.Counter({'CT0' : 2, 'CB0' : 1}),
            expected_result_air = pkpk_warnings.AirManySmartBandSmartBeltWarning,
            expected_result_ground = pkpk_warnings.GroundManySmartBandSmartBeltWarning,
        )

    def test16(self):
        self._run_with_exception(
            self._run_apply_rules,
            'Error: Invalid SmartBand quantity -20.',
            **{'counter' : collections.Counter({'CB0' : -20}),
               # An exception gets raised before we get to compare actual vs
               # expected, so no need to provide expected results here.
               'expected_result_air' : None,
               'expected_result_ground' : None,
              }
        )


class TestThoriumRodsRuleset(BaseItemRulesetTester):
    """
    Test the TestThoriumRodsRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.ThoriumRodsRuleset()

    def __init__(self):
        BaseItemRulesetTester.__init__(self)

    def test1(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                           'HZ0' : 2,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test2(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                           'TH1' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test3(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH2' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test4(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH3' : 4,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test5(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH4' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test6(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH5' : 0,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test7(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH5' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test8(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 1,
                                           'TH2' : 1,
                                           'TH3' : 1,
                                           'TH4' : 1,
                                           'TH5' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test9(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 1,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test10(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 40,
                                           #'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test11(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 41,
                                           #'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test12(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           #'TH3' : 40,
                                           'TH4' : 4,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test13(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           #'TH3' : 41,
                                           'TH4' : 5,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test14(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 40,
                                           'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test15(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 41,
                                           'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test16(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 40,
                                           'TH4' : 4,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test17(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 41,
                                           'TH4' : 4,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test18(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 40,
                                           'TH4' : 5,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test19(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 41,
                                           'TH4' : 5,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test24(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 40,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test25(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 41,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test26(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 40,
                                           'TH4' : 4,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909Warning,
            expected_result_ground = pkpk_warnings.UN2909Warning,
        )

    def test27(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 41,
                                           'TH4' : 4,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test28(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 40,
                                           'TH4' : 5,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test29(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 41,
                                           'TH4' : 5,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test30(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 100,
                                           #'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test31(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 101,
                                           #'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
        )

    def test32(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           #'TH3' : 100,
                                           'TH4' : 20,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test33(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           #'TH3' : 101,
                                           'TH4' : 21,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test34(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test35(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 1,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
        )

    def test36(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 20,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test37(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 20,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test38(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 21,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test39(self):
        self._run_apply_rules(
            counter = collections.Counter({#'TH1' : 100,
                                           #'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 21,
                                           #'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test40(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test41(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
        )

    def test42(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 20,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test43(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 21,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test44(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test45(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 1,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesLightRodsWarning,
        )

    def test46(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 20,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909WithExtraBoxWarning,
            expected_result_ground = pkpk_warnings.UN2909WithExtraBoxWarning,
        )

    def test47(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 20,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test48(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 100,
                                           'TH4' : 21,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test49(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 100,
                                           'TH2' : 100,
                                           'TH3' : 101,
                                           'TH4' : 21,
                                           'TH5' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )

    def test50(self):
        self._run_apply_rules(
            counter = collections.Counter({'TH1' : 1000,
                                           'TH2' : 1000,
                                           'TH3' : 1000,
                                           'TH4' : 1000,
                                           'TH5' : 1000,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
            expected_result_ground = pkpk_warnings.UN2909MultiplePackagesHeavyRodsWarning,
        )


class TestORMDRuleset(BaseItemRulesetTester):
    """
    Test the ORMDRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.ORMDRuleset()

    def __init__(self):
        BaseItemRulesetTester.__init__(self)

    def test_no_thorium(self):
        """
        Thorium generates no warning
        """
        self._run_apply_rules(
            counter = collections.Counter({'TH3' : 13,
                                           'TH4' : 14,
                                           'TH5' : 15,
                                           'TH1' : 16,
                                           'TH2' : 12,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test3(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test4(self):
        self._run_apply_rules(
            counter = collections.Counter({'PA0' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test5(self):
        self._run_apply_rules(
            counter = collections.Counter({'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test6(self):
        self._run_apply_rules(
            counter = collections.Counter({'HZ0' : 2,
                                           'CB0' : 6,
                                           'CT0' : 3,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirORMDWarning,
            expected_result_ground = pkpk_warnings.GroundORMDWarning,
        )

    def test7(self):
        self._run_apply_rules(
            counter = collections.Counter({'HZ0' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirORMDWarning,
            expected_result_ground = pkpk_warnings.GroundORMDWarning,
        )

    def test8(self):
        self._run_apply_rules(
            counter = collections.Counter({'HZ0' : 71,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.AirORMDWarning,
            expected_result_ground = pkpk_warnings.GroundORMDWarning,
        )

    def test9(self):
        self._run_apply_rules(
            counter = collections.Counter({'SB0' : 6,
                                           'BT0' : 300,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )



# Even though TestIonRuleset inherits from MultiDictBackedRuleset instead of
# BaseItemRulesetTester, it's still ok to use BaseItemRulesetTester as the base
# class for this class. BaseItemRulesetTester is fine for testing the IonRuleset
# with these common tests.
#
# MultiDictBackedRuleset brings some additional testing, such as verification of
# the multi-dict (e.g. making sure that it covers the combinatorial space
# completely with no overlaps).
class ContainerForCommonTests(BaseItemRulesetTester):
    """
    These tests apply to all the rulesets.
    """

    def __init__(self):
        BaseItemRulesetTester.__init__(self)

    def test2(self):
        """
        Unknown counter values are accepted, and generate no warning
        """
        self._run_apply_rules(
            # Counter with unknown values
            counter = collections.Counter(a=4, b=2, c=0, d=-2),

            # Rulesets do not check for unknown values. That is done higher up,
            # in the BatteryWarningCalculator class
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test6(self):
        """
        Helmets generate no warning
        Note: these item codes are no longer in use.
        """
        self._run_apply_rules(
            counter = collections.Counter({'HE0' : 1,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )

    def test7(self):
        """
        Even large quantities of helmets and helment lenses generate no warning
        Note: these item codes are no longer in use.
        """
        self._run_apply_rules(
            counter = collections.Counter({'HE0' : 41,
                                           'HE1' : 100,
                                          }
                                         ),
            expected_result_air = pkpk_warnings.NoWarning,
            expected_result_ground = pkpk_warnings.NoWarning,
        )


class TestMetalRulesetCommon(ContainerForCommonTests):
    """
    Run the common tests against the MetalRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.MetalRuleset()


class TestMetalAndIonOtherRulesetCommon(ContainerForCommonTests):
    """
    Run the common tests against the MetalAndIonOtherRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.MetalAndIonOtherRuleset()


class TestGeneralTrprRulesetCommon(ContainerForCommonTests):
    """
    Run the common tests against the GeneralTrprRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.GeneralTrprRuleset()


class TestIonRulesetCommon(ContainerForCommonTests):
    """
    Run the common tests against the IonRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.IonRuleset()


class TestThoriumRodsRulesetCommon(ContainerForCommonTests):
    """
    Run the common tests against the ThoriumRodsRuleset class.
    """

    # Define this at class level, so we only build it once, and reuse it many
    # times, just as is done in the real application.
    out = rulesets.ThoriumRodsRuleset()















# OLD code


# Somehow, this attempt at dynamically generating test cases based on
# ContainerForCommonTests was not working. Later additions to
# DynamicalyGeneratedTestContainer were clobbering earlier ones, or hiding them
# from Nose.
#
# So, instead, I just did it manually, as you can see above.
#
#
#class DynamicalyGeneratedTestContainer(unittest.TestCase):
#    """
#    This class is an empty container, to which test cases will be added,
#    dynamically.
#    """
#
#ruleset_package = (
#                   rulesets.MetalRuleset(),
#                   #rulesets.MetalAndIonOtherRuleset(),
#                   rulesets.GeneralTrprRuleset(),
#                   #rulesets.IonRuleset(),
#                  )
#
#
## Loop through all the rulesets, and generate an instance of ContainerForCommonTests for each
## ruleset. Dynamicaly add the ContainerForCommonTests instance to
## DynamicalyGeneratedTestContainer, so Nose can find it.
#for ruleset in ruleset_package:
#
#    ruleset_name = ruleset.__class__.__name__
#
#
#    # Dynamically generate a new class, that inherits from
#    # ContainerForCommonTests. The new class has an appropriate name, based upon
#    # the ruleset it is testing.
#    test_class_name = "TestCommon_aglagl_%s" % ruleset_name
#    test_class = type(test_class_name,
#                      (ContainerForCommonTests,),
#                      dict(),
#                     )
#
#
#    # Here, we set an attrubute of the new class. out stands for "object under
#    # test".
#    test_class.out = ruleset
#
#    # Make an instance of the new class, and add it to the dynamic test
#    # container.
#    #test_class_instance = test_class()
#    setattr(DynamicalyGeneratedTestContainer,
#            #'testClassFor%s' % ruleset_name,
#            test_class_name,
#            test_class,
#           )
#
#
