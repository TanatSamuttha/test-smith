from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

with open("tagger/prompt.txt", encoding="utf-8") as f:
    prompt = f.read()

async def tagging(filemd):
    contents = await filemd.read()
    string_data = contents.decode("utf-8")

    prompt_template = PromptTemplate(
        input_variables = ["question_markdown"],
        template = prompt
    )

    chain = prompt_template | llm

    response = chain.invoke({"question_markdown": string_data})

    print(response.content)
    return response.content.split(",")