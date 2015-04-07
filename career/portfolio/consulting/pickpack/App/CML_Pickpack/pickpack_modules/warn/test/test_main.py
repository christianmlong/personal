"""
Tests for the functions in the warn.main.py module
"""
# pylint: disable=too-many-public-methods

from CML_Pickpack.pickpack_modules.test.utility_classes_for_testing import BaseMainTester

class TestCalculateBatteryWarnings(BaseMainTester):
    def __init__(self):
        BaseMainTester.__init__(self)

    def test1(self):
        order_info = {'carrier_code' : 'UPS2',
                      'customer_number' : 10210,
                      #'order_entry_initials' : 'ZZZ',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                      (3, '648484023498', '164421', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                      (4, '648484111669', '164422', 0, 1.0, 'EA', 1, 0, 0, None, '2', 0),
                      (5, '648484028745', '164485', 0, 1.0, '10PK', 10, 0, 0, None, '2', 0),
                      (6, '648484220033', '187441', 0, 1.0, 'EA', 1, 0, 0, None, '2', 0),
                      (7, '648484209892', '187442', 0, 1.0, 'EA', 1, 0, 0, None, '2', 0),
                      (8, '648484209908', '187443', 0, 1.0, 'EA', 1, 0, 0, 'CT0', '2', 0),
                      (12, '648484330244', '213858', 0, 1.0, 'EA', 1, 0, 0, 'CB0', '2', 0),
                      (9, '648484316972', '216322', 0, 4.0, 'EA', 1, 0, 0, 'SB0', '2', 0),
                      (10, '648484338141', '222003', 0, 12.0, 'EA', 1, 0, 0, 'PA0', '2', 0),
                      (11, '648484030595', '604612', 0, 1.0, '4PK', 4, 0, 0, None, '2', 0),
                     ]
        expected_warnings = [
            [('Label each TRPR box with Ion label',
              'Mark "Ion, With Equipment" on document',
             ),
             ('ion1', 'battery_doc2'),
            ],
            [('Max 2 SmartBands/SmartBelts per box',
              'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
              '------------------',
              'Package Ion batteries in a separate box, max 2 per box',
              'Mark "Ion, Batteries Only" on the document for the battery box',
             ),
             ('ion2', 'battery_doc7'),
            ],
        ]
        expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0]
        expected_warning_categories = frozenset(['PA0', 'CB0', 'CT0', 'SB0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                 )

    def test2(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 10210,
                      #'order_entry_initials' : 'ZZZ',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'PA0', '2', 0),
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                     ]
        expected_warnings =  [
            ['Label each TRPR box with Ion label', 'ion1'],
        ]
        expected_inline_images = [2, 0]
        expected_warning_categories = frozenset(['PA0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                 )

    def test3(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 10210,
                      #'order_entry_initials' : 'ZZZ',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'PA0', '2', 0),
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                     ]
        expected_warnings =  [
            ['Label each TRPR box with Ion label', 'ion1'],
        ]
        expected_inline_images = [2, 0]
        expected_warning_categories = frozenset(['PA0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                 )

    def test4(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 10210,
                      #'order_entry_initials' : 'ZZZ',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'SB0', '2', 0),
                     ]
        expected_warnings = [['Pack TRPR batteries with other items, max 20 per box', 'ion2']]
        expected_inline_images = [2]
        expected_warning_categories = frozenset(['SB0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                 )

    def test5(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 10210,
                      #'order_entry_initials' : 'ZZZ',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'CB0', '2', 0),
                     ]
        expected_warnings = [
            ['SmartBands/SmartBelts get Ion label', 'ion1'],
        ]
        expected_inline_images = [2]
        expected_warning_categories = frozenset(['CB0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                 )

    def test6(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 10210,
                      #'order_entry_initials' : 'ZZZ',
                     }

        # Bad category
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'CB7', '2', 0),
                     ]
        expected_exception_msg =  "Error: Unknown category CB7."

        self.try_it_exception(order_info,
                              items,
                              expected_exception_msg,
                             )


class TestCalculateSpecialWarnings(BaseMainTester):
    def __init__(self):
        BaseMainTester.__init__(self)

    def test1(self):
        order_info = {'carrier_code' : 'UPS2',
                      'customer_number' : 40598,
                      #'order_entry_initials' : 'EDC',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                      (3, '648484023498', '164421', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                      (4, '648484111669', '164422', 0, 1.0, 'EA', 1, 0, 0, None, '2', 0),
                      (5, '648484028745', '164485', 0, 1.0, '10PK', 10, 0, 0, None, '2', 0),
                      (6, '648484220033', '187441', 0, 1.0, 'EA', 1, 0, 0, None, '2', 0),
                      (7, '648484209892', '187442', 0, 1.0, 'EA', 1, 0, 0, None, '2', 0),
                      (8, '648484209908', '187443', 0, 1.0, 'EA', 1, 0, 0, 'CT0', '2', 0),
                      (12, '648484330244', '213858', 0, 1.0, 'EA', 1, 0, 0, 'CB0', '2', 0),
                      (9, '648484316972', '216322', 0, 4.0, 'EA', 1, 0, 0, 'SB0', '2', 0),
                      (10, '648484338141', '222003', 0, 12.0, 'EA', 1, 0, 0, 'PA0', '2', 0),
                      (11, '648484030595', '604612', 0, 1.0, '4PK', 4, 0, 0, None, '2', 0),
                     ]
        expected_warnings = [
            [('Label each TRPR box with Ion label',
              'Mark "Ion, With Equipment" on document',
             ),
             ('ion1', 'battery_doc2'),
            ],
            [('Max 2 SmartBands/SmartBelts per box',
              'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
              '------------------',
              'Package Ion batteries in a separate box, max 2 per box',
              'Mark "Ion, Batteries Only" on the document for the battery box',
             ),
             ('ion2', 'battery_doc7'),
            ],
        ]
        expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0]
        expected_warning_categories = frozenset(['PA0', 'CB0', 'CT0', 'SB0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                  #add_seasonal_warning = True,
                   )

    def test2(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 40598,
                      #'order_entry_initials' : 'EDC',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'PA0', '2', 0),
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                     ]
        expected_warnings =  [
            ['Label each TRPR box with Ion label', 'ion1'],
        ]
        expected_inline_images = [2, 0]
        expected_warning_categories = frozenset(['PA0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                  #add_seasonal_warning = True,
                                 )

    def test3(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 40598,
                      #'order_entry_initials' : '',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'PA0', '2', 0),
                      (2, '648484140133', '136748', 0, 1.0, '2PK', 2, 0, 0, None, '2', 0),
                     ]
        expected_warnings =  [
            ['Label each TRPR box with Ion label', 'ion1'],
        ]
        expected_inline_images = [2, 0]
        expected_warning_categories = frozenset(['PA0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                  #add_seasonal_warning = True,
                                 )

    def test4(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 40598,
                      #'order_entry_initials' : 'EDD',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'SB0', '2', 0),
                     ]
        expected_warnings = [
            ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
        ]
        expected_inline_images = [2]
        expected_warning_categories = frozenset(['SB0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                  #add_seasonal_warning = True,
                                 )


    def test5(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 40598,
                      #'order_entry_initials' : 'EDC',
                     }
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'CB0', '2', 0),
                     ]
        expected_warnings = [
            ['SmartBands/SmartBelts get Ion label', 'ion1'],
        ]
        expected_inline_images = [2]
        expected_warning_categories = frozenset(['CB0'])
        self.try_it_list_of_items(order_info,
                                  items,
                                  expected_warnings,
                                  expected_inline_images,
                                  expected_warning_categories,
                                  #add_seasonal_warning = True,
                                 )


    def test6(self):
        order_info = {'carrier_code' : 'UPSG',
                      'customer_number' : 40598,
                      #'order_entry_initials' : 'EDC',
                     }

        # Bad category
        items      = [(1, '648484149532', '058685', 0, 1.0, '2PK', 2, 0, 0, 'CB7', '2', 0),
                     ]
        expected_exception_msg =  "Error: Unknown category CB7."

        self.try_it_exception(order_info,
                              items,
                              expected_exception_msg,
                             )


class TestCalculateBatteryWarningsFromPickpackDataMock(BaseMainTester):
    def __init__(self):
        BaseMainTester.__init__(self)

    def testAA02800(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA02800',
            expected_warnings = [
                [('Pack coin batteries in a separate box',
                  'Mark "Metal, Batteries Only" on document',
                 ),
                 ('metal2', 'battery_doc4'),
                ],
                [('Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ],
                [('Label each TRPR box with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ],
                [('Max 2 SmartBands/SmartBelts per box',
                  'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                  '------------------',
                  'Package Ion batteries in a separate box, max 2 per box',
                  'Mark "Ion, Batteries Only" on the document for the battery box',
                 ),
                 ('ion2', 'battery_doc7'),
                ]
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            expected_warning_categories = frozenset(['PA0', 'PA1', 'SB0', 'SB1', 'CT0', 'BT0', 'KT0', 'SB2', 'CB0']),
        )

    def testAA02900(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA02900',
            expected_warnings = [
                ['Pack coin batteries with other items', 'metal2'],
                ['Label each Helmet + SmartBand/SmartBelt kit with Ion label', 'ion1'],
                ['Label each TRPR box with Ion label', 'ion1'],
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            expected_warning_categories = frozenset(['PA0', 'PA1', 'SB0', 'SB1', 'CT0', 'BT0', 'KT0', 'SB2', 'CB0']),
        )

    def testAA20000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20000',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA00100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA00100',
            no_warning = True,
        )

    def testAA00100lowercase(self):
        self.try_it_order_id_scan(
            order_id_scan = 'aa00100',
            no_warning = True,
        )

    def testAA20100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20100',
            no_warning = True,
        )

    def testAA20200(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20200',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1'],
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0,
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0,
                                     ],
            expected_warning_categories = frozenset(['PA0', 'CB0']),
        )

    def testAA20300(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20300',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
                #['This order has 24 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 2],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA20300lowercase(self):
        self.try_it_order_id_scan(
            order_id_scan = 'aa20300',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
                #['This order has 24 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 2],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA20400(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20400',
            no_warning = True,
        )

    def testAA20500(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20500',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA20600(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20600',
            expected_warnings = [
                ['Pack coin batteries with other items',
                 'metal2',
                ],
                #['This order has 3 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [0, 0, 0, 1, 0, 0, 0, 0, 0],
            expected_warning_categories = frozenset(['BT0']),
        )

    def testAA20700(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20700',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1']
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 2],
            expected_warning_categories = frozenset(['PA0']),
        )

    def testAA20800(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20800',
            no_warning = True,
        )

    def testAA20900(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA20900',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 2],
            expected_warning_categories = frozenset(['PA1']),
        )

    def testAA21000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21000',
            expected_warnings = [
                #['This order has 9 helmets. The helmets must go Ground', 'helmet'],
            ],
        )

    def testAA21100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21100',
            expected_warnings = [
                [('Max 2 SmartBands/SmartBelts per box',
                  'SmartBands/SmartBelts get Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion2', 'battery_doc2'),
                ],
                ['This order has 3 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [2, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA21200(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21200',
            expected_warnings = [
                ['Pack SmartBand batteries with other items, max 75 per box', 'ion2'],
            ],
            expected_inline_images = [0, 2, 0],
            expected_warning_categories = frozenset(['SB1']),
        )

    def testAA21300(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21300',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 2, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA21400(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21400',
            no_warning = True,
        )

    def testAA21500(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21500',
            expected_warnings = [
                ['Pack coin batteries with other items', 'metal2'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            expected_warning_categories = frozenset(['BT0']),
        )

    def testAA21600(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21600',
            no_warning = True,
        )

    def testAA21700(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21700',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1'],
                #['This order has 13 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            expected_warning_categories = frozenset(['PA0']),
        )

    def testAA21800(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21800',
            no_warning = True,
        )

    def testAA21900(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA21900',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA22000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA22000',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA22100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA22100',
            expected_warnings = [
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
            ],
            expected_inline_images = [0, 0, 0, 0, 2, 0],
            expected_warning_categories = frozenset(['SB0']),
        )

    def testAA22200(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA22200',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [0, 0, 0, 0, 2, 0],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA22300(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA22300',
            expected_warnings = [
                [('SmartBands/SmartBelts get Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ]
            ],
            expected_inline_images = [0, 0, 0, 0, 2],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA22400(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA22400',
            expected_warnings = [
                [('SmartBands/SmartBelts get Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ]
            ],
            expected_inline_images = [2],
            expected_warning_categories = frozenset(['CB0']),
        )

    def testAA22500(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA22500',
            expected_warnings = [
                [('SmartBands/SmartBelts get Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ]
            ],
            expected_inline_images = [0, 0, 0, 0, 2],
            expected_warning_categories = frozenset(['CB0']),
        )

    # For now, no Thorium warnings or inline images.
    def testAA13500(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA13500',
            expected_warnings = [
                ['Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                 'ion1',
                ],
                ['Label shipping carton with UN 2909 label',
                 'un_2909',
                ],
            ],
            expected_inline_images = [2, 0, 0, 0, 0, 0, 0, 4],
            expected_warning_categories = frozenset(['TH3', 'KT0']),
        )

    def testAA13600(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA13600',
            expected_warnings = [
                ['Pack TRPR batteries with other items, max 20 per box',
                 'ion2',
                ],
                ['Label shipping carton with UN 2909 label',
                 'un_2909',
                ],
            ],
            expected_inline_images = [2, 0, 0, 0, 0, 4],
            expected_warning_categories = frozenset(['SB0', 'TH5']),
        )

    def testAA13700(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA13700',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label',
                 'ion1',
                ],
                ['Label shipping carton with UN 2909 label',
                 'un_2909',
                ],
            ],
            expected_inline_images = [0, 0, 2, 0, 0, 4, 4],
            expected_warning_categories = frozenset(['CB0', 'TH4', 'TH3']),
        )

    def testAA13800(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA13800',
            expected_warnings = [
                [('Pack coin batteries in a separate box',
                  'Mark "Metal, Batteries Only" on document',
                 ),
                 ('metal2',
                  'battery_doc4',
                 ),
                ],
                [('Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1',
                  'battery_doc2',
                 ),
                ],
                [('Label each TRPR box with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1',
                  'battery_doc2',
                 ),
                ],
                [('Max 2 SmartBands/SmartBelts per box',
                  'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                  '------------------',
                  'Package Ion batteries in a separate box, max 2 per box',
                  'Mark "Ion, Batteries Only" on the document for the battery box',
                 ),
                 ('ion2',
                  'battery_doc7',
                 ),
                ],
                [('Ship in multiple packages',
                  'Max 20 packs of rods per package',
                  'Wrap thoriated rods in a small box inside each shipping carton',
                  'Label shipping cartons with UN 2909 label'
                 ),
                 ('un_2909',
                  'boxes',
                 ),
                ],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4,
                                   ],
            expected_warning_categories = frozenset(['PA0' ,
                                                     'PA1' ,
                                                     'SB0' ,
                                                     'SB1' ,
                                                     'CT0' ,
                                                     'BT0' ,
                                                     'TH3' ,
                                                     'TH5' ,
                                                     'TH4' ,
                                                     'KT0' ,
                                                     'TH2' ,
                                                     'SB2' ,
                                                     'CB0' ,
                                                    ]
                                                   ),
        )

    def testAA13900(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA13900',
            expected_warnings = [
                ['Pack coin batteries with other items', 'metal2'],
                ['Label each Helmet + SmartBand/SmartBelt kit with Ion label', 'ion1'],
                ['Label each TRPR box with Ion label', 'ion1'],
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
                [('Ship in multiple packages',
                  'Max 20 packs of rods per package',
                  'Wrap thoriated rods in a small box inside each shipping carton',
                  'Label shipping cartons with UN 2909 label',
                 ),
                 ('un_2909',
                  'boxes',
                 ),
                ],
                [('Label ORM-D. Make sure the box rating is visible',
                  'Must ship by Ground',
                 ),
                 ('ormd',
                  'box_rating',
                 ),
                ],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 5, 5,
                                   ],
            expected_warning_categories = frozenset(['PA0' ,
                                                     'PA1' ,
                                                     'SB0' ,
                                                     'SB1' ,
                                                     'CT0' ,
                                                     'BT0' ,
                                                     'TH3' ,
                                                     'TH5' ,
                                                     'TH4' ,
                                                     'KT0' ,
                                                     'TH2' ,
                                                     'SB2' ,
                                                     'CB0' ,
                                                     'HZ0' ,
                                                    ]
                                                   ),
        )

    def testAA14000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA14000',
            expected_warnings = [
                [('Pack coin batteries in a separate box',
                  'Mark "Metal, Batteries Only" on document',
                 ),
                 ('metal2',
                  'battery_doc4',
                 ),
                ],
                [('Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1',
                  'battery_doc2',
                 ),
                ],
                [('Label each TRPR box with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1',
                  'battery_doc2',
                 ),
                ],
                [('Max 2 SmartBands/SmartBelts per box',
                  'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                  '------------------',
                  'Package Ion batteries in a separate box, max 2 per box',
                  'Mark "Ion, Batteries Only" on the document for the battery box',
                 ),
                 ('ion2',
                  'battery_doc7',
                 ),
                ],
                [('Ship in multiple packages',
                  'Max 20 packs of rods per package',
                  'Wrap thoriated rods in a small box inside each shipping carton',
                  'Label shipping cartons with UN 2909 label',
                 ),
                 ('un_2909',
                  'boxes',
                 ),
                ],
                [('STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.',
                  'Label ORM-D. Make sure the box rating is visible',
                 ),
                 'red_x',
                ],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 5, 5,
                                   ],
            expected_warning_categories = frozenset(['PA0',
                                                     'PA1',
                                                     'SB0',
                                                     'SB1',
                                                     'CT0',
                                                     'BT0',
                                                     'TH3',
                                                     'TH5',
                                                     'TH4',
                                                     'KT0',
                                                     'TH2',
                                                     'SB2',
                                                     'CB0',
                                                     'HZ0',
                                                    ]
                                                   ),
        )

    def testAA14100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA14100',
            expected_warnings = [
                [('STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.',
                  'Label ORM-D. Make sure the box rating is visible',
                 ),
                 'red_x',
                ],
            ],
            expected_inline_images = [5, 5],
            expected_warning_categories = frozenset(['HZ0']),
        )

    def testAA40100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40100',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA40200(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40200',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1'],
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
                #['This order has 4 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0],
            expected_warning_categories = frozenset(['PA0', 'CB0', 'CT0', 'SB0']),
            #add_seasonal_warning = True,
        )

    def testAA40300(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40300',
            expected_warnings = [
                [('Label each TRPR box with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ],
                [('Max 2 SmartBands/SmartBelts per box',
                  'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                  '------------------',
                  'Package Ion batteries in a separate box, max 2 per box',
                  'Mark "Ion, Batteries Only" on the document for the battery box',
                 ),
                 ('ion2', 'battery_doc7'),
                ],
                ['This order has 4 helmets. The helmets must go Ground', 'helmet'],
            ],
            expected_inline_images = [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0],
            expected_warning_categories = frozenset(['PA0', 'CB0', 'CT0', 'SB0']),
            #add_seasonal_warning = True,
        )

    def testAA40400(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40400',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1'],
            ],
            expected_inline_images = [2, 0],
            expected_warning_categories = frozenset(['PA0']),
            #add_seasonal_warning = True,
        )

    def testAA40500(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40500',
            expected_warnings = [
                ['Label each TRPR box with Ion label', 'ion1'],
            ],
            expected_inline_images = [2, 0],
            expected_warning_categories = frozenset(['PA0']),
            #add_seasonal_warning = True,
        )

    def testAA40600(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40600',
            expected_warnings = [
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
            ],
            expected_inline_images = [2],
            expected_warning_categories = frozenset(['SB0']),
            #add_seasonal_warning = True,
        )

    def testAA40700(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40700',
            expected_warnings = [
                ['SmartBands/SmartBelts get Ion label', 'ion1'],
            ],
            expected_inline_images = [2],
            expected_warning_categories = frozenset(['CB0']),
            #add_seasonal_warning = True,
        )

    def testAA40800(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40800',
            expected_warnings = [
                [('Pack coin batteries in a separate box',
                  'Mark "Metal, Batteries Only" on document',
                 ),
                 ('metal2', 'battery_doc4'),
                ],
                [('Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ],
                [('Label each TRPR box with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1', 'battery_doc2'),
                ],
                [('Max 2 SmartBands/SmartBelts per box',
                  'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                  '------------------',
                  'Package Ion batteries in a separate box, max 2 per box',
                  'Mark "Ion, Batteries Only" on the document for the battery box',
                 ),
                 ('ion2', 'battery_doc7'),
                ],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            expected_warning_categories = frozenset(['PA0', 'PA1', 'SB0', 'SB1', 'CT0', 'BT0', 'KT0', 'SB2', 'CB0']),
            #add_seasonal_warning = True,
        )

    def testAA40900(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA40900',
            expected_warnings = [
                ['Pack coin batteries with other items', 'metal2'],
                ['Label each Helmet + SmartBand/SmartBelt kit with Ion label', 'ion1'],
                ['Label each TRPR box with Ion label', 'ion1'],
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            expected_warning_categories = frozenset(['PA0', 'PA1', 'SB0', 'SB1', 'CT0', 'BT0', 'KT0', 'SB2', 'CB0']),
            #add_seasonal_warning = True,
        )

    def testAA41000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA41000',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA41100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA41100',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA41200(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA41200',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA41300(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA41300',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA41400(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA41400',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA42000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA42000',
            expected_warnings = [
                ['Pack SmartBand batteries with other items, max 75 per box', 'ion2'],
            ],
            expected_inline_images = [0, 2, 0],
            expected_warning_categories = frozenset(['SB1']),
            #add_seasonal_warning = True,
        )

    def testAA42100(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA42100',
            expected_warnings = [
                ['Pack coin batteries with other items', 'metal2'],
                ['Label each Helmet + SmartBand/SmartBelt kit with Ion label', 'ion1'],
                ['Label each TRPR box with Ion label', 'ion1'],
                ['Pack TRPR batteries with other items, max 20 per box', 'ion2'],
                [('Ship in multiple packages',
                  'Max 20 packs of rods per package',
                  'Wrap thoriated rods in a small box inside each shipping carton',
                  'Label shipping cartons with UN 2909 label',
                 ),
                 ('un_2909',
                  'boxes',
                 ),
                ],
                [('Label ORM-D. Make sure the box rating is visible',
                  'Must ship by Ground',
                 ),
                 ('ormd',
                  'box_rating',
                 ),
                ],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 5, 5,
                                   ],
            expected_warning_categories = frozenset(['PA0',
                                                     'PA1',
                                                     'SB0',
                                                     'SB1',
                                                     'CT0',
                                                     'BT0',
                                                     'KT0',
                                                     'TH5',
                                                     'TH4',
                                                     'TH3',
                                                     'TH2',
                                                     'SB2',
                                                     'CB0',
                                                     'HZ0',
                                                     ]
                                                    ),
            #add_seasonal_warning = True,
        )

    def testAA42200(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA42200',
            expected_warnings = [
                [('Pack coin batteries in a separate box',
                  'Mark "Metal, Batteries Only" on document',
                 ),
                 ('metal2',
                  'battery_doc4',
                 ),
                ],
                [('Label each Helmet + SmartBand/SmartBelt kit with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1',
                  'battery_doc2',
                 ),
                ],
                [('Label each TRPR box with Ion label',
                  'Mark "Ion, With Equipment" on document',
                 ),
                 ('ion1',
                  'battery_doc2',
                 ),
                ],
                [('Max 2 SmartBands/SmartBelts per box',
                  'Mark "Ion, With Equipment" on the document for the SmartBand/SmartBelt box',
                  '------------------',
                  'Package Ion batteries in a separate box, max 2 per box',
                  'Mark "Ion, Batteries Only" on the document for the battery box',
                 ),
                 ('ion2',
                  'battery_doc7',
                 ),
                ],
                [('Ship in multiple packages',
                  'Max 20 packs of rods per package',
                  'Wrap thoriated rods in a small box inside each shipping carton',
                  'Label shipping cartons with UN 2909 label',
                 ),
                 ('un_2909',
                  'boxes',
                 ),
                ],
                [('STOP. DO NOT SHIP BY AIR. ORM-D must ship by Ground.',
                  'Label ORM-D. Make sure the box rating is visible',
                 ),
                 'red_x',
                ],
            ],
            expected_inline_images = [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                    4, 4, 4, 4, 4, 5, 5,
                                   ],
            expected_warning_categories = frozenset(['PA0',
                                                     'PA1',
                                                     'SB0',
                                                     'SB1',
                                                     'CT0',
                                                     'BT0',
                                                     'KT0',
                                                     'TH5',
                                                     'TH4',
                                                     'TH3',
                                                     'TH2',
                                                     'SB2',
                                                     'CB0',
                                                     'HZ0',
                                                     ]
                                                    ),
            #add_seasonal_warning = True,
        )

    def testAA71000(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA71000',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )

    def testAA71001(self):
        self.try_it_order_id_scan(
            order_id_scan = 'AA71001',
            expected_warnings = [
            ],
            expected_inline_images = None,
            #add_seasonal_warning = True,
        )






















#



# Debugging breakpoints, in Komodo and in iPython
#
#
#
# Set remote breakpoint in Komodo. Komodo must be running on 1bk2zq1-190.
# Debugging listener must be listening on port 8201. See debug.py for
# configuration of remote debugging.
#
## DE BUG
#from CML_Common.error.debug import debug_utility_object as debugObj
#debugObj.debugBreakpoint()
#
#
#
#
# Set local breakpoint in iPython.
#
## DE BUG
#from CML_Common.error.debug import debug_utility_object as debugObj
#debugObj.debugIpythonBreakpoint()
#
#
#
#
#
# Set local breakpoint in pudb.
#
## DE BUG
#from CML_Common.error.debug import debug_utility_object as debugObj
#debugObj.debugPudbBreakpoint()
