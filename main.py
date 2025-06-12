# fastapi dev main.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-03-25")

class contentFromUser(BaseModel):
    content_name: str

with open("prompt.txt", "r", encoding="utf-8") as f:
    structure = f.read()

@app.post("/generate-task")
async def generate_task(contentFromUser: contentFromUser):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "คุณคือคนที่ต้องสร้างโจทย์ competetive programming โดยต้องทำตามโครงสร้างใน human message อย่างเคร่งครัด"),
        ("human", "ฉันกำลังจะสอนนักเรียนระดับ สอวน. คอมพิวเตอร์ ให้เขียนโปรแกรมเรื่อง **{content}**\nช่วยสร้างโมดูลการเรียนรู้ที่มีโครงสร้างโปรเจกต์แบบเดียวกับหัวข้อ {content}  โดยมีรายละเอียดดังนี้\n\n:"+structure)
    ])
    chain = prompt|llm
    res = chain.invoke({"content": contentFromUser.content_name})

    readme, makefile, header, main, task = res.content.split("________________________________________")

    return {"readme.md": readme,
            "Makefile": makefile,
            "header.h": header,
            "main.cpp": main,
            "task.cpp": task
            }