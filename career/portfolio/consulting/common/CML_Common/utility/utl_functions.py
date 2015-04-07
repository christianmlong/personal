"""
utl_functions.py

utility functions


Christian M. Long, developer

Initial implementation: September 10, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import shared modules
from CML_Common.utility import utl_constants

def wrapScalarValue(value):
    """
    If a single (scalar) value was passed in, wrap it inside a one-element
    tuple. If a sequence was passed in, return it unchanged.

    Since strings are iterable, a situation often arises where python iterates
    over the individual characters in a string rather than treating the string
    as one whole item. Passing the string through this function alleviates this
    problem, by wrapping the string up inside a one-element tuple.


    For example:

    >>> wrapScalarValue(2)
    (2,)

    >>> wrapScalarValue([2, 5])
    [2, 5]
    """

    # Note: Use the wrapInTuple function (defined below) instead of this one. It
    # handles wrapping any non-iterable except for strings.

    if isinstance(value, (bool, int, float, str, long)):
        return (value,)
    else:
        return value

def floatEquals(a, b):
    """
    Compares floats for equality. Uses the "close enough" EPSILON factor to
    avoid problems with comparing floats that are stored in binary format.
    e.g. this function will return True when comparing 1.999999999 with
    2.000000001.

    For example:

    >>> floatEquals(1, 2)
    False

    >>> floatEquals((1.0/3)*3, 1)
    True
    """
    return  abs(a - b) < utl_constants.EPSILON

def floatGreaterThan(a, b):
    """
    Returns True if a > b. Uses the "close enough" EPSILON factor to avoid
    problems with comparing floats that are stored in binary format.

    For example:

    >>> floatGreaterThan(2, 1)
    True

    >>> floatGreaterThan((1.0/3)*3, 1)
    False
    """
    return a > (b + utl_constants.EPSILON)

def floatLessThan(a, b):
    """
    Returns True if a < b. Uses the "close enough" EPSILON factor to avoid
    problems with comparing floats that are stored in binary format.

    For example:

    >>> floatLessThan(1, 2)
    True

    >>> floatLessThan((1.0/3)*3, 1)
    False
    """
    return a < (b - utl_constants.EPSILON)

def floatNotEquals(a, b):
    """
    Compares floats for inequality. Uses the "close enough" EPSILON factor to
    avoid problems with comparing floats that are stored in binary format.

    For example:

    >>> floatNotEquals(1, 2)
    True

    >>> floatNotEquals((1.0/3)*3, 1)
    False
    """
    return not floatEquals(a, b)

def floatGreaterThanOrEqualTo(a, b):
    """
    Returns True if a >= b. Uses the "close enough" EPSILON factor to avoid
    problems with comparing floats that are stored in binary format.

    For example:

    >>> floatGreaterThanOrEqualTo(1, 2)
    False

    >>> floatGreaterThanOrEqualTo((1.0/3)*3, 1)
    True
    """
    return not floatLessThan(a, b)

def floatLessThanOrEqualTo(a, b):
    """
    Returns True if a <= b. Uses the "close enough" EPSILON factor to avoid
    problems with comparing floats that are stored in binary format.

    For example:

    >>> floatLessThanOrEqualTo(1, 2)
    True

    >>> floatLessThanOrEqualTo((1.0/3)*3, 1)
    True
    """
    return not floatGreaterThan(a, b)

def floatInRange(a, minimum, maximum):
    """
    Returns True if minimum <= a <= maximum. Uses the "close enough" EPSILON
    factor to avoid problems with comparing floats that are stored in binary
    format.

    For example:

    >>> floatInRange(1, 2, 10)
    False

    >>> floatInRange((1.0/3)*3, 1, 2)
    True
    """
    return floatLessThanOrEqualTo(minimum, a) and floatLessThanOrEqualTo(a, maximum)

def twoDArrayToString(array, join_char=" "):
    """
    Flattens a 2d array of lists or tuples into a single list. Then, joins it
    into one long string using the join character provided, or using a space if
    no join character was provided.
    """
    outer_list = array

    # This is how nested list comprehensions are ordered.
    #
    # See these sites for reference.
    # http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
    # http://docs.python.org/tutorial/datastructures.html#nested-list-comprehensions
    flattened_list = [item for inner_list in outer_list for item in inner_list]

    return join_char.join(flattened_list)

def excludeItemsFromSequence(sequence,
                             indicies_to_exclude,
                            ):
    """
    Returns a copy of sequence. Removes the items whose indicies are listed in
    indicies_to_exclude.
    """
    if isinstance(sequence, tuple):
        was_tuple = True
    else:
        was_tuple = False

    return_value = list(sequence)
    for index in indicies_to_exclude:
        del return_value[index]

    if was_tuple:
        return_value = tuple(return_value)

    return return_value

def chunk(line,
          chunk_width,
         ):
    """
    Returns a list of chunk_width sized chunks. Does not try to break at word
    boundaries.
    """
    output_list = []
    # Chomp off screen-sized chunks of the line and add them to the output list.
    while len(line) > chunk_width:
        output_list.append(line[:chunk_width])
        line = line[chunk_width:]
    # Add any remaining tail end of the line to the output list.
    output_list.append(line)
    return output_list

def prettyChunk(word_list,
                chunk_width,
                delimiter = None,
               ):
    """
    Returns a list of chunk_width sized chunks. Breaks on spaces, unless
    'delimiter' is specified.
    """
    if delimiter is None:
        delimiter = ' '
    output_list = []
    output_line_list = []
    num_characters_in_line = 0

    for word in word_list:
        # Check length.
        if len(word) > chunk_width:
            # Word is too long to fit on the screen. Wrap the word forcibly.

            # First, dump the current output line bucket if any previous words
            # are already in there.
            if num_characters_in_line > 0:
                output_list.append((delimiter.join(output_line_list)).lstrip())
                output_line_list = []
                num_characters_in_line = 0

            # Next, add wrapped chunks of word directly to output list
            for word_chunk in chunk(word,
                                    chunk_width,
                                   ):
                output_list.append(word_chunk)

        # Omit zero-length check. This allows using multiple consecutive spaces
        # to format text on the screen. C. Long
        #elif len(word) == 0:
        #    # Word is zero length, due to consecutive delimiters. Pass and go
        #    # on to next word.
        #    pass

        else:
            # Check if adding word to output line would make output line too
            # long.
            if (len(word) + num_characters_in_line) > chunk_width:
                # Adding word to current line would cause overflow, so dump the
                # current output line bucket and start a new output line bucket
                # with word.
                output_list.append((delimiter.join(output_line_list)).lstrip())
                output_line_list = [word]
                num_characters_in_line = (len(word) + 1)
            else:
                # Word fits on current line
                output_line_list.append(word)
                num_characters_in_line += (len(word) + 1)

    # Done looping. Dump any remaining partial line into the output list and
    # return
    output_list.append((delimiter.join(output_line_list)).lstrip())
    return output_list

def wrapInTuple(value):
    """
    If a non-iterable was passed in, wrap it inside a one-element tuple. If a
    string was passed in, wrap it inside a one-element tuple. If a non-string
    sequence was passed in, return it unchanged.

    Since strings are iterable, a situation often arises where python iterates
    over the individual characters in a string rather than treating the string
    as one whole item. Passing the string through this function alleviates this
    problem, by wrapping the string up inside a one-element tuple.
    """
    if isinstance(value, str):
        return (value,)
    elif isIterable(value):
        return value
    else:
        return (value,)

def isIterable(item):
    """
    Returns true if item is iterable.
    """
    try:
        ignore_iterator = iter(item)
    except TypeError:
        return False
    else:
        return True
