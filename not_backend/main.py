# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import *  # Importujeme funkci z utils.py
from FasterWhisper import FasterWhisper
import os
from pydantic import BaseModel
from fastapi.responses import FileResponse
app = FastAPI()

# Nastavení CORS, aby Quasar mohl přistupovat k FastAPI serveru
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],  # Povolení přístupu pro Quasar na localhost:9000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nastavení složky pro nahrávání souborů
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Uchovává informace o posledním nahraném souboru
last_uploaded_file = {"filename": None}

# Pydantic model pro validaci dat
class TextData(BaseModel):
    text: str   
# Cesta k souboru
FILE_PATH = "../vue_folder/public/data.json"

#nahrani modelu
transcriber = FasterWhisper(model_size="base", device="cpu", compute_type="int8")

@app.get("/api/whisper")
async def whisper():
    name = "video_sample.mp4" # odstranit pozdeji, jen pro testovani
    file_name = last_uploaded_file.get("filename")
    if not file_name:
        raise HTTPException(status_code=400, detail="Žádný soubor nebyl nahrán.")
    message = transcriber.transcribe(file_name)  # Volání funkce z utils.py
    print(message)
    # Nahrazení nových řádků za <br> pro správné zobrazení na webu
    #message_with_breaks = message.replace("\n", "<br>")
    return JSONResponse(content={"message": message})

@app.get("/api/data")
async def get_data():
    data = {"message": "Hello!"}
    return JSONResponse(content=data)

# Endpoint pro nahrávání souborů
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        
        # Uložíme soubor do složky uploads
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        # Uložení názvu souboru pro další použití
        #last_uploaded_file["filename"] = file.filename
        last_uploaded_file["filename"]=file_location
        with open(file_location, "wb") as f:
            f.write(await file.read())
        return JSONResponse(content={"message": "File successfully uploaded", "filename": file.filename})
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=400)

# Endpoint pro uložení textu do souboru
@app.post("/api/save_text_to_json")
async def save_text_endpoint(data: TextData):
    try:
        # Zavolání funkce pro uložení textu
        save_text_to_file(FILE_PATH, data.text)
        return {"message": "Text byl úspěšně uložen do souboru."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chyba při ukládání: {e}")
#endpoint pro ziskani videa
@app.get("/get_video/{filename}")
async def get_video(filename: str):
    file_path = f"../backend/uploads/{filename}"
    return FileResponse(file_path)

# Spuštění serveru: uvicorn main:app --reload


