import requests
from typing import List, Optional
from pydantic import BaseModel
import io

class DocumentResponse(BaseModel):
    filename: str
    text: str
    metadata: dict = {}

class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[dict]
    themes: str

class DocumentClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def upload_files(self, files: List[io.BytesIO]) -> dict:
        """Upload and process documents"""
        try:
            file_data = [("files", (file.name, file.getvalue())) for file in files]
            response = requests.post(
                f"{self.base_url}/upload",
                files=file_data
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def ask_question(self, query: str, doc_filter: Optional[List[str]] = None) -> dict:
        """Query the document collection"""
        try:
            payload = {
                "query": query,
                "filter": doc_filter or []
            }
            response = requests.post(
                f"{self.base_url}/ask",
                json=payload
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_document(self, doc_id: str) -> DocumentResponse:
        """Retrieve a specific document"""
        response = requests.get(f"{self.base_url}/documents/{doc_id}")
        return DocumentResponse(**response.json())