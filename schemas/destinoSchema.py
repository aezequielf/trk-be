def destinoSchema(destino) ->  dict:
    return{
        "id": str(destino['_id']),
        "lugar": destino['lugar'],
        "area": destino['area'],
        "pcia": destino['pcia'],
        "pcia_id": destino["pcia_id"],
    }

def destinosSchema(destinos) -> list:
    return [destinoSchema(destino) for destino in destinos]

def detalleSchema(detalle) ->  dict:
    return{
        "id": str(detalle['_id']),
        "destino_id" : detalle["destino_id"],
        "lugar" : detalle["lugar"],
        "pcia": detalle['pcia'],
        "pcia_id": detalle["pcia_id"],
        "fecha": detalle['fecha'],
        "hora": detalle['hora'],
        "guia_id": detalle['guia_id'],
        "empresa": detalle["empresa"],
        "desc" : detalle["desc"]
    }

def detallesSchema(detalles) -> list:
    return [detalleSchema(detalle) for detalle in detalles]