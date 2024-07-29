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
    
    
    ```python
from pydantic import BaseModel
from typing import List, Union

class TCPProtocol(BaseModel):
    TCP: List[int]

class UDPProtocol(BaseModel):
    UDP: List[int]

class TCPStringProtocol(BaseModel):
    TCP: List[str]

class Provider(BaseModel):
    flag: str
    itam: int
    service: str
    protocol: List[Union[TCPProtocol, UDPProtocol, TCPStringProtocol, str]]

class ProviderList(BaseModel):
    providers: List[Provider]
    
    
