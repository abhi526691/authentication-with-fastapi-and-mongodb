from fastapi import FastAPI
import api

app = FastAPI()

app.include_router(api.router)


@app.get('/')
def hello():
    return "hello world"