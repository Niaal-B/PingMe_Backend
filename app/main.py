

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth ,dashboard

load_dotenv()

app = FastAPI(
    title="PingMe API",
    description="Backend for the real-time chat application.",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],  
)

app.include_router(auth.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to PingMe! FastAPI is running."}