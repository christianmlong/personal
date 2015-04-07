"""
utility_classes.py

Utility and helper classes used by the system to warn PickPack users about the
shipment packaging and labelling requirements they need to follow.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""
import collections, itertools

from CML_Common.utility import utl_decorators

from CML_Pickpack.pickpack_modules import pickpack_errors

@utl_decorators.add_constants_to_class({'Shipping'    : ('Air',
                                                         'Ground',
                                                        ),
                                       },
                                       magic_number = 100000,
                                      )
@utl_decorators.add_constants_to_class({'Codes' : {'MetalCoinBattery'                   : 'BT0',
                                                   'CompleteTRPR'                       : 'PA0',
                                                   'TRPRWithoutLens'                    : 'PA1',
                                                   'SmartBand'                           : 'CB0',
                                                   'SmartBelt'                           : 'CT0',
                                                   'TRPRBattery'                        : 'SB0',
                                                   'SmartBandBattery'                    : 'SB1',
                                                   'SmartBeltBattery'                    : 'SB2',
                                                   'MetalAndIonPackageKit'              : 'KT0',
                                                   'ThoriatedTungsten'                  : 'TH1',
                                                   'ThoriatedTungstenKit'               : 'TH2',
                                                   'ThoriatedTungstenRodsLight'         : 'TH3',
                                                   'ThoriatedTungstenRodsHeavy'         : 'TH4',
                                                   'ThoriatedTungstenAccessoryKit'      : 'TH5',
                                                   'ORM_D'                              : 'HZ0',
                                                   #'LeadAcidBattery'                    : 'LB0',
                                                  },
                                        'InlineWarningImage' : {'Blank'     : 0,
                                                                'Metal'     : 1,
                                                                'Ion'       : 2,
                                                                'MetalIon'  : 3,
                                                                'Thorium'   : 4,
                                                                'ORM_D'     : 5,
                                                                #'LeadAcid'  : 6,
                                                               },
                                       },
                                      )
class CommonConstants(object):
    """
    A convenient place to put constants that are needed by all classes.
    """

@utl_decorators.add_constants_to_class({'Image' : {'PackingInstruction965'          : 'battery_doc1',
                                                   'PackingInstruction966'          : 'battery_doc2',
                                                   'PackingInstruction967'          : 'battery_doc3',
                                                   'PackingInstruction968'          : 'battery_doc4',
                                                   'PackingInstruction969'          : 'battery_doc5',
                                                   'PackingInstruction970'          : 'battery_doc6',
                                                   'PackingInstruction966And965'    : 'battery_doc7',
                                                  },
                                       },
                                      )
class PackingInstructionConstants(object):
    """
    Mixin class for classes that deal with packing instructions for lithium
    batteries. Provides constants.
    """


class MultiDict(collections.Mapping, CommonConstants):
    """
    A dictionary that takes hashable tuples as its keys. The tulpe elements may
    be scalar (such as integer constants). They may also be instances of
    frozenset, representing multiple possible values at that position in the
    tuple.
    """
    # I call this class MultiDict because its keys can contain frozensets that
    # represent multiple valid values.
    def __init__(self,
                 ruleset,
                 combinatorial_dimensions,
                ):
        #collections.Mapping.__init__(self)         # No __init__member, and no need to initalize this base class.
        CommonConstants.__init__(self)
        self.reference_dict = dict(ruleset)
        # Used for testing only
        self.combinatorial_dimensions = combinatorial_dimensions

    def __contains__(self, key):
        raise pickpack_errors.ApplicationError("__contains__ is not implemented for MultiDict")

    def __delitem__(self, key):
        raise pickpack_errors.ApplicationError("__delitem__ is not implemented for MultiDict")

    def __setitem__(self, key):
        raise pickpack_errors.ApplicationError("__setitem__ is not implemented for MultiDict")

    def __iter__(self):
        return iter(self.reference_dict)

    def __len__(self):
        return len(self.reference_dict)

    def __getitem__(self, key):
        return self._get(key)

    def _get(self, candidate_key):

        # The candidate key is a tuple of integers. The tuple has one element
        # for each group of conditions (number of smart bands, number of smart
        # belts, etc.). That tuple element specifies the state of that condition
        # (e.g. 2 SmartBelts).
        #
        # In this function, we step through all the cases specified in
        # self.reference_dict.
        #
        # Each key in self.reference_dict is a tuple of conditions.
        # self.reference_dict maps those conditions to a certain subclass of
        # ShipmentWarning. self.reference_dict maps rules (each rule represented
        # as a tuple of conditions) to actions (each action represented as a
        # subclass of ShipmentWarning).
        #
        # What we're doing here is stepping through the keys of
        # self.reference_dict (the "rules"). Each key in self.reference_dict is
        # a tuple. For each key in self.reference_dict (call it a "reference
        # key"), we compare the "reference key" with the candidate_key that was
        # passed in to this function. When we get a match, we return the value
        # which corresponds to that key in self.reference_dict.
        #
        # Here's how we compare the reference key and the candidate key
        # (remember, both keys are tuples). First, we make sure the two tuples
        # are the same length. Then, we compare each position of the reference
        # key tuple with the corresponding position in candidate key tuple.
        #
        # Here's how we compare each position in the candidate and reference
        # keys. At each position, the candidate key has an integer. At each
        # position, ther reference key can have an integer, or a frozenset of
        # integers. If the reference key element at the current position is an
        # integer, we simply compare the integers. If the reference key element
        # at the current position is a frozenset, we check if the candidate key
        # element (an integer) is a member of the reference key element (a
        # frozenset).
        #
        # If the comparison returns true at all positions in the candidate key,
        # then we have a match. We return the corresponding value from
        # self.reference_dict.


        # POSSIBLE IMPROVEMENT
        # Here is a way to possibly do this more efficiently. Keep track of each
        # time a key of self.reference_dict is matched. When looping through the
        # rules in self.reference_dict looking for matches (call that a "table
        # scan"), proceed in order of popularity. We test the most popular rules
        # first, saving time.
        #
        # Another possibility - cache the top-n candidate keys and the result.
        #
        # I'm not sure I'm going to do both optimizations. If I do, the question
        # becomes whether or not to, on a cache hit, update the popularity count
        # for the corresponding rule. Do we want to make sure its popularity is
        # correctly counted, so that if it falls out of the top-n cache, it
        # still has its proper place in the regular (non-cache) matching
        # process? The problem is, that distorts the non-cache matching process,
        # since rules that generate a lot of cache hits would be at the top.
        # They would be checked first in a table scan. However, it doesn't make
        # sense to check them first, since their popularity reflects cache hits,
        # and not the actual popularity among all the candidate keys that made
        # it past the cache.
        #
        # Possible soultion: when the top-n cache changes, reset the popularity
        # counts to zero but retain the old popularity sort order, so we don't
        # go back to square one. However, that doesn't work, because then one
        # hit on a single rare rule puts it up above the 90% rules until they
        # re-establish their popularity. That is to say, even if we retain the
        # sort order, we still go back to square one on the popularity sort.
        # Probably I would need to retain the old popularity and the global
        # (since inception) popularity, and then do some complicated
        # cache-ageing calculation. It's almost certainly not worth it.
        #
        # So, a simple cache of the top-n results is probably a good idea (no
        # popularity sort for table scan). However, even a simple cache is not
        # so simple an affair. See the bottom of this file for an implementation
        # of the ARC cache.

        def _compare(candidate_key_element,
                     reference_key_element,
                    ):
            if isinstance(reference_key_element, frozenset):
                result = candidate_key_element in reference_key_element
            elif isinstance(reference_key_element, int):
                result = (candidate_key_element == reference_key_element)
            else:
                raise pickpack_errors.ApplicationError("Invalid reference key element %s" % reference_key_element)
            return result

        candidate_key_len = len(candidate_key)
        for reference_key, value in self.reference_dict.items():
            if candidate_key_len != len(reference_key):
                raise pickpack_errors.ApplicationError("Incompatible keys %s %s" % (candidate_key, reference_key))

            # This checks if _compare evaluates to True for all positions in the
            # candidate_key. This returns the first value it finds, which should
            # be the only value. See the docstring for this class for an
            # explanantion of the two ways of writing self.reference_dict:
            match = all(_compare(target, ref) for target, ref in itertools.izip(candidate_key, reference_key))
            if match:
                return value

        # We made it through the whole reference_dict without finding a match.
        # Raise KeyError.
        raise KeyError(candidate_key)


class ItemRuleset(CommonConstants):
    """
    Represents a set of rules to calculate warnings based on the items on an
    order.
    """

    # Note: We only build one instance from each ItemRuleset class, and store it
    # for the duration of the application, in a class attribute of the
    # ShipmentWarningCalculator class. Therefore, we must implement these
    # objects as immutable, not storing state in them during rule-check runs.

    def __init__(self):
        # Call base class' constructor
        CommonConstants.__init__(self)

    def apply_rules(self,
                    counter,
                    shipping_method,
                   ):
        """
        Takes the counter, which holds the tallied data about the item
        categories and quantities present in the order. Runs through the
        counter, and determines which warning to return. The return value is an
        instance of a subclass of ShipmentWarning.

        If no warning is needed, returns an instance of the NoWarning class.
        """
        decisive_factors = self._calcualte_decisive_factors(counter,
                                                            shipping_method,
                                                           )

        # We now have an integer or a tuple of integers, representing the
        # constant(s) that we use to indicate the value of each factor. We now
        # go to our table of rules (a dictionary), and we see which warning
        # class corresponds to this set of factors. We instantiate a warning
        # object from the warning class, and we return the warning object.
        warning_class = self.ruleset[decisive_factors]                                      # pylint: disable=no-member
        warning_object = warning_class()
        return warning_object

    def _calcualte_decisive_factors(self,
                                    counter,
                                    shipping_method,
                                   ):
        """
        Override in derived classes
        """


class SpecialRuleset(CommonConstants):
    """
    Represents a set of rules to calculate warnings based on data other than the
    items on an order.
    """
    def __init__(self):
        # Call base class' constructor
        CommonConstants.__init__(self)













# OLD code







# Cacheing
#
# http://code.activestate.com/recipes/576532/
# http://en.wikipedia.org/wiki/Adaptive_replacement_cache
#
#class Cache(object):
#    """
#    >>> dec_cache = Cache(10)
#    >>> @dec_cache
#    ... def identity(f):
#    ...     return f
#    >>> dummy = [identity(x) for x in range(20) + range(11,15) + range(20) +
#    ... range(11,40) + [39, 38, 37, 36, 35, 34, 33, 32, 16, 17, 11, 41]]
#    >>> dec_cache.t1
#    deque([(41,)])
#    >>> dec_cache.t2
#    deque([(11,), (17,), (16,), (32,), (33,), (34,), (35,), (36,), (37,)])
#    >>> dec_cache.b1
#    deque([(31,), (30,)])
#    >>> dec_cache.b2
#    deque([(38,), (39,), (19,), (18,), (15,), (14,), (13,), (12,)])
#    >>> dec_cache.p
#    5
#    """
#    def __init__(self, size):
#        self.cached = {}
#        self.c = size
#        self.p = 0
#        self.t1 = deque()
#        self.t2 = deque()
#        self.b1 = deque()
#        self.b2 = deque()
#
#    def replace(self, args):
#        if self.t1 and (
#            (args in self.b2 and len(self.t1) == self.p) or
#            (len(self.t1) > self.p)):
#            old = self.t1.pop()
#            self.b1.appendleft(old)
#        else:
#            old = self.t2.pop()
#            self.b2.appendleft(old)
#        del(self.cached[old])
#
#    def __call__(self, func):
#        def wrapper(*orig_args):
#            """decorator function wrapper"""
#            args = orig_args[:]
#            if args in self.t1:
#                self.t1.remove(args)
#                self.t2.appendleft(args)
#                return self.cached[args]
#            if args in self.t2:
#                self.t2.remove(args)
#                self.t2.appendleft(args)
#                return self.cached[args]
#            result = func(*orig_args)
#            self.cached[args] = result
#            if args in self.b1:
#                self.p = min(
#                    self.c, self.p + max(len(self.b2) / len(self.b1) , 1))
#                self.replace(args)
#                self.b1.remove(args)
#                self.t2.appendleft(args)
#                #print "%s:: t1:%s b1:%s t2:%s b2:%s p:%s" % (
#                #    repr(func)[10:30], len(self.t1),len(self.b1),len(self.t2),
#                #    len(self.b2), self.p)
#                return result
#            if args in self.b2:
#                self.p = max(0, self.p - max(len(self.b1)/len(self.b2) , 1))
#                self.replace(args)
#                self.b2.remove(args)
#                self.t2.appendleft(args)
#                #print "%s:: t1:%s b1:%s t2:%s b2:%s p:%s" % (
#                #   repr(func)[10:30], len(self.t1),len(self.b1),len(self.t2),
#                #   len(self.b2), self.p)
#                return result
#            if len(self.t1) + len(self.b1) == self.c:
#                if len(self.t1) < self.c:
#                    self.b1.pop()
#                    self.replace(args)
#                else:
#                    del(self.cached[self.t1.pop()])
#            else:
#                total = len(self.t1) + len(self.b1) + len(
#                    self.t2) + len(self.b2)
#                if total >= self.c:
#                    if total == (2 * self.c):
#                        self.b2.pop()
#                    self.replace(args)
#            self.t1.appendleft(args)
#            return result
#        return wrapper
#
#
#
#
# In the comments on this recipe, Raymond Hettinger says this:
#
#
# Thanks for the nice, clean translation of the spec in the patent application.
#
# As presented, the recipe uses collections.deque() which is efficient for the
# all of the operations except remove() and __contains__() which are both O(n)
# operations.
#
# Instead of collections.deque(), it would be better to use an alternate deque
# implementation that supports fast searching and removal. This can easily be
# expressed using collections.OrderedDict() which appeared in Py2.7 and Py3.1
# and has an ASPN recipe for earlier versions. In the recipe above, just
# substitute Deque for deque and define it as:
#
#class Deque:
#    'Fast searchable queue'
#    def __init__(self):
#        self.od = OrderedDict()
#    def appendleft(self, k):
#        od = self.od
#        if k in od:
#            del od[k]
#        od[k] = None
#    def pop(self):
#        return self.od.popitem(0)[0]
#    def remove(self, k):
#        del self.od[k]
#    def __len__(self):
#        return len(self.od)
#    def __contains__(self, k):
#        return k in self.od
#    def __iter__(self):
#        return reversed(self.od)
#    def __repr__(self):
#        return 'Deque(%r)' % (list(self),)
