@echo off
start "" /B pythonw.exe portal.py
timeout /t 108000 >nul 
taskkill /F /IM pythonw.exe >nul
