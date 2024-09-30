from src.adapters.exceptions import (
    LimitExceededException,
    ParameterNotFoundException,
    ParameterStoreException,
    TooManyRequestsException,
)


def test_parameter_store_exception() -> None:
    exception = ParameterStoreException("Parameter store error.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Parameter store error."


def test_parameter_not_found_exception() -> None:
    exception = ParameterNotFoundException("Parameter not found.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Parameter not found."


def test_limit_exceeded_exception() -> None:
    exception = LimitExceededException("Limit exceeded.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Limit exceeded."


def test_too_many_requests_exception() -> None:
    exception = TooManyRequestsException("Too many requests.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Too many requests."
