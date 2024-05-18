from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellido: str
    email: str
    esguia: bool = False
    creado: Optional[datetime] = None    

class Usuario_Login(Usuario):
    clave : str

class Clave(BaseModel):
    clave: str

class Credenciales(BaseModel):
    email: str
    clave: str

class Guia(BaseModel):
    esguia : Optional[bool] = None
    empresa: str
    matricula: str
    resolucion: str
    cels: list
    actividad: list



