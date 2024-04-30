import deepl
from google.cloud import translate_v2 as google_translate
import urllib.request
from abc import ABC, abstractmethod
import os

API_SERVICE_MAPPING_NAME = {
    "deepl": "DeepLTranslateAPI",
    "google": "GoogleTranslateAPI",
    "papago": "NaverPapagoAPI",
}


class AbstractAPI(ABC):
    @abstractmethod
    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
        pass


class DeepLTranslateAPI(AbstractAPI):
    """
    DeepL 번역기
    """

    def __init__(self, **kwargs) -> None:
        self.endpoint = os.getenv("DEEPL_ENDPOINT", None)
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.translator = deepl.Translator(self.auth_key, server_url=self.endpoint)

    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
        result = self.translator.translate_text(query, target_lang=tgt_lan)
        # {'output': [{'generated_text': '안녕하세요'}]}
        return {"output": result.text}


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


class NaverPapagoAPI(AbstractAPI):
    """
    Naver Papago 번역기
    """

    def __init__(self, **kwargs) -> None:
        self.client_id = os.getenv("NAVER_CLIENT_ID")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET")
        self.url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
        request = urllib.request.Request(self.url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", self.client_id)
        request.add_header("X-NCP-APIGW-API-KEY", self.client_secret)

        encText = urllib.parse.quote(query)
        data = f"source={src_lan}&target={tgt_lan}&text={encText}"
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            print(response_body.decode("utf-8"))
            # {'output': '{"message":{"result":{"srcLangType":"en","tarLangType":"ko","translatedText":"안녕하세요."}}}'}
            return {"output": response_body.decode("utf-8")}
