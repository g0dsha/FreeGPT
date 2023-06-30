@echo off

call update.bat
REM строка выше производит обновление каждый раз, при каждом запуске

call venv\Scripts\activate.bat
python run.py
pause
