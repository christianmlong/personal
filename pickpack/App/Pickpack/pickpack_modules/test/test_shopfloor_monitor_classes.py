"""
Tests for the Shopfloor Monitor utility classes

"""
# pylint: disable=missing-docstring,protected-access,invalid-name

from nose import tools

from Pickpack.pickpack_modules import pickpack_errors
from Pickpack.pickpack_modules import pickpack_constants

from Pickpack.pickpack_modules.shopfloor_monitor_classes import Column, make_column_structure

if pickpack_constants.SHOW_FULL_DIFF:
    # Force Nose to output the full diff
    from unittest import TestCase
    TestCase.maxDiff = None


def testColumn():
    a = Column('Column Def', 'Column_Name')
    tools.assert_equal(a.definition, "Column Def")
    tools.assert_equal(a.alias, "Column_Name")
    tools.assert_equal(a.definition_and_alias, "Column Def Column_Name")
    tools.assert_equal(a.name, "Column_Name")

def testColumnBlankName():
    with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
        a = Column('Column Def', "")                                            # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "Name can not be a zero-length string")

def testColumnNoneName():
    with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
        a = Column('Column Def', None)                                          # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "Name can not be None")

def testColumnNoName():
    with tools.assert_raises(TypeError) as context_mgr:
        a = Column('Column Def')                                                # pylint: disable=unused-variable,no-value-for-parameter
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "__init__() takes at least 3 arguments (2 given)")

def testColumnBadName():
    with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
        a = Column('Column Def', 'Column Name')                                 # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "Name can not contain spaces: name - 'Column Name'")

def testColumnNoArg():
    with tools.assert_raises(TypeError) as context_mgr:
        a = Column()                                                            # pylint: disable=unused-variable,no-value-for-parameter
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "__init__() takes at least 3 arguments (1 given)")

def testColumnBlankAlias():
    with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
        a = Column('Column Def', 'Column_Name', "")                             # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "If you supply alias, it can not be a zero-length string")

def testColumnSpaceAlias():
    with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
        a = Column('Column Def', 'Column_Name', "   ")                          # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "If you supply alias, it can not be a string with all spaces")

def testColumnWithAliasWithSpace():
    a = Column('Column Def', 'Column_Name', "Column Alias")
    tools.assert_equal(a.definition, "Column Def")
    tools.assert_equal(a.alias, "'Column Alias'")
    tools.assert_equal(a.definition_and_alias, "Column Def 'Column Alias'")
    tools.assert_equal(a.name, "Column_Name")

def testColumnWithAliasNoSpace():
    a = Column('Column Def', 'Column_Name', "Column_Alias")
    tools.assert_equal(a.definition, "Column Def")
    tools.assert_equal(a.alias, "Column_Alias")
    tools.assert_equal(a.definition_and_alias, "Column Def Column_Alias")
    tools.assert_equal(a.name, "Column_Name")

def testColumnNoAlias():
    a = Column('Column Def', 'Column_Name')
    tools.assert_equal(a.definition, "Column Def")
    tools.assert_equal(a.alias, "Column_Name")
    tools.assert_equal(a.definition_and_alias, "Column Def Column_Name")
    tools.assert_equal(a.name, "Column_Name")

def look_for_bad_indexing_behavior(a_column_structure):
    with tools.assert_raises(ValueError) as context_mgr:
        c = a_column_structure._indexof('a_non_existent_column')                # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "tuple.index(x): x not in tuple")

    with tools.assert_raises(ValueError) as context_mgr:
        c = a_column_structure._indexof('')                                     # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "tuple.index(x): x not in tuple")

    with tools.assert_raises(ValueError) as context_mgr:
        c = a_column_structure._indexof(None)                                   # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "tuple.index(x): x not in tuple")

    with tools.assert_raises(TypeError) as context_mgr:
        c = a_column_structure._indexof()                                       # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "_indexof() takes exactly 2 arguments (1 given)")

def test_column_structure_empty_arglist():
    a = make_column_structure()
    tools.assert_equal(a[:], ())
    tools.assert_equal(a._fields, ())
    tools.assert_equal(len(a), 0)
    with tools.assert_raises(ValueError) as context_mgr:
        c = a._indexof('column_name')                                           # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "tuple.index(x): x not in tuple")
    look_for_bad_indexing_behavior(a)

def test_column_structure_one_column():
    b = Column('Column Def', 'column_name')
    a = make_column_structure(b)
    tools.assert_is(a[0], b)
    tools.assert_is(a.column_name, b)
    tools.assert_equal(len(a), 1)
    tools.assert_equal(a._indexof('column_name'), 0)
    look_for_bad_indexing_behavior(a)

def test_column_structure_bad_name():
    b = Column('Column Def', '2column_name')
    with tools.assert_raises(ValueError) as context_mgr:
        a = make_column_structure(b)                                            # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "Type names and field names cannot start with a number: '2column_name'")

def test_column_structure_duplicate_name():
    b = Column('Column Def', 'column_name')
    c = Column('Column Def', 'column_name')
    with tools.assert_raises(ValueError) as context_mgr:
        a = make_column_structure(b, c)                                         # pylint: disable=unused-variable
    the_exception = context_mgr.exception
    tools.assert_equal(the_exception.message, "Encountered duplicate field name: 'column_name'")

def test_column_structure_two_columns():
    b = Column('Column Def', 'column_name')
    c = Column('Column Def2', 'column_name2')
    a = make_column_structure(b, c)
    tools.assert_is(a[0], b)
    tools.assert_is(a.column_name, b)
    tools.assert_is(a[1], c)
    tools.assert_is(a.column_name2, c)
    tools.assert_equal(len(a), 2)
    tools.assert_equal(a._indexof('column_name'), 0)
    tools.assert_equal(a._indexof('column_name2'), 1)
    look_for_bad_indexing_behavior(a)

#def test_extend_and_make_new():
#    b = Column('Column Def', 'column_name')
#    c = Column('Column Def2', 'column_name2')
#    a = make_column_structure(b)
#    tools.assert_is(a[0], b)
#    tools.assert_is(a.column_name, b)
#    tools.assert_equal(len(a), 1)
#    tools.assert_equal(a._indexof('column_name'), 0)
#
#    f = a._extend_and_make_new(c)
#    tools.assert_is(f[0], b)
#    tools.assert_is(f.column_name, b)
#    tools.assert_is(f[1], c)
#    tools.assert_is(f.column_name2, c)
#    tools.assert_equal(len(f), 2)
#    tools.assert_equal(f._indexof('column_name'), 0)
#    tools.assert_equal(f._indexof('column_name2'), 1)
#    look_for_bad_indexing_behavior(f)
#
#def test_append_and_make_new():
#    b = Column('Column Def', 'column_name')
#    c = Column('Column Def2', 'column_name2')
#
#    d = make_column_structure(b)
#    tools.assert_is(d[0], b)
#    tools.assert_is(d.column_name, b)
#    tools.assert_equal(len(d), 1)
#    tools.assert_equal(d._indexof('column_name'), 0)
#
#    e = make_column_structure(c)
#    tools.assert_is(e[0], c)
#    tools.assert_is(e.column_name2, c)
#    tools.assert_equal(len(e), 1)
#    tools.assert_equal(e._indexof('column_name2'), 0)
#
#    f = d._append_and_make_new(e)
#    tools.assert_is(f[0], b)
#    tools.assert_is(f.column_name, b)
#    tools.assert_is(f[1], c)
#    tools.assert_is(f.column_name2, c)
#    tools.assert_equal(len(f), 2)
#    tools.assert_equal(f._indexof('column_name'), 0)
#    tools.assert_equal(f._indexof('column_name2'), 1)
#    look_for_bad_indexing_behavior(f)
#
#    g = e._append_and_make_new(d)
#    tools.assert_is(g[0], c)
#    tools.assert_is(g.column_name2, c)
#    tools.assert_is(g[1], b)
#    tools.assert_is(g.column_name, b)
#    tools.assert_equal(len(g), 2)
#    tools.assert_equal(g._indexof('column_name2'), 0)
#    tools.assert_equal(g._indexof('column_name'), 1)
#    look_for_bad_indexing_behavior(g)


def test_adding_two_column_structure_objects_with_the_plus_sign():
    b = Column('Column Def', 'column_name')
    c = Column('Column Def2', 'column_name2')

    d = make_column_structure(b)
    tools.assert_is(d[0], b)
    tools.assert_is(d.column_name, b)
    tools.assert_equal(len(d), 1)
    tools.assert_equal(d._indexof('column_name'), 0)

    e = make_column_structure(c)
    tools.assert_is(e[0], c)
    tools.assert_is(e.column_name2, c)
    tools.assert_equal(len(e), 1)
    tools.assert_equal(e._indexof('column_name2'), 0)

    f = d + e
    tools.assert_is(f[0], b)
    tools.assert_is(f.column_name, b)
    tools.assert_is(f[1], c)
    tools.assert_is(f.column_name2, c)
    tools.assert_equal(len(f), 2)
    tools.assert_equal(f._indexof('column_name'), 0)
    tools.assert_equal(f._indexof('column_name2'), 1)
    look_for_bad_indexing_behavior(f)

    g = e + d
    tools.assert_is(g[0], c)
    tools.assert_is(g.column_name2, c)
    tools.assert_is(g[1], b)
    tools.assert_is(g.column_name, b)
    tools.assert_equal(len(g), 2)
    tools.assert_equal(g._indexof('column_name2'), 0)
    tools.assert_equal(g._indexof('column_name'), 1)
    look_for_bad_indexing_behavior(g)

def test_adding_a_column_to_a_column_structure_object_with_the_plus_sign():
    b = Column('Column Def', 'column_name')
    c = Column('Column Def2', 'column_name2')

    d = make_column_structure(b)
    tools.assert_is(d[0], b)
    tools.assert_is(d.column_name, b)
    tools.assert_equal(len(d), 1)
    tools.assert_equal(d._indexof('column_name'), 0)

    f = d + c
    tools.assert_is(f[0], b)
    tools.assert_is(f.column_name, b)
    tools.assert_is(f[1], c)
    tools.assert_is(f.column_name2, c)
    tools.assert_equal(len(f), 2)
    tools.assert_equal(f._indexof('column_name'), 0)
    tools.assert_equal(f._indexof('column_name2'), 1)
    look_for_bad_indexing_behavior(f)

def test_adding_a_column_to_the_front_of_a_column_structure_object_with_the_plus_sign():
    b = Column('Column Def', 'column_name')
    c = Column('Column Def2', 'column_name2')

    d = make_column_structure(b)
    tools.assert_is(d[0], b)
    tools.assert_is(d.column_name, b)
    tools.assert_equal(len(d), 1)
    tools.assert_equal(d._indexof('column_name'), 0)

    g = c + d
    tools.assert_equal(g.__class__.__name__, 'ColumnStructure')
    tools.assert_is(g[0], c)
    tools.assert_is(g.column_name2, c)
    tools.assert_is(g[1], b)
    tools.assert_is(g.column_name, b)
    tools.assert_equal(len(g), 2)
    tools.assert_equal(g._indexof('column_name2'), 0)
    tools.assert_equal(g._indexof('column_name'), 1)
    look_for_bad_indexing_behavior(g)

def testSelectClause():
    b = Column('emp.name', 'name')
    c = Column('sum(emp.wages)', 'wages')
    a = make_column_structure(b, c)
    expected_sql = 'select emp.name name,\nsum(emp.wages) wages'
    tools.assert_equal(a._select_clause_definitions_and_aliases, expected_sql)

def testSelectClauseWithAliasNoSpace():
    b = Column('emp.name', 'name', 'employee_name')
    c = Column('sum(emp.wages)', 'wages', 'total_wages')
    a = make_column_structure(b, c)
    expected_sql = 'select emp.name employee_name,\nsum(emp.wages) total_wages'
    tools.assert_equal(a._select_clause_definitions_and_aliases, expected_sql)

def testSelectClauseWithAliasWithSpace():
    b = Column('emp.name', 'name', 'Employee Name')
    c = Column('sum(emp.wages)', 'wages', 'Total Wages')
    a = make_column_structure(b, c)
    expected_sql = "select emp.name 'Employee Name',\nsum(emp.wages) 'Total Wages'"
    tools.assert_equal(a._select_clause_definitions_and_aliases, expected_sql)

def testSelectClauseJustDefs():
    b = Column('emp.name', 'name', 'employee_name')
    c = Column('sum(emp.wages)', 'wages', 'total_wages')
    a = make_column_structure(b, c)
    expected_sql = 'select emp.name,\nsum(emp.wages)'
    tools.assert_equal(a._select_clause_just_definitions, expected_sql)

def testSelectClauseJustAliases():
    b = Column('emp.name', 'name', 'employee_name')
    c = Column('sum(emp.wages)', 'wages', 'total_wages')
    a = make_column_structure(b, c)
    expected_sql = 'select employee_name, total_wages'
    tools.assert_equal(a._select_clause_just_aliases, expected_sql)

def testSelectClauseJustAliasesWithSpace():
    b = Column('emp.name', 'name', 'Employee Name')
    c = Column('sum(emp.wages)', 'wages', 'Total Wages')
    a = make_column_structure(b, c)
    expected_sql = "select 'Employee Name', 'Total Wages'"
    tools.assert_equal(a._select_clause_just_aliases, expected_sql)

def testOrderByClauseDefs():
    b = Column('emp.name', 'name')
    c = Column('sum(emp.wages)', 'wages')
    a = make_column_structure(b, c)
    expected_sql = 'order by emp.name,\nsum(emp.wages)'
    tools.assert_equal(a._order_by_clause_definitions, expected_sql)

def testOrderByClauseAliases():
    b = Column('emp.name', 'name')
    c = Column('sum(emp.wages)', 'wages')
    a = make_column_structure(b, c)
    expected_sql = 'order by name, wages'
    tools.assert_equal(a._order_by_clause_aliases, expected_sql)

def testOrderByClauseAliasesNoSpace():
    b = Column('emp.name', 'name', 'employee_name')
    c = Column('sum(emp.wages)', 'wages', 'total_wages')
    a = make_column_structure(b, c)
    expected_sql = 'order by employee_name, total_wages'
    tools.assert_equal(a._order_by_clause_aliases, expected_sql)

def testOrderByClauseAliasesWithSpace():
    b = Column('emp.name', 'name', 'Employee Name')
    c = Column('sum(emp.wages)', 'wages', 'Total Wages')
    a = make_column_structure(b, c)
    expected_sql = "order by 'Employee Name', 'Total Wages'"
    tools.assert_equal(a._order_by_clause_aliases, expected_sql)

def testGroupByClauseDefs():
    b = Column('emp.name', 'name')
    c = Column('sum(emp.wages)', 'wages')
    a = make_column_structure(b, c)
    expected_sql = 'group by emp.name,\nsum(emp.wages)'
    tools.assert_equal(a._group_by_clause_definitions, expected_sql)

def testGroupByClauseAliases():
    b = Column('emp.name', 'name')
    c = Column('sum(emp.wages)', 'wages')
    a = make_column_structure(b, c)
    expected_sql = 'group by name, wages'
    tools.assert_equal(a._group_by_clause_aliases, expected_sql)

def testGroupByClauseAliasesNoSpace():
    b = Column('emp.name', 'name', 'employee_name')
    c = Column('sum(emp.wages)', 'wages', 'total_wages')
    a = make_column_structure(b, c)
    expected_sql = 'group by employee_name, total_wages'
    tools.assert_equal(a._group_by_clause_aliases, expected_sql)

def testGroupByClauseAliasesWithSpace():
    b = Column('emp.name', 'name', 'Employee Name')
    c = Column('sum(emp.wages)', 'wages', 'Total Wages')
    a = make_column_structure(b, c)
    expected_sql = "group by 'Employee Name', 'Total Wages'"
    tools.assert_equal(a._group_by_clause_aliases, expected_sql)



















#
