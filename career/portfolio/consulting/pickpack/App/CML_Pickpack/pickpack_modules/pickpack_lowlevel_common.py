"""
pickpack_lowlevel_common.py

Common, shared functions for the Pick Pack server


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""
from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_errors

def isValidCarrierCode(carrier_code):
    """
    Returns True if the carrier code is recognized
    """
    if (isGroundCarrierCode(carrier_code)
        or isAirCarrierCode(carrier_code)
       ):
        return True
    else:
        return False

def isGroundCarrierCode(carrier_code):
    """
    Returns True if it is a Ground carrier code
    """
    return not isAirCarrierCode(carrier_code)
    #if carrier_code in pickpack_constants.GROUND_SHIPPERS:
    #    return True
    #elif carrier_code in pickpack_constants.OTHER_SHIPPERS_TREAT_AS_GROUND:
    #    return True
    #else:
    #    return False

def isAirCarrierCode(carrier_code):
    """
    Returns True if it is an air carrier code
    """
    if carrier_code in pickpack_constants.AIR_SHIPPERS:
        return True
    elif carrier_code in pickpack_constants.OTHER_SHIPPERS_TREAT_AS_AIR:
        return True
    else:
        return False

def isDowngradeToGroundAllowed(carrier_code,
                               service_level,
                               ship_to_state,
                               ship_to_country,
                              ):
    """
    Returns True if all or part of this order is allowed to be downgraded to
    Ground.
    """
    if (
        # Only Signature Service and Normal orders can be downgraded
        service_level in (pickpack_constants.SIGNATURE_SERVICE_CODE,
                          pickpack_constants.NORMAL_CODE,
                         )

        # Can't downgrade if it's already Ground
        and not isGroundCarrierCode(carrier_code)

        # Only shipments to the US can be downgraded
        and isUnitedStates(ship_to_country)

        # Alaska, Hawaii and Puerto Rico can not be downgraded
        and ship_to_state not in ('AK',
                                  'HI',
                                  'PR',
                                 )
    ):
        downgrade_is_allowed = True
    else:
        downgrade_is_allowed = False

    return downgrade_is_allowed

def isUnitedStates(ship_to_country):
    """
    Returns True if the ship_to_country is the code for the USA, or if it is
    blank.
    """
    if ship_to_country is None:
        raise pickpack_errors.ApplicationError("Error: Ship-to country is None")

    return (ship_to_country == pickpack_constants.UNITED_STATES_COUNTRY_CODE
            or ship_to_country == ''
           )

def isCanada(ship_to_country):
    """
    Returns True if the ship_to_country is the code for Canada.
    """
    if ship_to_country is None:
        raise pickpack_errors.ApplicationError("Error: Ship-to country is None")

    return ship_to_country == pickpack_constants.CANADA_COUNTRY_CODE












#
