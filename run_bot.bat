@echo off
title PvZ Helper Bot (Auto-Restart)
cd /d "%~dp0"

echo ========================================================
echo   PvZ Helper Bot - Auto-Restart Daemon
echo ========================================================

:loop
echo [%date% %time%] Starting main.py...
python main.py

set EXIT_CODE=%errorlevel%
echo.
echo [%date% %time%] Bot stopped with exit code %EXIT_CODE%.
echo [%date% %time%] Restarting in 3 seconds... (Press Ctrl+C to abort)
echo --------------------------------------------------------
timeout /t 3 /nobreak > nul
goto loop
