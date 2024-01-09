from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class DetallesDestino(BaseModel):
    fecha : Optional[Union[datetime,str]] 
    hora: str
    guiaid : str
    empresa : str
    desc : str

class Destino(BaseModel):
    id: Optional[str] = None
    lugar: str
    area : str
    provincia : str
    pcia_id : str
    detalles: list[DetallesDestino]


# el find para buscar recorridos que coincida con una fecha
# fechaBuscada = '2023-12-15'
# db.destinos.find(
#   {
#     "destinos.fecha": fechaBuscada
#   },
#   {_id: 1, lugar: 1,  area: 1,
#  detalles: { $elemMatch: { fecha: fechaBuscada} }
#   }
# );
    