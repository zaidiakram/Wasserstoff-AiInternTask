from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from api.rag_chatbot import query_rag_pipeline
from models.model import QueryRequest
import uvicorn
import os
from config import PathConfig
from pathlib import Path
from services.vectorstore import build_vector_store



app = FastAPI(title="Document RAG Chatbot")



@app.get("/Health_check")
def root():
    return {"message": "RAG Chatbot is running."}


@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    saved_files = []
    os.makedirs(PathConfig.DOCS_PATH, exist_ok=True)
    for file in files:
        filename = Path(file.filename)
        filepath = os.path.join(PathConfig.DOCS_PATH, file.filename)
        print(filepath)
        with open(filepath, "wb") as f:
            f.write(await file.read())
        saved_files.append(filename)

    try:
        doc_count = build_vector_store()
        return {"message": f"✅ Uploaded {len(saved_files)} files. Indexed {doc_count} documents."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/ask_question")
def ask_question(request: QueryRequest):
    try:
        answer = query_rag_pipeline(request.query, request.top_k)
        return {
            "query": request.query,
            "answer": answer
        }
    except Exception as e:
        return {"error": str(e)}
    

if __name__=="__main__":
    uvicorn.run("main:app", host="localhost", port=8080)

