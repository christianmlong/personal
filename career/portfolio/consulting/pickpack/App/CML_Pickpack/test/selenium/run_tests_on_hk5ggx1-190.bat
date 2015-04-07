@echo off


set base_path=C:\local files\Projects\Pack Validation\Dev\Working Copy
rem Only update the 'App' subdirectory. That way, the Komodo Project file in
rem Dev\kpf\pickpack.kpf doesn't get updated, and I don't get the annoying
rem "this file has changed on disk  . . ." message from Komodo
rem svn up "C:\local files\Projects\Pick Pack\Dev\Working Copy\App"
git -C "%base_path%" pull

set command_text=nosetests ^
--id-file="C:\Temp\noseids.txt" ^
--verbose ^
--detailed-errors ^
--where="%base_path%\App\Pickpack\test\selenium" %1 %2 %3 %4



echo.
echo.
echo.
echo.
echo ===================
echo.
echo Starting Nose tests
echo.
echo Did you restart the server, if needed?
echo.
echo.
echo.
echo %command_text%
echo.
echo.
echo.
call %command_text%
