import base64
from abc import ABCMeta
from typing import Any, Dict


def generate_hash(value: Any) -> str:
    value = value.encode("ascii")
    return base64.b64encode(value).decode("utf8")


class Singleton(type):
    _instances: Dict["Singleton", "Singleton"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @staticmethod
    def drop() -> None:
        Singleton._instances = {}


class SingletonHash(type):
    _instances: Dict[str, "SingletonHash"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        hash_cls = generate_hash(str(args) + str(kwargs))
        if hash_cls not in cls._instances:
            instance = super(SingletonHash, cls).__call__(*args, **kwargs)
            cls._instances[hash_cls] = instance

        return cls._instances[hash_cls]

    @staticmethod
    def drop() -> None:
        SingletonHash._instances = {}


class SingletonHashABC(SingletonHash, ABCMeta):
    pass
