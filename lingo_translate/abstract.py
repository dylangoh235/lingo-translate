from abc import ABC, abstractmethod


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
