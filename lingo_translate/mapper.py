# ================================================
# MODEL_SERVICE_MAPPING_NAME, API_SERVICE_MAPPING_NAME
#
#   호출 실패시 ModelNotFoundException을 호출
# ================================================
from lingo_translate.exception import (
    ModuleNotFoundException,
    LanguageMapperNotFoundException,
)
import yaml


def get_language_mapper(service):
    with open("language.yaml", "r", encoding="utf-8") as f:
        supported_language = yaml.safe_load(f)
        return supported_language[service]


def _get_services():
    with open("service.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_ALL_SERVICES = _get_services()
API_SERVICE_MAPPING_NAME = _ALL_SERVICES["api_services"]
MODEL_SERVICE_MAPPING_NAME = _ALL_SERVICES["model_services"]


def get_class_from_module(modules, name):
    module_class = getattr(modules, name, None)
    if module_class is None:
        raise ModuleNotFoundException(f"'{name}'을 찾을 수 없습니다.")

    return module_class


def convert_language(service, model, src_lan, tgt_lan):
    mapper_name = f"{service}_{model}_LANGUAGE_MAPPER"
    mapper = getattr(None, mapper_name)
    if mapper is None:
        raise LanguageMapperNotFoundException(f"{service}에 제공된 언어가 없습니다.")

    converted_src_lan, converted_tgt_lan = mapper[src_lan], mapper[tgt_lan]
    return converted_src_lan, converted_tgt_lan
