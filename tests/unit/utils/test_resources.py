import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.utils.resources import Resource  # Replace with the actual module path


class TestResourceLoadJson:

    @patch("src.utils.resources.os.path.isfile")
    @patch("src.utils.resources.os.getcwd")
    def test_load_json_file_not_found(
        self, mock_getcwd: MagicMock, mock_isfile: MagicMock
    ) -> None:
        # Arrange
        mock_getcwd.return_value = "/fake/directory"
        mock_isfile.return_value = False

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            Resource.load_json("nonexistent.json")

    @patch("src.utils.resources.os.path.isfile")
    @patch("src.utils.resources.os.getcwd")
    @patch("src.utils.resources.json.load")
    def test_load_json_success(
        self,
        mock_json_load: MagicMock,
        mock_getcwd: MagicMock,
        mock_isfile: MagicMock,
    ) -> None:
        # Arrange
        mock_getcwd.return_value = "/fake/directory"
        mock_isfile.return_value = True
        mock_json_load.return_value = {"key": "value"}
        mock_open_instance = mock_open(read_data='{"key": "value"}')

        with patch("builtins.open", mock_open_instance):
            # Act
            result = Resource.load_json("test.json")

        # Assert
        mock_isfile.assert_called_once_with(
            "/fake/directory/src/resources/test.json"
        )
        mock_open_instance.assert_called_once_with(
            "/fake/directory/src/resources/test.json", "r"
        )
        mock_json_load.assert_called_once_with(mock_open_instance())
        assert result == {"key": "value"}

    @patch("src.utils.resources.os.path.isfile")
    @patch("src.utils.resources.os.getcwd")
    @patch("src.utils.resources.json.load")
    @patch("src.utils.resources.logger")
    def test_load_json_json_decode_error(
        self,
        mock_logger: MagicMock,
        mock_json_load: MagicMock,
        mock_getcwd: MagicMock,
        mock_isfile: MagicMock,
    ) -> None:
        # Arrange
        mock_getcwd.return_value = "/fake/directory"
        mock_isfile.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError(
            "Expecting value", "doc", 0
        )
        mock_open_instance = mock_open(read_data="invalid json")

        with patch("builtins.open", mock_open_instance):
            # Act & Assert
            with pytest.raises(ValueError):
                Resource.load_json("test.json")
            mock_logger.error.assert_called_once_with(
                "Error: Expecting value: line 1 column 1 (char 0)"
            )

    @patch("src.utils.resources.os.path.isfile")
    @patch("src.utils.resources.os.getcwd")
    @patch("src.utils.resources.json.load")
    @patch("src.utils.resources.logger")
    def test_load_json_generic_exception(
        self,
        mock_logger: MagicMock,
        mock_json_load: MagicMock,
        mock_getcwd: MagicMock,
        mock_isfile: MagicMock,
    ) -> None:
        # Arrange
        mock_getcwd.return_value = "/fake/directory"
        mock_isfile.return_value = True
        mock_json_load.side_effect = Exception("generic error")
        mock_open_instance = mock_open(read_data='{"key": "value"}')

        # Act
        with patch("builtins.open", mock_open_instance):
            Resource.load_json("test.json")

        # Assert
        mock_logger.error.assert_called_once_with("Error: generic error")
