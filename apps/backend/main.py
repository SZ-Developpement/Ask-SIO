from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Ask SIO API is running"}