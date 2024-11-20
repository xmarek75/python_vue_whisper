# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import *  # Importujeme funkci z utils.py
app = FastAPI()

# Nastavení CORS, aby Quasar mohl přistupovat k FastAPI serveru
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],  # Povolení přístupu pro Quasar na localhost:9000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/whisper")
async def whisper():
    message = use_whisper()  # Volání funkce z utils.py
    return JSONResponse(content={"message": message})

@app.get("/api/data")
async def get_data():
    data = {"message": "Hello!"}
    return JSONResponse(content=data)

# Spuštění serveru: uvicorn main:app --reload
