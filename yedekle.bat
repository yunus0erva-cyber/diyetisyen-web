@echo off
chcp 65001 > nul
set PYTHON_PATH=C:\Users\doruk\AppData\Local\Programs\Python\Python311\python.exe

if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" yedekle.py
) else (
    python yedekle.py
)

pause
