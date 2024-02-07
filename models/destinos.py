from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class DetallesDestino(BaseModel):
    id: Optional[str] = None
    destino_id : str
    lugar: str
    pcia : str
    pcia_id : str
    fecha : Optional[Union[datetime,str]] 
    hora: str
    guia_id : str
    empresa : str
    desc : str

class Destino(BaseModel):
    id: Optional[str] = None
    lugar: str
    area : str
    pcia : str
    pcia_id : str


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
    

    # {
    #     "lugar": "Cerro Wonk",
    #     "area" : "la cumbrecita",
    #     "pcia" : "Cordoba",
    #     "pcia_id" : "656e59c935a4cd190c93b4b7",
    #     "detalles" : []
    # }