from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from models.pcias import Pcia
from models.usuarios import Usuario, Usuario_Login,Clave, Guia
from models.opiniones import Opinion
from models.destinos import Destino, DetallesDestino

cnx_motor = AsyncIOMotorClient('localhost',27017)

c_pcias = cnx_motor.tpdb.pcias
c_usuarios = cnx_motor.tpdb.usuarios
c_opiniones = cnx_motor.tpdb.opiniones
c_destinos = cnx_motor.tpdb.destinos

# crud provincias
async def crea_prov(pcia: Pcia):
    rta = await c_pcias.insert_one(pcia)
    return rta.inserted_id

async def lista_pcias():
    cursor = c_pcias.find({}).sort({'nombre':1})
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

async def actualiza_usuario_aguia(id: ObjectId, usuario: Usuario):
    rta = await c_usuarios.find_one_and_update({"_id": id},{"$set": dict(usuario)})
    return rta

# Actualizar opiniones de usuario para guías.

async def nueva_opinion_guia(id: ObjectId, opinion: Opinion):
    rta = await c_opiniones.insert_one(opinion)
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


# async def nuevo_detalle(id: ObjectId(), detalle : DetallesDestino):
#     rta = await c_destinos.find_one_and_update({"$push"{ "detalles" : detalle}}})
#     return rta