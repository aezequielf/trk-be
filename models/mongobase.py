from pydantic import BaseModel,  root_validator
from typing import Optional
from bson import ObjectId

class MongoBaseModel(BaseModel):
    id: Optional[str] = None


    @root_validator(pre=True)
    def convert_id(cls, values):
        if '_id' in values:
            values['id'] = str(values['_id'])
        return values

    class Config:
        allow_population_by_name = True
        json_encoders = { ObjectId: str }
