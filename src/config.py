import logging
import logging.config
import os
from typing import Optional, cast

from src.ports.parameter_store_port import ParameterStorePort
from src.utils.module import Module, Modules
from src.utils.resources import Resource
from src.utils.singleton import Singleton

logger = logging.getLogger()


class Config(metaclass=Singleton):
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    APP_PATH = os.getenv("APP_PATH", "/auth")
    PARAMETER_STORE_MODULE = os.getenv(
        "PARAMETER_STORE_MODULE", Module.SSM_PARAMETER_STORE.value
    )

    def __init__(self) -> None:
        self._configure_logging()
        self._parameter_store_adapter = self._load_parameter_store()

    def _configure_logging(self) -> None:
        logger_config = Resource.load_json("logger.json")
        logging.config.dictConfig(logger_config)
        logging.getLogger().setLevel(getattr(logging, self.LOG_LEVEL))

    def _load_parameter_store(
        self, module_name: Optional[str] = None
    ) -> ParameterStorePort:
        module = self.PARAMETER_STORE_MODULE
        if module_name:
            module = module_name

        parameters = Resource.load_json("parameters.json")
        parameter_map = parameters[module]
        return cast(
            ParameterStorePort,
            Modules.get_class_default_instance(
                module, parameter_map=parameter_map
            ),
        )

    def get_parameter(
        self, name: str, module_name: Optional[str] = None
    ) -> Optional[str]:
        parameter_store = self._parameter_store_adapter
        if module_name:
            parameter_store = self._load_parameter_store(module_name)
        return parameter_store.get_parameter(name)


class LocalConfig(Config):
    LOG_LEVEL = "INFO"


class TestConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    LOG_LEVEL = "INFO"


def config_factory(environment: str) -> Config:
    configs = {
        "local": LocalConfig,
        "test": TestConfig,
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
    }
    config_class = configs[environment]
    return config_class()


def get_config() -> Config:
    environment = os.getenv("ENVIRONMENT", "local")
    app_config = config_factory(environment)

    return app_config
