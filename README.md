# Mapa de Mexico - Indicadores de Lenguas Indigenas

Aplicacion web interactiva que visualiza indicadores de lenguas indigenas
a nivel municipal, derivados del Censo de Poblacion y Vivienda 2020 del INEGI.

## Funcionalidades
- Mapa interactivo con 3 capas de indicadores por municipio
- Total de hablantes de lengua indigena
- Numero de lenguas distintas por municipio
- Familia linguistica dominante por municipio
- Panel lateral con datos de municipios seleccionados
- Busqueda por estado y municipio

## Requisitos
- Python 3.10 o superior
- Conexion a internet para instalar dependencias (solo primera vez)

## Instrucciones - Linux y Mac
Primera vez:
  chmod +x instalar.sh
  ./instalar.sh

Siguientes veces:
  chmod +x correr.sh
  ./correr.sh

## Instrucciones - Windows
Primera vez: doble clic en instalar.bat
Siguientes veces: doble clic en correr.bat

## Fuente de datos
- Coordenadas geograficas: elaboracion propia
- Indicadores de lenguas indigenas: Censo 2020, INEGI
  Variable HLENGUA: habla lengua indigena
  Variable QDIALECT_INALI: clasificacion INALI

## Tecnologias
- Backend: Python, FastAPI, SQLite
- Frontend: HTML5, CSS3, JavaScript, Leaflet.js
- Procesamiento: pandas

## Autor
Saul Santibañez Molina
Servicio Social IIMAS, UNAM 2026
Supervisor: Dr. Ivan Vladimir Meza Ruiz
