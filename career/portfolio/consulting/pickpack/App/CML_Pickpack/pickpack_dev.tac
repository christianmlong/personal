from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_startup

# Create the application
application = pickpack_startup.configureApp(pickpack_constants.DEV)



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




## You can run this .tac file directly with:
##    twistd -ny service.tac
#
#"""
#This is an example .tac file which starts a webserver on port 8080 and
#serves files from the current working directory.
#
#The important part of this, the part that makes it a .tac file, is
#the final root-level section, which sets up the object called 'application'
#which twistd will look for
#"""
#
#import os
#from twisted.application import service, internet
#from twisted.web import static, server
#
#def getWebService():
#    """
#    Return a service suitable for creating an application object.
#
#    This service is a simple web server that serves files on port 8080 from
#    underneath the current working directory.
#    """
#    # create a resource to serve static files
#    fileServer = server.Site(static.File(os.getcwd()))
#    return internet.TCPServer(8080, fileServer)
#
## this is the core part of any tac file, the creation of the root-level
## application object
#application = service.Application("Demo application")
#
## attach the service to its parent application
#service = getWebService()
#service.setServiceParent(application)















#
