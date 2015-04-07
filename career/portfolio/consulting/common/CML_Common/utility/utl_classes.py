"""
utl_classes.py

utility classes


Christian M. Long, developer

Initial implementation: September 10, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

class Enum(object):
    """
    A class to represent enumerations. Objects instantiated fom this class have
    named attributes corresponding to the list_of_named_constants. Also, they
    allow "x in y" tests.
    """
    def __init__(self, list_of_named_constants):
        dict_of_constants = dict((name, index) for index, name in enumerate(list_of_named_constants))
        self.__dict__.update(dict_of_constants)
    def __contains__(self, item):
        # Enables tests of the x in y variety. Returns True if the "item"
        # argument is an integer that is in the enum.
        return item in self.__dict__.values()


class Freezable(object):
    """
    This is a base class used for objects where you want to define all the
    object's attributes ahead of time (in the class definition), and prevent any
    client code from adding any arbitrary attributes at run time.

    A derived class might look like this:

    class Foo(Freezable):
        def __init__(self):
            Freezable.__init__(self)

            # At the start of __init__, we explicity unfreeze the object. We
            # do this because, in the case of a long inheritance chain, the
            # object might have been frozen at the end of its BaseClass'
            # __init__.
            self.unfreeze_attribute_creation()

            self.bar = 42

            # At the end of __init__, we explicity freeze the object,
            # preventing the creation of any more attributes.
            self.freeze_attribute_creation()

    """
    # This recipe comes from
    # http://mail.python.org/pipermail/python-list/2008-July/1137342.html
    #
    # It has been modified to allow freeze and unfreeze, so that a chain of base
    # class and derived class __init__ calls can each set its own attributes,
    # and also can each call freeze() at the end of its own __init__.
    #
    # If we did not have freeze and unfreeze, only the most-derived classes
    # could call freeze(). The base classes would not be able to call freeze()
    # at the end of their own __init__. This would leave unprotected any
    # instances of base classes.

    def __init__(self):
        self._attribute_creation_has_been_frozen = None
        self.unfreeze_attribute_creation()

    def freeze_attribute_creation(self):
        """
        After this is called, no attributes can be created on instances of this
        class.
        """
        self._attribute_creation_has_been_frozen = True

    def unfreeze_attribute_creation(self):
        """
        Aattributes can once again be created on instances of this
        class.
        """
        self._attribute_creation_has_been_frozen = False

    def __setattr__(self, attr, value):
        """
        __setattr__ controlls the creation of all attributes on this object. If
        the object is frozen, and a previously-undefined attibute is accessed
        for setting, this raises an AttributeError.
        """
        # Special handling to allow our "frozen" flag to be set without
        # hindrance.
        if attr != '_attribute_creation_has_been_frozen':

            # Has the object been frozen?
            if self._attribute_creation_has_been_frozen:

                # Does the attribute exist already?
                if not hasattr(self, attr):
                    err_msg = "Set %s = %s: Attribute creation outside of " \
                              "%s class definition is not allowed." % \
                              (attr, value, self.__class__.__name__)
                    raise AttributeError(err_msg)

        # Tests pass, so it's ok to create or set the attribute.
        object.__setattr__(self, attr, value)











#
