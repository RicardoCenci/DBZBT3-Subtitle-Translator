python --version 3>NUL
if errorlevel 1 goto errorNoPython
cd ./Source
python setup.py build
pause
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed
start "" "https://www.python.org/downloads/windows/"
