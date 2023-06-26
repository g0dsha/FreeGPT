@echo off
python -m pip install virtualenv

call install.bat
REM После установки всех пакетов можете удалить эту строку, чтобы пропустить проверку. 

call venv\Scripts\activate.bat
python run.py
pause

REM Упаковано и собрано телеграм каналом Neutogen News: https://t.me/neurogen_news
