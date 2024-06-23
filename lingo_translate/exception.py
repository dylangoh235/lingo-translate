class ModuleNotFoundException(Exception):
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.args[0] if self.args else ""}'


class ServiceNotFoundException(Exception):
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.args[0] if self.args else ""}'


class OutputFormatNotValidException(Exception):
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.args[0] if self.args else ""}'


class LanguageMapperNotFoundException(Exception):
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.args[0] if self.args else ""}'


class InvalidLanguageCodeException(Exception):
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.args[0] if self.args else ""}'
