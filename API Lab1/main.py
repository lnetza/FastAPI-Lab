from fastapi import FastAPI

app = FastAPI()


@app.get("/")

def home():
    return {"url": "https://www.google.com"}