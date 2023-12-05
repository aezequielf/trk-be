from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.pcias import pcia
from routes.usuarios import usuario


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


