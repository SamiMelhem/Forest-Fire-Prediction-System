from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/predict")
async def predict():
    return {"message": "Here is your prediction"}