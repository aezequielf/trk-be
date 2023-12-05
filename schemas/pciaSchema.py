def pciaSchema(pcia) ->  dict:
    return{
        "id": str(pcia['_id']),
        "nombre": pcia['nombre'],
    }
def pciasSchema(pcias) -> list:
    return [pciaSchema(pcia) for pcia in pcias]