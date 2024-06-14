from lingo_translate.abstract import AbstractModel


class TorchTransformerModel(AbstractModel):
    def translate(self, text: str, src_lang: str, tgt_lang: str, **kwargs) -> dict:
        return super().translate(text, src_lang, tgt_lang, **kwargs)
