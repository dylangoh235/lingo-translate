from lingo_suggestion.exception import ServiceNotFoundException
import lingo_suggestion.model_load as model_load
from typing import Dict, Any
from lingo_suggestion.exception import (
    ModuleNotFoundException,
)
import yaml
import os
import importlib.util

def _get_services():
    with open("service.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

_ALL_SERVICES = _get_services()
SUGGESTION_SERVICE_MAPPING_NAME = _ALL_SERVICES["suggestion_services"]

class Abstract:

    def __init(self, target_word, text=None, cntxt_len=None):
        self.target_word = target_word
        self.text = text
        self.cntxt_len = cntxt_len


class ModelLoader:

    MODEL_MAPPING: Dict[str, str] = SUGGESTION_SERVICE_MAPPING_NAME

    def __init__(self, model: str):
        self.model = model

    def get_class_from_module(self, module, name):
        module_class = module.get(name, None)
        if module_class is None:
            raise ModuleNotFoundException(f"'{name}' class does not exist in module.")
        return module_class

    def load_class(self, module_file, class_name):
        try:
            module_path = os.path.abspath(os.path.join("lingo_suggestion", "models", f"{module_file}.py"))
            print(f"Module path: {module_path}")

            if not os.path.exists(module_path):
                raise ModuleNotFoundException(f"Module file '{module_file}.py' does not exist.")
            
            with open(module_path, 'r') as f:
                code = f.read()
            
            module_namespace = {}
            exec(code, module_namespace)
            print(f"Module namespace keys: {list(module_namespace.keys())}")

            model_class = self.get_class_from_module(module_namespace, class_name)
            
            return model_class
        
        except ModuleNotFoundException as e:
            print(f"ModuleNotFoundException: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return None

    def model_return(self):
        print(f"Model: {self.model}, Model Mapping: {self.MODEL_MAPPING}")
        if self.model in self.MODEL_MAPPING:
            print("Model load starting..")
            model_class = self.load_class(self.model, self.MODEL_MAPPING[self.model])
            if model_class:
                return model_class()
            else:
                print(f"Failed to load class for model {self.model}")
                raise ModuleNotFoundException(f"Failed to load class for model {self.model}")
        else:
            raise ServiceNotFoundException(
                f"{self.model} does not exist in yaml, please add a model or change the name"
            )
