from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer #, OAuth2PasswordRequestForm
from schemas.usuarioSchema import usuarioSchema, usuariosSchema
from models.usuarios import Usuario, Usuario_Login, Clave, Credenciales, Guia
from db.mongo import crea_usuario, lista_usuarios, un_usuario, eliminar_usuario, actualiza_usuario,\
actualiza_pass_usuario, un_usuario_mail, actualiza_usuario_aguia
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

OAuth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes="bcrypt")
ALGENC= "HS256"
TOKEN_DURATION= 30
SECRET = "metIcETUSTrYPTorDemEgAMInFedNODyFasitudmetIcETUSTrYPTorDemEgAMInFedNODyFasitud"

usuario = APIRouter()




@usuario.get('/', response_model=list[Usuario], status_code=200)
async def listado_usuarios():
    return usuariosSchema( await lista_usuarios()) 

async def current_user(token: str = Depends(OAuth2)):
    try:
        id_usuario = jwt.decode(token,SECRET, algorithms=ALGENC).get("sub")
        if id_usuario == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Algo Salió mal', 
                            headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail='Credenciales incorrectas o token inváldo/expirado !!!', 
                    headers={"WWW-Authenticate": "Bearer"}) 
    try:
        usuario = Usuario(**usuarioSchema(await un_usuario(ObjectId(id_usuario))))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Algo Salió mal sub erroneo', 
                            headers={"WWW-Authenticate": "Bearer"})
    return usuario

@usuario.get("/yo")
async def funcion_yo(valor : Usuario = Depends(current_user)):
    return valor

@usuario.post("/login")
async def login_user(form: Credenciales):
    try:
        usuario = usuarioSchema(await un_usuario_mail(form.email))
    except TypeError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Usuario y claves erroneos")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Algo Salió mal")
    if crypt.verify(form.clave, usuario['clave']):
        expire= datetime.utcnow()+ timedelta(minutes=TOKEN_DURATION)
        token ={
            "sub" : usuario["id"],
            "exp": expire,
        }
        return {"token": jwt.encode(token, SECRET, algorithm=ALGENC ) , "type": "bearer"}
    raise HTTPException(404, 'Combinacion usuario y claves incorrecto')
    

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

@usuario.post('/add', response_model=str, status_code=201)
async def nuevo_usuario(usuario: Usuario_Login):
    usuario = usuario.model_dump(exclude={"id"})
    usuario["nombre"]=usuario["nombre"].title()
    usuario["apellido"]=usuario["apellido"].title()
    usuario["email"]=usuario["email"].lower()
    usuario["clave"]=crypt.hash(usuario["clave"])
    usuario["creado"]=datetime.now()
    try:
        rta = await crea_usuario(usuario)
    except DuplicateKeyError:
        raise HTTPException(409, 'El correo ya existe, no se puede duplicar')
    return "Ok: "+str(rta)

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

@usuario.put("/{id}/aguia", response_model=str, status_code=202)
async def actualizar_guia(id: str, guia: Guia ):
    guia = guia.model_dump()
    try:
        ObjectId(id).is_valid
    except:
        raise HTTPException(406, "Id inválido")
    try:
        await actualiza_usuario_aguia(ObjectId(id),guia)
    except: 
        raise HTTPException(500, "No se actualizo nada")
    return " Datos de usuario actualizado !!!!"



