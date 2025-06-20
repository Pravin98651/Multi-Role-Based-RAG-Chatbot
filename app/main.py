from typing import Dict
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .services.chat_service import ChatService
from dotenv import load_dotenv
from .services.document_processor import DocumentProcessor

load_dotenv()

app = FastAPI()
security = HTTPBasic()
chat_service = ChatService()
document_processor = DocumentProcessor()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}

class ChatRequest(BaseModel):
    message: str


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}


@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"], "username": user["username"]}

#
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}

def startup_load_documents():
    try:
        print("[Startup] Loading and indexing documents...")
        document_processor.load_documents()
        print("[Startup] Document indexing complete.")
    except Exception as e:
        print(f"[Startup] Error loading documents: {e}")

@app.on_event("startup")
def on_startup():
    startup_load_documents()


@app.post("/chat")
def chat(request: ChatRequest, user=Depends(authenticate)):
    try:
        print(f"[Chat] User: {user['username']} | Role: {user['role']} | Message: {request.message}")
        response = chat_service.generate_response(
            role=user["role"],
            query=request.message
        )
        return {
            "response": response,
            "role": user["role"],
            "username": user["username"]
        }
    except Exception as e:
        import traceback
        print(f"[Chat] Error: {e}")
        traceback.print_exc()
        return {
            "response": f"Sorry, an error occurred: {str(e)}",
            "role": user["role"],
            "username": user["username"]
        }