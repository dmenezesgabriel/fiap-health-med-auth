from src.domain.exceptions import (
    ExpiredVerificationCodeException,
    InvalidCredentialsException,
    InvalidVerificationCodeException,
    RequirementsDoesNotMatchException,
    UnauthorizedException,
    UserAlreadyConfirmed,
    UserAlreadyExistsException,
    UserNotConfirmedException,
    UserNotFoundException,
)


def test_user_already_exists_exception() -> None:
    exception = UserAlreadyExistsException("User already exists.")
    assert isinstance(exception, Exception)
    assert str(exception) == "User already exists."


def test_user_not_found_exception() -> None:
    exception = UserNotFoundException("User not found.")
    assert isinstance(exception, Exception)
    assert str(exception) == "User not found."


def test_user_not_confirmed_exception() -> None:
    exception = UserNotConfirmedException("User not confirmed.")
    assert isinstance(exception, Exception)
    assert str(exception) == "User not confirmed."


def test_user_already_confirmed() -> None:
    exception = UserAlreadyConfirmed("User already confirmed.")
    assert isinstance(exception, Exception)
    assert str(exception) == "User already confirmed."


def test_unauthorized_exception() -> None:
    exception = UnauthorizedException("Unauthorized access.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Unauthorized access."


def test_expired_verification_code_exception() -> None:
    exception = ExpiredVerificationCodeException("Verification code expired.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Verification code expired."


def test_invalid_verification_code_exception() -> None:
    exception = InvalidVerificationCodeException("Invalid verification code.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Invalid verification code."


def test_invalid_credentials_exception() -> None:
    exception = InvalidCredentialsException("Invalid credentials.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Invalid credentials."


def test_requirements_does_not_match_exception() -> None:
    exception = RequirementsDoesNotMatchException("Requirements do not match.")
    assert isinstance(exception, Exception)
    assert str(exception) == "Requirements do not match."
