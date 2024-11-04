from fastapi import APIRouter, HTTPException, status
from schemas.destinoSchema import destinoSchema, destinosSchema, detalleSchema, detallesSchema
from models.destinos import  DetallesDestino
from models.pcias import Pcia, Destino
from db.mongo import nuevo_destino, lista_destinos, lista_destinos_pcia #, lista_travesias_pcia_fecha, lista_dest_pcia_desde_hoy, lista_detalle_destinos, destino_id
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from datetime import datetime


destino = APIRouter()


@destino.post('/add/{id}', response_model=str, status_code=201)
async def agrega_destino( id: str, destino : Destino):
    destino = destino.model_dump(exclude={"id"})
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Id invalido')
    rta = await nuevo_destino(ObjectId(id),destino)
    if (rta == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se agreg nada')
    return "Destino Creado Correctamente "

@destino.get('/', response_model=list[Pcia], status_code=200)
async def listado_destinos():
    return await lista_destinos()

@destino.get('/{busqueda}', response_model=list[Pcia], status_code=200)
async def listado_destinos(busqueda : str):
    return await lista_destinos(busqueda)


@destino.get('/pcia/{id}',response_model=list[Pcia], status_code=200)
async def listado_destinos_pcias(id: str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Id invalido')
    try:
        return await lista_destinos_pcia(ObjectId(id))
    except:
        return []

