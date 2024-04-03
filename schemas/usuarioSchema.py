def usuarioSchema(usuario) -> dict:
    return {
    "id": str(usuario['_id']), 
    "nombre": usuario['nombre'],
    "apellido": usuario['apellido'],
    "email": usuario['email'],
    "esguia": usuario['esguia'],
    "clave": usuario['clave'],
    "creado" : usuario['creado']
    }

def usuariosSchema(usuarios) -> list:
    return [usuarioSchema(usuario) for usuario in usuarios]

