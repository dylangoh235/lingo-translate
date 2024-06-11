def _find_submodules():
    from pathlib import Path
    from importlib import import_module

    package_path = Path(__file__).resolve().parent
    return tuple(p.stem for p in package_path.glob("*.py") if p.stem != "__init__")


__submodules__ = _find_submodules()
del _find_submodules


def __dir__():
    from importlib import import_module

    names = []
    for module_name in __submodules__:
        module = import_module(f".{module_name}", __package__)
        try:
            names += module.__all__
        except AttributeError:
            names += (n for n in dir(module) if n[:1] != "_")
    return sorted(names)


__all__ = __dir__()


def __getattr__(name):
    from importlib import import_module

    for module_name in __submodules__:
        module = import_module(f".{module_name}", __package__)
        try:
            # cache the attribute so future imports don't call __getattr__ again
            obj = getattr(module, name)
            globals()[name] = obj
            return obj
        except AttributeError:
            pass
    raise AttributeError(name)
