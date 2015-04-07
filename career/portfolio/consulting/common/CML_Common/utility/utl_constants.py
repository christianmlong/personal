"""
utl_constants.py

Constants and string literals


Christian M. Long, developer

Initial implementation: September 10, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# "Close enough" factor used when comparing floating point numbers which are
# inherently imprecise. Two numbers are considered to be equal if the difference
# between them is less than epsilon.
EPSILON = .0001

# Format string for formatting time
TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z" # Tue, 10 Dec 2003 18:07:53 CST
