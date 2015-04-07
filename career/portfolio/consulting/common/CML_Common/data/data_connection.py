"""
data_connection.py

Provides database connection objects for applications.


Christian M. Long, developer

Initial implementation: September 5, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import shared modules
from CML_Common.utility import utl_decorators
from CML_Common.error import error


class BaseDatabaseConnector(object):
    """
    A base class for classes used to store and render database connection
    information.
    """
    def __init__(self, dbapi_module):
        self._dbapi_module = dbapi_module

    #    Properties                  +++++++++++++++++++
    # pylint: disable=E0202, E0211, W0212, C0111
    @utl_decorators.makeProperty
    def dbapi_module():
        doc = """
              A named constant, indicating which dbapi module should be used to
              make the connection to the database.
              """
        def fget(self):
            return self._dbapi_module
        return locals()
    # pylint: enable=E0202, E0211, W0212, C0111


#class ConnStringDatabaseConnector(BaseDatabaseConnector):
#    """
#    A base class for classes used to store and render database connection
#    information, for use with databases where we connect via a connection
#    string.
#    """
#    def __init__(self,
#                 dbapi_module,
#                 ):
#        # Call base class __init__. Note: I don't use super(), I do it the
#        # traditional way as shown here.
#        BaseDatabaseConnector.__init__(self, dbapi_module)


class ODBCDatabaseConnector(BaseDatabaseConnector):
    """
    A base class for classes used to store and render database connection
    information, for use with databases where we connect via ODBC.
    """
    def __init__(self,
                 dbapi_module,
                 dsn,
                 ):
        # Call base class __init__. Note: I don't use super(), I do it the
        # traditional way as shown here.
        BaseDatabaseConnector.__init__(self, dbapi_module)
        self.dsn = dsn


#class SalesDatabaseConnector(BaseDatabaseConnector):
#    """
#    A class to store database connection parameters for the Sales database, and
#    render them in the appropriate format for the dbapi module's connect()
#    function.
#    """
#    def __init__(self, dbapi_module, database):
#        # Call base class __init__. Note: I don't use super(), I do it the
#        # traditional way as shown here.
#        BaseDatabaseConnector.__init__(self,
#                                       dbapi_module,
#                                      )
#
#        # Decide on which values we are going to pass to our base class'
#        # constructor.
#        if database == self.Constants.Database.Sales_Test:
#            host = 'abcd'
#        elif database == self.Constants.Database.Sales_Prod:
#            host = 'efgh'
#        else:
#            err_msg = "Unrecognized option"
#            raise error.ApplicationError(err_msg)
#
#        self.dictionary = {'host' : '%s:1433' % host,
#                           'database' : 'database',
#                           'user' : 'none',
#                           'password' : 'none',
#                          }
#
#    #    Named constants             +++++++++++++++++++
#    # pylint: disable=W0232
#    #
#    # Locally disabled pylint messages
#    #    W0232: Class has no __init__ method
#    class Constants:
#        """
#        Named constants for use by this class, in convenient dot notation.
#        Clients can address these constants using this form:
#        the_object.Constants.DbapiModule.pymssql
#        """
#        class DbapiModule:
#            """
#            Named constants for specifying which dbapi module to use to connect
#            to a database. pymssql, etc.
#            """
#            _magicNumber = 18000
#            pymssql            = 0 + _magicNumber
#
#        class Database:
#            """
#            Named constants for specifying which database to connect to.
#            """
#            _magicNumber = 18500
#            Sales_Test          = 0 + _magicNumber
#            Sales_Prod          = 1 + _magicNumber
#    # pylint: enable=W0232
#
#    #    Methods                     ++++++++++++++++++
#    def renderConnectionInfo(self):
#        """
#        Builds and returns the connnection info in the format required by the
#        dbapi connection object.
#        """
#        return self.dictionary


class AplusDatabaseConnector(ODBCDatabaseConnector):
    """
    A class to store database connection parameters for the APlus database (on
    the AS400), and render them in the appropriate format for the dbapi
    module's connect() function.
    """
    def __init__(self, dbapi_module, database):

        # Decide on which values we are going to pass to our base class'
        # constructor.
        if database == self.Constants.Database.APlus_Test:
            dsn = 'Test'
        elif database == self.Constants.Database.APlus_Prod:
            dsn = 'Prod'
        else:
            err_msg = "Unrecognized option"
            raise error.ApplicationError(err_msg)

        # Call base class __init__. Note: I don't use super(), I do it the
        # traditional way as shown here.
        ODBCDatabaseConnector.__init__(self,
                                       dbapi_module,
                                       dsn,
                                      )

    #    Named constants             +++++++++++++++++++
    # pylint: disable=W0232
    #
    # Locally disabled pylint messages
    #    W0232: Class has no __init__ method
    class Constants(object):
        """
        Named constants for use by this class, in convenient dot notation.
        Clients can address these constants using this form:
        the_object.Constants.DbapiModule.pyodbc
        """
        class DbapiModule(object):
            """
            Named constants for specifying which dbapi module to use to connect
            to a database. pyodbc, etc.
            """
            _magicNumber = 19000
            pyodbc = 0 + _magicNumber

        class Database(object):
            """
            Named constants for specifying which database to connect to.
            """
            _magicNumber = 25000
            APlus_Test          = 0 + _magicNumber
            APlus_Prod          = 1 + _magicNumber
    # pylint: enable=W0232

    #    Methods                     ++++++++++++++++++
    def renderConnectionInfo(self):
        """
        Builds and returns the connnection info in the format required by the
        dbapi connection object.
        """
        return 'DSN=%s;UID=NONE;PWD=NONE;' % self.dsn


class DatabaseConnectionInfo(object):
    """
    A helper class for making and holding database connections. One
    globally-shared instance of this class (called data_connection_object) is
    instantiated when the module loads.

    This module provides (limited) flexibility to use different dbapi access
    modules, such as cx_Oracle, pymssql, etc. Client code specifies which module
    it wants. Client code is then responsible for adhering to the conventions of
    its chosen module - in term of paramstyle, format of connection string, etc.
    Client code also specifies which database it wants to connect to.

    Client code uses instances of the NdsDatabaseConnector and
    SalesDatabaseConnector classes to specify its preferences.
    """
    def __init__(self):
        #self._nds_db_connection_info = None
        #self._sales_db_connection_info = None
        self._aplus_db_connection_info = None

        #self._mssql_dbapi_module = None
        self._iseries_dbapi_module = None

        #self._persistent_nds_db_connection = None
        #self._persistent_sales_db_connection = None
        self._persistent_aplus_db_connection = None

    #    Properties                  +++++++++++++++++++
    # pylint: disable=E0202, E0211, W0212, C0111
    #@utl_decorators.makeProperty
    #def mssqlDbapiModule():
    #    doc = """
    #          The dbapi module used to make a connection to a MS SQL Server
    #          database. This returns a reference to the module itself.
    #          """
    #    def fget(self):
    #        return self._mssql_dbapi_module
    #    return locals()

    @utl_decorators.makeProperty
    def iSeriesDbapiModule():
        doc = """
              The dbapi module used to make a connection to a DB2 database
              running on an IBM iSeries machine (AS400). This returns a
              reference to the module itself.
              """
        def fget(self):
            return self._iseries_dbapi_module
        return locals()

    #@utl_decorators.makeProperty
    #def persistentSalesDbConnection():
    #    doc = """
    #          Returns a persistent dbapi connection object (pymssql), connected
    #          to the sales database. Used for read access to database. We do not
    #          write to the sales database.
    #          """
    #    def fget(self):
    #        return self._persistent_sales_db_connection
    #    return locals()

    @utl_decorators.makeProperty
    def persistentAplusDbConnection():
        doc = """
              Returns a persistent dbapi connection object (pyodbc), connected
              to the APlus database. Used for read access to database. Database
              writes each get their own connection and their own transaction.
              """
        def fget(self):
            # Make and cache a persistent database connection, if needed.
            if self._persistent_aplus_db_connection is None:
                self._persistent_aplus_db_connection = self.newAplusDbConnection()
            return self._persistent_aplus_db_connection
        return locals()
    # pylint: enable=E0202, E0211, W0212, C0111

    #    Database connection methods  ++++++++++++++++++
    #def newSalesDbConnection(self):
    #    """
    #    Returns a new dbapi connection object, connected to the sales database.
    #    """
    #    return self._mssql_dbapi_module.connect(**self._sales_db_connection_info)

    def newAplusDbConnection(self):
        """
        Returns a new dbapi connection object, connected to the Aplus database.
        """
        return self._iseries_dbapi_module.connect(self._aplus_db_connection_info)       # pylint: disable=no-member

    #def connect(self, sales_connector, aplus_connector):
    def connect(self, aplus_connector):
        """
        Makes database connections. Caches persistent database connections.
        """
        #self._sales_db_connection_info = None
        self._aplus_db_connection_info = None

        #self._mssql_dbapi_module = None
        self._iseries_dbapi_module = None

        #self._persistent_sales_db_connection = None
        self._persistent_aplus_db_connection = None

        #if sales_connector.dbapi_module == sales_connector.Constants.DbapiModule.pymssql:
        #    import pymssql
        #    self._mssql_dbapi_module = pymssql
        #else:
        #    err_msg = "Unrecognized option"
        #    raise error.ApplicationError(err_msg)

        if aplus_connector.dbapi_module == aplus_connector.Constants.DbapiModule.pyodbc:
            import pyodbc
            self._iseries_dbapi_module = pyodbc
        else:
            err_msg = "Unrecognized option"
            raise error.ApplicationError(err_msg)

        #self._sales_db_connection_info = sales_connector.renderConnectionInfo()
        self._aplus_db_connection_info = aplus_connector.renderConnectionInfo()

        # Make and cache persistent database connections. Note: do not connect
        # to APlus here. We connect to APlus only if needed. The connection is
        # cached in the persistentAplusDbConnection property of the
        # DatabaseConnectionInfo class. The connection is made only once, if
        # needed, in the fget of the the persistentAplusDbConnection property.
        #self._persistent_sales_db_connection = self.newSalesDbConnection()
        self._persistent_aplus_db_connection = self.newAplusDbConnection()

    #def customSalesConnector(self, mssql_dbapi_module, sales_db_connection_info):
    #    """
    #    This allows an external module to supply its own Sales DB connection
    #    info.
    #    """
    #    # This is the actual module, such as pymssql
    #    self._mssql_dbapi_module = mssql_dbapi_module
    #
    #    # This is the connection string
    #    self._sales_db_connection_info = sales_db_connection_info
    #
    #    # Make and cache persistent a database connection.
    #    self._persistent_sales_db_connection = self.newSalesDbConnection()

    def customAplusConnector(self, iseries_dbapi_module, aplus_db_connection_info):
        """
        This allows an external module to supply its own Aplus DB
        connection info.
        """
        # This is the actual module, such as pyodbc
        self._iseries_dbapi_module = iseries_dbapi_module

        # This is the connection string
        self._aplus_db_connection_info = aplus_db_connection_info

        # Make and cache persistent a database connection.
        self._persistent_aplus_db_connection = self.newAplusDbConnection()


# Create a single, shared, module-level instance of DatabaseConnectionInfo
data_connection_object = DatabaseConnectionInfo()
