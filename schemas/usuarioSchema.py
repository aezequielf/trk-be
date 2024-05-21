def usuarioSchema(usuario) -> dict:
    if not usuario['esguia']:
        return{
        "id": str(usuario['_id']), 
        "nombre": usuario['nombre'],
        "apellido": usuario['apellido'],
        "email": usuario['email'],
        "esguia": usuario['esguia'],
        "clave": usuario['clave'],
        "creado" : usuario['creado']
        }
    return {
    "id": str(usuario['_id']), 
    "nombre": usuario['nombre'],
    "apellido": usuario['apellido'],
    "email": usuario['email'],
    "esguia": usuario['esguia'],
    "clave": usuario['clave'],
    "creado" : usuario['creado'],
    "empresa" : usuario['empresa'],
    "matricula" : usuario['matricula'],
    "resolucion" : usuario['resolucion'],
    "cels" : usuario['cels'],
    "actividad" : usuario['actividad']
    }

def usuariosSchema(usuarios) -> list:
    return [usuarioSchema(usuario) for usuario in usuarios]

