from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def primera():
    return "hola trekkpoint"