from lingo_translate.manager import Translator
from lingo_translate.mapper import API_SERVICE_MAPPING_NAME, MODEL_SERVICE_MAPPING_NAME
from lingo_suggestion.model_load import SUGGESTION_SERVICE_MAPPING_NAME
import lingo_translate.exception as exception
from lingo_suggestion.suggestion import synonym_suggestion
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn


load_dotenv()

with open("temp_schema.json", mode="rt", encoding="utf-8") as patched_schema:
    schema_to_patch = json.load(patched_schema)

class RequestBody(BaseModel):
    service: str
    query: str
    sourceLan: str
    targetLan: str
    kwargs: dict | None


class SuggestionBody(BaseModel):
    model: str
    targetWord: str
    sentence: bool
    cntxt_len: int
    text: str
    abbreviation: bool


app = FastAPI()
translator = Translator()


@app.exception_handler(exception.InvalidLanguageCodeException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=jsonable_encoder({"detail": str(exc)}))


@app.exception_handler(exception.LanguageMapperNotFoundException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=jsonable_encoder({"detail": str(exc)}))


@app.exception_handler(exception.OutputFormatNotValidException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=jsonable_encoder({"detail": str(exc)}))


@app.exception_handler(exception.ModuleNotFoundException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=jsonable_encoder({"detail": str(exc)}))


@app.exception_handler(exception.ServiceNotFoundException)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=jsonable_encoder({"detail": str(exc)}))


@app.get("/lingo-ai/api/translate")
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
        **request.kwargs,
    )
    return response


@app.get("/lingo-ai/api/model-list")
async def model_list():
    data = {
        "models": {
            "translationModel": list(MODEL_SERVICE_MAPPING_NAME.keys())
            + list(API_SERVICE_MAPPING_NAME.keys()),
            "suggestionModel": list(SUGGESTION_SERVICE_MAPPING_NAME.keys()),
        },
    }
    return data


@app.get("/lingo-ai/api/suggestion")
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
        abbreviation=request.abbreviation,
    )

    response = {"suggestions": synonyms}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
