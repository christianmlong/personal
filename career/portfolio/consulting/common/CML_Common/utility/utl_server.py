"""
utl_server.py

Information about the server we are running on.


Christian M. Long, developer

Initial implementation: September 10, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import Python standard modules
import socket

# Import shared modules
from CML_Common.utility import utl_decorators

@utl_decorators.memoizeFunction
def getHostname():
    """
    Calls socket.gethostname(). This function is memoized, which means the logic
    in it will only ever run once. Future calls to getHostname will return the
    cached result.
    """
    return socket.gethostname()
