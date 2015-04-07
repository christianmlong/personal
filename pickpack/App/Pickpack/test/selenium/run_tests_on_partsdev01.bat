@echo off

set TEST_RUNNER_PATH="%~dp0run_tests_on_partsdev01.py"

C:\PythonEnvs\PackValidation\Scripts\python.exe %TEST_RUNNER_PATH% %1 %2 %3 %4

pause




