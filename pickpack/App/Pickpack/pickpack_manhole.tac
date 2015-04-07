from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import pickpack_startup

# Create the application. Also create an ssh service to which clients can
# attach. This allows inspection of the running service, for debugging.
#
# See the definition of configureAppWithManhole for more info, and for usage
# tips.
application = pickpack_startup.configureAppWithManhole(pickpack_constants.MANHOLE)
