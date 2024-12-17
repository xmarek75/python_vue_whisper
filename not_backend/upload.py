from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

# Složka pro ukládání souborů
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "File successfully uploaded"}
