# fastapi dev API.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from task_gen import taskgen
from tagger import tagger

from fastapi.responses import StreamingResponse
from io import BytesIO
import zipfile

app = FastAPI()

class contentName(BaseModel):
    content_name: str

@app.post("/task-gen")
async def task_gen(req: contentName):
    task_files = taskgen.generate_task(req)

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipf:
        for upload_file in task_files:
            upload_file.file.seek(0)
            zipf.writestr(upload_file.filename, upload_file.file.read())
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/zip", headers={
        "Content-Disposition": f"attachment; filename={req.content_name}_tasks.zip"
    })

@app.post("/get-tag")
async def read_file(file: UploadFile = File(...)):
    tag = await tagger.tagging(file)
    return {"tag": tag}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ระบุ origin ที่อนุญาต (หรือใช้ ["*"] ชั่วคราว)
    allow_credentials=True,
    allow_methods=["*"],    # อนุญาตทุก method เช่น GET, POST, OPTIONS
    allow_headers=["*"],    # อนุญาตทุก header
)