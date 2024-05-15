import os  
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

embed_ada = OpenAIEmbeddings(model = "text-embedding-ada-002")

"""Used for getting a RetrieverVectorStore instance

documents -> list of documents from ingestor.getDocument"""
def getRetriever(documents):
    vecstore = FAISS.from_documents(documents,embed_ada)
    return vecstore.as_retriever(search_type = "mmr",
                         search_kwargs = {"k" : 3,"fetch_k" : 20})
