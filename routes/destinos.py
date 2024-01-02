from fastapi import APIRouter, HTTPException
from schemas.destinoSchema import destinoSchema, destinosSchema
from models.destinos import Destino, DetallesDestino
from db.mongo import nuevo_destino, lista_destinos, lista_destinos_pcia
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


destino = APIRouter()

@destino.post('/add')
async def agrega_destino( destino : Destino):
    destino = destino.model_dump(exclude={"id"})
    rta = await nuevo_destino(destino)
    return "Destino Creado Correctamente: "+str(rta)

@destino.get('/')
async def listado_destinos():
    return destinosSchema( await lista_destinos())

@destino.get('/pcia/{id}')
async def listado_destinos_pcias(id: str):
    try:
        return destinosSchema( await lista_destinos_pcia(id))
    except:
        return []

# @destino.put('/{id}')
# async def detalle_destino(id : str, detalle: DetallesDestino):
#     rta = await nuevo_detalle(ObjectId(id); detalle)

