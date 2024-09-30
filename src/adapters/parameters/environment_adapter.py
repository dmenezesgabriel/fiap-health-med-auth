import logging
import os
from typing import Dict, Optional

from src.adapters.exceptions import ParameterNotFoundException
from src.ports.parameter_store_port import ParameterStorePort
from src.utils.singleton import SingletonHashABC

logger = logging.getLogger()


class EnvironmentParameterStoreAdapter(
    ParameterStorePort, metaclass=SingletonHashABC
):
    def __init__(self, parameter_map: Optional[Dict[str, str]] = None) -> None:
        self.__parameter_map = parameter_map
        logger.info("Initialized Environment parameter store")

    def __get_parameter(self, key: str) -> Optional[str]:
        parameter = os.getenv(key)
        if parameter:
            return parameter
        raise ParameterNotFoundException("Parameter not found.")

    def get_parameter(self, name: str) -> Optional[str]:
        if not self.__parameter_map:
            return self.__get_parameter(name)
        try:
            return self.__get_parameter(self.__parameter_map[name])
        except KeyError:
            raise ParameterNotFoundException("Parameter not found.")
