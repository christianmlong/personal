"""
Tests for the classes in the warn.utility_classes.py module

"""


from Pickpack.pickpack_modules.warn import utility_classes
from Pickpack.pickpack_modules.test.utility_classes_for_testing import MultiDictBackedRuleset



class BaseDummyRuleset(MultiDictBackedRuleset):
    """
    Base for DummyRulesets.
    """
    def __init__(self):
        MultiDictBackedRuleset.__init__(self)

        self._A = range(10, 14)
        self._B = range(20, 24)
        self._C = range(30, 34)
        self._D = range(40, 44)
        self._E = range(50, 54)
        self._F = range(60, 64)

        self._A_Any = frozenset((self._A[0],
                            self._A[1],
                           )
                          )
        self._B_Any = frozenset((self._B[0],
                            self._B[1],
                            self._B[2],
                            self._B[3],
                           )
                          )
        self._B_OneOrTwo = frozenset((self._B[1],
                                 self._B[2],
                                )
                               )
        self._B_OneOrMore = frozenset((self._B[1],
                                  self._B[2],
                                  self._B[3],
                                 )
                                )
        self._B_TwoOrMore = frozenset((self._B[2],
                                  self._B[3],
                                 )
                                )
        self._C_Any = frozenset((self._C[0],
                            self._C[1],
                            self._C[2],
                            self._C[3],
                           )
                          )
        self._C_OneOrTwo = frozenset((self._C[1],
                                 self._C[2],
                                )
                               )
        self._C_OneOrMore = frozenset((self._C[1],
                                  self._C[2],
                                  self._C[3],
                                 )
                                )
        self._C_TwoOrMore = frozenset((self._C[2],
                                  self._C[3],
                                 )
                                )
        self._D_Any = frozenset((self._D[0],
                            self._D[1],
                           )
                          )
        self._E_Any = frozenset((self._E[0],
                            self._E[1],
                           )
                          )
        self._F_Any = frozenset((self._F[0],
                            self._F[1],
                           )
                          )

        self.combinatorial_dimensions = (self._A_Any, self._B_Any, self._C_Any, self._D_Any, self._E_Any, self._F_Any)


class Marker(object):
    """
    Simple marker
    """
    def __init__(self, marker_value):
        self.marker_value = marker_value


class TestDummyRuleset1(BaseDummyRuleset):
    """
    Test our tests against a DummyRuleset.
    """
    def __init__(self):
        BaseDummyRuleset.__init__(self)
        ruleset = {
            (self._A_Any,        self._B[0],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('001'),
            (self._A_Any,        self._B[0],              self._C_OneOrTwo,        self._D[0],          self._E[0],          self._F[0])          : Marker('002'),
            (self._A_Any,        self._B_OneOrTwo,        self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('003'),
            (self._A_Any,        self._B[1],              self._C[1],              self._D[0],          self._E[0],          self._F[0])          : Marker('004'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E_Any,         self._F[1])          : Marker('005'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E[1],          self._F[0])          : Marker('006'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[1],          self._E_Any,         self._F_Any)         : Marker('007'),
            (self._A[0],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('008'),
            (self._A[0],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('009'),
            (self._A[0],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('010'),
            (self._A[0],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('011'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('012a'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('012b'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('012c'),
            (self._A[1],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('013'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('014a'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('014b'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('014c'),
            (self._A[1],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('015'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('016a'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('016b'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('016c'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E_Any,         self._F[1])          : Marker('017a'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E[1],          self._F[0])          : Marker('017b'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('017c'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('017d'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('017e'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('017f'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('017g'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('017h'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('017i'),
            (self._A[1],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('018a'),
            (self._A[1],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('018b'),
        }
        self.out = DummyMultiDictBackedRuleset(ruleset,
                                               self.combinatorial_dimensions,
                                              )


class TestDummyRuleset2(BaseDummyRuleset):
    """
    Test our tests against a DummyRuleset. This contains a bad ruleset, and the
    expected exceptions
    """
    def __init__(self):
        BaseDummyRuleset.__init__(self)
        ruleset = {
            (self._A_Any,        self._B[0],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('101'),
            (self._A_Any,        self._B[0],              self._C_OneOrTwo,        self._D[0],          self._E[0],          self._F[0])          : Marker('102'),
            (self._A_Any,        self._B_OneOrTwo,        self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('103'),
            (self._A_Any,        self._B[1],              self._C[1],              self._D[0],          self._E[0],          self._F[0])          : Marker('104'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E_Any,         self._F[1])          : Marker('105'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E[1],          self._F[0])          : Marker('106'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[1],          self._E_Any,         self._F_Any)         : Marker('107'),
            (self._A[0],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('108'),
            (self._A[0],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('109'),
            (self._A[0],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('110'),
            (self._A[0],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('111'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('112a'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('112b'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('112c'),
            (self._A[1],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('113'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('114a'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('114b'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('114c'),
            (self._A[1],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('115'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('116a'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('116b'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('116c'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E_Any,         self._F[1])          : Marker('117a'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E[1],          self._F[0])          : Marker('117b'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('117c'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('117d'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('117e'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('117f'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('117g'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('117h'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('117i'),
        #    This ruleset has overlap
        #   (self._A[1],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('118a Bad rule'),
            (self._A[1],         self._B_OneOrMore,       self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('118a Bad rule'),
            (self._A[1],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('118b'),
        }
        self.allowed_completeness_exception = "Duplicate reference keys found"
        self.allowed_collision_exception = ("These two keys are not mutually exclusive "
                                            "(11, frozenset([21, 22, 23]), frozenset([32, 33]), 40, 50, 60) "
                                            "(11, frozenset([22, 23]), frozenset([32, 33, 31]), 40, 50, 60)"
                                           )
        self.out = DummyMultiDictBackedRuleset(ruleset,
                                               self.combinatorial_dimensions,
                                              )


class TestDummyRuleset3(BaseDummyRuleset):
    """
    Test our tests against a DummyRuleset. This contains a bad ruleset, and the
    expected exceptions
    """
    def __init__(self):
        BaseDummyRuleset.__init__(self)
        ruleset = {
            (self._A_Any,        self._B[0],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('201'),
            (self._A_Any,        self._B[0],              self._C_OneOrTwo,        self._D[0],          self._E[0],          self._F[0])          : Marker('202'),
            (self._A_Any,        self._B_OneOrTwo,        self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('203'),
            (self._A_Any,        self._B[1],              self._C[1],              self._D[0],          self._E[0],          self._F[0])          : Marker('204'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E_Any,         self._F[1])          : Marker('205'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E[1],          self._F[0])          : Marker('206'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[1],          self._E_Any,         self._F_Any)         : Marker('207'),
            (self._A[0],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('208'),
            (self._A[0],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('209'),
            (self._A[0],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('210'),
            (self._A[0],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('211'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('212a'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('212b'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('212c'),
            (self._A[1],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('213'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('214a'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('214b'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('214c'),
            (self._A[1],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('215'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('216a'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('216b'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('216c'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E_Any,         self._F[1])          : Marker('217a'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E[1],          self._F[0])          : Marker('217b'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('217c'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('217d'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('217e'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('217f'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('217g'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('217h'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('217i'),
            (self._A[1],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('218a'),
        #    This ruleset has incomplete coverage
        #   (self._A[1],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('218b'),
            (self._A[1],         self._B[2],              self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('218b Bad rule'),
        }
        self.allowed_completeness_exception = "The reference keys do not cover the entire combinatorial space. 3 slots left over."
        self.allowed_collision_exception = None
        self.out = DummyMultiDictBackedRuleset(ruleset,
                                               self.combinatorial_dimensions,
                                              )


class TestDummyRuleset4(BaseDummyRuleset):
    """
    Test our tests against a DummyRuleset. This contains a ruleset that is
    broken in several ways, and the expected exceptions
    """
    def __init__(self):
        BaseDummyRuleset.__init__(self)
        ruleset = {
        #    This ruleset has incomplete coverage and duplicate coverage
            (self._A_Any,        self._B[0],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('301'),
            (self._A_Any,        self._B[0],              self._C_OneOrTwo,        self._D[0],          self._E[0],          self._F[0])          : Marker('302'),
            (self._A_Any,        self._B_OneOrTwo,        self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('303'),
            (self._A_Any,        self._B[1],              self._C[1],              self._D[0],          self._E[0],          self._F[0])          : Marker('304'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E_Any,         self._F[1])          : Marker('305'),
           #(self._A[0],         self._B_Any,             self._C_Any,             self._D[0],          self._E[1],          self._F[0])          : Marker('306'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D_Any,         self._E[1],          self._F[0])          : Marker('306 Collision'),
            (self._A[0],         self._B_Any,             self._C_Any,             self._D[1],          self._E_Any,         self._F_Any)         : Marker('307'),
            (self._A[0],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('308'),
            (self._A[0],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('309'),
            (self._A[0],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('310'),
            (self._A[0],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('311'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('312a'),
           #(self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('312b'),
            (self._A[1],         self._B_OneOrMore,       self._C_OneOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('312c'),
            (self._A[1],         self._B[3],              self._C[0],              self._D[0],          self._E[0],          self._F[0])          : Marker('313'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('314a'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('314b'),
            (self._A[1],         self._B_TwoOrMore,       self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('314c'),
            (self._A[1],         self._B[0],              self._C[3],              self._D[0],          self._E[0],          self._F[0])          : Marker('315'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E_Any,         self._F[1])          : Marker('316a'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[0],          self._E[1],          self._F[0])          : Marker('316b'),
            (self._A[1],         self._B[0],              self._C_TwoOrMore,       self._D[1],          self._E_Any,         self._F_Any)         : Marker('316c'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E_Any,         self._F[1])          : Marker('317a'),
            (self._A[1],         self._B[0],              self._C[1],              self._D[0],          self._E[1],          self._F[0])          : Marker('317b'),
           #(self._A[1],         self._B[0],              self._C[1],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('317c'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('317d'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('317e'),
            (self._A[1],         self._B[1],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('317f'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E_Any,         self._F[1])          : Marker('317g'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[0],          self._E[1],          self._F[0])          : Marker('317h'),
            (self._A[1],         self._B[0],              self._C[0],              self._D[1],          self._E_Any,         self._F_Any)         : Marker('317i'),
            (self._A[1],         self._B[1],              self._C_TwoOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('318a'),
            (self._A[1],         self._B_TwoOrMore,       self._C_OneOrMore,       self._D[0],          self._E[0],          self._F[0])          : Marker('318b'),
        }
        self.allowed_completeness_exception = "Duplicate reference keys found"
        self.allowed_collision_exception = ("These two keys are not mutually exclusive "
                                            "(10, frozenset([20, 21, 22, 23]), frozenset([32, 33, 30, 31]), frozenset([40, 41]), 51, 60) "
                                            "(10, frozenset([20, 21, 22, 23]), frozenset([32, 33, 30, 31]), 41, frozenset([50, 51]), frozenset([60, 61]))"
                                           )
        self.out = DummyMultiDictBackedRuleset(ruleset,
                                               self.combinatorial_dimensions,
                                              )


class DummyMultiDictBackedRuleset(object):
    """
    A standin for real MultiDictBackedRuleset objects.
    """
    def __init__(self,
                 reference_dict,
                 combinatorial_dimensions,
                ):
        self.ruleset = utility_classes.MultiDict(ruleset = reference_dict,
                                                  combinatorial_dimensions = combinatorial_dimensions,
                                                 )



















#
