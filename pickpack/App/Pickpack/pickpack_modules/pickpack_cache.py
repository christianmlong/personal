"""
pickpack_cache.py

Caching for the Pick Pack server


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

import time

from twisted.internet import defer

from Common.utility import utl_decorators

from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules import pickpack_constants

from Pickpack.pickpack_modules.pickpack_resource import PickPackGettableResource

class TimedCache(object):
    """
    A very simple cache object with time expiry. The cache_lifetime argument
    specifies how long the data should be cached, in seconds.
    """
    def __init__(self, cache_lifetime):
        self._cache_data = None

        self._cache_timestamp = None
        self._cache_lifetime = int(cache_lifetime)

        self._reset_timer()

    def _reset_timer(self):
        self._cache_timestamp = time.time()

    #    Properties                  +++++++++++++++++++
    #
    # A note about properties:
    #
    # Properties are special attributes of class objects. Properties are created
    # using the property() function. Here, we're using the
    # utl_decorators.makeProperty function as a decorator. It takes the function
    # it decorates and replaces it with a property.
    #
    #
    # Example:
    #
    # @utl_decorators.makeProperty
    # def user_id():
    #     doc = """
    #           User Id property of GlobalUtilityClass.
    #           """
    #     def fget(self):
    #         return self._user_id
    #     def fset(self, value):
    #         self._user_id = str(value)
    #     # Return the local scope, containing the fget and fset functions,
    #     # no fdel function, and a docstring.  Once passed through the
    #     # utl_decorators.makeProperty decorator, user_id will be a property.
    #     return locals()
    #
    #
    #
    # pylint: disable=E0202, E0211, W0212, C0111
    #
    # Locally disabled pylint messages
    #   E0202: An attribute inherited from ### hides this method
    #   E0211: Method has no argument
    #   W0212: Access to a protected member _user_initials of a client class
    #   C0111: Missing docstring

    @utl_decorators.makeProperty
    def cache_data():
        doc = """
              The data in the cache
              """
        def fget(self):
            if not pickpack_constants.ENABLE_CACHE:
                # Cacheing not enabled
                raise pickpack_errors.CacheMiss

            if self._cache_data is None:
                # No data in the cache yet
                raise pickpack_errors.CacheMiss

            if time.time() > self._cache_timestamp + self._cache_lifetime:
                # The data in the cache has expired
                raise pickpack_errors.CacheMiss

            # Cache hit, return data from cache
            return self._cache_data

        # No need for a setter property. All setting will happen via
        # set_cache_data_callback().
        #def fset(self, value):
        #    self._set_cache_data(value)

        return locals()
    # pylint: enable=E0202, E0211, W0212, C0111

    def set_cache_data_callback(self, cache_data):
        """
        This function is used as a callback, to set the value in the cache.
        """
        # Make sure to use our _set_cache_data() method here, rather than going
        # after the "private" instance variable (self._cache_data) directly.
        self._set_cache_data(cache_data)

        # This is a callback, called from a deferred. We pass the data along
        # so it can continue to be passed down the deferred chain.
        return cache_data

    def _set_cache_data(self, value):
        self._cache_data = value
        self._reset_timer()



class CachedResource(PickPackGettableResource):
    """
    Base class for classes that cache data for the Parts server processes.
    """
    def __init__(self):
        # Call the constructor of our base class
        PickPackGettableResource.__init__(self)

        # Default timeout is 30 seconds
        self.cache_timeout = 30

    def dataMethod(self,
                   request,
                  ):
        """
        Override in derived classes.
        """
        raise NotImplementedError

    def getCachedData_deferred(self, *args):
        """
        Get the data from cache or from the db.
        """
        # Note: This naive cache implementation is not resistent to the dogpile
        # effect. That happens when one request comes in, gets a cache miss, and
        # starts the process of running the database query to refresh the cache
        # data. Meanwhile, another request comes in (before the first one
        # completes and resets the timer on the cache), sees the data is stale,
        # and launches its own database query.
        #
        # Lots of closely-spaced requests can cause more queries than necessary.
        # In this implementation, with few clients and low refresh rates, it
        # shouldn't be a problem.

        try:
            # Is there a cache object in self.cache_dict for this set of
            # arguments?
            cache_object = self.cache_dict[args]                                                        # pylint: disable=no-member
        except KeyError:
            # We did not find a cache object for these arguments. Create a new
            # cache object, and store it in self.cache_dict, indexed by args. It
            # expires every 30 seconds.
            cache_object = self.cache_dict[args] = TimedCache(cache_lifetime = self.cache_timeout)       # pylint: disable=no-member
            # Start the process of querying the database and populating the
            # cache. Return a deferred that will eventually supply us with fresh
            # data.
            return self.handle_cache_miss(cache_object, args)

        try:
            # Is there fresh data in the cache object?
            cache_data = cache_object.cache_data
        except pickpack_errors.CacheMiss:
            # Cache miss. The data has expired. Return a deferred that will
            # eventually supply us with fresh data.
            return self.handle_cache_miss(cache_object, args)
        else:
            # Cache hit. Return an already-fired deferred containing the cached
            # data.
            return defer.succeed(cache_data)

    def handle_cache_miss(self, cache_object, args):
        """
        This gets called when there's a cache miss, or the cache was expired, or
        to populate a newly-created cache object.

        Returns a deferred, which will eventually give us the results of the
        database query we make to get fresh data.
        """

        # Set in motion the process to re-query the database. That returns a
        # deferred.
        deferred = self.getDbData_deferred(*args)                               # pylint: disable=no-member

        # Set up the deferred so that it populates the cache with the fresh data
        # once it gets the data back. We do this by adding the cache's setter
        # function to the end of this deferred's callback chain.
        deferred.addCallback(cache_object.set_cache_data_callback)

        # Return the deferred so Twisted can manage it.
        return deferred
