"""
write_pickpack_tests.py

Script to automatically generate a test for each mock order in
pickpack_data_mock.
"""

# Nose should not run this when it is runing tests.
__test__ = False

import os.path
from CML_Pickpack.pickpack_modules.test import write_endpoint_tests

def main():
    """
    Main function
    """
    write_endpoint_tests.write_tests("Pickpack",
                                     os.path.basename(__file__),
                                     "packinglist",
                                    )

if __name__ == '__main__':
    main()
