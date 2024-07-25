from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.mongobase import MongoBaseModel

class Usuario(MongoBaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    esguia: bool = False
    creado: Optional[datetime] = None   
    empresa: Optional[str] = None
    matricula: Optional[str] = None
    resolucion: Optional[str] = None
    cel: Optional[str] = None
    celalt: Optional[str] = None
    actividad: Optional[str] = None 

    # class Config:
    #     allow_population_by_name = True
    #     json_encoders = {
    #         ObjectId: str
    #     }
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
    cel: str
    celalt: str
    actividad: str



