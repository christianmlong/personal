"""
pickpack_constants.py

Constants for the Pick Pack server


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import os

_user_pass = ['UID=NONE', 'PWD=NONE']

# Add the isolation level. 2 = Read uncommitted (*CHG)
_isolation_level = 'CMT=2'
_user_pass_and_isolation = _user_pass[:]
_user_pass_and_isolation.append(_isolation_level)

_prod_dsn_name              = 'DSN=Prod'
_test_dsn_name              = 'DSN=Test'
_test_mt_dsn_name           = 'DSN=TestMT'

_prod_con_str_elements = [_prod_dsn_name]
_prod_con_str_elements.extend(_user_pass)
_test_con_str_elements = [_test_dsn_name]
_test_con_str_elements.extend(_user_pass)
_test_mt_con_str_elements = [_test_mt_dsn_name]
_test_mt_con_str_elements.extend(_user_pass)
_prod_con_str_elements_for_update = [_prod_dsn_name]
_prod_con_str_elements_for_update.extend(_user_pass_and_isolation)
_test_con_str_elements_for_update = [_test_dsn_name]
_test_con_str_elements_for_update.extend(_user_pass_and_isolation)
_test_mt_con_str_elements_for_update = [_test_mt_dsn_name]
_test_mt_con_str_elements_for_update.extend(_user_pass_and_isolation)

DEV_CON_STR                     = ""
PROD_CON_STR                    = ';'.join(_prod_con_str_elements)
TEST_CON_STR                    = ';'.join(_test_con_str_elements)
TEST_MT_CON_STR                 = ';'.join(_test_mt_con_str_elements)

DEV_CON_STR_FOR_UPDATE          = ""
PROD_CON_STR_FOR_UPDATE         = ';'.join(_prod_con_str_elements_for_update)
TEST_CON_STR_FOR_UPDATE         = ';'.join(_test_con_str_elements_for_update)
TEST_MT_CON_STR_FOR_UPDATE      = ';'.join(_test_mt_con_str_elements_for_update)

DEV_NAME = "Pick Pack Automation - DEV"
PROD_NAME = "Pick Pack Automation"
TEST_NAME = "Pick Pack Automation - TEST"
MANHOLE_NAME = "Pick Pack Automation - Diagnosic"
TEST_MT_NAME = "Pick Pack Automation - TEST MT"


DEV_PORT = 8082
PROD_PORT = 8081
TEST_PORT = 8083
MANHOLE_PORT = 8084
TEST_MT_PORT = 8085

DEV = 1001
PROD = 1002
TEST = 1004
MANHOLE = 1005
TEST_MT = 1006

MOCK_DATA = 1010
DATABASE_DATA = 1011

CONSUMABLES_SCALE = 1020
SERVICE_PARTS_SCALE = 1021
BOTH_SCALE = 1022
ALL_SCALES = 1023
#SPECIAL_TEAM = 1024
FOUR_UP = 1025

TODAY_SURE = 1030
SIGNATURE_SERVICE = 1031
SERVICE_FILE = 1032
NORMAL = 1033

SHOW_UNTIL_PACKING_BENCH = 1040
SHOW_UNTIL_SCALE = 1041


TEST_CUSTOM_LIBRARY = "wgta83fmn"            # New Test
PROD_CUSTOM_LIBRARY = "wgta83f"
TEST_MT_CUSTOM_LIBRARY = "wgta83fmt"         # Old Test

TEST_PROCEDURE_LIBRARY = "aplus83mmn"        # New Test
PROD_PROCEDURE_LIBRARY = "aplus83mme"
TEST_MT_PROCEDURE_LIBRARY = "aplus83mmt"     # Old Test


SERVER_DICT = { DEV :       (DEV_NAME,
                             DEV_PORT,
                             DEV_CON_STR,
                             DEV_CON_STR_FOR_UPDATE,
                             MOCK_DATA,
                             None,
                             None,
                            ),

                PROD :      (PROD_NAME,
                             PROD_PORT,
                             PROD_CON_STR,
                             PROD_CON_STR_FOR_UPDATE,
                             DATABASE_DATA,
                             PROD_CUSTOM_LIBRARY,
                             PROD_PROCEDURE_LIBRARY,
                            ),

                TEST :      (TEST_NAME,
                             TEST_PORT,
                             TEST_CON_STR,
                             TEST_CON_STR_FOR_UPDATE,
                             DATABASE_DATA,
                             TEST_CUSTOM_LIBRARY,
                             TEST_PROCEDURE_LIBRARY,
                            ),

                MANHOLE :   (MANHOLE_NAME,
                             MANHOLE_PORT,
                             DEV_CON_STR,
                             DEV_CON_STR_FOR_UPDATE,
                             MOCK_DATA,
                             None,
                             None,
                            ),

                TEST_MT :   (TEST_MT_NAME,
                             TEST_MT_PORT,
                             TEST_MT_CON_STR,
                             TEST_MT_CON_STR_FOR_UPDATE,
                             DATABASE_DATA,
                             TEST_MT_CUSTOM_LIBRARY,
                             TEST_MT_PROCEDURE_LIBRARY,
                            ),
              }

DB_FALSE = 0
DB_TRUE = 1

NO_DATA_FOUND = "NO_DATA_FOUND"

#DATA_TABLE_ID = "table_1"

STATIC_PATH = os.path.join(".", "static")
APP_ROOT_PATH = os.path.join(STATIC_PATH, "html", "app_root.html")
IMG_URL_PATH = "/static/img"
IMG_EXT = ".png"

# Truncate the list of order numbers to this max lenth
MAX_ORDER_NUMBERS = 60


# These are the APlus ship codes
AIR_SHIPPERS = ('UPSS',     # UPS SATURDAY DELIVERY
                'UPS1',     # UPS-NEXT DAY PRIORITY 1
                'UPS2',     # UPS-2ND DAY AIR
                'UPS3',     # UPS-3RD DAY
                'UPM',      # UPS/SECOND DAY AIR A.M.
                'UPSP',     # UPS/NEXT DAY AIR SAVER
                'UPSW',     # UPS WORLD WIDE EXPRESS
                'UPSL',     # UPS INTERNATIONAL
                'UPSA',     # UPS NEXT DAY AIR EARLY A.M.
                'UPT',      # UPS EXPRESS CRITICAL
                'UPWS',     # UPS WORLDWIDE SAVER
               )
GROUND_SHIPPERS = ('UPSG',                 #  ups ground
                  )
OTHER_SHIPPERS_TREAT_AS_AIR = ()
OTHER_SHIPPERS_TREAT_AS_GROUND = ()
#OTHER_SHIPPERS_DO_NOTHING = ()
OTHER_SHIPPERS = (OTHER_SHIPPERS_TREAT_AS_AIR
                  + OTHER_SHIPPERS_TREAT_AS_GROUND
                  #+ OTHER_SHIPPERS_DO_NOTHING
                 )
ALL_SHIPPERS = (AIR_SHIPPERS
                + GROUND_SHIPPERS
                + OTHER_SHIPPERS
               )

# These are the service level codes
TODAY_SURE_CODE = 'T'
SIGNATURE_SERVICE_CODE = 'SS'
SERVICE_FILE_CODE = 'S'
NORMAL_CODE = 'N'

# APlus has these country codes
UNITED_STATES_COUNTRY_CODE = '100'
CANADA_COUNTRY_CODE = '122'

# Certain customers get special treatment
HARPER_CUSTOMER_NUMBER = 34142
WCW_MEXICO_CUSTOMER_NUMBER = 17702

# Tell nose to show the full diff when testing
#SHOW_FULL_DIFF = True
SHOW_FULL_DIFF = False

# Add delay to mock data, for testing.
ENABLE_DELAY = False
#ENABLE_DELAY = True
DELAY_SECONDS = 5

# Turn cacheing on or off, for testing
# TO DO DEBUG ONLY
#ENABLE_CACHE = False
ENABLE_CACHE = True
