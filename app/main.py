from fastapi import FastAPI

app = FastAPI(title="FastAPI Chat App")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Chat App!"}
