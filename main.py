from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

with open("prompt.txt", "r", encoding="utf-8") as f:
    structure = f.read()

prompt = ChatPromptTemplate.from_messages([
    ("system", "คุณคือคนที่ต้องสร้างโจทย์ competetive programming โดยต้องทำตามโครงสร้างใน human message อย่างเคร่งครัด"),
    ("human", "ฉันกำลังจะสอนนักเรียนระดับ สอวน. คอมพิวเตอร์ ให้เขียนโปรแกรมเรื่อง **{content}**\nช่วยสร้างโมดูลการเรียนรู้ที่มีโครงสร้างโปรเจกต์แบบเดียวกับหัวข้อ {content}  โดยมีรายละเอียดดังนี้\n\n:"+structure)
])

chain = prompt|llm

res = chain.invoke({"content":"binary search"})

with open(f"result/full.txt", "w", encoding="utf-8") as f:
    f.write(res.content)

txtfile = res.content.split("________________________________________")

fileName = ["readme.md", "Makefile", "include/header.h", "tests/main.cpp", "src/task.cpp"]
for file, name in zip(txtfile, fileName):
    with open(f"result/{name}", "w", encoding="utf-8") as f:
        f.write(file)

print("success")