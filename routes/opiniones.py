from fastapi import APIRouter, HTTPException
from models.opiniones import Opinion
from db.mongo import crea_opinion, obtener_opinion_id, obtener_opiniones
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


opinion = APIRouter()

@opinion.get('/list')
async def lista_opiniones():
    opiniones =[Opinion(** opinion) for opinion in await obtener_opiniones()]
    return opiniones

@opinion.post('/add')
async def agrega_opiniones( opinion: Opinion):
    nueva_opinion = opinion.model_dump(exclude={'id'},)
    rta = await crea_opinion(nueva_opinion)
    if rta.acknowledged:
        return str(rta.inserted_id)
    raise HTTPException(406, 'Algo salio mal')