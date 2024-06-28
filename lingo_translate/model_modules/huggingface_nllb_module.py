from lingo_translate.mapper import AbstractModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers.tokenization_utils import TruncationStrategy
import torch


class HuggingFaceTranslation:
    """
    Huggingface에서 제공하는 모델을 활용하여 번역

    Huggingface에서 제공한 코드를 가져와 수정하였습니다.

    https://github.com/huggingface/transformers
    """

    def __init__(self, model_name: str = "facebook/nllb-200-distilled-1.3B"):
        self.load_model(model_name)

    def load_model(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def sanitize_parameters(
        self, src_lang=None, tgt_lang=None, stop_sequence=None, **generate_kwargs
    ):
        preprocess_params = {}
        postprocess_params = {}
        forward_params = generate_kwargs
        if stop_sequence:
            stop_sequence_ids = self.tokenizer.encode(
                stop_sequence, add_special_tokens=False
            )
            if len(stop_sequence_ids) > 1:
                raise ValueError(
                    "Stopping on a multiple token sequence is not supported."
                )
            generate_kwargs["eos_token_id"] = stop_sequence_ids[0]
        if src_lang is not None:
            preprocess_params["src_lang"] = src_lang
        if tgt_lang is not None:
            preprocess_params["tgt_lang"] = tgt_lang
        return preprocess_params, forward_params, postprocess_params

    def preprocess(
        self,
        *args,
        truncation=TruncationStrategy.DO_NOT_TRUNCATE,
        src_lang=None,
        tgt_lang=None,
    ):
        inputs = self.tokenizer._build_translation_inputs(
            *args,
            return_tensors="pt",
            truncation=truncation,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
        )
        return inputs

    def forward(self, model_inputs, **params):
        with torch.no_grad():
            in_b, _ = model_inputs["input_ids"].shape

            output_ids = self.model.generate(**model_inputs, **params)
            out_b = output_ids.shape[0]
            output_ids = output_ids.reshape(in_b, out_b // in_b, *output_ids.shape[1:])
        return {"output_ids": output_ids}

    def postprocess(self, model_outputs, clean_up_tokenization_spaces=False):
        return_name = "generated"
        records = []
        for output_ids in model_outputs["output_ids"][0]:
            record = {
                f"{return_name}_text": self.tokenizer.decode(
                    output_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                )
            }
            records.append(record)
        return records

    def calculate_perplexity(self, input_ids):
        with torch.no_grad():
            outputs = self.model(input_ids, labels=input_ids)
        return torch.exp(outputs.loss).item()


class HuggingFaceNllbModel(HuggingFaceTranslation, AbstractModel):
    """
    huggingface 모델을 번역하고 점수 계산을 위한 클래스

    Huggingface에서 제공한 코드를 가져와 수정하였습니다.

    https://github.com/huggingface/transformers

    preprocess, forward, postprocess 총 3단계로 나뉘고 preprocess에서는 토큰화, forward에는 인퍼런스, postprocess에서는 디코딩을 합니다.

    이후 입력된 텍스트의 토큰화 된 값을 이용하여 perplexity score를 측정합니다.

    """

    def translate(self, text: str, src_lang: str, tgt_lang: str, **kwargs):
        preprocess_params, forward_params, postprocess_params = (
            self.sanitize_parameters(src_lang=src_lang, tgt_lang=tgt_lang)
        )

        # Forward translation
        model_inputs = self.preprocess(text, **preprocess_params)
        model_outputs = self.forward(model_inputs, **forward_params)
        translation_text = self.postprocess(model_outputs, **postprocess_params)
        perplexity = self.calculate_perplexity(model_inputs["input_ids"])

        # Backward translation
        preprocess_params, forward_params, postprocess_params = (
            self.sanitize_parameters(src_lang=tgt_lang, tgt_lang=src_lang)
        )
        back_model_inputs = self.preprocess(text, **preprocess_params)
        back_model_outputs = self.forward(back_model_inputs, **forward_params)
        back_translation_text = self.postprocess(
            back_model_outputs, **postprocess_params
        )
        back_perplexity = self.calculate_perplexity(back_model_inputs["input_ids"])

        return {
            "output": translation_text[0]['generated_text'],
            "score": perplexity,
        }
