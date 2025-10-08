from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PingMe Real-Time Chat API",
    description="Secured backend for chat rooms using WebSockets and JWT.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "PingMe API is up and running!"}
