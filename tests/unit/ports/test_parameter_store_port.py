from typing import Optional
from unittest.mock import patch

import pytest

from src.ports.parameter_store_port import ParameterStorePort


class ConcreteParameterStore(ParameterStorePort):
    def get_parameter(self, key: str) -> Optional[str]:
        return f"Value for {key}"


class TestParameterStorePort:

    def test_abstract_class_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            ParameterStorePort()

    def test_abstract_method_raises_not_implemented_error(self) -> None:
        class IncompleteStore(ParameterStorePort):
            def get_parameter(self, key: str) -> Optional[str]:
                return super().get_parameter(key)

        incomplete_store = IncompleteStore()
        with pytest.raises(NotImplementedError):
            incomplete_store.get_parameter("test_key")

    def test_concrete_class_can_be_instantiated(self) -> None:
        store = ConcreteParameterStore()
        assert isinstance(store, ParameterStorePort)

    def test_concrete_implementation(self) -> None:
        store = ConcreteParameterStore()
        result = store.get_parameter("test_key")
        assert result == "Value for test_key"

    def test_get_parameter_called_with_correct_argument(self) -> None:
        store = ConcreteParameterStore()
        with patch.object(
            store, "get_parameter", wraps=store.get_parameter
        ) as mock_get_parameter:
            store.get_parameter("some_key")
            mock_get_parameter.assert_called_once_with("some_key")

    @pytest.mark.parametrize(
        "return_value, expected_result",
        [
            (None, None),
            ("mocked_value", "mocked_value"),
            ("", ""),
            ("special_value", "special_value"),
        ],
    )
    def test_get_parameter_returns(
        self, return_value: Optional[str], expected_result: Optional[str]
    ) -> None:
        store = ConcreteParameterStore()
        with patch.object(store, "get_parameter", return_value=return_value):
            result = store.get_parameter("test_key")
            assert result == expected_result

    @pytest.mark.parametrize(
        "key",
        [
            "normal_key",
            "",
            "!@#$%^&*()_+",
        ],
    )
    def test_get_parameter_with_different_keys(self, key: str) -> None:
        store = ConcreteParameterStore()
        result = store.get_parameter(key)
        assert result == f"Value for {key}"


class TestParameterStorePortEdgeCases:

    def test_subclass_with_additional_methods(self) -> None:
        class ExtendedStore(ParameterStorePort):
            def get_parameter(self, key: str) -> Optional[str]:
                return f"Extended {key}"

            def additional_method(self) -> str:
                return "Additional functionality"

        store = ExtendedStore()
        assert store.get_parameter("test") == "Extended test"
        assert store.additional_method() == "Additional functionality"


@pytest.mark.parametrize(
    "custom_value",
    [
        "Custom test",
        "Another custom value",
        "",
    ],
)
def test_parameter_store_port_subclass_type_check(custom_value: str) -> None:
    class CustomStore(ParameterStorePort):
        def get_parameter(self, key: str) -> Optional[str]:
            return custom_value

    def use_parameter_store(store: ParameterStorePort) -> Optional[str]:
        return store.get_parameter("test")

    custom_store = CustomStore()
    result = use_parameter_store(custom_store)
    assert result == custom_value


if __name__ == "__main__":
    pytest.main()
