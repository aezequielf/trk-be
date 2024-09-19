from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.mongobase import MongoBaseModel


class Validacion(BaseModel):
    email: EmailStr
    resolucion: str
    provincia: str 

class Usuario(MongoBaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    esguia: bool = False
    creado: Optional[datetime] = None   
    empresa: Optional[str] = None
    cel: Optional[str] = None
    celalt: Optional[str] = None
    validacion: Optional[list[dict]] = None


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
    cel: str
    celalt: str




