@echo off

if not exist venv (
    py -m pip install virtualenv
    py -m virtualenv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
start pythonw main.py %*
exit