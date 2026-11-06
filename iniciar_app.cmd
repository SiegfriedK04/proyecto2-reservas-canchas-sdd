@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
)

call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py crear_datos_demo

echo.
echo CourtFlow estara disponible en http://127.0.0.1:8000/
python manage.py runserver

