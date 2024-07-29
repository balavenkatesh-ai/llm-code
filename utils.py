from pydantic import BaseModel, Field
from typing import List

class NetworkRule(BaseModel):
    flag: str
    source_itam: int
    destination_itam: int
    sources: List[str]
    destinations: List[str]
    services: List[str]

class NetworkRules(BaseModel):
    __root__: List[NetworkRule]