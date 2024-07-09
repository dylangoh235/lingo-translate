from lingo_translate.mapper import AbstractModel
from transformers import pipeline
import torch

class TorchTransformerModel(AbstractModel):
    def __init__(self, **kwargs) -> None:
        self.model = kwargs.get("model", None)
    def translate(self, text: str, src_lang: str, tgt_lang: str, **kwargs) -> dict:
        translator = pipeline(f"translation_{src_lang}_to_{tgt_lang}", model=self.model)
        result = translator(text)
        
        return {"output": result[0]['translation_text']}

