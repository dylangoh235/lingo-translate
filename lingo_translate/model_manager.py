from lingo_translate.mapper import (
    AbstractModel,
    get_class_from_module,
    get_language_mapper,
    convert_language,
    MODEL_SERVICE_MAPPING_NAME,
)
from lingo_translate.exception import ServiceNotFoundException
import lingo_translate.model_modules as model_modules
from typing import Dict, Any


class ModelManager:
    """
    모델 기반의 번역 서비스를 관리하는 클래스입니다.

    Attributes
    ----------
    _model_mapping : Dict[str, str]
        서비스 이름과 해당 Model 클래스 이름을 매핑하는 사전입니다.
    model : model_modules.AbstractModel
        현재 활성화된 Model 객체입니다.

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

    MODEL_MAPPING: Dict[str, str] = MODEL_SERVICE_MAPPING_NAME

    def __init__(self) -> None:
        self.model = None

    def initialize_model(self, service: str, **kwargs) -> AbstractModel:
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
        if service in self.MODEL_MAPPING:
            model_module_name = self.MODEL_MAPPING[service]
            self.language_mapper = get_language_mapper(service)
            model_class = get_class_from_module(
                model_modules, model_module_name, AbstractModel
            )
            return model_class(**kwargs)
        else:
            raise ServiceNotFoundException(
                f"해당 {service}가 Model map에 존재하지 않는 서비스 입니다."
            )

    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
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
        converted_src_lan, converted_tgt_lan = convert_language(self.language_mapper, src_lan, tgt_lan)
        result = self.model.translate(query, converted_src_lan, converted_tgt_lan, **kwargs)
        return result

    def change_service(self, service: str, **kwargs) -> None:
        """
        서비스를 변경하고 해당 서비스에 맞는 API 객체를 새롭게 초기화합니다.

        Parameters
        ----------
        service : str
            변경할 서비스의 이름입니다.
        """
        self.model = self.initialize_model(service, **kwargs)
