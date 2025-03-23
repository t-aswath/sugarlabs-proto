from fastapi import FastAPI
import json
from model import invoke
from pdtypes import Body, Response


app = FastAPI()


@app.post("/")
async def predict(request: Body) -> Response:
    result = await invoke(request.text)
    try:
        response = json.loads(result.content)
        return response
    except json.JSONDecodeError:
        return Response(suggestions=[])

