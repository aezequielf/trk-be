from fastapi import APIRouter, HTTPException
from schemas.opinionSchema import opinionSchema, opinionesSchema
from models.opiniones import Opinion
from db.mongo import nueva_opinion_guia
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


opinion = APIRouter()

@opinion.get('/')
async def nueva_opinion():
    return 'opinar aqui'