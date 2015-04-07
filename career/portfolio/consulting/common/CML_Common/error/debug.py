"""
debug.py

Provides debugging services for applications.

Here's an example of how to set remote breakpoint in Komodo. Komodo must be
running on 1bk2zq1-190. Debugging listener must be listening on port 8201.

    from CML_Common.error.debug import debug_utility_object as debugObj
    debugObj.debugBreakpoint()



Christian M. Long, developer

Initial implementation: September 18, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import Python standard modules
import os
import sys
import inspect
import cStringIO

# Import shared modules
from CML_Common.utility import utl_decorators
from CML_Common.utility import utl_classes
from CML_Common.utility import utl_constants
from CML_Common.error import log

# Module constants
# Note use DBG instead of DE BUG to avoid pylint flagging it as a TO DO.
REMOTE_DBG_HOST = "asdfghjk.joco.com"
REMOTE_DBG_PORT = 8481
LOG_DIRECTORY = r"C:\Temp\logs"
LOGFILE = "log.log"
MAX_LOGFILE_SIZE = 100000        # Maximum size of logfile, in bytes

class DebugUtility(object):
    """
    A utility class for helping with debugging. One globally-shared instance of
    this class (called debug_utility_object) is instantiated when the module
    loads.

    Typical usage: a higher-level application (such as MRA) has knowledge of its
    own debugging settings, but it does not have access to that information
    right away. Configuration files have to be read, database calls made,
    command-line options parsed, etc. When the utility object is first
    instantiated (here, at module import), some reasonable defaults are
    provided. Once the higher-level application is running and has figured out
    its configuration, it changes the configuration of the utility object
    accordingly.

    This approach allows the foundation modules and the higher-level application
    to share the same utility object. The utility object works in basic defaults
    mode while application modules are loading and configuration is being read.
    Later its configuration is changed to match the needs of the higher-level
    application.
    """
    # Sample usage
    #
    ## Import debug utility object
    #from CML_Common.error.debug import debug_utility_object as debugObj
    ## Example: Set remote breakpoint in Komodo. Komodo must be running on
    ## REMOTE_DBG_HOST
    #debugObj.debugBreakpoint()

    def __init__(self):
        # Provide a reasonable default behavior for now. Higher-level
        # applications will reconfigure debug_level to meet their needs when
        # they are ready.
        if __debug__:
            self._debug_level = self.DebugLevelConstants.Light
        else:
            self._debug_level = self.DebugLevelConstants.NoDebug

    #    Properties                  +++++++++++++++++++
    # pylint: disable=E0202, E0211, W0212, C0111
    @utl_decorators.makeProperty
    def debug_level():
        doc = """
              What level of debugging verbosity?
              """
        def fget(self):
            return self._debug_level
        def fset(self, value):
            assert value in self.DebugLevelConstants
            self._debug_level = value
        return locals()
    # pylint: enable=E0202, E0211, W0212, C0111

    #    Named Constants             +++++++++++++++++++
    # Named constants in convenient dot notation. If the shared
    # debug_utility_object was imported like this:
    #   #from CML_Common.error.debug import debug_utility_object as debugObj
    # then these constants can be addressed using this form:
    #   debugObj.DebugLevelConstants.ExtraHeavy
    named_constants = ["NoDebug",       # 0
                       "Light",         # 1
                       "Medium",        # 2
                       "Heavy",         # 3
                       "ExtraHeavy"]    # 4
    DebugLevelConstants = utl_classes.Enum(named_constants)

    #    Methods                     +++++++++++++++++++
    def debugPause(self, calling_location, debug_threshhold, msg = None):
        """
        Only acts at or above the debug level specified in debug_threshhold.
        Pauses program and waits for user to press enter. Allows user to see
        data before clearing the screen and repainting the menu. Prints calling
        location and optional message.
        """
        if self._debug_level >= debug_threshhold:
            if msg is None:
                raw_input("Debug pause - \nInside %s" % calling_location)
            else:
                raw_input("Debug pause - \nInside %s\n%s" % (calling_location, msg))

    def debugPrint(self, debug_threshhold, item = None, item_list = None, item_dict = None):
        """
        Only acts at or above the debug level specified in debug_threshhold.
        Prints the item passed by the calling function, and also prints the name
        of the calling function and other info. Also accepts lists of items for
        printing, and dictionaries. All parameters optional.
        """
        if self._debug_level >= debug_threshhold:
            # Build the entry string by appending to a list
            string_list = []
            string_list.append("\nData =======================")
            if item is not None:
                string_list.append("Item:")
                string_list.append("%s  -- %s" % (item, type(item)))
            if item_list is not None:
                string_list.append("\nItemList:")
                try:
                    for i in item_list:
                        string_list.append("%s  -- %s" % (i, type(i)))
                except TypeError:
                    string_list.append("%s  -- %s" % (item_list, type(item_list)))
            if item_dict is not None:
                string_list.append("\nItemDict:")
                try:
                    for x, y in item_dict.items():
                        string_list.append("%s : %s  -- %s" % (x, y, type(y)))
                except TypeError:
                    string_list.append("%s  -- %s" % (item_dict, type(item_dict)))
            string_list.append("\nCalling Location ==========")
            # Print all the functions in the stack. Don't bother showing this
            # function - inspect.stack()[0] Keeping references to frame objects,
            # as found in the first element of the frame records returned by
            # inspect.stack(), can cause the program to create reference cycles.
            # Explicitly delete references to these frame objects when we are
            # done with them.
            try:
                if self._debug_level >= self.DebugLevelConstants.ExtraHeavy:
                    traceback_list = inspect.stack()[1:]
                else:
                    traceback_list = inspect.stack()[1:2]

                for frame_record in traceback_list:
                    try:
                        frame_object, \
                        file_name,    \
                        line_number,  \
                        function_name = frame_record[0:4]
                        string_list.append("Function %s\nline # %i in file %s" % \
                                          (function_name,
                                           line_number,
                                           file_name))
                        string_list.append("\nParameters of function %s:" % function_name)
                        string_list.append(inspect.formatargspec
                                            (inspect.getargvalues(frame_object))
                                         )
                        string_list.append("\nLocals of function %s:" % function_name)
                        for var_name, var_value in frame_object.f_locals.items():
                            if not var_name.startswith("__"):
                                string_list.append("%s : %s" % (var_name, var_value))
                        string_list.append("")
                    finally:
                        # Avoid circular references by explicitly deleting these
                        # references to frame objects.
                        del frame_object
                        del frame_record
            finally:
                # Avoid circular references by explicitly deleting this
                # reference to the list of stack frames.
                del traceback_list

            string_list.append("============================\n\n")

            # Build the big string from the list of strings, adding a newline
            # between each item.
            big_string = '\n'.join(string_list)

            # Print the string to the screen, and pause
            print big_string
            self.debugPause(function_name, debug_threshhold)

    def debugBreakpoint(self, debug_threshhold = None):
        """
        Only acts at or above the debug level specified in debug_threshhold.
        Breaks code execution on the server and initializes an interactive
        debugging session on the Komodo machine (asdfghk.joco.com).
        """
        if debug_threshhold is None:
            # Set threshhold to low if it was not supplied.
            debug_threshhold = self.DebugLevelConstants.Light
        if self._debug_level >= debug_threshhold:
            from dbgp.client import brk
            brk(host=REMOTE_DBG_HOST, port=REMOTE_DBG_PORT)

    def debugIpythonBreakpoint(self, debug_threshhold = None):
        """
        Only acts at or above the debug level specified in debug_threshhold.
        Breaks code execution on the server and initializes an interactive
        debugging session in iPython on the server.
        """
        if debug_threshhold is None:
            # Set threshhold to low if it was not supplied.
            debug_threshhold = self.DebugLevelConstants.Light
        if self._debug_level >= debug_threshhold:
            import ipdb
            ipdb.set_trace()

    def debugPudbBreakpoint(self, debug_threshhold = None):
        """
        Only acts at or above the debug level specified in debug_threshhold.
        Breaks code execution on the server and initializes an interactive
        debugging session in pudb on the server.
        """
        if debug_threshhold is None:
            # Set threshhold to low if it was not supplied.
            debug_threshhold = self.DebugLevelConstants.Light
        if self._debug_level >= debug_threshhold:
            import pudb
            pudb.set_trace()

    def debugLog(self, debug_threshhold, msg):
        """
        Only acts at or above the debug level specified in debug_threshhold.
        Logs information about the common module.
        """
        if self._debug_level >= debug_threshhold:
            logger = log.LogUtility(LOG_DIRECTORY,
                                           MAX_LOGFILE_SIZE,
                                           utl_constants.TIME_FORMAT,
                                          )
            logger.writeToLogFile(msg, LOGFILE)

    def logSystemConfig(self, debug_threshhold):
        """
        Shows important data about the current execution environment, such as
        the path, the terminal type, the loaded modules, and other environment
        variables.
        """
        if self._debug_level >= debug_threshhold:
            big_string = cStringIO.StringIO()
            big_string.write("System Configuration\n")
            big_string.write("\nPath\n")
            big_string.write("%s\n" % str(sys.path))
            big_string.write("\nModules\n")
            mod_dict = sys.modules
            for mod in mod_dict.values():
                try:
                    big_string.write("%s\n" % str(mod.__name__))
                except AttributeError:
                    big_string.write("No name\n")
                try:
                    big_string.write("%s\n" % str(mod.__file__))
                except AttributeError:
                    big_string.write("No file\n")
            big_string.write("\nArguments\n")
            big_string.write("%s\n" % str(sys.argv))
            big_string.write("\nVersion\n")
            big_string.write("%s\n" % str(sys.version))
            big_string.write("\nEnvironment\n")
            for key, val in os.environ.items():
                big_string.write("%s:  %s\n" % (key, val))

            # Print the string to the screen, and pause
            print big_string.getvalue()
            self.debugPause("debugShowSystemConfig", debug_threshhold)
            self.debugLog(debug_threshhold, big_string.getvalue())

# Create a single shared instance of DebugUtility.
debug_utility_object = DebugUtility()


def dropInToDebuggerOnUnhandledError():
    """
    Set up so that we drop in to Komodo debugger if an unhandled error gets to
    the top of the stack.
    """
    from dbgp.client import brkOnExcept
    brkOnExcept(host=REMOTE_DBG_HOST, port=REMOTE_DBG_PORT)
