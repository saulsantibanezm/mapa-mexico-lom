# Mapa de México — Lenguas Indígenas 🗺️

Aplicación web interactiva que visualiza la distribución de lenguas indígenas en México a nivel municipal, usando datos reales del Censo de Población y Vivienda 2020 del INEGI.

Desarrollado como proyecto de Servicio Social en el Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas (IIMAS), UNAM.

## Características

- 🗣️ Indicadores de lenguas indígenas para 2,412 municipios (Censo INEGI 2020)
- 🗺️ Mapa interactivo con 3 capas de visualización seleccionables
- 👥 Total de hablantes de lengua indígena por municipio
- 🔤 Número de lenguas distintas por municipio
- 🏷️ Familia lingüística dominante por municipio
- 🔍 Búsqueda directa de estados y municipios
- 📋 Panel lateral con datos de municipios seleccionados
- 📱 Diseño responsivo

## Requisitos

- Python 3.10 o superior → https://python.org/downloads
- En Windows: marcar "Add Python to PATH" durante la instalación

## Instalación y ejecución

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

### Desde USB (sin Git)

**Linux y Mac:**
```bash
unzip mapa-mexico-lom.zip
cd mapa-mexico-lom
chmod +x instalar.sh
./instalar.sh
```

**Windows:** doble clic en `instalar.bat`

## Estructura del proyecto
mapa-mexico-lom/
├── main.py # Backend FastAPI (7 endpoints)
├── create_db.py # Genera la base de datos desde CSV
├── requirements.txt # Dependencias Python
├── coordenadas_municipios.csv # Datos geográficos de municipios
├── municipios.db # Base de datos SQLite
├── processing/
│ ├── censo_lengua_indigena.py # ETL: procesa microdatos del Censo 2020
│ └── cargar_indicadores.py # Carga indicadores a la base de datos
├── data/
│ └── processed/
│ └── indicadores_lom.csv # Indicadores agregados por municipio
└── templates/
└── index.html # Interfaz web completa

## Pipeline de datos
Censo INEGI 2020 (15M registros)
↓
censo_lengua_indigena.py
↓
indicadores_lom.csv (2,412 municipios)
↓
cargar_indicadores.py
↓
municipios.db → API REST → Mapa interactivo

## Fuente de datos

- **Coordenadas geográficas:** elaboración propia
- **Indicadores de lenguas indígenas:** Censo de Población y Vivienda 2020, INEGI
  - Variable `HLENGUA`: habla lengua indígena
  - Variable `QDIALECT_INALI`: clasificación de lengua (INALI)

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python + pandas | ETL de microdatos censales |
| FastAPI | Backend con 7 endpoints REST |
| SQLite | Base de datos relacional |
| Leaflet.js | Mapa interactivo con capas dinámicas |
| HTML5/CSS3/JS | Interfaz de usuario |
| OpenStreetMap | Proveedor de tiles del mapa base |

## Autor

**Saul Santibañez Molina**
Servicio Social — IIMAS, UNAM 2026
Supervisor: Dr. Ivan Vladimir Meza Ruiz

Repositorio base: https://github.com/saulsantibanezm/mapa-mexico
