"""

    Run the selenium tests on the partsdev01 dev server.

"""




import subprocess, os, argparse, time

def main():
    """
    Main function to start the tests.
    """

    parser = argparse.ArgumentParser(description='Run Selenium tests for Pack Validation.')
    parser.add_argument('--restart',
                        action='store_true',
                        help='Restart server before test run',
                       )
    # parser.add_argument('-f',
    #                     '--fast',
    #                     action='store_const',
    #                     const=2,
    #                     dest='speed',
    #                     help='Runs only fast tests. This is the default.',
    #                    )
    # parser.add_argument('-a',
    #                     '--all',
    #                     action='store_const',
    #                     const=0,
    #                     dest='speed',
    #                     help='Runs all tests, fast and slow',
    #                    )
    #

    args, leftover_args = parser.parse_known_args()


    if args.restart:
        # Restart dev service
        subprocess.check_call([r"C:\Users\clongadmin\Documents\Projects\Pack Validation\Dev\Working Copy\Dev\Utilities\run_command.bat",
                               "restart",
                               "pickpack_dev",
                              ],
                             )



    # Wait six seconds, to let the process restart. I do it this way, because the
    # self-elevating powershell script I use kills its ancestor process before
    # continuing. POSSIBLE_IMPROVEMENT: redo the powershell script so that I can use
    # subprocess.check_call to wait for it to complete.
    time.sleep(6)






    nose_path = r'C:\PythonEnvs\PackValidation\Scripts\nosetests.exe'
    selenium_tests_path = r'C:\Users\clongadmin\Documents\Projects\Pack Validation\Dev\Working Copy\App\Pickpack\test\selenium'
    id_file_path = r'C:\Temp\selenium_nosetests_id_file.txt'

    if not os.path.exists(nose_path):
        raise SystemError('%s does not exist' % nose_path)

    callspec = [nose_path,
                "--verbose",
                "--detailed-errors",
                "--with-id",
                "--id-file=%s" % id_file_path,
                "--where=%s" % selenium_tests_path,
               ]

    # Add any arguments that were passed to this script - pass them through to
    # nosetests.
    if leftover_args:
        callspec.extend(leftover_args)

    # Be verbose
    for item in callspec:
        print item

    # Run the nose process
    subprocess.call(callspec)


if __name__ == '__main__':
    main()
