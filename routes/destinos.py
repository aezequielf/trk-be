from fastapi import APIRouter, HTTPException
from schemas.destinoSchema import destinoSchema, destinosSchema, detalleSchema, detallesSchema
from models.destinos import Destino, DetallesDestino
from db.mongo import nuevo_destino, lista_destinos, lista_destinos_pcia, nuevo_detalle,lista_destinos_pcia_fecha
#, lista_dest_pcia_desde_hoy
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

# @destino.get('/pcia/{id}/todas',response_model=list[Destino], status_code=200)
# async def listado_destinos_pcias_desde_hoy(id: str):
#     try:
#         return destinosSchema( await lista_dest_pcia_desde_hoy(id))
#     except:
#         return []

@destino.get('/pcia/{id}/{fecha}', response_model=list[dict],status_code=200)
async def listado_destinos_pcias_fecha(id: str, fecha: str):
    try:
        fecha = datetime.fromisoformat(fecha)
    except:
        raise HTTPException(406, "Fecha mal formada o inesperada")
    try:
        return  await lista_destinos_pcia_fecha(id, fecha)
    except:
        return []

@destino.post('/adddetalle')
async def detalle_destino( detalle: DetallesDestino):
    if type(detalle.fecha) == str:
        try:
            detalle.fecha = datetime.fromisoformat(detalle.fecha)
        except:
            raise HTTPException(406, "Fecha mal formada o inesperada")
    detalle = detalle.model_dump(exclude={"id"})
    try:
        rta = await nuevo_detalle( detalle)
    except:
       raise HTTPException(417, "Algún dato enviado es inválido")
    return "Detalle actualizado "+str(rta)


# // Supongamos que la fecha que estás buscando es "2023-12-15"
# var fechaBuscada = new Date("2023-12-15");

# // Consulta MongoDB para filtrar solo los elementos del array servicios que coincidan con la fecha
# db.destinos.find(
#   {
#     "pica_id": "asdfdasfa"
#     "detalles.fecha": fechaBuscada
#   },
#   {
#     _id: 1, 
#     lugar: 1, 
#     area: 1, 
#     provincia: 1 ,
#     pcia_id: 1 ,
#     detalles: {
#       $elemMatch: {
#         fecha: fechaBuscada
#       }
#     }
#   }
# );
