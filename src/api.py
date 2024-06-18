from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from the server!"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}