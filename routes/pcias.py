from fastapi import APIRouter, HTTPException
from models.pcias import Pcia
from db.mongo import crea_prov, lista_pcias, una_pcia, eliminar_pcia
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


pcia = APIRouter()

@pcia.get("/", response_model=list[Pcia], status_code=200)
async def lista_de_pcias():
    return await lista_pcias()

@pcia.get("/{id}", response_model=Pcia, status_code=200)
async def lista_una_prov(id: str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    try:
        pcia = await una_pcia(ObjectId(id))
    except:
        raise HTTPException(404, "No Existe")
    return Pcia(**pcia)
    
@pcia.post("/add", response_model=str, status_code=201)
async def crear_una_prov(pcia: Pcia):
    pcia = pcia.model_dump(exclude={"id"})
    pcia['nombre']= pcia['nombre'].title()
    try:
        rta = await crea_prov(pcia)
    except DuplicateKeyError:
        raise HTTPException(409, 'El nombre de la provicia ya existe')
    return "pcia insertada : "+str(rta)

@pcia.delete("/{id}", response_model=str, status_code=200)
async def eliminar_una_pcia(id: str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    id = ObjectId(id)
    rta = await eliminar_pcia(id)
    if rta.acknowledged:
        if rta.deleted_count > 0:
            return f"Pcia con id {str(id)} Eliminada"
        else:
            return "Pcia Inexistente, nada borrado"
    raise HTTPException(500, 'Algo salio mal')