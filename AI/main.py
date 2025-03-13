from fastapi import FastAPI
from model import invoke
from pydantic import BaseModel


app = FastAPI()


class Body(BaseModel):
    text: str


@app.post("/")
async def predict(request: Body):
    result = await invoke(request.text)
    return {"message": result}
