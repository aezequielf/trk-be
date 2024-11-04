from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from models.pcias import Pcia, Destino
from models.usuarios import Usuario, Usuario_Login,Clave, Guia
from models.opiniones import Opinion
from models.destinos import  DetallesDestino
from models.travesias import Travesia
from datetime import datetime
import random

cnx_motor = AsyncIOMotorClient('localhost',27017)

c_pcias = cnx_motor.tpdb.pcias
c_usuarios = cnx_motor.tpdb.usuarios
c_opiniones = cnx_motor.tpdb.opiniones
c_destinos = cnx_motor.tpdb.destinos
c_detalles = cnx_motor.tpdb.detalles
c_travesias = cnx_motor.tpdb.travesias
prestadores = cnx_motor.tpdb.prestadores


# crud provincias
async def crea_prov(pcia: Pcia):
    rta = await c_pcias.insert_one(pcia)
    return rta.inserted_id

async def lista_pcias():
    cursor = c_pcias.find({},{'destinos' : 0}).sort("nombre",1)
    l_pcias = [Pcia(**una_prov) async for una_prov in cursor]
    return l_pcias

async def una_pcia(id: ObjectId):
    pcia = await c_pcias.find_one({"_id": id},{'destinos': 0})
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

async def agrega_validacion_guia(id: ObjectId, provincia : str, resolucion : str):
    # genero numero aleatorios
    num = ''
    for a in [str(random.randint(0,9)) for _ in range(5)]:
        num += a
    token = str(id)[:9]+'f'+num
    rta = await c_usuarios.find_one({"_id": id})
    if "validacion" in rta and provincia in [valid["provincia"] for valid in rta["validacion"]]:
        return None
    datos_validar =  { "provincia" : provincia , "token" : token, "resolucion": resolucion, "validado": False }
    await c_usuarios.find_one_and_update({"_id": id}, {"$push": {"validacion" : datos_validar}})
    return datos_validar

async def obtener_prestador(resolucion : str, email : str = None):
    if (email == None):
        cursor = prestadores.find({"resolucion" :  resolucion})
        rta = [prestador async for prestador in cursor]
        return rta 
    rta = await prestadores.find_one({"email": email, "resolucion" : resolucion})
    return rta

async def marcar_prestador(id : ObjectId):
    rta = prestadores.update_one({"_id" : id},{ "$set" : {"marcado" : True}})
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
#Destinos dentro de la coleccion provincias

# esta está obsoleta
async def nuevo_destino(id: ObjectId, destino : Destino):
    destino['id'] = str(ObjectId())
    rta = await c_pcias.find_one_and_update({'_id': id},{ '$push': {'destinos' : destino }})
    return rta


async def lista_destinos(criterio : str = None):
    pipe = [
        {
            '$unwind': {
                'path': '$destinos'
            }
        }, {
            '$match': {
                'destinos.lugar': {
                    '$regex' : criterio,
                    '$options' : 'i'
                }

            }
        }
    ]

    if(criterio == None):
        pipe = [
            {
                '$unwind': {
                    'path': '$destinos'
                }
            }
        ]
    cursor = c_pcias.aggregate(pipe)
    l_destinos = [Pcia(**destino) async for destino in cursor]
    return l_destinos

async def lista_destinos_pcia(pcia_id : ObjectId):
    agregacion = [
        {
            '$match': {
                '_id': pcia_id
            }
        }, {
            '$unwind': {
                'path': '$destinos'
            }
        }, {
            '$sort': {
                "destinos.lugar": 1
            }
        }
    ]
    cursor = c_pcias.aggregate(agregacion)
    l_destinos = [Pcia(**destino) async for destino in cursor]
    return l_destinos

# cambiamos detalles por travesias que es su nombre correcto

# async def nuevo_detalle( detalle : DetallesDestino):
#     rta = await c_detalles.insert_one(detalle)
#     return rta.inserted_id

async def nueva_travesia(travesia : Travesia):
    rta = await c_travesias.insert_one(travesia)
    if (rta.acknowledged):
        return rta.inserted_id
    return None

async def localiza_trav_id(id : ObjectId):
    travesia = await c_travesias.find_one({'_id' : id})
    return travesia

async def lista_trav_guia(id : ObjectId):
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


# async def lista_travesias_pcia_fecha(pcia_id : str, fecha: datetime = None):
#     if fecha==None:
#         fecha_hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#         pipeline = [
#             {
#                 '$match': {
#                     'fecha': {
#                         '$gte': fecha_hoy
#                     },
#                 'pcia_id': pcia_id
                    
#                 }
#             }, {
#                 '$group': {
#                     '_id': {
#                         '$dateToString': {
#                             'format': '%Y-%m-%d', 
#                             'date': '$fecha'
#                         }
#                     }
#                 }
#             }, {
#                 '$sort': {
#                     'fecha': 1
#                 }
#             }
#         ]

#         l_detalles = [un_detalle async for un_detalle in c_detalles.aggregate(pipeline)]
#         return l_detalles

#     pipeline = [
#             {
#                 '$match': {
#                     'pcia_id': pcia_id,
#                     'fecha': { "$eq" :fecha}
#                 }
#             },
#             {
#                 '$group': { "_id" :"$lugar" ,
#                            "destino_id" : {"$first" : "$destino_id"} }
#             },
#             {
#                 '$sort': {
#                "lugar": 1  }
#             }
#         ]
#     l_detalles = [un_detalle async for un_detalle in c_detalles.aggregate(pipeline)]
#     return l_detalles

async def lista_travesias_pcia_desde_hoy(pcia_id : str):
    fecha = datetime.today()
    pipeline = [
    {
        '$match': {
            'pcia_id': pcia_id, 
            'fecha': {
                '$gte': fecha
            }
        }
    }, {
        '$group': {
            '_id': '$lugar', 
            'destino_id': {
                '$first': '$destino_id'
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }, {
        '$project': {
            'lugar': '$_id', 
            '_id': 0, 
            'destino_id': 1
        }
    }
    ]
    l_destinos = [un_destino async for un_destino in c_travesias.aggregate(pipeline)]
    return l_destinos

async def destino_id(id: ObjectId):
    return await c_destinos.find_one({'_id': id})
    
async def lista_detalle_destinos(destino_id : str):
    fecha = datetime.today()
    l_detalles = [un_detalle async for un_detalle in c_detalles.find({"destino_id" : destino_id, "fecha" : { "$gte" : fecha}}).sort({ "fecha" : 1})] 
    return l_detalles
