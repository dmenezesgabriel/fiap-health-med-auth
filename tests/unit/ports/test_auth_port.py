from typing import Any, Dict

import pytest
from pydantic import EmailStr

from src.common.dto import (
    AccessTokenResponseDTO,
    ChangePasswordDTO,
    ConfirmForgotPasswordDTO,
    ForgotPasswordResponseDTO,
    GetUserResponseDTO,
    SignUpResponseDTO,
    UserSigninDTO,
    UserSignupDTO,
    UserVerifyDTO,
)
from src.ports.auth_port import AuthPort


class TestAuthPort:

    def test_abstract_class_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            AuthPort()

    def test_abstract_method_raises_not_implemented_error(self) -> None:
        class IncompleteAuthPort(AuthPort):
            def user_signup(self, user: UserSignupDTO) -> SignUpResponseDTO:
                return super().user_signup(user)

            def verify_account(self, data: UserVerifyDTO) -> Dict[str, Any]:
                return super().verify_account(data)

            def resend_confirmation_code(
                self, email: EmailStr
            ) -> Dict[str, Any]:
                return super().resend_confirmation_code(email)

            def get_user(self, email: EmailStr) -> GetUserResponseDTO:
                return super().get_user(email)

            def user_signin(
                self, data: UserSigninDTO
            ) -> AccessTokenResponseDTO:
                return super().user_signin(data)

            def forgot_password(
                self, email: EmailStr
            ) -> ForgotPasswordResponseDTO:
                return super().forgot_password(email)

            def confirm_forgot_password(
                self, data: ConfirmForgotPasswordDTO
            ) -> Dict[str, Any]:
                return super().confirm_forgot_password(data)

            def change_password(
                self, data: ChangePasswordDTO
            ) -> Dict[str, Any]:
                return super().change_password(data)

            def new_access_token(
                self, refresh_token: str
            ) -> AccessTokenResponseDTO:
                return super().new_access_token(refresh_token)

            def logout(self, access_token: str) -> Dict[str, Any]:
                return super().logout(access_token)

        incomplete_auth_port = IncompleteAuthPort()

        # Testing if each method raises NotImplementedError
        with pytest.raises(NotImplementedError):
            incomplete_auth_port.user_signup(
                UserSignupDTO(
                    full_name="Test User",
                    email="test@example.com",
                    password="password123",
                    role="user",
                    cpf="12345678901",
                )
            )

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.verify_account(
                UserVerifyDTO(
                    email="test@example.com", confirmation_code="123456"
                )
            )

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.resend_confirmation_code("test@example.com")

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.get_user("test@example.com")

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.user_signin(
                UserSigninDTO(email="test@example.com", password="password123")
            )

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.forgot_password("test@example.com")

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.confirm_forgot_password(
                ConfirmForgotPasswordDTO(
                    email="test@example.com",
                    confirmation_code="123456",
                    new_password="newpassword123",
                )
            )

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.change_password(
                ChangePasswordDTO(
                    old_password="oldpassword123",
                    new_password="newpassword123",
                    access_token="access_token",
                )
            )

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.new_access_token("refresh_token")

        with pytest.raises(NotImplementedError):
            incomplete_auth_port.logout("access_token")


if __name__ == "__main__":
    pytest.main()
