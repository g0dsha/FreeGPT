@echo off
python -m pip install virtualenv
call install.bat ::После установки всех пакетов можете удалить эту строку, чтобы пропустить проверку. 

call venv\Scripts\activate.bat
python run.py
pause

:: Упаковано и собрано телеграм каналом Neutogen News: https://t.me/neurogen_news
