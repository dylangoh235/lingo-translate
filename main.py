from lingo.manager import Translator
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class RequestBody(BaseModel):
    service: str
    query: str
    sourceLan: str
    targetLan: str
    kargs: dict | None


app = FastAPI()
translator = Translator()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/translate")
async def translate(request: RequestBody):
    """
    {
         service: "string", // model
         query: "string",
         sourceLan: "string",
         targetLan: "string",
         kargs: dict
    }

    """

    result = translator.translate(
        query=request.query,
        src_lan=request.sourceLan,
        tgt_lan=request.targetLan,
        service=request.service,
    )

    response = {"query": result["output"]}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
