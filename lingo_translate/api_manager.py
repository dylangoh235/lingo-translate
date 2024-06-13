from lingo_translate.abstract import AbstractAPI
from lingo_translate.mapper import (
    get_class_from_module,
    get_language_mapper,
    API_SERVICE_MAPPING_NAME,
)
from lingo_translate.exception import (
    ServiceNotFoundException,
    InvalidLanguageCodeException,
)
import lingo_translate.api_modules as api_modules
from typing import Dict, Any


class APIManager:
    """
    API 기반의 번역 서비스를 관리하는 클래스입니다.

    Attributes
    ----------
    _api_mapping : Dict[str, str]
        서비스 이름과 해당 API 클래스 이름을 매핑하는 사전입니다.
    kwargs : Dict[str, Any]
        API 초기화에 사용될 추가 인자들입니다.
    api
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

    API_MAPPING: Dict[str, str] = API_SERVICE_MAPPING_NAME

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        self.kwargs = kwargs
        self.api = None
        self.language_mapper = None

    def initialize_api(self, service: str) -> AbstractAPI:
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
        if service in self.API_MAPPING:
            api_module_name = self.API_MAPPING[service]
            self.language_mapper = get_language_mapper(service)
            api_class = get_class_from_module(api_modules, api_module_name)
            return api_class(**self.kwargs)
        else:
            raise ServiceNotFoundException(
                f"해당 {service}가  존재하지 않는 서비스 입니다."
            )

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
        try:
            converted_src_lan = self.language_mapper[src_lan]
            converted_tgt_lan = self.language_mapper[tgt_lan]
        except KeyError as e:
            raise InvalidLanguageCodeException(f"Invalid language code: {e}")

        result = self.api.translate(query, converted_src_lan, converted_tgt_lan)
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
