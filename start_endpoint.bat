@echo off

call venv\Scripts\activate.bat
python endpoint.py --enable_proxy
pause

:: Упаковано и собрано телеграм каналом Neutogen News: https://t.me/neurogen_news
