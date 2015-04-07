"""
log.py

Provides logging services for applications.


Christian M. Long, developer

Initial implementation: September 18, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import Python standard modules
import errno
import os
import time

class LogUtility(object):
    """
    A utility class for logging.
    """
    def __init__(self, log_directory, max_logfile_size, time_format):
        self._log_directory = log_directory
        self._max_logfile_size = max_logfile_size
        self._time_format = time_format

    def writeToLogFile(self, log_text, log_file_name, user_id = None):
        """
        Writes the log text to the specified log file. The directory to use is
        read from the self._log_directory attribute.
        """
        # Add date and time and user Id to log file entry
        log_text = "%s   User Id: %s\n%s\n" % (time.strftime(self._time_format),
                                              user_id,
                                              log_text,
                                             )

        # Build the full path to the logfile
        path_to_log_file = os.path.join(self._log_directory, log_file_name)

        # Check file size. If file is larger than MAX_LOGFILE_SIZE, rename the
        # file with a .old extension. The call to open(path_to_log_file, 'a')
        # will then start a new file.
        try:
            filesize = os.path.getsize(path_to_log_file)
        # Handle only errors of type OSError. All other errors propagate upward.
        except OSError as the_err:
            # Ignore the OSError if it was a "File Not Found" error; reraise all
            # other OSErrors. If file was not found, it will be created later,
            # by the call to file().
            if the_err.errno != errno.ENOENT:
                # The plain raise statement reraises the same exception that
                # we're handling right now.
                raise
            else:
                # OK to continue silently on file not found. The file will be
                # created later.
                pass
        else:
            # We got the file size OK.  Now check it.
            if  filesize > self._max_logfile_size:
                source = path_to_log_file
                dest = "%s.old" % path_to_log_file
                os.rename(source, dest)

        with open(path_to_log_file, 'a') as log_file:
            log_file.write(log_text)
