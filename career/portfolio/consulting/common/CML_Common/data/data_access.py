"""
data_access.py

Common Data Services

Provides database access for any application.


Christian M. Long, developer

Initial implementation: September 10, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import shared modules
from CML_Common.error import error
from CML_Common.error import error_objects
from CML_Common.utility import utl_functions

# Import data connection object
from CML_Common.data.data_connection import data_connection_object as db

# Import debug utility object
from CML_Common.error.debug import debug_utility_object as debugObj


#    Transaction functions    ++++++++++++++++++++++++++++++++++++++++++++++++++
def transactionManager(function_to_run,
                       params = (),
                       treat_param_sequence_as_one_parameter = False,
                      ):
    """
    Runs the specified function as a transaction; that is, either the operations
    in function_to_run all succeed or, if any operation fails, all the operations
    in function_to_run are rolled back. If the transaction does get rolled back,
    this function will raise an error.

    Functions must be specially written to work inside this transaction manager.
    The "function to run" must take a <DBAPI module> Connection object as its
    first parameter. A brand new connection object will be created just for this
    transaction, and that connection will be supplied to the "function to run".

    A parameter tuple can be passed in to supply any additional arguments for
    the call to function_to_run. Also, a single parameter of type int, str, bool
    or float can be passed in. It will be wrapped in a one-element tuple
    automatically. If treat_param_sequence_as_one_parameter is True, then if
    params is a sequence, the whole sequence will be passed to the called
    function in one argument, instead of getting smeared out in to multiple
    arguments with the * symbol.

    Important Note: When passing the function in to the transactionManager, do
    not include parentheses after the passed function's name. In example below,
    notice that myFunction is passed in without trailing parentheses. This is
    because we are passing in a reference to a function. This reference will
    later be used to call the function inside the transaction. Were we to
    include parentheses after the function name, we would be passing in the
    results of the function call instead of a reference to the function.

    ---

    Sample calls:
    A function with two parameters requires a two-element tuple.
        params = ("Here's my parameter", "Here's another")
        transactionManager(myFunction, params)

    When the function takes one parameter, pass it in directly.
        transactionManager(myOtherFunction, 98.6)

    When the function has no parameters, omit the params argument altogether.
        transactionManager(yetAnotherFunction)

    Note that we do not allow myFunction to return a value. We keep
    transactional write operations separate from read operations.
        result = transactionManager(myFunction, params)
        ^^^^^^^^ Not allowed.

    ---

    Note that in some cases (large or complex transactions) it may be useful to
    write a wrapper function which serves to contain all the calls to the other
    functions needed in the transaction. However, in simple cases, no wrapper
    function is needed and you can pass the target function directly to the
    transactionManager, as in the example below.

    params = (usr,
              seq_no,
              message,
              None,
             )

    data_access.transactionManager(mra_data.archiveQueueItem, params)

    Or, another example:

    sql = '''
          UPDATE     item_planning_vw
          SET        max_stock = :1
          WHERE      item_no = :2
          '''
    sql_params = (max_qty, item_number)    # Parameters for the SQL statement
    execute_sql_args = (sql, sql_params)   # Arguments for the call to data_access.executeSQL,
                                           # wrapped up in a tuple
    data_access.transactionManager(data_access.executeSQL, execute_sql_args)

    ---

    """
    #debugObj.debugPrint(debug_threshhold = debugObj.DebugLevelConstants.Heavy,
    #                    item = str(function_to_run),
    #                    item_list = params)

    # The asterisk in *params indicates that a tuple is being passed in.
    # Instead of passing in the tuple as a tuple, the asterisk instructs Python
    # to pass the elements of the tuple as positional arguments to the function.
    #
    # In the case of functions that take only one parameter, we still insist
    # that that one parameter be wrapped up inside a one-element tuple.
    # Otherwise, for example, in the case where a function is called that
    # requires one string parameter, we would mistakenly treat the string as a
    # sequence, and spread the letters of the string out into individual
    # parameters.
    #
    # For simple functions, it looks like there is a lot of excess packing and
    # unpacking of parameter tuples. This packing and unpacking is required so
    # we can support more complex transactions, which calculate and manipulate
    # individual parameters during the course of the transaction. In other
    # words, we can't just pack all the parameters up into a tuple right away,
    # and pipeline this tuple all the way through to the call to
    # <DBAPI module>.cursor.execute().
    #
    # We pack and unpack so that more complex transactions can manipulate
    # individual parameters. Therefore, we can't rewrite called functions to
    # pass a pipelined params straight to (for example) data_access.executeSQL,
    # and thus we can't eliminate the need for the * here in the call to
    # function_to_run.

    # If a single parameter was passed in, wrap it inside a one-element tuple.
    #
    # Note: this operates on the parameter(s) passed to the transactionManager,
    # and which the transactionManager will then pass on to the transaction
    # wrapper (function_to_run).
    #
    # We also call wrapScalarValue at other points in the process. For example,
    # when we are calling a stored procedure using ProcedureCaller, we wrap any
    # single parameters passed to just that procedure. Also, when we are
    # converting parameters, we wrap any single parameters that we find.
    #
    # So, it's ok to call wrapScalarValue at multiple levels. We call it here at
    # a high level (the overall transaction). We call it at a medium level
    # (individual procedure calls) and we call it at a low level (when
    # converting each row of a param sequence so that it matches paramstyle)
    params = utl_functions.wrapScalarValue(params)

    # Make a new connection to the APlus database just for this transaction
    transaction_connection = db.newAplusDbConnection()

    try:
        if treat_param_sequence_as_one_parameter:
            should_be_none = function_to_run(transaction_connection, params)
        else:
            should_be_none = function_to_run(transaction_connection, *params)

        # We don't allow return values, to keep it simple
        if should_be_none is not None:
            err_msg = "No return values allowed from transactionManager"
            raise error.ApplicationError(err_msg)

    except (
            # HandleableDatabaseError is a base class for a number of errors,
            # such as RollbackTransaction, NdsError, etc.
            error.HandleableDatabaseError,

            # DbapiModuleError is a base class for a number of errors,
            # such as MssqlError, Db2Error, etc.
            error.DbapiModuleError,
           ):
        # We caught a reasonable exception, one we would expect in the case of a
        # database failure such as No Data Found, or Duplicate Key. Not good,
        # but not completely unexpected. Transaction failed; rollback changes,
        # and then reraise error so that the calling process can handle it and
        # be informed that an error occured.
        rollbackChanges(transaction_connection)
        raise

    except error_objects.external_handleable_exceptions_object.exceptions as ex:             # pylint: disable=catching-non-exception
        # We caught an exception that was registered by client code as being
        # 'handleable'. Transaction failed; rollback changes, and then reraise
        # error so that the calling process can handle it and be informed that
        # an error occured.
        #
        # Note that if the client code does not register any exceptions as
        # handleable, we will never fall in to this except clause.
        #
        # Here's why: if no exceptions were registered,
        # external_handleable_exceptions_object.exceptions returns an empty tuple.
        #
        # This:
        #     except ():
        # catches no exceptions, whereas this:
        #     except:
        # catches all exceptions.

        rollbackChanges(transaction_connection)

        # Transform the exception, to mark its trip through this database
        # handling code. This allows client code to catch and handle it
        # differently than the same exception raised in client code that did not
        # make a trip through the database code.
        raise error.ExternalHandleableError(ex)

    except Exception as original_error:
        # Unexpected error; rollback changes
        rollbackChanges(transaction_connection)
        # Transaction rolled back; reraise whatever unexpected error caused the
        # problem in the first place. This error will be handled at a higher
        # level.
        if debugObj.debug_level >= debugObj.DebugLevelConstants.Medium:
            print "Original exception in here!@#@"
            import traceback
            traceback.print_exc()
            print "^^^^^^^^^^^^"
            for i in original_error.args:
                print i
        raise

    else:
        # Success. Function ran OK; commit changes now
        commitChanges(transaction_connection)

def commitChanges(conn):
    """
    Commits all changes to the database from the specified connection. Also,
    closes the database connection.
    """
    # Close the connection even if commit fails
    try:
        conn.commit()
    finally:
        conn.close()

def rollbackChanges(conn):
    """
    Rolls back all changes to the database from the specified connection since
    the last commit. Also, closes the database.
    """
    # Close the connection even if rollback fails
    try:
        conn.rollback()
    finally:
        conn.close()

def registerHandleableExceptions(handleable_exceptions):
    """
    This is used by client code to register some of its exceptions as
    handleable. This allows the data_access module to treat these exceptions as
    handleable instead of freaking out.
    """
    error_objects.external_handleable_exceptions_object.append(handleable_exceptions)


#    Public basic data access functions     ++++++++++++++++++++++++++++++++++
# These functions provide an easy interface to basic data access functionality.
# All the rest of the MRA application calls these simple functions for data
# access and updates.
#
# The executeSQL function is meant to be executed as part of a transaction, it
# requires that a connection object be passsed in (the temporary connection that
# is being used for that transaction).
#
# The other basic data access functions are non-transactional, they are used for
# read-only access, and they use the shared persistent database connection
# object that we created at initialization. These read-only functions are:
# exists, existsExactlyOneRow, fetchExactlyOneRow, fetchZeroOrOneRow,
# fetchOneRowOfMany, fetchAllRows, fetchScalarValue, fetchVector, fetchCount.

def exists(conn,
           sql,
           params = None,
          ):
    """
    Generic SQL execution code for seeing if a matching record exists in the
    database. Passes arguments to fetchOneRowOfMany for data access. Returns
    True if data found, False otherwise. More than one matching row may exist.
    """
    data = fetchOneRowOfMany(conn, sql, params)
    if data is not None:
        success = True
    else:
        success = False
    return success

def existsExactlyOneRow(conn,
                        sql,
                        params = None,
                       ):
    """
    Generic SQL execution code for seeing if exactly one matching record exists
    in the database. Passes arguments to fetchZeroOrOneRow for data access.
    Requires an SQL statement, and a sequence of parameters for the SQL
    statement if any are needed. Returns True if exactly one row found, False if
    no rows are found, and raises error.DatabaseKeyError if more than one
    row is found.
    """
    data = fetchZeroOrOneRow(conn, sql, params)
    if data is None:
        success = False
    else:
        success = True
    return success

def fetchScalarValue(conn,
                     sql,
                     params = None,
                    ):
    """
    Generic SQL execution code for fetching a single (scalar) value, such as is
    returned by select count(*). If conn is passed as None, this function uses
    the shared persistent database connection created at startup, otherwise uses
    the passed-in connection. Requires an SQL statement, and a sequence of
    parameters for the SQL statement if any are needed. Returns None if no data
    found. Otherwise, returns the value.
    """
    data = fetchZeroOrOneRow(conn, sql, params)
    if data is not None:
        # A value was returned. Unpack it from its list, and return it as a
        # scalar value.
        data = data[0]
    return data

def fetchVector(conn,
                sql,
                params = None,
               ):
    """
    Generic SQL execution code for fetching a one-dimensional array of values (a
    vector) from a query that has only one column and returns zero to many rows.
    If conn is passed as None, this function uses the shared persistent database
    connection created at startup, otherwise uses the passed-in connection.
    Requires an SQL statement, and a sequence of parameters for the SQL
    statement if any are needed. Returns None if no data found. Otherwise,
    returns the values in a single, non-nested list.
    """
    data = fetchAllRows(conn, sql, params)
    if data is None:
        # No data.  Return None
        return None
    else:
        # Some values were returned. Unnest the values from the nested list, and
        # return.
        return [row[0] for row in data]

def fetchCount(conn,
               sql,
               params = None,
              ):
    """
    Generic SQL execution code for fetching the value of count(*). If conn is
    passed as None, this function uses the shared persistent database connection
    created at startup, otherwise uses the passed-in connection. Requires an SQL
    statement, and a sequence of parameters for the SQL statement if any are
    needed. Raises error.NdsError if no data found.
    """
    data = fetchScalarValue(conn, sql, params)
    if data is None:
        err_msg = "No data returned from count(*).\n%s" % sql
        raise error.Db2Error(err_msg)
    # This will raise TypeError if the conversion can not happen.
    return int(data)

def fetchExactlyOneRow(conn,
                       sql,
                       params = None,
                      ):
    """
    Generic SQL execution code for fetching one row of data. If conn is passed
    as None, this function uses the shared persistent database connection
    created at startup, otherwise uses the passed-in connection.

    Raises error.NoDataFound if no data was found. Raises
    error.DatabaseKeyError if more than one row was found. Otherwise,
    returns the data.
    """
    data = fetchZeroOrOneRow(conn, sql, params)
    if data is None:
        raise error.NoDataFound("No data found")
    return data

# ==

def fetchZeroOrOneRow(conn,
                      sql,
                      params = None,
                     ):
    """
    Generic SQL execution code for fetching one row of data. If conn is passed
    as None, this function uses the shared persistent database connection
    created at startup, otherwise uses the passed-in connection.

    Returns None if no data found. Raises error.DatabaseKeyError if more
    than one row was found. Otherwise, returns the data.
    """
    a_cursor = executor.executeSQL(conn, sql, params)
    data = a_cursor.fetchone()

    # Check for more than one row returned
    another_row = a_cursor.fetchone()
    if another_row is not None:
        err_msg = "More than one row returned.\n%s\n%s" % (data, another_row)
        raise error.DatabaseKeyError(err_msg)

    a_cursor.close()
    return scrubDataIfNeeded(conn, data)

def fetchOneRowOfMany(conn,
                      sql,
                      params = None,
                     ):
    """
    Generic SQL execution code for fetching one row of data out of a possilble
    multi-row result set. If conn is passed as None, this function uses the
    shared persistent database connection created at startup, otherwise uses the
    passed-in connection.

    Returns None if no data found. Otherwise, returns the data. Does not raise
    an error if more than one row was found.
    """
    a_cursor = executor.executeSQL(conn, sql, params)

    # From cx_Oracle docs for cursor.fetchone():
    #     Fetch the next row of a query result set, returning a single tuple or
    #     None when no more data is available.
    data = a_cursor.fetchone()
    a_cursor.close()
    return scrubDataIfNeeded(conn, data)

def fetchAllRows(conn,
                 sql,
                 params = None,
                ):
    """
    Generic SQL execution code for fetching many rows of data. If conn is passed
    as None, this function uses the shared persistent database connection
    created at startup, otherwise uses the passed-in connection.

    Returns None if no data found. Otherwise, returns the data as a list of
    lists.
    """
    a_cursor = executor.executeSQL(conn, sql, params)

    # From cx_Oracle docs for cursor.fetchall():
    #    Fetch all (remaining) rows of a query result, returning them as a list
    #    of tuples. An empty list is returned if no more rows are available.
    data = a_cursor.fetchall()
    a_cursor.close()
    if data == []:
        data = None
    return scrubDataIfNeeded(conn, data)

def executeSQL(conn,
               sql,
               params = None,
              ):
    """
    Generic SQL execution code for INSERT, UPDATE and DELETE. Must be run inside
    the transactionManager and must receive an open <DBAPI module> connection
    object.

    Commit or rollback are managed by the transactionManager, so no commits or
    rollbacks happen here. If params is None, then just the straight SQL is
    executed, without parameters. No return value.
    """
    executor.executeSQL(conn,
                sql,
                params,
                conn_optional = False,
                return_cursor = False,
               )

def multiExecuteSQL(conn,
                    sql,
                    param_sequence,
                   ):
    """
    Repeatedly executes an SQL statement based on a sequence of lists of input
    values. For example, if a three element sequence is passed in, where each
    element is itself a list containing all the necessary parameters for one SQL
    execution, then three SQL executions are carried out. Must be run inside the
    transactionManager and must receive an open <DBAPI module> connection
    object, an SQL statement, and a sequence of lists of parameters for the SQL
    executions. Commit or rollback are managed by the transactionManager, so no
    commits or rollbacks happen here. No return value.
    """
    executor.executeSQL(conn,
                sql,
                param_sequence,
                conn_optional = False,
                return_cursor = False,
                multi_row = True,
               )


#    Private utility functions and classes    ++++++++++++++++++++++++++++++++++

class SqlExecutor(object):
    """
    Used to execute sql queries against the database.
    """
    def __init__(self):
        self.exceptions_to_wrap = self.calculateExceptionsToWrap()

    @staticmethod
    def calculateExceptionsToWrap():
        """
        We catch certain database exceptions and wrap them in our own errors.
        This makes it easier for clients to handle errors, by making hte errors
        we throw more predictable and consistent.

        Here we build a tupe of the exceptions we should catch, based on which
        dabase connection modules are loaded.
        """
        exceptions_to_wrap = []
        #if db.mssqlDbapiModule is not None:
        #    exceptions_to_wrap.append(db.mssqlDbapiModule.DatabaseError)
        if db.iSeriesDbapiModule is not None:
            exceptions_to_wrap.append(db.iSeriesDbapiModule.DatabaseError)

        return tuple(exceptions_to_wrap)

    def executeSQL(self,
                   conn,
                   sql,
                   params,
                   conn_optional = True,
                   return_cursor = True,
                   multi_row = False,
                  ):
        """
        Executes SQL and optionally returns a cursor ready for reading.

        If conn_optional is True and conn is passed as None, this function uses
        the shared persistent database connection created at startup, otherwise
        uses the passed-in connection.

        If conn_optional is False and conn is passed as None, raises
        error.ApplicationError.

        If return_cursor is False, the function closes the cursor after
        executing the SQL, and there is no return value. If return_cursor is
        True, it returns an open <DBAPI module> cursor. The calling function
        must call cursor.close()

        If multi_row is True, uses cursor.executemany.
        """
        #debugObj.debugBreakpoint(debugObj.DebugLevelConstants.ExtraHeavy)

        # Use persistent connection if no connection passed in and conn_optional
        # is True.
        if conn is None and not conn_optional:
            err_msg = "If conn_optional is False, a connection must be passed in."
            raise error.ApplicationError(err_msg)

        a_cursor = conn.cursor()

        if multi_row:
            if params is None:
                err_msg = "If multi_row is True, a sequence of parameters must be passed in."
                raise error.ApplicationError(err_msg)
            function_to_run = a_cursor.executemany
        else:
            function_to_run = a_cursor.execute

        if params is not None:
            params = convertParamsToMatchParamstyle(params,
                                                    #conn,
                                                    multi_row,
                                                   )

        try:
            if params is None:
                function_to_run(sql)
            else:
                function_to_run(sql,
                                params,
                               )

        except self.exceptions_to_wrap as ex:
            raise wrapDbException(ex)

        if return_cursor:
            return a_cursor
        else:
            a_cursor.close()

# Here we make one module-level variable to hold one instance of the SqlExecutor
# class.
executor = SqlExecutor()

def wrapDbException(ex):
    """
    Here we take a DatabaseError from a python DBAPI-compliant module (e.g.
    cx_Oracle, pymssql, pyodbc) and we wrap it inside a custom exception from
    the error module. This allows the calling procedure to handle the
    error more easily.
    """
    ## Determine which module raised the error. Set our custom error accordingly.
    #custom_db_exception = chooseByDbapiModule(ex,
    #                                          [error.MssqlError,
    #                                           error.Db2Error,
    #                                          ],
    #                                         )
    custom_db_exception = error.Db2Error

    ex_args = utl_functions.wrapScalarValue(ex.args)

    if ex_args is None:
        return custom_db_exception("No error arguments")
    else:
        return custom_db_exception(*ex_args)

def convertParamsToMatchParamstyle(params,
                                   #conn,
                                   multi_row = False,
                                  ):
    """
    Different databases have different paramstyles. However, rather than change
    all the query code, I just adapt to the different paramstyles. This handles
    the pymssql paramstyle as well. Pass multi_row = True for use with
    cursor.executemany.
    """

    # pymssql connection to sales database uses the 'pyformat' paramstyle.
    # pyodbc connection to Aplus database uses the 'qmark' paramstyle.

    #paramstyle = chooseByDbapiModule(conn,
    #                                 [db.mssqlDbapiModule,
    #                                  db.iSeriesDbapiModule,
    #                                 ],
    #                                ).paramstyle

    paramstyle = db.iSeriesDbapiModule.paramstyle

    if (paramstyle == 'named'
        or paramstyle == 'pyformat'
       ):
        if multi_row:
            return [_convertOneParamRow(param_row) for param_row in params]
        else:
            return _convertOneParamRow(params)
    elif (paramstyle == 'numeric'
          or paramstyle == 'qmark'
         ):
        # Do nothing, the queries and parameters are already formatted for the
        # 'numeric' paramstyle.
        #
        # The 'qmark' param style uses the same parameter format as 'numeric'.
        # However, the queries must be formatted with question marks as
        # placeholders for the data.
        return params
    else:
        # Other paramstyles are not supported
        err_msg = "Unsupported paramstyle %s" % paramstyle
        raise error.ApplicationError(err_msg)

def _convertOneParamRow(params):
    # Convert our parameters so they can be used with the 'named' or 'pyformat'
    # paramstyles.
    #
    # The python enumerate() function would work here, except that it uses
    # integers as the indexes. For example:
    #    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    #    list(enumerate(seasons, start=1))
    #    [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
    #
    # We need strings for indexes, so instead of using enumerate() we build the
    # sequence we need using zip() and range().
    #
    # Note: see the body of the transactionManager function for an explanation
    # of why we need multiple calls to wrapScalarValue at different layers of
    # the process.
    params = utl_functions.wrapScalarValue(params)
    start = 1
    stop = len(params) + 1
    indexes = (str(index) for index in range(start, stop))
    return dict(zip(indexes, params))

#def chooseByDbapiModule(obj,
#                        list_of_options,
#                       ):
#    """
#    Polymorphically, we can handle objects that originate in several different
#    DBAPI2 modules (cx_Oracle, pymssql, pyodbc, etc.). Sometimes, we are given
#    an object of unknown origin, and we need to decide which DBAPI2 module it
#    came from. This function does just that. Supply an object from a DBAPI2
#    module, and a list of choices, and it will return the list item that
#    corresponds to the DBAPI2 module from which it arose.
#
#    The list must be in this order [cx_Oracle, pymssql, pyodbc]
#    """
#    try:
#        module = obj.__module__
#    except AttributeError:
#        module = obj.__class__.__module__
#
#    if (db.mssqlDbapiModule is not None
#          and module == db.mssqlDbapiModule.__name__
#         ):
#        return list_of_options[0]
#    elif (db.iSeriesDbapiModule is not None
#          and module == db.iSeriesDbapiModule.__name__
#         ):
#        return list_of_options[1]
#    else:
#        err_msg = "Unknown DBAPI2 module %s" % module
#        raise error.ApplicationError(err_msg)

def scrubDataIfNeeded(conn,
                      data,
                     ):
    """
    When you run queries against APlus, you get trailing whitespace on your
    strings. Here we strip that whitespace, but only if the data came from
    APlus.

    Also, integer numbers are returned as decimals. Here I convert them to
    int().
    """
    if conn is None:
        return data

    # Just scrub everything
    return _recursiveScrub(data)

def _recursiveScrub(data):
    import decimal

    if isinstance(data, str):
        clean = data.strip()
        if len(clean) == 0:
            clean = None
        return clean
    elif isinstance(data, unicode):
        ascii_string = data.encode('ascii', 'ignore')
        clean = ascii_string.strip()
        if len(clean) == 0:
            clean = None
        return clean
    elif isinstance(data, decimal.Decimal):
        temp = int(data)
        if data == temp:
            return temp
        else:
            return float(data)
    elif isinstance(data, (list, tuple)):
        clean = []
        for item in data:
            clean.append(_recursiveScrub(item))
        if isinstance(data, tuple):
            clean = tuple(clean)
        return clean
    elif (db.iSeriesDbapiModule is not None
          and isinstance(data, db.iSeriesDbapiModule.Row)
         ):
        clean = []
        for item in data:
            clean.append(_recursiveScrub(item))
        return clean
    else:
        return data


#

# OLD code
    #debugObj.debugPrint(debug_threshhold = debugObj.DebugLevelConstants.Heavy,
    #                    item = "Inside executeSQL\n %s" % sql,
    #                    item_list = params)
