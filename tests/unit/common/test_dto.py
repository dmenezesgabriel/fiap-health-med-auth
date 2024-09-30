import pytest
from pydantic import ValidationError

from src.common.dto import (
    AccessTokenResponseDTO,
    ChangePasswordDTO,
    ChangePasswordRequestDTO,
    ConfirmForgotPasswordDTO,
    ForgotPasswordResponseDTO,
    GetUserResponseDTO,
    RefreshTokenDTO,
    SignUpResponseDTO,
    UserSigninDTO,
    UserSignupDTO,
    UserVerifyDTO,
)


class TestUserSignupDTO:
    def test_valid_user_signup_dto(self) -> None:
        # Arrange
        data = {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "password": "strongpassword",
            "role": "user",
            "cpf": "12345678910",
        }

        # Act
        user_signup = UserSignupDTO(**data)

        # Assert
        assert user_signup.full_name == "John Doe"
        assert user_signup.email == "john.doe@example.com"
        assert user_signup.password == "strongpassword"
        assert user_signup.role == "user"

    def test_invalid_user_signup_dto(self) -> None:
        # Arrange
        data = {
            "full_name": "A very long name that exceeds limit of characters",
            "email": "invalid-email",
            "password": "short",
            "role": "user",
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            UserSignupDTO(**data)


class TestUserVerifyDTO:
    def test_valid_user_verify_dto(self) -> None:
        # Arrange
        data = {"email": "john.doe@example.com", "confirmation_code": "123456"}

        # Act
        user_verify = UserVerifyDTO(**data)

        # Assert
        assert user_verify.email == "john.doe@example.com"
        assert user_verify.confirmation_code == "123456"

    def test_invalid_user_verify_dto(self) -> None:
        # Arrange
        data = {
            "email": "invalid-email",
            "confirmation_code": "1234567",  # Too long
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            UserVerifyDTO(**data)


class TestUserSigninDTO:
    def test_valid_user_signin_dto(self) -> None:
        # Arrange
        data = {"email": "john.doe@example.com", "password": "strongpassword"}

        # Act
        user_signin = UserSigninDTO(**data)

        # Assert
        assert user_signin.email == "john.doe@example.com"
        assert user_signin.password == "strongpassword"

    def test_invalid_user_signin_dto(self) -> None:
        # Arrange
        data = {"email": "invalid-email", "password": "short"}

        # Act & Assert
        with pytest.raises(ValidationError):
            UserSigninDTO(**data)


class TestConfirmForgotPasswordDTO:
    def test_valid_confirm_forgot_password_dto(self) -> None:
        # Arrange
        data = {
            "email": "john.doe@example.com",
            "confirmation_code": "123456",
            "new_password": "strongnewpassword",
        }

        # Act
        confirm_forgot_password = ConfirmForgotPasswordDTO(**data)

        # Assert
        assert confirm_forgot_password.email == "john.doe@example.com"
        assert confirm_forgot_password.confirmation_code == "123456"
        assert confirm_forgot_password.new_password == "strongnewpassword"

    def test_invalid_confirm_forgot_password_dto(self) -> None:
        # Arrange
        data = {
            "email": "invalid-email",
            "confirmation_code": "1234567",  # Too long
            "new_password": "short",
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            ConfirmForgotPasswordDTO(**data)


class TestChangePasswordDTO:
    def test_valid_change_password_dto(self) -> None:
        # Arrange
        data = {
            "old_password": "oldstrongpassword",
            "new_password": "newstrongpassword",
            "access_token": "token123",
        }

        # Act
        change_password = ChangePasswordDTO(**data)

        # Assert
        assert change_password.old_password == "oldstrongpassword"
        assert change_password.new_password == "newstrongpassword"
        assert change_password.access_token == "token123"

    def test_invalid_change_password_dto(self) -> None:
        # Arrange
        data = {
            "old_password": "short",
            "new_password": "newshort",
            "access_token": "token123",
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            ChangePasswordDTO(**data)


class TestChangePasswordRequestDTO:
    def test_valid_change_password_request_dto(self) -> None:
        # Arrange
        data = {
            "old_password": "oldstrongpassword",
            "new_password": "newstrongpassword",
        }

        # Act
        change_password_request = ChangePasswordRequestDTO(**data)

        # Assert
        assert change_password_request.old_password == "oldstrongpassword"
        assert change_password_request.new_password == "newstrongpassword"

    def test_invalid_change_password_request_dto(self) -> None:
        # Arrange
        data = {"old_password": "short", "new_password": "newshort"}

        # Act & Assert
        with pytest.raises(ValidationError):
            ChangePasswordRequestDTO(**data)


class TestRefreshTokenDTO:
    def test_valid_refresh_token_dto(self) -> None:
        # Arrange
        data = {"refresh_token": "refresh_token_example"}

        # Act
        refresh_token = RefreshTokenDTO(**data)

        # Assert
        assert refresh_token.refresh_token == "refresh_token_example"


class TestSignUpResponseDTO:
    def test_valid_sign_up_response_dto(self) -> None:
        # Arrange
        data = {
            "data": [
                {
                    "user_id": "user123",
                    "user_confirmed": True,
                    "code_delivery_destination": "email",
                    "code_delivery_type": "email_verification",
                }
            ]
        }

        # Act
        sign_up_response = SignUpResponseDTO(**data)

        # Assert
        assert sign_up_response.data[0]["user_id"] == "user123"
        assert sign_up_response.data[0]["user_confirmed"] is True


class TestAccessTokenResponseDTO:
    def test_valid_access_token_response_dto(self) -> None:
        # Arrange
        data = {
            "data": [
                {
                    "access_token": "access_token_example",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                    "id_token": "id_token_example",
                    "refresh_token": "refresh_token_example",
                }
            ]
        }

        # Act
        access_token_response = AccessTokenResponseDTO(**data)

        # Assert
        assert (
            access_token_response.data[0]["access_token"]
            == "access_token_example"
        )


class TestForgotPasswordResponseDTO:
    def test_valid_forgot_password_response_dto(self) -> None:
        # Arrange
        data = {
            "data": [
                {
                    "code_delivery_destination": "email",
                    "code_delivery_type": "email_verification",
                }
            ]
        }

        # Act
        forgot_password_response = ForgotPasswordResponseDTO(**data)

        # Assert
        assert (
            forgot_password_response.data[0]["code_delivery_destination"]
            == "email"
        )


class TestGetUserResponseDTO:
    def test_valid_get_user_response_dto(self) -> None:
        # Arrange
        data = {
            "data": [
                {
                    "username": "john_doe",
                    "user_attributes": [
                        {"name": "age", "value": "30"},
                        {"name": "location", "value": "USA"},
                    ],
                    "user_created_at": "2023-01-01T00:00:00Z",
                    "user_last_modified_at": "2023-01-01T01:00:00Z",
                    "user_status": "active",
                    "user_enabled": True,
                }
            ]
        }

        # Act
        get_user_response = GetUserResponseDTO(**data)

        # Assert
        assert (
            get_user_response.data[0].username == "john_doe"
        )  # Change this line
        assert get_user_response.data[0].user_attributes[0]["name"] == "age"
        assert get_user_response.data[0].user_attributes[0]["value"] == "30"
