# ================================================
# 유저는 Translator class에서 translate method만 호출함
#
# ================================================
from lingo_translate.api_manager import APIManager
from lingo_translate.model_manager import ModelManager
from lingo_translate.mapper import (
    API_SERVICE_MAPPING_NAME,
    MODEL_SERVICE_MAPPING_NAME,
)
from lingo_translate.exception import (
    ServiceNotFoundException,
    OutputFormatNotValidException,
)
from dotenv import load_dotenv
from typing import Dict, Any


class Translator:
    """
    다양한 번역 서비스 API를 통해 텍스트 번역을 관리하고 실행하는 Facade 클래스입니다.

    Attributes
    ----------
    api_manager : APIManager
        현재 활성화된 서비스를 관리하는 APIManager 객체입니다.
    model_manager : ModelManager
        현재 활성화된 서비스를 관리하는 ModelManager 객체입니다.

    Methods
    -------
    translate(query: str, src_lan: str, tgt_lan: str, service: str = "google", **kwargs: Dict[str, Any])
        주어진 입력 텍스트를 지정된 소스 언어에서 목표 언어로 번역합니다.

        현재 지원하는 서비스는 deepl, google, papago, huggingface, langchain, torch 입니다.
    """

    def __init__(self):
        load_dotenv()
        self.api_manager: APIManager = APIManager()
        self.model_manager: ModelManager = ModelManager()

    def translate(
        self,
        query: str,
        src_lan: str,
        tgt_lan: str,
        service: str = "google",
        **kwargs: Dict[str, Any],
    ):
        """
        입력된 텍스트를 지정된 소스 언어에서 목표 언어로 번역하여 결과를 반환합니다.s

        Parameters
        ----------
        query : str
            번역할 입력 텍스트입니다.
        src_lan : str
            입력 텍스트의 언어입니다.
        tgt_lan : str
            목표 텍스트의 언어입니다.
        service : str, optional
            사용할 번역 서비스의 이름입니다. 기본값은 "google"입니다.
            현재 지원하는 서비스는 deepl, google, papago, huggingface, langchain, torch 입니다.

        Returns
        -------
        output : dict
            번역 결과와 관련 정보를 담은 딕셔너리입니다.
            예시) {"output": "Hello", "score": None}

        Raises
        ------
        ValueError
            지원하지 않는 번역 서비스를 지정했을 때 발생합니다.
        """

        if service in API_SERVICE_MAPPING_NAME:
            manager = self.api_manager
        elif service in MODEL_SERVICE_MAPPING_NAME:
            manager = self.model_manager
        else:
            raise ServiceNotFoundException("지원하지 않는 서비스 입니다.")

        manager.change_service(service)

        result = manager.translate(query, src_lan, tgt_lan, **kwargs)
        if "output" not in result:
            raise OutputFormatNotValidException("output이 결과에 없습니다.")

        response = {"output": result["output"], "score": result.get("score", 0)}
        return response
