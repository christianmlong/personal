"""
data_datetime.py

Provides SQL statements for common queries.


Christian M. Long, developer

Initial implementation: September 5, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import Python standard modules
import time

def getTodayAsDateTuple():
    """
    Gets today's date from the system, and returns a tuple (year, month, day,
    hour, minute, second) representing today's date.
    """
    return time.localtime()[0:6]

def pythonTimeTupleFromDateTuple(date_tuple):
    """
    Takes a simple tuple (year, month, day, hour, minute, second) representing a
    date and returns Python's internal time representation, which is a
    nine-element tuple.
    """
    # The time tuple as returned by gmtime(), localtime(), and strptime(), and
    # accepted by asctime(), mktime() and strftime(), is a tuple of 9 integers:
    #
    # Index    Field          Values
    #   0      year             (for example, 1993)
    #   1      month            range [1,12]
    #   2      day              range [1,31]
    #   3      hour             range [0,23]
    #   4      minute           range [0,59]
    #   5      second           range [0,61]
    #   6      weekday          range [0,6], Monday is 0
    #   7      Julian day       range [1,366]
    #   8      daylight savings 0, 1 or -1
    #
    # We take a round trip through Python's internal date representation to get
    # a completely valid full time tuple, with correct values for Julian day and
    # daylight savings time.
    partial_tuple = (date_tuple[0],
                     date_tuple[1],
                     date_tuple[2],
                     date_tuple[3],
                     date_tuple[4],
                     date_tuple[5],
                     0,
                     1,
                     -1)
    return time.localtime(time.mktime(partial_tuple))

def formatDateTuple(date_tuple, format_string):
    """
    Takes a simple tuple (year, month, day, hour, minute, second) representing a
    date, and a format string, and returns the date formatted according to the
    format string.
    """
    return time.strftime(format_string, pythonTimeTupleFromDateTuple(date_tuple))

def formatNow(format_string):
    """
    Returns the system date formatted according to the format string.
    """
    return time.strftime(format_string)

def prettyDatetime(time_tuple = None):
    """
    Returns the specified date and time, formatted in a readable way. Leading
    zeros are stripped. If no time tuple is specified, then this function calls
    localtime() to get the current time in the local time zone.

    For example:         Tuesday Jan 3, 2012   1:57 PM
    """
    if time_tuple is None:
        time_tuple = time.localtime()

    return "%s    %s" % prettyDateAndTime(time_tuple)

def prettyDateAndTime(time_tuple = None):
    """
    Returns the specified date and time, formatted in a readable way. Leading
    zeros are stripped. If no time tuple is specified, then this function calls
    localtime() to get the current time in the local time zone.

    This function differs from prettyDatetime() in that it returns a tuple of
    two strings, representing the date and the time.

    Only one call is made to time.localtime()

    For example:         ('Tuesday Jan 3, 2012', '1:57 PM')
    """
    if time_tuple is None:
        time_tuple = time.localtime()

    return (prettyDate(time_tuple),
            prettyTime(time_tuple),
           )

def prettyDate(time_tuple = None):
    """
    Returns the specified date, formatted in a readable way. Leading zeros are
    stripped. If no time tuple is specified, then this function calls
    localtime() to get the current time in the local time zone.

    For example:         Tuesday Jan 3, 2012
    """
    if time_tuple is None:
        time_tuple = time.localtime()

    return "%s %s, %s" % (time.strftime('%A %b', time_tuple),
                          time.strftime('%d', time_tuple).lstrip('0'),
                          time.strftime('%Y', time_tuple),
                         )

def prettyTime(time_tuple = None):
    """
    Returns the specified time, formatted in a readable way. Leading zeros are
    stripped. If no time tuple is specified, then this function calls
    localtime() to get the current time in the local time zone.

    For example:         Tuesday Jan 3, 2012   1:57 PM
    """
    if time_tuple is None:
        time_tuple = time.localtime()

    return time.strftime('%I:%M %p', time_tuple).lstrip('0')






#
