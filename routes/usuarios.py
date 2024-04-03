from fastapi import APIRouter, HTTPException
from schemas.usuarioSchema import usuarioSchema, usuariosSchema
from models.usuarios import Usuario, Usuario_Login, Clave, Credenciales
from db.mongo import crea_usuario, lista_usuarios, un_usuario, eliminar_usuario, actualiza_usuario, actualiza_pass_usuario, un_usuario_mail
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from passlib.context import CryptContext
from datetime import datetime

crypt = CryptContext(schemes="bcrypt")
usuario = APIRouter()

@usuario.get('/', response_model=list[Usuario], status_code=200)
async def listado_usuarios():
    return usuariosSchema( await lista_usuarios()) 

@usuario.get('/{id}', response_model=Usuario, status_code=200)
async def un_usuarios(id: str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    try:
        usuario = usuarioSchema(await un_usuario(ObjectId(id)))
    except:
        raise HTTPException(404, "No encontrado ese id")
    return usuario

@usuario.post('/login', response_model=str, status_code=202)
async def valida_usuario(credenciales: Credenciales):
    clave = await un_usuario_mail(credenciales.email)
    if clave=='vacio':
        raise HTTPException(404, 'Usuario y claves erroneos')
    if crypt.verify(credenciales.clave, clave):
        return 'usuaio ok'
    else:
        raise HTTPException(404, 'Combinacion usuario y claves incorrecto')


@usuario.post('/add', response_model=str, status_code=201)
async def nuevo_usuario(usuario: Usuario_Login):
    usuario = usuario.model_dump(exclude={"id"})
    if len(usuario["nombre"].split()) > 1:
        nombres = usuario["nombre"].split()
        usuario["nombre"] = ''
        for nombre in nombres:
            usuario["nombre"] += nombre.capitalize()+' '
        usuario["nombre"] =  usuario["nombre"].rstrip()
    else:
        usuario["nombre"]=usuario["nombre"].capitalize()
    if len(usuario["apellido"].split()) > 1:
        apellidos = usuario["apellido"].split()
        usuario["apellido"] = ''
        for apellido in apellidos:
            usuario["apellido"] += apellido.capitalize()+' '
        usuario["apellido"] = usuario["apellido"].rstrip()
    else:
        usuario["apellido"]=usuario["apellido"].capitalize()
    usuario["email"]=usuario["email"].lower()
    usuario["clave"]=crypt.hash(usuario["clave"])
    usuario["creado"]=datetime.now()
    try:
        rta = await crea_usuario(usuario)
    except DuplicateKeyError:
        raise HTTPException(409, 'El correo ya existe, no se puede duplicar')
    return "Usuario Creado Correctamente: "+str(rta)

@usuario.delete('/{id}', response_model=str, status_code=202)
async def un_usuarios(id: str):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    rta = await eliminar_usuario(ObjectId(id))
    if rta.acknowledged:
        if rta.deleted_count > 0:
            return f"Usuarios con id {id} Eliminado"
        else:
            return "Usuario Inexistente, nada borrado"
    raise HTTPException(500, 'Algo salio mal')

@usuario.put("/{id}", response_model=str, status_code=202)
async def actualizar_usuario(id: str, usuario: Usuario):
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    try:
        await actualiza_usuario(ObjectId(id),usuario)
    except DuplicateKeyError:
        raise HTTPException(403, "Ese Correo ya está en uso, no se puede actualizar")
    except: 
        raise HTTPException(500, "No se actualizo nada")
    return " Datos de usuario actualizado !!!!"

@usuario.put("/{id}/chpass", response_model=str, status_code=202)
async def actualizar_clave_usuario(id: str, clave: Clave):
    clave = clave.model_dump()
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    try:
        await actualiza_pass_usuario(ObjectId(id),clave)
    except: 
        raise HTTPException(500, "No se actualizo nada")
    return " Datos de usuario actualizado !!!!"

