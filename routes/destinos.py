from fastapi import APIRouter, HTTPException
from schemas.destinoSchema import destinoSchema, destinosSchema
from models.destinos import Destino, DetallesDestino
from db.mongo import nuevo_destino, lista_destinos
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
    print('aca ')
    return destinosSchema( await lista_destinos())

# @destino.put('/{id}')
# async def detalle_destino(id : str, detalle: DetallesDestino):
#     rta = await nuevo_detalle(ObjectId(id); detalle)

