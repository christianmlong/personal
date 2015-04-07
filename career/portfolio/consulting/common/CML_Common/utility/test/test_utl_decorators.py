"""

test_utl_decorators.py

This module provides tests for utl_decorators.py


Christian M. Long, developer

Initial implementation: September 24, 2007
Initial language: Python 2.5.1
Current language: Python 2.5.1  www.python.org
"""
# pylint: disable=C0103,C0111,E1101,E1101,R0904

import unittest
import doctest

# Import module to test
from CML_Common.utility import utl_decorators

# Build a unittest suite from doctest tests
doctest_suite = unittest.TestSuite()
doctest_suite.addTest(doctest.DocTestSuite(utl_decorators))

class UnitTestThisModule(unittest.TestCase):
    def test_add_constants_to_class(self):


        class Base(object):
            pass

        @utl_decorators.add_constants_to_class({'Image' : {'I1' : 'doc1',
                                                           'I2' : 'doc2',
                                                           'I3' : 'doc3',
                                                           'I4' : 'doc4',
                                                           'I5' : 'doc5',
                                                           'I6' : 'doc6',
                                                          },
                                               },
                                              )
        class A(Base):
            pass

        self.assertEqual(A.Constants.Image.__dict__,
                         {'I1': 'doc1',
                          'I2': 'doc2',
                          'I3': 'doc3',
                          'I4': 'doc4',
                          'I5': 'doc5',
                          'I6': 'doc6',
                          'name': "Container 'Image'",
                         },
                        )


        @utl_decorators.add_constants_to_class({'Image' : {'One' : 'A',
                                                           'Two' : 'B',
                                                          },
                                               },
                                              )
        class B(A):
            pass

        self.assertEqual(B.Constants.Image.__dict__,
                         {'I1': 'doc1',
                          'I2': 'doc2',
                          'I3': 'doc3',
                          'I4': 'doc4',
                          'I5': 'doc5',
                          'I6': 'doc6',
                          'One': 'A',
                          'Two': 'B',
                          'name': "Container 'Image'",
                         },
                        )
        self.assertEqual(B.Constants.Image.One, 'A')
        self.assertEqual(B.Constants.Image.Two, 'B')


        @utl_decorators.add_constants_to_class({'Image' : {'One' : 'C',
                                                           'Two' : 'D',
                                                          },
                                               },
                                              )
        class C(A):
            pass

        self.assertEqual(C.Constants.Image.__dict__,
                         {'I1': 'doc1',
                          'I2': 'doc2',
                          'I3': 'doc3',
                          'I4': 'doc4',
                          'I5': 'doc5',
                          'I6': 'doc6',
                          'One': 'C',
                          'Two': 'D',
                          'name': "Container 'Image'",
                         },
                        )
        self.assertEqual(C.Constants.Image.One, 'C')
        self.assertEqual(C.Constants.Image.Two, 'D')

        class D(A):
            pass

        self.assertEqual(D.Constants.Image.__dict__,
                         {'I1': 'doc1',
                          'I2': 'doc2',
                          'I3': 'doc3',
                          'I4': 'doc4',
                          'I5': 'doc5',
                          'I6': 'doc6',
                          'name': "Container 'Image'",
                         },
                        )
        with self.assertRaises(AttributeError):
            print D.Constants.Image.One
        with self.assertRaises(AttributeError):
            print D.Constants.Image.Two



        class E(Base):
            pass

        with self.assertRaises(AttributeError):
            print E.Constants
        with self.assertRaises(AttributeError):
            print Base.Constants



if __name__ == '__main__':
    unittest.main()
