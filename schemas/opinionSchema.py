def opinionSchema(opinion) -> dict:
    return {
    "id": str(opinion['_id']), 
    "guiaid": opinion["guiaid"],
    "estrellas": opinion['estrellas'],
    "opinion": opinion['opinion'],
    "usId": opinion['usId'],
    "nombre": opinion['nombre']
    }

def opinionesSchema(opiniones) -> list:
    return [opinionSchema(opinion) for opinion in opiniones]