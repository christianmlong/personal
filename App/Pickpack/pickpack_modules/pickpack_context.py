"""
pickpack_context.py

Context objects for the Pick Pack server.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from Common.utility import utl_decorators

from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import pickpack_errors

@utl_decorators.add_constants_to_class({'Flavor'    : ('Normal',
                                                      ),
                                       },
                                       magic_number = 200000,
                                      )
class Context(object):
    """
    A class to make context objects, used to carry context info down through the
    call chain.
    """
    NORMAL_PORTS = (pickpack_constants.DEV_PORT,
                    pickpack_constants.PROD_PORT,
                    pickpack_constants.TEST_PORT,
                    pickpack_constants.MANHOLE_PORT,
                    pickpack_constants.TEST_MT_PORT,
                   )

    def __init__(self,
                 port,
                ):
        if port in self.NORMAL_PORTS:
            self._flavor = self.Constants.Flavor.Normal                         # pylint: disable=no-member
        else:
            raise pickpack_errors.ApplicationError("Unrecognized port %s" % port)

    #    Properties                  +++++++++++++++++++
    # pylint: disable=E0202, E0211, W0212, C0111
    @utl_decorators.makeProperty
    def flavor():
        def fget(self):
            return self._flavor
        return locals()
    # pylint: enable=E0202, E0211, W0212, C0111
