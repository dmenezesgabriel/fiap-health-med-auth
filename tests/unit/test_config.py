from unittest.mock import MagicMock, call, patch

from src.config import Config, config_factory, get_config


class TestConfig:
    @patch.object(Config, "_configure_logging")
    @patch.object(Config, "_load_parameter_store")
    def test__init__success(
        self,
        mock_load_parameter_store: MagicMock,
        mock_configure_logging: MagicMock,
    ) -> None:
        # act
        config = Config()

        # assert
        mock_configure_logging.assert_called_once()
        mock_load_parameter_store.assert_called_once()
        assert hasattr(config, "_parameter_store_adapter")

    @patch.object(Config, "_load_parameter_store")
    @patch("src.config.Resource.load_json")
    @patch("src.config.logging.config.dictConfig")
    @patch("src.config.logging.getLogger")
    @patch.object(Config, "__init__", return_value=None)
    def test__configure_logging_success(
        self,
        mock__init__: None,
        mock_get_logger: MagicMock,
        mock_dict_config: MagicMock,
        mock_resource_load_json: MagicMock,
        mock_load_parameter_store: MagicMock,
    ) -> None:
        # arrange
        Config.drop()

        # act
        config = Config()
        config._configure_logging()
        # assert
        mock_resource_load_json.assert_any_call("logger.json")
        assert mock_resource_load_json.call_count == 1
        assert mock_get_logger.call_count == 1
        assert mock_dict_config.call_count == 1

    @patch("src.config.Modules.get_class_default_instance")
    @patch("src.config.Resource.load_json")
    @patch("src.config.logging.config.dictConfig")
    @patch.object(Config, "__init__", return_value=None)
    def test_load_parameter_store_no_module_name(
        self,
        mock__init__: None,
        mock_dict_config: MagicMock,
        mock_resource_load_json: MagicMock,
        mock_modules_get_class_default_instance: MagicMock,
    ) -> None:
        # arrange
        param_dict = {"ssm": {"PARAM": "/path/param"}}
        mock_resource_load_json.return_value = param_dict
        Config.drop()

        # act
        config = Config()
        config._load_parameter_store(module_name=None)

        # assert
        mock_resource_load_json.assert_any_call("parameters.json")
        assert mock_resource_load_json.call_count == 1
        assert mock_modules_get_class_default_instance.call_count == 1
        assert mock_modules_get_class_default_instance.call_args_list == [
            call(
                config.PARAMETER_STORE_MODULE,
                parameter_map={"PARAM": "/path/param"},
            ),
        ]

    @patch("src.config.Modules.get_class_default_instance")
    @patch("src.config.Resource.load_json")
    @patch("src.config.logging.config.dictConfig")
    @patch.object(Config, "__init__", return_value=None)
    def test_load_parameter_store_with_module_name(
        self,
        mock__init__: None,
        mock_dict_config: MagicMock,
        mock_resource_load_json: MagicMock,
        mock_modules_get_class_default_instance: MagicMock,
    ) -> None:
        # arrange
        param_dict = {
            "ssm": {"PARAM1": "/path/param1"},
            "environment": {"PARAM2": "/path/param2"},
        }
        mock_resource_load_json.return_value = param_dict
        Config.drop()

        # act
        config = Config()
        config._load_parameter_store(module_name="environment")

        # assert
        mock_resource_load_json.assert_any_call("parameters.json")
        assert mock_resource_load_json.call_count == 1
        assert mock_modules_get_class_default_instance.call_count == 1
        assert mock_modules_get_class_default_instance.call_args_list == [
            call(
                "environment",
                parameter_map={"PARAM2": "/path/param2"},
            ),
        ]

    @patch.object(Config, "_load_parameter_store")
    def test_get_parameter_no_module_name(
        self,
        mock_load_parameter_store: MagicMock,
    ) -> None:
        # arrange
        Config.drop()

        # act
        config = Config()
        config.get_parameter("PARAM")

        # assert
        mock_load_parameter_store.assert_called_once_with()

    @patch.object(Config, "_load_parameter_store")
    def test_get_parameter_with_module_name(
        self,
        mock_load_parameter_store: MagicMock,
    ) -> None:
        # arrange
        Config.drop()

        # act
        config = Config()
        config.get_parameter("PARAM", module_name="module")

        # assert
        assert mock_load_parameter_store.call_count == 2


class TestConfigFactory:
    @patch.object(Config, "__init__", return_value=None)
    def test_config_factory_success(self, mock_init: MagicMock) -> None:
        # act
        config_factory(environment="test")

        # assert
        mock_init.assert_called_once()


class TestGetConfig:
    @patch.object(Config, "__init__", return_value=None)
    def test_get_config_success(self, mock_init: MagicMock) -> None:
        # act
        config = get_config()

        # assert
        mock_init.assert_called_once()
        assert isinstance(config, Config)
