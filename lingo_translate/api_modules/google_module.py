from lingo_translate.abstract import AbstractAPI
from google.cloud import translate_v2 as google_translate
import os


# TODO GOOGLE TRANSLATE 테스트 필요
class GoogleTranslateAPI(AbstractAPI):
    """
    Google 번역기
    """

    def __init__(self, **kwargs) -> None:
        self.auth_key = os.getenv("GOOGLE_CREDENTIALS")
        self.translator = google_translate.Client(credentials=self.auth_key)

    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
        result = self.translator.translate(
            query, source_language=src_lan, target_language=tgt_lan
        )
        return {"output": result["translatedText"]}
