def usuarioSchema(usuario) -> dict:
    # cambio el objectid por string y como usuario ya es un dict no solo controlo eso y devuelvo el resto
    usuario['id'] = str(usuario['_id'])
    del(usuario['_id'])
    return usuario
    # schema = {
    #     "id": str(usuario['_id']), 
    #     "nombre": usuario['nombre'],
    #     "apellido": usuario['apellido'],
    #     "email": usuario['email'],
    #     "esguia": usuario['esguia'],
    #     "clave": usuario['clave'],
    #     "creado": usuario['creado']
    # }
    # schema.update({
    #         "empresa": usuario.get('empresa'),
    #         "matricula": usuario.get('matricula'),
    #         "resolucion": usuario.get('resolucion'),
    #         "cel": usuario.get('cel'),
    #         "actividad": usuario.get('actividad'),
    #         "celalt" : usuario.get('celalt')
    #     })
    # return schema

#esto lo aprendí después
    # # Agregar campo "celalt" si está presente en el usuario
    # if 'celalt' in usuario:
    #     schema["celalt"] = usuario['celalt']

    # # Agregar campos adicionales si el usuario es guía
    # if usuario['esguia']:
    #     schema.update({
    #         "empresa": usuario.get('empresa'),
    #         "matricula": usuario.get('matricula'),
    #         "resolucion": usuario.get('resolucion'),
    #         "cel": usuario.get('cel'),
    #         "actividad": usuario.get('actividad')
    #     })

# esta fue mi idea principal
# def usuarioSchema(usuario) -> dict:
#     if usuario['esguia']:

#             return {
#             "id": str(usuario['_id']), 
#             "nombre": usuario['nombre'],
#             "apellido": usuario['apellido'],
#             "email": usuario['email'],
#             "esguia": usuario['esguia'],
#             "clave": usuario['clave'],
#             "creado" : usuario['creado'],
#             "empresa" : usuario['empresa'],
#             "matricula" : usuario['matricula'],
#             "resolucion" : usuario['resolucion'],
#             "cel" : usuario['cel'],
#             "celalt" : usuario['celalt'],
#             "actividad" : usuario['actividad']
#             }

#     return{
#         "id": str(usuario['_id']), 
#         "nombre": usuario['nombre'],
#         "apellido": usuario['apellido'],
#         "email": usuario['email'],
#         "esguia": usuario['esguia'],
#         "clave": usuario['clave'],
#         "creado" : usuario['creado']
#         }

def usuariosSchema(usuarios) -> list:
    return [usuarioSchema(usuario) for usuario in usuarios]

