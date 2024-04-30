import lingo.api_modules as api_modules
import lingo.model_modules as model_modules
from dotenv import load_dotenv
from typing import Dict
import os


def get_class(modules, model_name):
    return getattr(modules, model_name, None)


class APIManager:
    """
    API 기반의 번역 서비스를 관리하는 클래스입니다.

    Attributes
    ----------
    _api_mapping : Dict[str, str]
        서비스 이름과 해당 API 클래스 이름을 매핑하는 사전입니다.
    kwargs : dict
        API 초기화에 사용될 추가 인자들입니다.
    api : api_modules.AbstractAPI
        현재 활성화된 API 객체입니다.

    Parameters
    ----------
    service : str
        사용할 번역 서비스의 이름입니다.

    Methods
    -------
    initialize_api(service: str) -> api_modules.AbstractAPI
        주어진 서비스 이름에 따라 API 객체를 초기화하고 반환합니다.
    translate(query: str, src_lan: str, tgt_lan: str) -> dict
        주어진 텍스트를 번역하여 결과를 반환합니다.
    change_service(service: str) -> None
        서비스를 변경하고 해당 서비스의 API 객체를 초기화합니다.
    """

    _api_mapping: Dict[str, str] = api_modules.API_SERVICE_MAPPING_NAME

    def __init__(self, service: str, **kwargs) -> None:
        self.kwargs = kwargs
        self.api: api_modules.AbstractAPI = self.initialize_api(service)

    def initialize_api(self, service: str) -> api_modules.AbstractAPI:
        """
        주어진 서비스 이름에 해당하는 API 클래스를 초기화하고 인스턴스를 생성합니다.

        Parameters
        ----------
        service : str
            초기화할 번역 서비스의 이름입니다.

        Returns
        -------
        api_modules.AbstractAPI
            생성된 API 객체입니다.

        Raises
        ------
        ValueError
            지원하지 않는 서비스 이름이 주어졌을 때 발생합니다.
        """
        if service in self._api_mapping:
            api_class_name = self._api_mapping[service]
            api_class = get_class(api_modules, api_class_name)
            if not api_class:
                raise ValueError(f"No API class found for {api_class_name}")
            return api_class(**self.kwargs)
        else:
            raise ValueError(f"Unsupported service: {service}")

    def translate(self, query: str, src_lan: str, tgt_lan: str) -> dict:
        """
        주어진 텍스트를 번역하여 결과를 반환합니다.

        Parameters
        ----------
        query : str
            번역할 텍스트입니다.
        src_lan : str
            원본 언어의 코드입니다.
        tgt_lan : str
            목표 언어의 코드입니다.

        Returns
        -------
        dict
            번역 결과를 담은 사전입니다.
        """
        result = self.api.translate(query, src_lan, tgt_lan)
        return result

    def change_service(self, service: str) -> None:
        """
        서비스를 변경하고 해당 서비스에 맞는 API 객체를 새롭게 초기화합니다.

        Parameters
        ----------
        service : str
            변경할 서비스의 이름입니다.
        """
        self.api = self.initialize_api(service)


class ModelManager:
    """
    모델 기반의 번역 서비스를 관리하는 클래스입니다.

    Attributes
    ----------
    _model_mapping : Dict[str, str]
        서비스 이름과 해당 Model 클래스 이름을 매핑하는 사전입니다.
    api : model_modules.AbstractModel
        현재 활성화된 API 객체입니다.

    Parameters
    ----------
    service : str
        초기화할 모델 서비스의 이름입니다.

    Methods
    -------
    initialize_model(service: str) -> model_modules.AbstractModel
        주어진 서비스 이름에 따라 Model 객체를 초기화하고 반환합니다.
    translate(query: str, src_lan: str, tgt_lan: str) -> dict
        주어진 텍스트를 번역하여 결과를 반환합니다.
    change_service(service: str) -> None
        서비스를 변경하고 해당 서비스의 Model 객체를 초기화합니다.
    """

    _model_mapping: Dict[str, str] = model_modules.MODEL_SERVICE_MAPPING_NAME

    def __init__(self, service: str, **kwargs) -> None:
        self.kwargs = kwargs
        self.model: model_modules.AbstractModel = self.initialize_model(service)

    def initialize_model(self, service: str) -> model_modules.AbstractModel:
        """
        주어진 서비스 이름에 맞는 모델 객체를 초기화하고 반환합니다.

        Parameters
        ----------
        service : str
            초기화할 모델 서비스의 이름입니다.

        Returns
        -------
        model_modules.AbstractModel
            초기화된 모델 객체입니다.

        Raises
        ------
        ValueError
            주어진 서비스 이름이 지원되지 않거나, 모델 클래스를 찾을 수 없을 때 발생합니다.
        """
        if service in self._model_mapping:
            model_class_name = self._model_mapping[service]
            model_class = get_class(model_modules, model_class_name)
            if not model_class:
                raise ValueError(f"No model class found for {model_class_name}")
            return model_class(**self.kwargs)
        else:
            raise ValueError(f"Unsupported translation service: {service}")

    def translate(self, query: str, src_lan: str, tgt_lan: str) -> dict:
        """
        주어진 텍스트를 번역하여 결과를 반환합니다.

        Parameters
        ----------
        query : str
            번역할 텍스트입니다.
        src_lan : str
            원본 언어의 코드입니다.
        tgt_lan : str
            목표 언어의 코드입니다.

        Returns
        -------
        dict
            번역 결과를 담은 사전입니다.
        """
        result = self.model.translate(query, src_lan, tgt_lan)
        return result

    def change_service(self, service: str) -> None:
        """
        서비스를 변경하고 해당 서비스에 맞는 API 객체를 새롭게 초기화합니다.

        Parameters
        ----------
        service : str
            변경할 서비스의 이름입니다.
        """
        self.model = self.initialize_model(service)


class Translator:
    """
    다양한 번역 서비스 API를 통해 텍스트 번역을 관리하고 실행하는 클래스입니다.

    Attributes
    ----------
    api_manager : APIManager
        DeepL과 같은 API 기반 번역 서비스를 관리합니다.
    model_manager : ModelManager
        Hugging Face와 같은 모델 기반 번역 서비스를 관리합니다.

    Methods
    -------
    translate(query: str, src_lan: str, tgt_lan: str, service: str = "google", **kwargs)
        주어진 입력 텍스트를 지정된 소스 언어에서 목표 언어로 번역합니다.

        현재 지원하는 서비스는 deepl, google, papago, huggingface, langchain, torch 입니다.
    """

    def __init__(self):
        load_dotenv()
        self.api_manager: APIManager = APIManager("deepl")
        self.model_manager: ModelManager = ModelManager("huggingface")

    def translate(
        self, query: str, src_lan: str, tgt_lan: str, service: str = "google", **kwargs
    ):
        """
        입력된 텍스트를 지정된 소스 언어에서 목표 언어로 번역하여 결과를 반환합니다.

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

        if service in api_modules.API_SERVICE_MAPPING_NAME:
            manager = self.api_manager
        elif service in model_modules.MODEL_SERVICE_MAPPING_NAME:
            manager = self.model_manager
        else:
            raise ValueError("Unsupported translation service.")

        # TODO 모델, API마다 언어 코드가 다르기에 언어 inference 과정 추가
        manager.change_service(service)
        result = manager.translate(query, src_lan, tgt_lan, **kwargs)

        return result
