from abc import ABC, abstractmethod
from typing import Optional


class ParameterStorePort(ABC):
    @abstractmethod
    def get_parameter(self, key: str) -> Optional[str]:
        raise NotImplementedError
