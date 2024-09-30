import base64
from unittest.mock import MagicMock, patch

from src.utils.singleton import Singleton, SingletonHash, generate_hash


class TestGenerateHash:

    def test_generate_hash(self) -> None:
        # Arrange
        value = "test_value"
        expected_hash = base64.b64encode(value.encode("ascii")).decode("utf8")

        # Act
        result = generate_hash(value)

        # Assert
        assert result == expected_hash


class TestSingleton:

    def teardown_method(self) -> None:
        # Ensure Singleton instances are cleared after each test
        Singleton.drop()

    def test_singleton_instance(self) -> None:
        # Arrange
        class MyClass(metaclass=Singleton):
            pass

        # Act
        instance1 = MyClass()
        instance2 = MyClass()

        # Assert
        assert instance1 is instance2

    def test_singleton_drop(self) -> None:
        # Arrange
        class MyClass(metaclass=Singleton):
            pass

        instance1 = MyClass()

        # Act
        Singleton.drop()
        instance2 = MyClass()

        # Assert
        assert instance1 is not instance2


class TestSingletonHash:

    def teardown_method(self) -> None:
        # Ensure SingletonHash instances are cleared after each test
        SingletonHash.drop()

    @patch("src.utils.singleton.generate_hash")
    def test_singleton_hash_instance(
        self, mock_generate_hash: MagicMock
    ) -> None:
        # Arrange
        mock_generate_hash.side_effect = lambda x: (
            "hash1" if "value1" in x else "hash2"
        )

        class MyClass(metaclass=SingletonHash):
            def __init__(self, value: str) -> None:
                self.value = value

        # Act
        instance1 = MyClass("value1")
        instance2 = MyClass("value1")
        instance3 = MyClass("value2")

        # Assert
        assert instance1 is instance2
        assert instance1 is not instance3
        assert instance2 is not instance3

    def test_singleton_hash_drop(self) -> None:
        # Arrange
        class MyClass(metaclass=SingletonHash):
            def __init__(self, value: str) -> None:
                self.value = value

        instance1 = MyClass("value1")

        # Act
        SingletonHash.drop()
        instance2 = MyClass("value1")

        # Assert
        assert instance1 is not instance2
