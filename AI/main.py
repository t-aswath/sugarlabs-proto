from fastapi import FastAPI
from model import invoke
from pydantic import BaseModel


app = FastAPI()


class Body(BaseModel):
    text: str


@app.post("/")
async def prett(request: Body):
    result = invoke(request.text)
    return {"message": result}
