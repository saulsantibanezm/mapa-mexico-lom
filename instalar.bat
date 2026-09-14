@echo off
echo ======================================
echo  Mapa de Mexico - Lenguas Indigenas
echo ======================================
echo.
echo Instalando dependencias...
python -m venv venv
call venv\Scripts\activate
pip install fastapi uvicorn jinja2 pandas openpyxl
echo.
echo Configurando base de datos...
python create_db.py
python processing\cargar_indicadores.py
echo.
echo Todo listo. Iniciando servidor...
echo Abre http://127.0.0.1:8000 en tu navegador
echo.
python -m uvicorn main:app --reload
