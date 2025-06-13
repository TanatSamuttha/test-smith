from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from tempfile import SpooledTemporaryFile
from fastapi import UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv

# init
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# RAG for example
loader = TextLoader("task_gen/example.txt", encoding="utf-8")
example = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=60)
chunks = text_splitter.split_documents(example)
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(chunks, embedding)
retrievers = vectorstore.as_retriever()

# Load prompt
with open("task_gen/prompt.txt", "r", encoding="utf-8") as f:
    structure = f.read()

# Call from API
class contentFromUser(BaseModel):
    content_name: str

async def generate_task(contentFromUser: contentFromUser) -> list[UploadFile]:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "คุณคือคนที่ต้องสร้างโจทย์ competetive programming โดยต้องทำตามโครงสร้างใน human message อย่างเคร่งครัด"),
        ("human", "ฉันกำลังจะสอนนักเรียนระดับ สอวน. คอมพิวเตอร์ ให้เขียนโปรแกรมเรื่อง **{content}**\nช่วยสร้างโมดูลการเรียนรู้ที่มีโครงสร้างโปรเจกต์แบบเดียวกับหัวข้อ {content}  โดยมีรายละเอียดดังนี้\n\n:"+structure+"รูปแบบต้องเหมือนกับเอกสารนี้ {context}")
    ])
    chain = prompt | llm
    content_name = contentFromUser.content_name.lower().replace(" ", "_")
    res = await chain.ainvoke({"content": content_name, "context": retrievers})

    taskfile = res.content.split("________________________________________")
    task_name = taskfile[0].replace("\n", "")
    pos = task_name.find('.txt')
    if pos != -1:
        task_name = task_name[pos + len('.txt'):]

    task_files = []
    file_name = ["readme.md", "Makefile", f"{task_name}.h", "main.cpp", f"{task_name}.cpp"]

    for file, name in zip(taskfile, file_name):
        temp_file = SpooledTemporaryFile()
        temp_file.write(file.encode("utf-8"))
        temp_file.seek(0)
        task_files.append(UploadFile(filename=name, file=temp_file))

    return task_files