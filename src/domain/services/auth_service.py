import logging
from typing import Any, Dict

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

logger = logging.getLogger()


class AuthService:
    def __init__(self, auth_adapter: AuthPort) -> None:
        self.__auth_adapter = auth_adapter

    def user_signup(self, user: UserSignupDTO) -> SignUpResponseDTO:
        response = self.__auth_adapter.user_signup(user)
        return response

    def verify_account(self, data: UserVerifyDTO) -> Dict[str, Any]:
        response = self.__auth_adapter.verify_account(data)
        return response

    def resend_confirmation_code(self, email: EmailStr) -> Dict[str, Any]:
        response = self.__auth_adapter.resend_confirmation_code(email)
        return response

    def user_signin(self, data: UserSigninDTO) -> AccessTokenResponseDTO:
        response = self.__auth_adapter.user_signin(data)
        return response

    def forgot_password(self, email: EmailStr) -> ForgotPasswordResponseDTO:
        response = self.__auth_adapter.forgot_password(email)
        return response

    def confirm_forgot_password(
        self, data: ConfirmForgotPasswordDTO
    ) -> Dict[str, Any]:
        response = self.__auth_adapter.confirm_forgot_password(data)
        return response

    def change_password(self, data: ChangePasswordDTO) -> Dict[str, Any]:
        response = self.__auth_adapter.change_password(data)
        return response

    def new_access_token(self, refresh_token: str) -> AccessTokenResponseDTO:
        response = self.__auth_adapter.new_access_token(refresh_token)
        return response

    def logout(self, access_token: str) -> Dict[str, Any]:
        response = self.__auth_adapter.logout(access_token)
        return response

    def user_details(self, email: EmailStr) -> GetUserResponseDTO:
        response = self.__auth_adapter.get_user(email)
        return response
