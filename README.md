# API que consume https://restcountries.com/v3.1/all?fields=name,cca3,borders,capital,population,area,region,languages,currencies

API REST desarrollada con FastAPI que consume la **REST Countries API** y entrega información procesada sobre los países del mundo.  
Incluye análisis de vecindad, rutas terrestres, estadísticas regionales y búsquedas avanzadas.

---

##  Tecnologías Utilizadas

| **Python 3.10+** | Lenguaje principal para implementar la lógica de la API. |
| **FastAPI** | Framework para crear la API REST, definir endpoints y manejar las solicitudes HTTP. |
| **Uvicorn** | Servidor ASGI utilizado para ejecutar la aplicación FastAPI en modo desarrollo o producción. |
| **Requests** | Librería para consumir la API externa [REST Countries](https://restcountries.com) y obtener los datos de los países. |
| **Pydantic** | Utilizado para definir modelos de datos (schemas) y validar automáticamente la estructura del JSON recibido en la peticion POST. |

---

##  Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone <https://github.com/rafael-glitch/Autivo-prueba.git>
   cd autivo_prueba_tecnica
   ´´´
2. **crear y activa el entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # En Windows
   source venv/bin/activate  # En Linux o macOS
   ´´´
---
3. **instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ´´´
---

4. **ejecutar API**
   ```bash
   uvicorn main:app --reload
   ´´´
   ---
5. **Probar en el navegador**
    http://127.0.0.1:8000/docs
    GET     /                           mensaje de vienvenida
    GET     /countries/{code}/neighbors muestra los paises del codigo especificado(codigo de chile: CHL)
    GET     /route?from=XXX&to=YYY      determina si existe ruta terrestre entre 2 paises
    GET     /regions/{region}/stats     muestra las estadisticas de poblacion y area por reguino (americas)
    POST    /countries/search           busca paises segun filtros espesificos
