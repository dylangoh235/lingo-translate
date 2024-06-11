from lingo_translate.manager import Translator
from lingo_suggestion.engine import synonym_recommendation
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class RequestBody(BaseModel):
    service: str
    query: str
    sourceLan: str
    targetLan: str
    kargs: dict | None


class SuggestionBody(BaseModel):
    model: str
    targetWord: str
    sentence: bool
    cntxt_len: int
    text: str
    abbreviation: bool


class ResponseBody(BaseModel):
    score: int
    query: str


app = FastAPI()
translator = Translator()


@app.get("/translate")
async def translate(request: RequestBody):
    """
    {
         service: "string", // model
         query: "string",
         sourceLan: "string",
         targetLan: "string",
         kwargs: dict
    }

    """

    response = translator.translate(
        query=request.query,
        src_lan=request.sourceLan,
        tgt_lan=request.targetLan,
        service=request.service,
    )
    return response


@app.get("/suggestion")
async def suggestion(request: SuggestionBody):
    synonym_recommend = synonym_recommendation(
        model=request.model,
        targetWord=request.targetWord,
        sentence=request.sentence,
        cntxt_len=request.cntxt_len,
        text=request.text,
    )

    response = {"suggestions": synonym_recommend.post_processing()}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
