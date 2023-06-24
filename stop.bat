@echo off

:loop

for /f "delims=" %%i in ('py lib\get_pid.py') do set "pid=%%i"

if not "%pid%" == "None" (
    taskkill /pid %pid% /f
    goto loop
) else (
    echo "Program stopped."
)
pause