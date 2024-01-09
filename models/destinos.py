from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class DetallesDestino(BaseModel):
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
    
{
  "fecha" : "2024-01-28",
    "hora": "8 am",
    "guiaid" : "987asdf987ee",
    "empresa" : "siga siga",
    "desc" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magni non nesciunt excepturi deserunt voluptatum ipsa ipsam quia, earum at, tempora numquam similique eveniet?"
}
    # {
    #     "lugar": "Cerro Wonk",
    #     "area" : "la cumbrecita",
    #     "pcia" : "Cordoba",
    #     "pcia_id" : "656e59c935a4cd190c93b4b7",
    #     "detalles" : []
    # }