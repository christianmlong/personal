"""
shopfloor_monitor_classes.py

Utility classes for the Shopfloor Monitor application


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""
# pylint: disable=missing-docstring,protected-access

import collections

from CML_Common.utility import utl_decorators

from CML_Pickpack.pickpack_modules import pickpack_errors


class Column(object):
    """
    Represents a column in an sql clause (e.g. a select, or a group by, or an
    order by clause).
    """
    def __init__(self,
                 definition,
                 name,
                 alias = None,
                ):
        """
        Supply an alias if you want it to differ from the column name. The
        column name must be a valid Python identifier, but the alias can contain
        spaces.
        """
        if name is None:
            raise pickpack_errors.ApplicationError("Name can not be None")

        if name == '':
            raise pickpack_errors.ApplicationError("Name can not be a zero-length string")

        if name.find(' ') != -1:
            raise pickpack_errors.ApplicationError("Name can not contain spaces: name - '%s'" % name)

        self.definition = definition
        self.name = name
        if alias is not None:
            if alias == '':
                raise pickpack_errors.ApplicationError("If you supply alias, it can not be a zero-length string")

            if alias.strip() == '':
                raise pickpack_errors.ApplicationError("If you supply alias, it can not be a string with all spaces")

            if alias.find(' ') != -1:
                # Alias contains spaces, single-quote it
                self.alias = "'%s'" % alias
            else:
                self.alias = alias
        else:
            self.alias = self.name

        self.definition_and_alias = "%s %s" % (self.definition,
                                               self.alias,
                                              )


def make_column_structure(*args):
    """
    Factory function for a ColumnStructure object. args is a sequence of Column
    objects.
    """
    # The namedtuple function returns a new class, which is a subclass of tuple.
    # The new class is named 'ColumnStructure'. It will have fields accessible by
    # attribute lookup as well as being indexable and iterable.
    ColumnStructure = collections.namedtuple('ColumnStructure', (column.name for column in args))           # pylint: disable=invalid-name

    # This is the way the namedtuple factory function works. You pass it a
    # sequence of strings, and it defines a new class for you, where the data
    # can be accessed sequentially (like a tuple) and attributes can also be
    # accessed by name.

    # Next, we further customize the new class - we add some new methods. To
    # prevent conflicts with field names, the method names start with an
    # underscore.
    def _indexof(self, field_name):
        """
        Given a field name in the named tuple, return its index.
        """
        return self._fields.index(field_name)
    ColumnStructure._indexof = _indexof

    #def _extend_and_make_new(self, *args):
    #    """
    #    Return a new namedtuple, with the the field names and values of self,
    #    and adding the columns specified in *args.
    #    """
    #    # We need to convert the ColumnStructure objects to tuples before adding
    #    # them using the plus sign. Otherwise, the ColumnStructure.__add__
    #    # method gets called recursively until we get a maximum recursion error.
    #    return make_column_structure(*(tuple(self) + tuple(args)))
    #ColumnStructure._extend_and_make_new = _extend_and_make_new
    #
    #def _append_and_make_new(self, other_column):
    #    """
    #    Return a new namedtuple, with the the field names and values of self,
    #    and adding the other column.
    #    """
    #    return self + other_column
    #ColumnStructure._append_and_make_new = _append_and_make_new
    #
    #def _insert_at_front_and_make_new(self, other):
    #    """
    #    Return a new namedtuple, with the the field names and values of self,
    #    and adding the columns from other to the front.
    #    """
    #    return other + self
    #ColumnStructure._insert_at_front_and_make_new = _insert_at_front_and_make_new

    def __add__(self, other):
        """
        Implement addition for the ColumnStructure class
        """
        if isinstance(other, Column):
            other_structure = make_column_structure(other)
        elif other.__class__.__name__ == 'ColumnStructure':
            other_structure = other
        else:
            raise TypeError("Can not add items of type %s to ColumnStructure objects" % type(other))

        # We need to convert the ColumnStructure objects to tuples before adding
        # them using the plus sign. Otherwise, the ColumnStructure.__add__
        # method gets called recursively until we get a maximum recursion error.
        return make_column_structure(*(tuple(self) + tuple(other_structure)))
    ColumnStructure.__add__ = __add__

    def __radd__(self, other):
        """
        Implement addition for the ColumnStructure class
        """
        if isinstance(other, Column):
            other_structure = make_column_structure(other)
        elif other.__class__.__name__ == 'ColumnStructure':
            raise pickpack_errors.ApplicationError("Strange error, should have called __add__ instead of __radd__")
        else:
            raise TypeError("Can not add ColumnStructure objects to items of type %s" % type(other))

        # We need to convert the ColumnStructure objects to tuples before adding
        # them using the plus sign. Otherwise, the ColumnStructure.__add__
        # method gets called recursively until we get a maximum recursion error.
        return make_column_structure(*(tuple(other_structure) + tuple(self)))
    ColumnStructure.__radd__ = __radd__

    @utl_decorators.makeProperty
    def _definitions():
        doc = """
              Returns a tuple of the column definitions.
              """
        def fget(self):
            return (column.definition for column in self)
        # Return the local scope, containing the fget function, no fset or fdel
        # function, and a docstring. Once passed through the
        # utl_decorators.makeProperty decorator,
        # _select_clause_definitions_and_aliases will be a property.
        return locals()
    ColumnStructure._definitions = _definitions

    @utl_decorators.makeProperty
    def _aliases():
        doc = """
              Returns a tuple of the column aliases.
              """
        def fget(self):
            return (column.alias for column in self)
        return locals()
    ColumnStructure._aliases = _aliases

    @utl_decorators.makeProperty
    def _definitions_and_aliases():
        doc = """
              Returns a tuple containing the definition and alias for each
              column.
              """
        def fget(self):
            return (column.definition_and_alias for column in self)
        return locals()
    ColumnStructure._definitions_and_aliases = _definitions_and_aliases

    @utl_decorators.makeProperty
    def _select_clause_definitions_and_aliases():
        doc = """
              Returns a sql select clause that consists of the column definitions and
              aliases, comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'select',
                                             include_definitions = True,
                                             include_aliases = True,
                                            )
        return locals()
    ColumnStructure._select_clause_definitions_and_aliases = _select_clause_definitions_and_aliases

    @utl_decorators.makeProperty
    def _select_clause_just_definitions():
        doc = """
              Returns a sql select clause that consists of only the column
              defiinitions, comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'select',
                                             include_definitions = True,
                                             include_aliases = False,
                                            )
        return locals()
    ColumnStructure._select_clause_just_definitions = _select_clause_just_definitions

    @utl_decorators.makeProperty
    def _select_clause_just_aliases():
        doc = """
              Returns a sql select clause that consists of only the column aliases,
              comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'select',
                                             include_definitions = False,
                                             include_aliases = True,
                                            )
        return locals()
    ColumnStructure._select_clause_just_aliases = _select_clause_just_aliases

    @utl_decorators.makeProperty
    def _order_by_clause_definitions():
        doc = """
              Returns a sql order by clause that consists of the column definitions,
              comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'order by',
                                             include_definitions = True,
                                             include_aliases = False,
                                            )
        return locals()
    ColumnStructure._order_by_clause_definitions = _order_by_clause_definitions

    @utl_decorators.makeProperty
    def _order_by_clause_aliases():
        doc = """
              Returns a sql order by clause that consists of the column aliases,
              comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'order by',
                                             include_definitions = False,
                                             include_aliases = True,
                                            )
        return locals()
    ColumnStructure._order_by_clause_aliases = _order_by_clause_aliases

    @utl_decorators.makeProperty
    def _group_by_clause_definitions():
        doc = """
              Returns a sql group by clause that consists of the column definitions,
              comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'group by',
                                             include_definitions = True,
                                             include_aliases = False,
                                            )
        return locals()
    ColumnStructure._group_by_clause_definitions = _group_by_clause_definitions

    @utl_decorators.makeProperty
    def _group_by_clause_aliases():
        doc = """
              Returns a sql group by clause that consists of the column aliases,
              comma separated.
              """
        def fget(self):
            return self._build_column_clause(clause_type = 'group by',
                                             include_definitions = False,
                                             include_aliases = True,
                                            )
        return locals()
    ColumnStructure._group_by_clause_aliases = _group_by_clause_aliases

    def _build_column_clause(self,
                             clause_type,
                             include_definitions,
                             include_aliases,
                            ):
        """
        Build the sql for columns. Used for select, group by and order by.
        """
        if len(self) == 0:
            return ''

        if include_definitions and include_aliases:
            all_columns_text = ",\n".join(self._definitions_and_aliases)
        elif include_definitions:
            all_columns_text = ",\n".join(self._definitions)
        elif include_aliases:
            # No need for newlines when joining aliases. It's more readable if
            # they are all on one line.
            all_columns_text = ", ".join(self._aliases)
        else:
            raise pickpack_errors.ApplicationError("At least one of include_aliases and include_definitions must be true.")

        return "%s %s" % (clause_type, all_columns_text)
    ColumnStructure._build_column_clause = _build_column_clause

    # Here we make an instace of the new ColumnStructure class we just defined.
    # We pass in the sequence of column objects, to initialize the new object.
    return ColumnStructure(*args)

#
#class Clause(object):
#    """
#    Represents an sql clause.
#    """
#    def __init__(self,
#                 columns = None,
#                 #empty_string_for_empty_column_list,
#                ):
#        self.sql = self.build_column_clause(columns,
#                                            #empty_string_for_empty_column_list,
#                                           )
#
#    def build_column_clause(self,
#                            columns,
#                            #empty_string_for_empty_column_list,
#                           ):
#        """
#        Build the sql for columns. Used for select, group by and order by.
#        """
#        if columns is None or len(columns) == 0:
#            #if empty_string_for_empty_column_list:
#            #    return ''
#            #else:
#            #    return self.CLAUSE_TYPE                                         # pylint: disable=no-member
#            return ''
#        if self.INCLUDE_ALIASES:                                                # pylint: disable=no-member
#            all_columns_text = ",\n".join(column.definition_and_alias for column in columns)
#        else:
#            all_columns_text = ",\n".join(column.definition for column in columns)
#        return "%s %s" % (self.CLAUSE_TYPE, all_columns_text)                   # pylint: disable=no-member
#
#    def __str__(self):
#        """
#        When an instance of this class is used in a string context, return
#        self.sql
#        """
#        return self.sql
#
#
#class SelectClause(Clause):
#    """
#    Represents an sql select clause.
#    """
#    CLAUSE_TYPE = 'select'
#    INCLUDE_ALIASES = True
#
#
#class OrderByClause(Clause):
#    """
#    Represents an sql order by clause.
#    """
#    CLAUSE_TYPE = 'order by'
#    INCLUDE_ALIASES = False
#
#
#class GroupByClause(Clause):
#    """
#    Represents an sql group by clause.
#    """
#    CLAUSE_TYPE = 'group by'
#    INCLUDE_ALIASES = False
