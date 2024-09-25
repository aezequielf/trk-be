from typing import Optional, Union
from pydantic import BaseModel
from models.mongobase import MongoBaseModel


class Destino(BaseModel):
    id: Optional[str] = None
    lugar: str
    area: str

class Pcia(MongoBaseModel):
    nombre: str
    destinos: Optional[Union[Destino,list[Destino]]] = None