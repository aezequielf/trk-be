from models.mongobase import MongoBaseModel


class Opinion(MongoBaseModel):
    guiaid : str
    estrellas: int
    opinion: str
    userid: str
    nombre: str

# funcion para agregar en algún módulo y que se pueda llamar usando el import

# def validate_object_id(object_id: str) -> ObjectId:
#     try:
#         return ObjectId(object_id)
#     except (TypeError, ValueError):
#         raise HTTPException(status_code=400, detail="Invalid ObjectId")