from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import pickpack_startup

# Create the application, using mock test data instead of a connecting to the
# database.
application = pickpack_startup.configureApp(pickpack_constants.TEST)



# The application will be started and managed by the twistd command-line script.
# when the following command is run at the command prompt.
#    twistd -y pickpack_debug.tac
#
# Here's a brief explanation of .tac files, from twisted:
#    To use 'twistd -y', your .tac file must create a suitable object (e.g., by
#    calling service.Application()) and store it in a variable named
#    'application'. twistd loads your .tac file and scans the global variables
#    for one of this name.
#
#    Please read the 'Using Application' HOWTO in the twisted docs for details.
