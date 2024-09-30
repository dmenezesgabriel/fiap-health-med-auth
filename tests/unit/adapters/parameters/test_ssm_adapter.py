from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from src.adapters.cloud.aws_client_adapter import AWSClientAdapter
from src.adapters.exceptions import (
    ParameterNotFoundException,
    ParameterStoreException,
)
from src.adapters.parameters.ssm_adapter import SSMParameterStoreAdapter

MODULE_PATH = "src.adapters.cloud.aws_client_adapter"


class TestSSMParameterStoreAdapter:

    @patch.object(AWSClientAdapter, "__init__", lambda x, client_type: None)
    @patch(
        f"{MODULE_PATH}.AWSClientAdapter.client",
        new_callable=MagicMock,
    )
    def test_get_parameter_success(self, mock_client: MagicMock) -> None:
        # Arrange
        mock_client.get_parameter.return_value = {
            "Parameter": {"Value": "test_value"}
        }
        SSMParameterStoreAdapter.drop()
        adapter = SSMParameterStoreAdapter()

        # Act
        result = adapter.get_parameter("test_param")

        # Assert
        mock_client.get_parameter.assert_called_once_with(
            Name="test_param", WithDecryption=True
        )
        assert result == "test_value"

    @patch.object(AWSClientAdapter, "__init__", lambda x, client_type: None)
    @patch(
        f"{MODULE_PATH}.AWSClientAdapter.client",
        new_callable=MagicMock,
    )
    def test_get_parameter_not_found(self, mock_client: MagicMock) -> None:
        # Arrange
        error_response = {"Error": {"Code": "ParameterNotFoundException"}}
        mock_client.get_parameter.side_effect = ClientError(
            error_response, "get_parameter"
        )
        SSMParameterStoreAdapter.drop()
        adapter = SSMParameterStoreAdapter()

        # Act & Assert
        with pytest.raises(ParameterNotFoundException) as context:
            adapter.get_parameter("test_param")

        assert context.value.args[0]["code"] == "ssm.error.get_parameter"
        assert "Parameter not found" in context.value.args[0]["message"]
        mock_client.get_parameter.assert_called_once_with(
            Name="test_param", WithDecryption=True
        )

    @patch.object(AWSClientAdapter, "__init__", lambda x, client_type: None)
    @patch(
        f"{MODULE_PATH}.AWSClientAdapter.client",
        new_callable=MagicMock,
    )
    def test_get_parameter_store_exception(
        self, mock_client: MagicMock
    ) -> None:
        # Arrange
        error_response = {"Error": {"Code": "SomeOtherError"}}
        mock_client.get_parameter.side_effect = ClientError(
            error_response, "get_parameter"
        )
        SSMParameterStoreAdapter.drop()
        adapter = SSMParameterStoreAdapter()

        # Act & Assert
        with pytest.raises(ParameterStoreException) as context:
            adapter.get_parameter("test_param")

        assert context.value.args[0]["code"] == "ssm.error.get_parameter"
        assert "Parameter store error" in context.value.args[0]["message"]
        mock_client.get_parameter.assert_called_once_with(
            Name="test_param", WithDecryption=True
        )

    @patch.object(AWSClientAdapter, "__init__", lambda x, client_type: None)
    @patch(
        f"{MODULE_PATH}.AWSClientAdapter.client",
        new_callable=MagicMock,
    )
    def test_get_parameter_with_map(self, mock_client: MagicMock) -> None:
        # Arrange
        mock_client.get_parameter.return_value = {
            "Parameter": {"Value": "mapped_value"}
        }
        parameter_map = {"fake_name": "mapped_key"}
        SSMParameterStoreAdapter.drop()
        adapter = SSMParameterStoreAdapter(parameter_map=parameter_map)

        # Act
        result = adapter.get_parameter("fake_name")

        # Assert
        mock_client.get_parameter.assert_called_once_with(
            Name="mapped_key", WithDecryption=True
        )
        assert result == "mapped_value"
