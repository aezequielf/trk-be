def destinoSchema(destino) ->  dict:
    return{
        "id": str(destino['_id']),
        "lugar": destino['lugar'],
        "area": destino['area'],
        "provincia": destino['provincia'],
        "pcia_id": destino["pcia_id"],
        "detalles": destino['detalles']
    }

def destinosSchema(destinos) -> list:
    return [destinoSchema(destino) for destino in destinos]