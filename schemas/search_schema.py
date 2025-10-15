from pydantic import BaseModel
from typing import List, Optional


class SearchFilters(BaseModel):
    minPopulation: Optional[int] = None
    maxPopulation: Optional[int] = None
    languages: Optional[List[str]] = None
    region: Optional[str] = None