from fastapi import APIRouter, HTTPException, status
from models.travesias import Travesia
from db.mongo import list_travesias, nueva_travesia, localiza_trav_id,borra_travesia, lista_trav_guia, actualiza_travesia, lista_travesias_pcia_desde_hoy
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from datetime import datetime

travesia = APIRouter()

@travesia.get('/')
async def listado_travesias():
    travesias = [Travesia(**travesia) for travesia in await list_travesias()]
    return travesias

@travesia.get('/guia/{id}')
async def listar_travesia_guia(id: str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Id incorrecto')
    travesiasxguia =  [Travesia(**travesia) for travesia in await lista_trav_guia(id) ]
    return travesiasxguia

@travesia.post('/add')
async def agrega_travesia(travesia : Travesia):
    if type(travesia.fecha) == str:
        try:
            travesia.fecha = datetime.fromisoformat(travesia.fecha)
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail= "Fecha mal formada o inesperada")
    travesia = travesia.model_dump(exclude={"id"})
    travesia_id = await nueva_travesia(travesia)
    if(travesia_id != None):
        return Travesia(**await localiza_trav_id(travesia_id))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="algo salio mal")


@travesia.delete('/del/{id}')
async def borrar_travesia(id : str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Id incorrecto')
    rta = await borra_travesia(ObjectId(id))
    if rta.acknowledged:
        if rta.deleted_count > 0:
            return f"Travesía  Eliminada"
        else:
            return "Travesia Inexistente, nada borrado"
    raise HTTPException(500, 'Algo salio mal')

@travesia.put('/actualiza')
async def act_travesia(travesia: Travesia):
    id = travesia.id
    travesia = travesia.model_dump(exclude={"id"})
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Id incorrecto')
    rta = Travesia(** await actualiza_travesia(ObjectId(id), travesia))
    return rta
# Todo

@travesia.get('/pcia/{id}/todas',response_model=list[dict], status_code=200)
async def listado_destinos_pcias_desde_hoy(id: str):
    try:
        return await lista_travesias_pcia_desde_hoy(id)
        # return destinosSchema( await lista_dest_pcia_desde_hoy(id))
    except:
        print('esta') 
        return []


# @travesia.get('/pcia/{id}/fechas', response_model=list[dict],status_code=200)
# async def listado_travesias_pcias_fecha(id: str):
#     try:
#         return  await lista_travesias_pcia_fecha(id)
#     except:
#         return []
    


# @travesia.get('/pcia/{id}/{fecha}', response_model=list[dict],status_code=200)
# async def listado_destinos_pcias_fecha(id: str, fecha: str):
#     try:
#         fecha = datetime.fromisoformat(fecha)
#     except:
#         raise HTTPException(406, "Fecha mal formada o inesperada")
#     try:
#         return  await lista_travesias_pcia_fecha(id, fecha)
#     except:
#         return []
    
# @travesia.get('/{id}')
# async def traer_destino(id: str):
#     try:
#         ObjectId(id).is_valid
#     except:
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Id invalido')
#     return destinoSchema(await destino_id(ObjectId(id)))

# @travesia.get('/lista/{id_destino}', response_model=list[DetallesDestino], status_code=200)
# async def listado_destinos_detas(id_destino :str):
#     try:
#         return detallesSchema(await lista_detalle_destinos(id_destino))
#     except:
#         raise HTTPException(406, "Algo salio mal")
    
