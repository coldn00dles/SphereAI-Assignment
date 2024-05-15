import os
from ragmodel.ingestor import getDocument
from ragmodel.indexer import getRetriever
from ragmodel.ragchain import getRAGChain
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

class Message(BaseModel): 
    content: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ingestion 
docs = getDocument("docs/")

# Indexing / Embedding
ret = getRetriever(docs)

# RAG Chain
rag_chain = getRAGChain(ret)



@app.get("/api")  # return api status
async def hello_word():
    return "Yo! Hello world, The backend is running !!!"

@app.post("/api/chatbot/")
async def chatbot_response(question: Message):
    try:
        output = rag_chain.invoke(question.content)
        if output:
            return JSONResponse(content={"output": output}) 
        else:
            return JSONResponse(content={"output": "No answer found"})
    except HTTPException as http_error:
        raise http_error