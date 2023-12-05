from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellido: str
    email: str
    esguia: bool = False

class Usuario_Login(Usuario):
    clave : str
