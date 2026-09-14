@echo off
echo Iniciando Mapa de Mexico - Lenguas Indigenas...
call venv\Scripts\activate
python processing\cargar_indicadores.py
python -m uvicorn main:app --reload
