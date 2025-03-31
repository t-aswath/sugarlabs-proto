import json
from dotenv import load_dotenv
from fastapi import FastAPI
from pdtypes import Body, Response
from model import chain, invoke
from langsmith import traceable

load_dotenv()

app = FastAPI()


@traceable(name="predict", run_type="tool")
@app.post("/")
async def predict(request: Body) -> Response:
    try:
        result = await invoke(request.text)
        return json.loads(result.content)
    except json.JSONDecodeError:
        return Response(suggestions=[])


@traceable(name="predict", run_type="tool")
@app.post("/chain")
async def start(request: Body) -> Response:
    try:
        result = await chain(request.text, request.level)
        return result
    except json.JSONDecodeError:
        return Response(suggestions=[])
