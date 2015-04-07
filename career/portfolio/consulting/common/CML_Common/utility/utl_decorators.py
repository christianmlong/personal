"""
utl_decorators.py

Definitions of decorator functions


Christian M. Long, developer

Initial implementation: August 7, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

import copy

# Import shared modules
from Common.error import error

# A note about decorators:
#
# Decorators are directives that are placed before a function definition. A
# decorator is applied using the @ character.
#
# A decorator takes a function, modifies it, and then replaces the original
# function with the modified one. It's an easy way to add similar functionality
# to many functions at once.

# Note 1:
# To avoid confusion about the Method Resolution Order (MRO), we call the base
# class __init__ explicitly, without using super(). We do not use any
# diamond-shaped inheritance graphs, so super is not needed.
#
# Of course, all multiple-inheritance trees in python have a diamond structure
# with 'object' at the base, but since object.__init__ does nothing, we don't
# need to worry about it. See "Python's Super Considered Harmful" at
# http://fuhm.net/super-harmful/ for an explanation of the pitfalls involved
# with using super().

def makeProperty(function):
    """
    This function is used as a decorator. The function it decorates must return
    its own locals() when called.

    This means that when we call function(), we get a dictionary that represents
    all attributes currently bound in function.

    These attributes are the fset, fget, fdel and doc arguments required by the
    built-in property() function.
    """
    # Here's an example of how this decorator might be used. The commented
    # pylint declarations are used to keep pylint from complaining about some of
    # the magic here.
    #
    #    #    Properties                  +++++++++++++++++++
    #    # pylint: disable=E0202, E0211, W0212, C0111
    #    @utl_decorators.makeProperty
    #    def db2DbapiModule():
    #        doc = """
    #              The dbapi module used to make a connection to a DB2 database.
    #              This returns a reference to the module itself.
    #              """
    #        def fget(self):
    #            return self._db2_dbapi_module
    #        return locals()
    #    # pylint: enable=E0202, E0211, W0212, C0111

    return property(**function())

def memoizeFunction(function):
    """
    Decorator that caches a function's return value each time it is called. If
    called later with the same arguments, the cached value is returned, and not
    re-evaluated.
    """
    class _Factory(_MemoizeSomething):                                          # pylint: disable=used-before-assignment
        """
        A class for making callable instances.
        """
        def __init__(self, function):
            # Call the base class __init__ explicitly. See Note 1 at top of
            # file.
            _MemoizeSomething.__init__(self, function)

        def produceReturnValue(self, *args):
            """
            We wrap an ordinary function; return its value.
            """
            return self._function(*args)

    return _Factory(function)

def memoizeMethod(method):
    """
    Decorator that caches a method's return value each time it is called. If
    called later with the same arguments, the cached value is returned, and not
    re-evaluated.
    """
    # We need extra code here so that our decorated method behaves properly
    # during the lookup process. When a method (that is: a function which is an
    # attribute of an instance's class) is called, the lookup calls __get__ and
    # expects to receive a bound method. A bound method has an attribute im_self
    # which refers to the instance from which the method was obtained. This is
    # how the "self" parameter of methods gets populated automatically.
    #
    # Here, we supply our own implementation of __get__ which stores the
    # instance ("self") so we can supply it ourselves during the __call__ phase.
    class _Factory(_MemoizeSomething):
        """
        A class for making callable instances.
        """
        def __init__(self, method):
            # Call the base class __init__ explicitly. See Note 1 at top of
            # file.
            _MemoizeSomething.__init__(self, method)

        def __get__(self, instance, cls=None):
            self._instance = instance       # pylint: disable=W0201
            return self

        def produceReturnValue(self, *args):
            """
            Behave like a bound method. (we must supply the "self" argument
            ourselves). Return the value.
            """
            return self._function(self._instance, *args)

    return _Factory(method)

def memoizeFunctionWithCacheLimit(cache_items_limit):
    """
    Decorator that caches a function's return value each time it is called. If
    called later with the same arguments, the cached value is returned, and not
    re-evaluated. When the cache fills up with more items than
    cache_items_limit, the least recently used item is discarded.
    """
    class _Factory(_MemoizeSomethingWithCacheLimit):                            # pylint: disable=used-before-assignment
        """
        A class for making callable instances.
        """
        def __init__(self, function, cache_items_limit):
            # Call the base class __init__ explicitly. See Note 1 at top of
            # file.
            _MemoizeSomethingWithCacheLimit.__init__(self, function, cache_items_limit)

        def produceReturnValue(self, *args):
            """
            We wrap an ordinary function; return its value.
            """
            return self._function(*args)

    return _WrapperForDecoratorsWithArguments(_Factory, cache_items_limit)

def memoizeMethodWithCacheLimit(cache_items_limit):
    """
    Decorator that caches a method's return value each time it is called. If
    called later with the same arguments, the cached value is returned, and not
    re-evaluated. When the cache fills up with more items than
    cache_items_limit, the least recently used item is discarded.
    """
    # See note above about decorating methods
    class _Factory(_MemoizeSomethingWithCacheLimit):
        """
        A class for making callable instances.
        """
        def __init__(self, function, cache_items_limit):
            # Call the base class __init__ explicitly. See Note 1 at top of
            # file.
            _MemoizeSomethingWithCacheLimit.__init__(self, function, cache_items_limit)

        def __get__(self, instance, cls=None):
            self._instance = instance       # pylint: disable=W0201
            return self

        def produceReturnValue(self, *args):
            """
            Behave like a bound method. (we must supply the "self" argument
            ourselves). Return the value.
            """
            return self._function(self._instance, *args)

    return _WrapperForDecoratorsWithArguments(_Factory, cache_items_limit)


class _WrapperForDecoratorsWithArguments(object):
    """
    Wrapper class used to receive the value of decorator arguments and produce
    a decorator.
    """
    #
    # Example:
    #
    # @decoratorWithArgs(10)
    # def froz():
    #   . . .
    #
    # When using a decorator that takes arguments, a two-step happens. First,
    # decoratorWithArgs is called, passing in the argument 10. decoratorWithArgs
    # must return a callable (a decorator) which is then used to actually
    # decorate froz().
    #
    def __init__(self, class_to_instantiate, *args, **kwargs):
        # Now we're taking the arguments (10 in the example above) and storing
        # them for later use.
        self._args = args
        self._kwargs = kwargs

        # We're also storing a reference to the class we need to instantiate
        # later to get the decorator we want.
        self._class_to_instantiate = class_to_instantiate

    def __call__(self, function):
        # Now the actual decorator is being called, and the function to be
        # decorated is being passed in. Return the bottom-line callable,
        # appropriately modified with the previously supplied arguments
        return self._class_to_instantiate(function, *self._args, **self._kwargs)

class _MemoizeSomething(object):
    """
    Base class for classes which are used to make callable instances.
    """
    def __init__(self, function):
        self._function = function
        self._cache = {}

    def __repr__(self):
        """
        Return the function's docstring.
        """
        return self._function.__doc__

    def __call__(self, *args):
        # Is the tuple of arguments hashable? (no lists or other mutable
        # objects)
        try:
            cache_hit = self._cache.has_key(args)
        except TypeError:
            # args is not hashable so we don't use the cache; we just call the
            # function.
            return self.produceReturnValue(*args)

        if cache_hit:
            return self._cache[args]
        else:
            value = self._cache[args] = self.produceReturnValue(*args)
            return value

class _MemoizeSomethingWithCacheLimit(_MemoizeSomething):
    """
    Base class for classes which are used to make callable instances. Cache size
    limits are enforced.
    """
    def __init__(self, function, cache_items_limit):
        self._cache_items_limit = cache_items_limit
        # A list to store the hashes of the arguments, in order from
        # least-recently-used to most-recently-used
        self._cache_item_hashes = []
        # Call the base class __init__ explicitly. See Note 1 at top of file.
        _MemoizeSomething.__init__(self, function)

    def __call__(self, *args):
        # Is this tuple of arguments hashable? (no lists or other mutable
        # objects)
        try:
            key = hash(args)
        except TypeError:
            # args is not hashable so we don't use the cache; we just call the
            # function.
            return self.produceReturnValue(*args)

        try:
            # Look for the hash signature of this argument tuple in our list of
            # most recent hits. If it is found, move it to the end of the list
            # (most-recently-used).
            self._cache_item_hashes.append(self._cache_item_hashes.pop(self._cache_item_hashes.index(key)))
        except ValueError:
            # We do not have a hit in the cache for this argument tuple. Store
            # its return value in the cache, store its hash in the MRU list, and
            # check the MRU list against the size limit.
            self._cache[key] = self.produceReturnValue(*args)
            self._cache_item_hashes.append(key)
            if len(self._cache_item_hashes) > self._cache_items_limit:
                # We're over the limit. Drop the least recently used item from
                # the cache and from the MRU list.
                del self._cache[self._cache_item_hashes.pop(0)]

        return self._cache[key]


# Class decorator to add enumerated named constants to a class
#
# Note: you can, of course, just add the named constants directly to the class
# inside the class body (before __init__). For example:
#
#
#
#        class MyClass:
#            """
#            My class that does stuff
#            """
#
#            # Named constants, accessible as MyClass.Constants.BarcodeStyle
#            class Constants:
#                """
#                Container for named constants
#                """
#
#                class BarcodeStyle:
#                    """
#                    Named constants for indicating the barcode style
#                    """
#                    _magicNumber = 21000
#                    UPC_A               = 0 + _magicNumber
#                    Code3Of9            = 1 + _magicNumber
#                    Code3Of9NoInterp    = 2 + _magicNumber
#                    Code128             = 3 + _magicNumber
#
#
# However, with this style, if you add constants to both a superclass and a
# subclass, the subclass' Constants replaces the superclass' Constants.
#
# In contrast, by using this decorator (@add_constants_to_class) we can add
# constants at multiple points in the class hierarchy without overwriting the
# superclass' constants.
#
# However, one problem I encountered was that constants added by subclasses were
# visible throughout the class hierarchy. They were even visible by sublcasses
# in another branch of the hierarchy, as long as they shared an ancestor.
#
# I fixed this by using copy.deepcopy to give each subclass its own local
# copy of its supercass' constants, to which it could add its own local
# constants.

def add_constants_to_class(dictionary_of_constants,
                           magic_number = None,
                          ):
    """
    Use this class decorator to add named constants to a class.

    Here's an example of usage without magic_number:
        @utl_decorators.add_constants_to_class({'Resolution' : {'EightDotsPerMM' : 8,
                                                                'TwelveDotsPerMM' : 12,
                                                               },
                                                'LabelTop'   : {'Zero' : 0,
                                                                'TwentyDotsUp' : -20,
                                                                'TwentyDotsDown' : 20,
                                                               },
                                               },
                                              )
        class SomeClass(object):

    The resulting named constants are accessible like this:
        SomeClass.Constants.Resolution.EightDotsPerMM
        SomeClass.Constants.LabelTop.TwentyDotsDown


    Here's an example of usage with magic_number:
        @utl_decorators.add_constants_to_class({'FontStyle'    : ('Default',
                                                                  'FontD',
                                                                  'FontE',
                                                                  ),
                                                'FontWeight'   : ('Light',
                                                                  'Normal',
                                                                  'Bold',
                                                                 ),
                                               },
                                               magic_number = 20000,
                                              )
        class SomeClass(object):

    The resulting enumerated named constants are accessible like this:
        SomeClass.Constants.FontStyle.FontD
        SomeClass.Constants.FontWeight.Bold

    These enumerated named constants are useful when we want to specify options
    but we don't care about their values. magic_number is a salt to keep the
    numbers unique and avoid unwanted collisions.

    To add both a named constant and an enumerated named constant to a class,
    use the decorator twice.
        @utl_decorators.add_constants_to_class({'Resolution' : {'EightDotsPerMM' : 8,
                                                                'TwelveDotsPerMM' : 12,
                                                               },
                                               },
                                              )
        @utl_decorators.add_constants_to_class({'FontStyle'    : ('Default',
                                                                  'FontD',
                                                                  'FontE',
                                                                  ),
                                               },
                                               magic_number = 20000,
                                              )
        class SomeClass(object):

    """

    def a_decorator_with_the_arguments_applied_to_it(cls):          # pylint: disable=C0111
        container_name = 'Constants'

        if hasattr(cls, container_name):
            # The class we are decorating already has a "Constants" object as
            # one of its attributes (either inherited, or from a previous
            # decoration on this class). We make our own local copy (to avoid
            # leaking our constants throughout the class hierarchy).
            #
            # Note that, in cases where the decorator is called twice on the
            # same class, this means we will do some unnecessary extra copying.
            # For simplicity, I don't worry about that extra copying.
            setattr(cls,
                    container_name,
                    copy.deepcopy(getattr(cls, container_name))
                   )
        else:
            # The class we are decorating does not yet have a "Constants" object
            # as one of its attributes, so, we add it.
            setattr(cls,
                    container_name,
                    ConstantsContainer(container_name),
                   )
        container = getattr(cls, container_name)

        # magic_number is defined in outer scope, so we can't change it here.
        # So, we make a local copy that we can increment.
        if magic_number is not None:
            magic_number_incremented = magic_number

        # Loop through the named groups, adding them each to "Constants".
        for name_of_constants_group, group_of_constants in dictionary_of_constants.items():
            if magic_number is not None:
                group_of_constants = make_enum_dictionary(group_of_constants,
                                                          magic_number_incremented,
                                                         )
                # Increment magic number, if there is more than one group of
                # enum constants to be made.
                magic_number_incremented += 100

            if hasattr(container,
                       name_of_constants_group,
                      ):
                # The container already exists. Update it with the contents of
                # the new container.
                existing_container = getattr(container,
                                             name_of_constants_group,
                                            )
                existing_container.update(group_of_constants)
            else:
                # Add a container to the "Constants" container. That container has
                # the named constants as attributes.
                setattr(container,
                        name_of_constants_group,
                        ConstantsContainer(name_of_constants_group,
                                           group_of_constants,
                                          ),
                       )

        # We have decorated the class, now return it
        return cls

    # We have built the decorator according to the "dictionary_of_constants"
    # argument. Now return it.
    return a_decorator_with_the_arguments_applied_to_it

def make_enum_dictionary(group_of_constants,
                         magic_number,
                        ):
    """
    Given a sequence of strings, this returns a dictionary where the strings are
    keys, and the values are an enumeration starting at magic_number.

    For example:
    a = ('Default', 'FontD', 'FontE')
    make_enum_dictionary(a, 100)

    results in:
    {'Default': 100, 'FontD': 101, 'FontE': 102}
    """
    start = magic_number
    stop = len(group_of_constants) + magic_number
    return dict(zip(group_of_constants, range(start, stop)))

class ConstantsContainer(object):
    """
    Class to make objects that will be used as named constants.
    """
    def __init__(self,
                 container_name,
                 entries = None,
                ):
        # This name attribute is used just for error messages
        self.name = "Container '%s'" % container_name
        if entries is not None:
            self.update(entries)

    def update(self,
               entries,
              ):
        """
        Allows multiple classes to add to a dictionary of constants. Raises an
        error if one class tries to clobber a dictionary entry from another
        class.

        This allows a constants dictionary to be built up by several layers of a
        class hierarchy.
        """
        set1 = frozenset(self.__dict__.keys())
        set2 = frozenset(entries.keys())

        if not set1.isdisjoint(set2):
            collisions = list(set1.intersection(set2))
            # The attribute or attributes already exist. Raise an error.
            err_msg = ("%s already has attributes %s" %
                       (self.name,                    # pylint: disable=W0212
                        collisions,
                       )
                      )
            raise error.ApplicationError(err_msg)

        self.__dict__.update(entries)


#
