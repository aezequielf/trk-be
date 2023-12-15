from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.pcias import pcia
from routes.usuarios import usuario
from routes.opiniones import opinion
from routes.destinos import destinos


origenes = ["http://localhost:4200","http://127.0.0.1:4200"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origenes,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pcia,prefix="/pcias")
app.include_router(usuario,prefix="/usuarios")
app.include_router(opinion,prefix="/opina")
app.include_router(destinos,prefix="/destinos")


