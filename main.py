# fastapi dev main.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
class contentFromUser(BaseModel):
    content_name: str

# RAG for example
loader = TextLoader("example.txt", encoding="utf-8")
example = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=60)
chunks = text_splitter.split_documents(example)
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(chunks, embedding)
retrievers = vectorstore.as_retriever()

# Load prompt
with open("prompt.txt", "r", encoding="utf-8") as f:
    structure = f.read()

# API
@app.post("/generate-task")
async def generate_task(contentFromUser: contentFromUser):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "คุณคือคนที่ต้องสร้างโจทย์ competetive programming โดยต้องทำตามโครงสร้างใน human message อย่างเคร่งครัด"),
        ("human", "ฉันกำลังจะสอนนักเรียนระดับ สอวน. คอมพิวเตอร์ ให้เขียนโปรแกรมเรื่อง **{content}**\nช่วยสร้างโมดูลการเรียนรู้ที่มีโครงสร้างโปรเจกต์แบบเดียวกับหัวข้อ {content}  โดยมีรายละเอียดดังนี้\n\n:"+structure+"รูปแบบต้องเหมือนกับเอกสารนี้ {context}")
    ])
    chain = prompt | llm
    content_name = contentFromUser.content_name.lower().replace(" ", "_")
    res = chain.invoke({"content": content_name, "context": retrievers})

    with open(f"full.txt", "w", encoding="utf-8") as f:
        f.write(res.content)

    task_name, readme, makefile, header, main, task = res.content.split("________________________________________")
    task_name = task_name.replace("\n", "")
    pos = task_name.find('.txt')
    if pos != -1:
        task_name = task_name[pos + len('.txt'):]

    return {"task_name": task_name,
            "readme.md": readme,
            "Makefile": makefile,
            f"{task_name}.h": header,
            "main.cpp": main,
            f"{task_name}.cpp": task
            }