from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from models.pcias import Pcia
from models.usuarios import Usuario, Usuario_Login,Clave, Guia
from models.opiniones import Opinion
from models.destinos import Destino, DetallesDestino
from models.travesias import Travesia
from datetime import datetime

cnx_motor = AsyncIOMotorClient('localhost',27017)

c_pcias = cnx_motor.tpdb.pcias
c_usuarios = cnx_motor.tpdb.usuarios
c_opiniones = cnx_motor.tpdb.opiniones
c_destinos = cnx_motor.tpdb.destinos
c_detalles = cnx_motor.tpdb.detalles
c_travesias = cnx_motor.tpdb.travesias


# crud provincias
async def crea_prov(pcia: Pcia):
    rta = await c_pcias.insert_one(pcia)
    return rta.inserted_id

async def lista_pcias():
    cursor = c_pcias.find({}).sort("nombre",1)
    l_pcias = [una_prov async for una_prov in cursor]
    return l_pcias

async def una_pcia(id: ObjectId):
    pcia = await c_pcias.find_one({"_id": id})
    return pcia

async def eliminar_pcia(id: ObjectId):
    rta = await c_pcias.delete_one({"_id": id})
    return rta

# crud usuarios y perfiles

async def crea_usuario(usuario: Usuario_Login):
    rta = await c_usuarios.insert_one(usuario)
    return rta.inserted_id

async def lista_usuarios():
    cursor = c_usuarios.find({})
    l_usuarios = [un_user async for un_user in cursor]
    return l_usuarios

async def un_usuario(id: ObjectId):
    usuario = await c_usuarios.find_one({"_id": id})
    return usuario

async def un_usuario_mail( email : str):
    usuario = await c_usuarios.find_one({'email': email })
    return usuario

async def eliminar_usuario(id: ObjectId):
    rta = await c_usuarios.delete_one({"_id": id})
    return rta

async def actualiza_usuario(id: ObjectId, usuario: Usuario):
    rta = await c_usuarios.find_one_and_update({"_id": id},{"$set": dict(usuario)})
    return rta

# Actualizar datos de usuario para agregar datos de guía.

async def actualiza_pass_usuario(id: ObjectId, clave: Clave):
    rta = await c_usuarios.find_one_and_update({"_id": id},{"$set": clave})
    return rta

async def actualiza_usuario_aguia(id: ObjectId, datosgia: Guia):
    rta = await c_usuarios.find_one_and_update({"_id": id},{"$set": dict(datosgia)})
    return rta

# Actualizar opiniones de usuario para guías.

async def crea_opinion(opinion: Opinion):
    rta = await c_opiniones.insert_one(opinion)
    return rta

async def obtener_opiniones():
    cursor = c_opiniones.find({})
    opiniones = [opinion async for opinion in cursor]
    return opiniones

async def obtener_opinion_id(id : ObjectId):
    rta = await c_opiniones.find_one({'_id': id})
    return rta

# crud recorridos/ travesías

async def nuevo_destino(destino : Destino):
    rta = await c_destinos.insert_one(destino)
    return rta.inserted_id

async def lista_destinos():
    cursor = c_destinos.find({})
    l_destinos = [un_destino async for un_destino in cursor]
    return l_destinos

async def lista_destinos_pcia(pcia_id : str):
    cursor = c_destinos.find({"pcia_id" : pcia_id})
    l_destinos = [un_destino async for un_destino in cursor]
    return l_destinos

# cambiamos detalles por travesias que es su nombre correcto

async def nuevo_detalle( detalle : DetallesDestino):
    rta = await c_detalles.insert_one(detalle)
    return rta.inserted_id

async def nueva_travesia(travesia : Travesia):
    rta = await c_travesias.insert_one(travesia)
    if (rta.acknowledged):
        return rta.inserted_id
    return None

async def localiza_trav_id(id : ObjectId):
    travesia = await c_travesias.find_one({'_id' : id})
    return travesia

async def lista_trav_guia(id : str):
    cursor_travesias = c_travesias.find({'guia_id': id}).sort({'fecha' : 1})
    l_travesias = [travesia async for travesia in cursor_travesias]
    return l_travesias

async def list_travesias():
    cursortravesias = c_travesias.find({})
    l_travesias = [travesia async for travesia in cursortravesias]
    return l_travesias

async def actualiza_travesia(id: ObjectId, travesia: Travesia):
    rta = await c_travesias.find_one_and_update({"_id": id},{"$set":travesia})
    return rta

async def borra_travesia(id: ObjectId):
    rta = await c_travesias.delete_one({"_id": id})
    return rta


async def lista_destinos_pcia_fecha(pcia_id : str, fecha: datetime = None):
    if fecha==None:
        fecha_hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        pipeline = [
            {
                '$match': {
                    'fecha': {
                        '$gte': fecha_hoy
                    },
                'pcia_id': pcia_id
                    
                }
            }, {
                '$group': {
                    '_id': {
                        '$dateToString': {
                            'format': '%Y-%m-%d', 
                            'date': '$fecha'
                        }
                    }
                }
            }, {
                '$sort': {
                    'fecha': 1
                }
            }
        ]

        l_detalles = [un_detalle async for un_detalle in c_detalles.aggregate(pipeline)]
        return l_detalles

    pipeline = [
            {
                '$match': {
                    'pcia_id': pcia_id,
                    'fecha': { "$eq" :fecha}
                }
            },
            {
                '$group': { "_id" :"$lugar" ,
                           "destino_id" : {"$first" : "$destino_id"} }
            },
            {
                '$sort': {
               "lugar": 1  }
            }
        ]
    l_detalles = [un_detalle async for un_detalle in c_detalles.aggregate(pipeline)]
    return l_detalles

async def lista_dest_pcia_desde_hoy(pcia_id : str):
    fecha = datetime.today()
    pipeline = [
            {
                '$match': {
                    'pcia_id': pcia_id,
                    'fecha': { "$gte" :fecha}
                }
            },
            {
                '$group': { "_id" :"$lugar" ,
                           "destino_id" : {"$first" : "$destino_id"} }
            },
            {
                '$sort': {
               "_id": 1  }
            }
        ]
    l_detalles = [un_detalle async for un_detalle in c_detalles.aggregate(pipeline)]
    return l_detalles

async def destino_id(id: ObjectId):
    return await c_destinos.find_one({'_id': id})
    
async def lista_detalle_destinos(destino_id : str):
    fecha = datetime.today()
    l_detalles = [un_detalle async for un_detalle in c_detalles.find({"destino_id" : destino_id, "fecha" : { "$gte" : fecha}}).sort({ "fecha" : 1})] 
    return l_detalles
