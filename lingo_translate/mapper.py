# ================================================
# mapper.py
#   - MODEL_SERVICE_MAPPING_NAME, API_SERVICE_MAPPING_NAME
#       get_services()로 service.yaml에 있는 정보 불러옴
#       get_class_from_module로 <service>_modules 폴더에서 class 불러올 수 있음
#       호출 실패시 ModelNotFoundException을 호출
#   - convert_langauge()
#       지정된 언어 형식으로 들어오면 서비스와 모델을 변경
#       호출 실패시 LanguageMapperNotFoundException 호출
# ================================================
import lingo_translate.api_modules as api_modules
import lingo_translate.model_modules as model_modules
from lingo_translate.exception import (
    ModuleNotFoundException,
    LanguageMapperNotFoundException,
)
from abc import ABC, abstractmethod
import yaml


def _get_services():
    with open("service.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _is_service_exist(modules, service_name):
    if not getattr(modules, service_name, None):
        raise ModuleNotFoundException(f"'{service_name}'을 찾을 수 없습니다.")


def is_services_all_exist():
    # _all_services = _get_services()
    # for api_service in _all_services["api_services"]:
    #     print(api_service)
    #     _is_service_exist(api_modules, api_service)

    # for model_service in _all_services["model_services"]:
    #     _is_service_exist(model_modules, model_service)
    pass


_ALL_SERVICES = _get_services()
API_SERVICE_MAPPING_NAME = _ALL_SERVICES["api_services"]
MODEL_SERVICE_MAPPING_NAME = _ALL_SERVICES["model_services"]


def get_class_from_module(modules, name, base_class):
    module_class = getattr(modules, name, None)
    if not module_class:
        raise ModuleNotFoundException(f"'{name}'을 찾을 수 없습니다.")

    if not issubclass(module_class, base_class):
        raise ModuleNotFoundException(
            f"'{name}'은(는) '{base_class.__name__}'의 하위 클래스가 아닙니다."
        )
    return module_class


def get_language_mapper(service):
    with open("language.yaml", "r", encoding="utf-8") as f:
        supported_language = yaml.safe_load(f)
        return supported_language[service]


def convert_language(mapper: dict, src_lan: str, tgt_lan: str):
    converted_src_lan = mapper.get(src_lan)
    converted_tgt_lan = mapper.get(tgt_lan)
    if converted_src_lan is None or converted_tgt_lan is None:
        raise LanguageMapperNotFoundException(
            f"사용한 서비스에 제공된 언어가 없습니다."
        )

    return converted_src_lan, converted_tgt_lan


class AbstractAPI(ABC):
    """
    API를 사용한 번역용 Abstract Base Class
    """

    @abstractmethod
    def translate(self, query: str, src_lan: str, tgt_lan: str, **kwargs) -> dict:
        pass


class AbstractModel(ABC):
    """
    모델을 사용한 번역용 Abstract Base Class
    """

    @abstractmethod
    def translate(self, text: str, src_lang: str, tgt_lang: str, **kwargs) -> dict:
        pass
