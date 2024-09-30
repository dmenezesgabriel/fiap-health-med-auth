from unittest.mock import MagicMock

import pytest

from src.common.dto import (
    AccessTokenResponseDTO,
    ChangePasswordDTO,
    ConfirmForgotPasswordDTO,
    ForgotPasswordResponseDTO,
    GetUserResponseDTO,
    SignUpResponseDTO,
    User,
    UserSigninDTO,
    UserSignupDTO,
    UserVerifyDTO,
)
from src.domain.exceptions import (
    InvalidCredentialsException,
    InvalidVerificationCodeException,
    UserNotFoundException,
)
from src.domain.services.auth_service import AuthService
from src.ports.auth_port import AuthPort


@pytest.fixture
def mock_auth_adapter() -> MagicMock:
    return MagicMock(spec=AuthPort)


@pytest.fixture
def auth_service(mock_auth_adapter: MagicMock) -> AuthService:
    return AuthService(auth_adapter=mock_auth_adapter)


class TestAuthSignupSignin:

    def test_user_signup(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        user_signup_dto = UserSignupDTO(
            email="test@example.com",
            password="password",
            full_name="Test User",
            role="user",
            cpf="12345678901",
        )
        mock_auth_adapter.user_signup.return_value = SignUpResponseDTO(
            data=[
                {
                    "user_id": "test_user_id",
                    "user_confirmed": True,
                    "code_delivery_destination": "test@example.com",
                    "code_delivery_type": "email",
                }
            ]
        )

        # Act
        response = auth_service.user_signup(user_signup_dto)

        # Assert
        assert response.data[0]["user_id"] == "test_user_id"

    def test_user_signin(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        signin_dto = UserSigninDTO(
            email="test@example.com", password="password"
        )
        expected_response = AccessTokenResponseDTO(
            data=[
                {
                    "access_token": "token",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                    "id_token": "id_token",
                    "refresh_token": "refresh_token",
                }
            ]
        )
        mock_auth_adapter.user_signin.return_value = expected_response

        # Act
        response = auth_service.user_signin(signin_dto)

        # Assert
        assert response.data[0]["access_token"] == "token"
        assert response.data[0]["refresh_token"] == "refresh_token"

    def test_resend_confirmation_code(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        email = "test@example.com"

        # Act
        auth_service.resend_confirmation_code(email)

        # Assert
        mock_auth_adapter.resend_confirmation_code.assert_called_once_with(
            email
        )


class TestAuthPasswordToken:

    def test_forgot_password(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        email = "test@example.com"
        mock_auth_adapter.forgot_password.return_value = (
            ForgotPasswordResponseDTO(
                data=[
                    {
                        "code_delivery_destination": "test@example.com",
                        "code_delivery_type": "email",
                    }
                ]
            )
        )

        # Act
        response = auth_service.forgot_password(email)

        # Assert
        assert (
            response.data[0]["code_delivery_destination"] == "test@example.com"
        )

    def test_confirm_forgot_password(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        confirm_dto = ConfirmForgotPasswordDTO(
            email="test@example.com",
            confirmation_code="123456",
            new_password="new_password",
        )
        mock_auth_adapter.confirm_forgot_password.return_value = {
            "status": "success"
        }

        # Act
        response = auth_service.confirm_forgot_password(confirm_dto)

        # Assert
        assert response["status"] == "success"

    def test_confirm_forgot_password_invalid_code(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        confirm_dto = ConfirmForgotPasswordDTO(
            email="test@example.com",
            confirmation_code="123456",
            new_password="new_password",
        )
        mock_auth_adapter.confirm_forgot_password.side_effect = (
            InvalidVerificationCodeException("Invalid code")
        )

        # Act and Assert
        with pytest.raises(InvalidVerificationCodeException) as excinfo:
            auth_service.confirm_forgot_password(confirm_dto)

        assert "Invalid code" in str(excinfo.value)

    def test_change_password(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        change_password_dto = ChangePasswordDTO(
            access_token="valid_token",
            old_password="old_password",
            new_password="new_password",
        )
        mock_auth_adapter.change_password.return_value = {
            "status": "password_changed"
        }

        # Act
        response = auth_service.change_password(change_password_dto)

        # Assert
        assert response["status"] == "password_changed"

    def test_change_password_invalid_token(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        change_password_dto = ChangePasswordDTO(
            access_token="invalid_token",
            old_password="old_password",
            new_password="new_password",
        )
        mock_auth_adapter.change_password.side_effect = (
            InvalidCredentialsException("Invalid token")
        )

        # Act and Assert
        with pytest.raises(InvalidCredentialsException) as excinfo:
            auth_service.change_password(change_password_dto)

        assert "Invalid token" in str(excinfo.value)

    def test_new_access_token(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        refresh_token = "valid_refresh_token"
        expected_response = AccessTokenResponseDTO(
            data=[
                {
                    "access_token": "new_access_token",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                    "id_token": "new_id_token",
                    "refresh_token": "new_refresh_token",
                }
            ]
        )
        mock_auth_adapter.new_access_token.return_value = expected_response

        # Act
        response = auth_service.new_access_token(refresh_token)

        # Assert
        assert response.data[0]["access_token"] == "new_access_token"
        assert response.data[0]["refresh_token"] == "new_refresh_token"


class TestAuthAccountVerification:

    def test_verify_account(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        verify_dto = UserVerifyDTO(
            email="test@example.com", confirmation_code="123456"
        )
        mock_auth_adapter.verify_account.return_value = {"status": "verified"}

        # Act
        response = auth_service.verify_account(verify_dto)

        # Assert
        assert response["status"] == "verified"

    def test_verify_account_user_not_found(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        verify_dto = UserVerifyDTO(
            email="nonexistent@example.com", confirmation_code="123456"
        )
        mock_auth_adapter.verify_account.side_effect = UserNotFoundException(
            "User not found"
        )

        # Act and Assert
        with pytest.raises(UserNotFoundException) as excinfo:
            auth_service.verify_account(verify_dto)

        assert "User not found" in str(excinfo.value)


class TestAuthUserDetails:

    def test_user_details(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        """Test the user_details method."""
        # Arrange
        email = "test@example.com"
        mock_auth_adapter.get_user.return_value = GetUserResponseDTO(
            data=[
                User(
                    username="test_user",
                    user_attributes=[],
                    user_created_at="2023-01-01T00:00:00Z",
                    user_last_modified_at="2023-01-01T00:00:00Z",
                    user_status="ACTIVE",
                    user_enabled=True,
                )
            ]
        )

        # Act
        response = auth_service.user_details(email)

        # Assert
        assert response.data[0].username == "test_user"


class TestLogout:
    def test_logout(
        self, mock_auth_adapter: MagicMock, auth_service: AuthService
    ) -> None:
        # Arrange
        access_token = "valid_access_token"

        # Act
        auth_service.logout(access_token)

        # Assert
        mock_auth_adapter.logout.assert_called_once_with(access_token)
