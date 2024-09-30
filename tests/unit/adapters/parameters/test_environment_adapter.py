from typing import Dict, Optional
from unittest.mock import MagicMock, patch

import pytest

from src.adapters.exceptions import ParameterNotFoundException
from src.adapters.parameters.environment_adapter import (
    EnvironmentParameterStoreAdapter,
)


# Fixtures
@pytest.fixture
def parameter_map() -> Dict[str, str]:
    return {"DB_USER": "ENV_DB_USER", "DB_PASSWORD": "ENV_DB_PASSWORD"}


@pytest.fixture
def env_adapter(
    parameter_map: Dict[str, str]
) -> EnvironmentParameterStoreAdapter:
    return EnvironmentParameterStoreAdapter(parameter_map=parameter_map)


@pytest.fixture
def empty_adapter() -> EnvironmentParameterStoreAdapter:
    return EnvironmentParameterStoreAdapter()


class TestInitialization:
    def test_init(self, env_adapter: EnvironmentParameterStoreAdapter) -> None:
        assert env_adapter is not None


class TestGetParameterNoMap:
    @patch("src.adapters.parameters.environment_adapter.os.getenv")
    def test_get_parameter_no_map(
        self,
        mock_getenv: MagicMock,
        empty_adapter: EnvironmentParameterStoreAdapter,
    ) -> None:
        # Arrange
        mock_getenv.return_value = "db_user_value"

        # Act
        result: Optional[str] = empty_adapter.get_parameter("DB_USER")

        # Assert
        mock_getenv.assert_called_once_with("DB_USER")
        assert result == "db_user_value"

    @patch("src.adapters.parameters.environment_adapter.os.getenv")
    def test_get_parameter_not_found(
        self,
        mock_getenv: MagicMock,
        empty_adapter: EnvironmentParameterStoreAdapter,
    ) -> None:
        # Arrange
        mock_getenv.return_value = None

        # Act and Assert
        with pytest.raises(
            ParameterNotFoundException, match="Parameter not found."
        ):
            empty_adapter.get_parameter("UNKNOWN_PARAM")


class TestGetParameterWithMap:
    @patch("src.adapters.parameters.environment_adapter.os.getenv")
    def test_get_parameter_with_map(
        self,
        mock_getenv: MagicMock,
        env_adapter: EnvironmentParameterStoreAdapter,
    ) -> None:
        # Arrange
        mock_getenv.return_value = "db_user_value"

        # Act
        result: Optional[str] = env_adapter.get_parameter("DB_USER")

        # Assert
        mock_getenv.assert_called_once_with("ENV_DB_USER")
        assert result == "db_user_value"

    @patch("src.adapters.parameters.environment_adapter.os.getenv")
    def test_get_parameter_invalid_key_with_map(
        self,
        mock_getenv: MagicMock,
        env_adapter: EnvironmentParameterStoreAdapter,
    ) -> None:
        # Arrange
        mock_getenv.return_value = None

        # Act and Assert
        with pytest.raises(
            ParameterNotFoundException, match="Parameter not found."
        ):
            env_adapter.get_parameter("INVALID_KEY")
