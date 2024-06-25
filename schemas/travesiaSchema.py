def travesiaSchema(travesia) ->  dict:
    schema = {
        "id": str(travesia['_id']),
        "destino_id" : travesia["destino_id"],
        "dificultad" : travesia["dificultad"],
        "lugar" : travesia["lugar"],
        "pcia": travesia['pcia'],
        "pcia_id": travesia["pcia_id"],
        "fecha": travesia['fecha'],
        "hora": travesia['hora'],
        "guia_id": travesia['guia_id'],
        "empresa": travesia["empresa"],
        "pencuentro": travesia["pencuentro"],
        "coordenadas": travesia["coordenadas"],
        "desc" : travesia["desc"],
        "ingreso" : travesia["ingreso"],
        "detingreso" : travesia["detingreso"],
        "traslado" : travesia["traslado"],
        "dettraslado": travesia["dettraslado"],
        "desayuno" : travesia["desayuno"],
        "rmarcha" : travesia["rmarcha"],
        "merienda" : travesia["merienda"],
        "detpension" : travesia["detpension"],
        "pernocte" : travesia["pernocte"],
        "detpernocte" : travesia["detpernocte"],
        "botiquin" : travesia["botiquin"],
        "detbotiquin" : travesia["detbotiquin"],
        "csatelital" : travesia["csatelital"],
        "cvhf" : travesia["cvhf"],
        "detcomunicaciones" : travesia["detcomunicaciones"],
        "rfoto" : travesia["rfoto"],
        "detfoto" : travesia["detfoto"],
        "scarga" : travesia["scarga"],
        "detcarga" : travesia["detcarga"],
        "imontania" : travesia["imontania"],
        "detindumentaria" : travesia["detindumentaria"],
        "cequipaje" : travesia["cequipaje"],
        "detcuidado" : travesia["detcuidado"],
        "precio" : travesia["precio"],
    }
    return schema


def travesiasSchema(travesias) -> list:
    schemas = [travesiaSchema(travesia) for travesia in travesias]
    return schemas
