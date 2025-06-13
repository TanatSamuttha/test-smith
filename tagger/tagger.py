from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from tagger import PDF_MD

from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

with open("tagger/prompt.txt", encoding="utf-8") as f:
    prompt = f.read()

async def tagging(filepdf):
    string_md = await PDF_MD.convert_pdf_to_markdown_string(filepdf)

    prompt_template = PromptTemplate(
        input_variables = ["question_markdown"],
        template = prompt
    )

    chain = prompt_template | llm

    response = await chain.ainvoke({"question_markdown": string_md})

    print(response.content)
    return response.content.replace(" ", "").split(",")