

from fastapi import FastAPI
from dotenv import load_dotenv

from app.api import auth 

load_dotenv()

app = FastAPI(
    title="PingMe API",
    description="Backend for the real-time chat application.",
    version="1.0.0"
)


app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to PingMe! FastAPI is running."}