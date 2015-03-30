@echo off

pushd "%CD%"

rem     cd to dir, if given
if not [%1] EQU [] (
    if exist %1 ( cd %1 )
)

echo.
echo -------------------------------------------
echo.
echo.
echo.

rem Show various information about this git directory
if exist .git (

  echo.
  echo "== Remote URL: "
  git remote -v
  echo.

  echo "== Remote Branches: "
  git branch -r -vv
  echo.

  echo "== Local Branches:"
  git branch -vv
  echo.

  echo "== Configuration (.git/config)"
  cat .git/config
  echo.

  echo "== Most Recent Commit"
  git --no-pager log --max-count=1
  echo.

  echo "== Status"
  git status
  rem git status --porcelain
  echo.

  rem echo "Type 'git log' for more commits, or 'git show' for full commit details."
) else (
  echo "Not a git repository."
)

echo.

popd




rem Notes

rem rem Find base of git directory
rem while [ ! -d .git ] && [ ! `pwd` = "/" ]; do cd ..; done
