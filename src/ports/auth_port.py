from abc import ABC, abstractmethod
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


class AuthPort(ABC):
    @abstractmethod
    def user_signup(self, user: UserSignupDTO) -> SignUpResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def verify_account(self, data: UserVerifyDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def resend_confirmation_code(self, email: EmailStr) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, email: EmailStr) -> GetUserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def user_signin(self, data: UserSigninDTO) -> AccessTokenResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def forgot_password(self, email: EmailStr) -> ForgotPasswordResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def confirm_forgot_password(
        self, data: ConfirmForgotPasswordDTO
    ) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def change_password(self, data: ChangePasswordDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def new_access_token(self, refresh_token: str) -> AccessTokenResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def logout(self, access_token: str) -> Dict[str, Any]:
        raise NotImplementedError
