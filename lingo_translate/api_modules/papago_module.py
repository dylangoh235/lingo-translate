from lingo_translate.mapper import AbstractAPI
import urllib.request
import os


# TODO
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
