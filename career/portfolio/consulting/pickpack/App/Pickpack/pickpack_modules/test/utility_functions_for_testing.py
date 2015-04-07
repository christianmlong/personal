"""
Utility and support functions for testing

    utility_functions_for_testing.py

"""

#import datetime
from Pickpack.pickpack_modules import pickpack_errors

#def ecommerce_promotion_is_active():
#    """
#    Certain warnings depend on the time of year. This returns True or False,
#    indicating whether a seasonal e-commerce promotion is currently in
#    effect.
#    """
#    this_year = datetime.date.year()
#    next_year = this_year + 1
#    start_date = datetime.date(this_year, 11, 25)
#    end_date = datetime.date(next_year, 1, 31)
#    return start_date <= datetime.date.today() <= end_date

def read_json_from_response(response):
    """
    If an error occurs while rendering the json, raise an error with the text of
    the response.
    """
    try:
        return_value = response.json()
    except ValueError:
        #print response.text
        raise pickpack_errors.ApplicationError(response.text)
    return return_value
