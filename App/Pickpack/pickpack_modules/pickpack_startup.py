"""
pickpack_startup.py

Sets up and configures the Pick Pack server.


Christian M. Long, developer

christianzlong@gmail.com

Language: Python 2.7  www.python.org
"""

from twisted.application import internet
from twisted.application import service
from twisted.web import server

from Pickpack.pickpack_modules import pickpack_main
from Pickpack.pickpack_modules import pickpack_constants
from Pickpack.pickpack_modules import pickpack_data

def configureApp(configuration):
    """
    Set up the Twisted server objects
    """
    # Read parameters
    (description,
     port,
     con_string,
     con_string_for_update,
     mock_data,
     custom_library,
     procedure_library,
    ) = pickpack_constants.SERVER_DICT[configuration]

    # Connect to data
    pickpack_data.connectToData(con_string,
                                con_string_for_update,
                                mock_data,
                                custom_library,
                                procedure_library,
                               )

    # Create the application
    application = service.Application(description)

    # Create the service
    site = server.Site(pickpack_main.PickPackAppRoot())
    webserver = internet.TCPServer(port, site)                      # pylint: disable=no-member

    # Add the service to the application.
    webserver.setServiceParent(application)

    # Return the application. When twistd runs the .tac file, it will find and
    # use this application object.
    return application

def configureAppWithManhole(configuration):
    """
    Set up the Twisted server objects, and set up the twisted.manhole system,
    which allows you to inspect a running twisted application over ssh.
    """
    from twisted.conch import manhole_tap

    # Get the application by performing the normal, non-debug steps.
    application = configureApp(configuration)

    namespace = {'myapp' : application}

    options = {
        #'namespace'  : locals(),
        'namespace'  : namespace,
        # The password file users.txt may contain as little as one line with a
        # sample username and password, e.g. admin:admin.
        'passwd'     : 'users.txt',
        'sshPort'    : '2222',
        'telnetPort' : None,
    }

    # Create the service
    shell_service = manhole_tap.makeService(options)

    # Add the service to the application. This application already has the
    # PickPack app added to it.
    shell_service.setServiceParent(application)

    # Return the application. When twistd runs the .tac file, it will find and
    # use this application object.
    return application

    # Notes:
    #
    # Here's how to use Twisted.Manhole for debugging purposes.
    #
    # Fire up ssh
    #   ssh -p 2222 admin@localhost
    #
    # This results in a python interpreter prompt. Paste in this python code, to
    # drill down and get a reference to one of my running objects. The dir() and
    # help() functions are useful here to scope out the structure of the objects
    # into which you want to drill.
    #
    #   import twisted
    #   a = myapp
    #   b = a.getComponent(twisted.application.service.IService)
    #   c = b.services[0]
    #   d = c.args[1]
    #   e = d.resource
    #   f = e.children['clippership']
    #   g = f.children['warnings']
    #
    #
    # So, now we have a reference to an object. What can we do with it? Well, in
    # this case, we would need to cook up a fake request object to pass to
    # g.dataMethod(). I'm not going to do that right now.
    #
    # However, I can import and call individual functions directly.
    #   from Pickpack.pickpack_modules import pickpack_data_mock
    #   from Pickpack.pickpack_modules import pickpack_format
    #   order_number = 'AA02200'
    #   h = pickpack_data_mock.getClippershipWarningsData_deferred(order_number)
    #   i = h.result['order_notes']
    #   j = pickpack_format._formatClippershipWarnings(i)
    #
    #  Of course, you can do that from a regular python prompt on the server,
    #  without having an instance of Pick Pack running in Twisted. (Make sure
    #  you are in the pickpack virtualenv, run 'workon pickpack').
    #
    # But, there is one cool thing we can do with the manhole. I can reload
    # individual modules at runtime, and they will reflect any changes that have
    # been made to the module.
    #   from Pickpack.pickpack_modules import pickpack_format
    #   from twisted.python.rebuild import rebuild
    #   rebuild(pickpack_format)
    #   print pickpack_format._formatClippershipWarnings(i)




#
