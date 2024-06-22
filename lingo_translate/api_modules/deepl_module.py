from lingo_translate.mapper import AbstractAPI
import deepl
import os


class DeepLTranslateAPI(AbstractAPI):
    """
    DeepL 번역기
    """

    def __init__(self, **kwargs) -> None:
        self.endpoint = os.getenv("DEEPL_ENDPOINT", "https://api-free.deepl.com")
        self.translator = deepl.Translator(
            auth_key=os.getenv("DEEPL_AUTH_KEY"), server_url=self.endpoint
        )

    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
        result = self.translator.translate_text(query, target_lang=tgt_lan)
        return {"output": result.text}
