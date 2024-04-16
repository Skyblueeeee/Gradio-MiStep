@echo off
set PYTHON_PATH=..\..\tool_env\python.exe

if not exist "%PYTHON_PATH%" (
    echo Python is not installed or the path is incorrect.
)
cd MiStep
set SCRIPT_PATH=stop.py
"%PYTHON_PATH%" "%SCRIPT_PATH%"

set SCRIPT_PATH=start.py
"%PYTHON_PATH%" "%SCRIPT_PATH%" 

pause