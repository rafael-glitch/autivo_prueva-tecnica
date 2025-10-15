from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from service.countries_service import CountriesService
from schemas.search_schema import SearchFilters
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API de Análisis Geográfico", version="1.0.0")


# Inicializar servicio (carga y cache de datos)
service = CountriesService()


@app.get("/")
def home():
    return {"message": "API de Análisis Geográfico 🌍"}
# 🔹 Modelo para búsqueda avanzada
class SearchFilters(BaseModel):
    minPopulation: Optional[int] = None
    maxPopulation: Optional[int] = None
    languages: Optional[List[str]] = None
    region: Optional[str] = None

# 1. Análisis de Vecindad
@app.get("/countries/{code}/neighbors")
def neighbors_analysis(code: str):
    code = code.upper()
    result = service.get_neighbors_analysis(code)
    if result is None:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return result


# 2. Rutas Terrestres
@app.get("/route")
def route(from_code: str = Query(..., alias="from"), to_code: str = Query(..., alias="to")):
    from_code = from_code.upper()
    to_code = to_code.upper()
    path = service.find_land_route(from_code, to_code)
    if path is None:
        return {"connected": False, "message": f"No hay conexión terrestre entre {from_code} y {to_code}"}
    return {"connected": True, "path": path}


# 3. Estadísticas Regionales
@app.get("/regions/{region}/stats")
def region_stats(region: str):
    stats = service.get_region_stats(region)
    if stats is None:
        raise HTTPException(status_code=404, detail="Región no encontrada o sin datos")
    return stats


# 4. Búsqueda Avanzada
@app.post("/countries/search")
def search_countries(filters: SearchFilters):
    try:
        result = service.search_countries(filters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))