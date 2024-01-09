from fastapi import APIRouter, HTTPException
from schemas.destinoSchema import destinoSchema, destinosSchema
from models.destinos import Destino, DetallesDestino
from db.mongo import nuevo_destino, lista_destinos, lista_destinos_pcia, nuevo_detalle
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from datetime import datetime


destino = APIRouter()

@destino.post('/add', response_model=str, status_code=201)
async def agrega_destino( destino : Destino):
    destino = destino.model_dump(exclude={"id"})
    rta = await nuevo_destino(destino)
    return "Destino Creado Correctamente: "+str(rta)

@destino.get('/', response_model=list[Destino], status_code=200)
async def listado_destinos():
    return destinosSchema( await lista_destinos())

@destino.get('/pcia/{id}',response_model=list[Destino], status_code=200)
async def listado_destinos_pcias(id: str):
    try:
        return destinosSchema( await lista_destinos_pcia(id))
    except:
        return []

@destino.put('/{id}')
async def detalle_destino(id : str, detalle: DetallesDestino):
    if type(detalle.fecha) == str:
        anio, mes, dia = detalle.fecha.split('-')
        detalle.fecha = datetime(int(anio),int(mes),int(dia))
    detalle = detalle.model_dump()
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    try:
        await nuevo_detalle(ObjectId(id), detalle)
    except:
       raise HTTPException(417, "Id inválido")
    return "Detalle actualizado"

# // Supongamos que la fecha que estás buscando es "2023-12-15"
# var fechaBuscada = "2023-12-15";

# // Consulta MongoDB para filtrar solo los elementos del array servicios que coincidan con la fecha
# db.tuColeccion.find(
#   {
#     "servicios.fecha": fechaBuscada
#   },
#   {
#     _id: 1, // Incluir el campo _id si lo necesitas
#     lugar: 1, // Incluir el campo lugar
#     area: 1, // Incluir el campo area
#     servicios: {
#       $elemMatch: {
#         fecha: fechaBuscada
#       }
#     }
#   }
# );
