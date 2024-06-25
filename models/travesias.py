from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class Travesia(BaseModel):
    id: Optional[str] = None
    destino_id : str
    dificultad : str
    lugar: str
    pcia : str
    pcia_id : str
    fecha : Optional[Union[datetime,str]] 
    hora: str
    guia_id : str
    empresa : str
    pencuentro : str
    coordenadas : str
    desc : str
    ingreso : bool
    detingreso : str
    traslado: bool
    dettraslado: str
    desayuno: bool
    rmarcha: bool
    merienda: bool
    detpension: str
    pernocte: bool
    detpernocte: str
    botiquin: bool
    detbotiquin: str
    csatelital: bool
    cvhf:bool
    detcomunicaciones: str
    rfoto: bool
    detfoto: str
    scarga: bool
    detcarga: str
    imontania: bool
    detindumentaria: str
    cequipaje: bool
    detcuidado: str
    precio: int