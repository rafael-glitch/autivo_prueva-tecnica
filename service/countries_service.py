from unittest import result
import requests
from typing import Dict, List, Optional, Set, Any
from collections import deque


REST_URL = "https://restcountries.com/v3.1/all?fields=name,cca3,borders,capital,population,area,region,languages,currencies"


class CountriesService:
    def __init__(self):
        self._data = None
        self._by_cca3 = None
        self._load_data()


    def _load_data(self):
        try:
            resp = requests.get(REST_URL, timeout=60)
            resp.raise_for_status()
            self._data = resp.json()
            # indexar por CCA3
            self._by_cca3 = {c['cca3']: c for c in self._data if 'cca3' in c}
            print(f"Cargados {len(self._data)} países correctamente.")
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos: {e}")
            self._data = []
            self._by_cca3 = {}


    def _get_country(self, code: str) -> Optional[Dict[str, Any]]:
        return self._by_cca3.get(code)


    # 1. Vecindad
    def get_neighbors_analysis(self, code: str) -> Optional[Dict[str, Any]]:
        country = self._get_country(code)
        if not country:
            return None
        borders = country.get('borders', []) or []
        neighbors = []
        total_pop = country.get('population', 0)


        # languages of the queried country
        country_langs = set((country.get('languages') or {}).values())


        neighbors_sharing_lang = []


        for b in borders:
            nb = self._get_country(b)
            if not nb:
                continue
            name = nb.get('name', {}).get('common')
            capital = (nb.get('capital') or ["N/A"])[0]
            population = nb.get('population', 0)
            neighbors.append({"code": b, "name": name, "capital": capital, "population": population})
            total_pop += population


            nb_langs = set((nb.get('languages') or {}).values())
            if country_langs & nb_langs:
                neighbors_sharing_lang.append({"code": b, "name": name, "shared_languages": list(country_langs & nb_langs)})


        return {
            "country": {"code": code, "name": country.get('name', {}).get('common'), "population": country.get('population', 0)},
            "neighbors": neighbors,
            "total_border_population": total_pop,
            "neighbors_sharing_language": neighbors_sharing_lang
        }
# 2. Rutas terrestres (BFS)
    def find_land_route(self, from_code: str, to_code: str) -> Optional[List[str]]:
        if from_code == to_code:
            return [from_code]
        start = self._get_country(from_code)
        end = self._get_country(to_code)
        if not start or not end:
            return None


        # BFS
        visited = set()
        queue = deque()
        queue.append((from_code, [from_code]))
        visited.add(from_code)


        while queue:
            curr_code, path = queue.popleft()
            curr = self._get_country(curr_code)
            borders = curr.get('borders', []) or []
            for nb_code in borders:
                if nb_code in visited:
                    continue
                new_path = path + [nb_code]
                if nb_code == to_code:
                    return new_path
            visited.add(nb_code)
            queue.append((nb_code, new_path))
        return None
    # 3. Estadísticas regionales
    def get_region_stats(self, region: str) -> Optional[Dict[str, Any]]:
        region_lower = region.lower()
        countries = [c for c in self._data if (c.get('region') or '').lower() == region_lower]
        if not countries:
            return None
        total_countries = len(countries)
        populations = [c.get('population', 0) for c in countries]
        total_population = sum(populations)
        average_population = total_population / total_countries if total_countries else 0


        # unique languages
        languages: Set[str] = set()
        for c in countries:
            langs = (c.get('languages') or {}).values()
            for l in langs:
                languages.add(l)
        # top 5 by population
        top5 = sorted(countries, key=lambda x: x.get('population', 0), reverse=True)[:5]
        top5_list = [{"name": t.get('name', {}).get('common'), "population": t.get('population', 0)} for t in top5]
        return {
            "region": region,
            "total_countries": total_countries,
            "total_population": total_population,
            "average_population": average_population,
            "unique_languages_count": len(languages),
            "top5_by_population": top5_list
        }
    # 4. Búsqueda avanzada
    def search_countries(self, filters):
        results = []

        for c in self._data:
            name = c.get("name", {}).get("common", "N/A")
            code = c.get("cca3", "N/A")
            population = c.get("population", 0)
            region = c.get("region", "N/A")
            langs = set((c.get("languages") or {}).values())

            # --- Aplicar filtros (AND) ---
            if filters.minPopulation is not None and population < filters.minPopulation:
                continue
            if filters.maxPopulation is not None and population > filters.maxPopulation:
                continue
            if filters.region and filters.region.lower() != region.lower():
                continue
            if filters.languages:
                # Debe hablar al menos uno de los idiomas especificados
                if not any(lang in langs for lang in filters.languages):
                    continue

            # Si pasa todos los filtros, agregarlo
            results.append({"name": name, "code": code})

        return {"total": len(results), "countries": results}