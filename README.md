# Mapa de México — Lenguas Indígenas 🗺️

Aplicación web interactiva que visualiza la distribución de lenguas indígenas en México a nivel municipal, usando datos del Censo de Población y Vivienda 2020 del INEGI.

## Características

- 🗣️ Indicadores de lenguas indígenas por municipio (Censo INEGI 2020)
- 🗺️ Mapa interactivo con 3 capas de visualización
- 👥 Total de hablantes de lengua indígena por municipio
- 🔤 Número de lenguas distintas por municipio
- 🏷️ Familia lingüística dominante por municipio
- 🔍 Búsqueda directa de estados y municipios
- 📋 Panel lateral con datos de municipios seleccionados
- 📍 Marcadores con coordenadas precisas
- 📱 Diseño responsivo

## Instalación y ejecución

### Requisitos previos
- Python 3.10 o superior → https://python.org/downloads
- En Windows: marcar "Add Python to PATH" durante la instalación

### Linux y Mac

```bash
git clone https://github.com/saulsantibanezm/mapa-mexico-lom.git
cd mapa-mexico-lom
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_db.py
python processing/cargar_indicadores.py
python -m uvicorn main:app --reload
```

Abre http://127.0.0.1:8000 en tu navegador.

### Windows

```bash
git clone https://github.com/saulsantibanezm/mapa-mexico-lom.git
cd mapa-mexico-lom
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python create_db.py
python processing\cargar_indicadores.py
python -m uvicorn main:app --reload
```

Abre http://127.0.0.1:8000 en tu navegador.

### Uso desde USB (sin Git)

Si tienes el archivo ZIP del proyecto:

**Linux y Mac:**
```bash
unzip mapa-mexico-lom.zip
cd mapa-mexico-lom
chmod +x instalar.sh
./instalar.sh
```

**Windows:** doble clic en `instalar.bat`

## Fuente de datos

- Coordenadas geográficas: elaboración propia
- Indicadores de lenguas indígenas: Censo de Población y Vivienda 2020, INEGI
  - Variable `HLENGUA`: habla lengua indígena
  - Variable `QDIALECT_INALI`: clasificación de lengua (INALI)

## Tecnologías

- **Backend:** Python, FastAPI, SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Leaflet.js
- **Procesamiento:** pandas (chunks de 300,000 filas)
- **Mapa base:** OpenStreetMap

## Autor

Saul Santibañez Molina — Servicio Social IIMAS, UNAM 2026
Supervisor: Dr. Ivan Vladimir Meza Ruiz
