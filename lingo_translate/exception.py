class LingoException(Exception):
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.args[0] if self.args else ""}'


class ModuleNotFoundException(LingoException):
    pass


class ServiceNotFoundException(LingoException):
    pass


class OutputFormatNotValidException(LingoException):
    pass


class LanguageMapperNotFoundException(LingoException):
    pass


class InvalidLanguageCodeException(LingoException):
    pass
