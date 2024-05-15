from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def getRAGChain(retriever):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2, streaming=True)
    template = """You are a helpful assistant who tenders to questions asked about candidates using the context below, provided from their resumes. You are required to start your sentences with the words 'the candidate' and then proceed. Make sure to be to the point. You will be parsing through the contents of a resume, keep in mind. Do not start your response with the words candidate if asked about your purpose, only do so for questions relevant to the candidate.
    Context : {context} 
    The user has asked : {question}
    Answer : """

    prompt = PromptTemplate.from_template(template)

    lcel_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return lcel_chain