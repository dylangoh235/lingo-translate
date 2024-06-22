from lingo_translate.manager import Translator
from lingo_translate.mapper import API_SERVICE_MAPPING_NAME, MODEL_SERVICE_MAPPING_NAME
import lingo_translate.exception as exception
from lingo_suggestion.suggestion import synonym_suggestion
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

load_dotenv()

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


@app.exception_handler(exception.InvalidLanguageCodeException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={exc})


@app.exception_handler(exception.LanguageMapperNotFoundException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={exc})


@app.exception_handler(exception.OutputFormatNotValidException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={exc})


@app.exception_handler(exception.ModuleNotFoundException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={exc})


@app.exception_handler(exception.ServiceNotFoundException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={exc})


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


@app.get("/model-list")
async def model_list():
    return [MODEL_SERVICE_MAPPING_NAME] + [API_SERVICE_MAPPING_NAME]


@app.get("/suggestion")
async def suggestion(request: SuggestionBody):
    
    """
    model : string, choose model to suggest synonym

    target_word : integer, index of target word

    sentence : bool, choose sentence-by-sentence or word-by-word

    cntxt_len : integer, number of units to check context

    text : string, paragraph including target word

    abbreviation : bool, whether or not to abbreviation conversion to add synonym suggestion
    """

    synonyms = synonym_suggestion(request.model).suggestion(
        target_word=request.targetWord,
        sentence=request.sentence,
        cntxt_len=request.cntxt_len,
        text=request.text,
        abbreviation=request.abbreviation
    )

    response = {"suggestions": synonyms}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
