import logging
from typing import Any, Dict, cast

import botocore
import botocore.exceptions
from pydantic import EmailStr

from src.adapters.cloud.aws_client_adapter import AWSClientAdapter
from src.adapters.exceptions import (
    LimitExceededException,
    TooManyRequestsException,
)
from src.common.dto import (
    AccessTokenResponseDTO,
    ChangePasswordDTO,
    ConfirmForgotPasswordDTO,
    ForgotPasswordResponseDTO,
    GetUserResponseDTO,
    SignUpResponseDTO,
    User,
    UserAttributeDTO,
    UserSigninDTO,
    UserSignupDTO,
    UserVerifyDTO,
)
from src.config import get_config
from src.domain.exceptions import (
    ExpiredVerificationCodeException,
    InvalidCredentialsException,
    InvalidVerificationCodeException,
    RequirementsDoesNotMatchException,
    UnauthorizedException,
    UserAlreadyExistsException,
    UserNotConfirmedException,
    UserNotFoundException,
)

logger = logging.getLogger()
config = get_config()


class AWSCognitoAdapter(AWSClientAdapter):
    def __init__(self, client_type: str = "cognito-idp") -> None:
        super().__init__(client_type=client_type)
        self.cognito_app_pool_id = config.get_parameter(
            "AWS_COGNITO_USER_POOL_ID"
        )
        self.cognito_user_pool_client_id = config.get_parameter(
            "AWS_COGNITO_APP_CLIENT_ID"
        )

    def user_signup(self, user: UserSignupDTO) -> SignUpResponseDTO:
        try:
            response = self.client.sign_up(
                ClientId=self.cognito_user_pool_client_id,
                Username=user.email,
                Password=user.password,
                UserAttributes=[
                    {
                        "Name": "name",
                        "Value": user.full_name,
                    },
                    {
                        "Name": "email",
                        "Value": user.email,
                    },
                    {"Name": "custom:role", "Value": user.role},
                    {"Name": "custom:cpf", "Value": user.cpf},
                    {"Name": "custom:crm", "Value": user.crm or "-"},
                ],
            )
            return SignUpResponseDTO(
                data=[
                    dict(
                        user_id=response["UserSub"],
                        user_confirmed=response["UserConfirmed"],
                        code_delivery_destination=response[
                            "CodeDeliveryDetails"
                        ]["Destination"],
                        code_delivery_type=response["CodeDeliveryDetails"][
                            "AttributeName"
                        ],
                    )
                ]
            )
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "UsernameExistsException":
                raise UserAlreadyExistsException("User already exists")
            if error.response["Error"]["Code"] == "InvalidPasswordException":
                raise RequirementsDoesNotMatchException(
                    "Password requirements does not match"
                )
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def verify_account(self, data: UserVerifyDTO) -> Dict[str, Any]:
        try:
            response = cast(
                Dict[str, Any],
                self.client.confirm_sign_up(
                    ClientId=self.cognito_user_pool_client_id,
                    Username=data.email,
                    ConfirmationCode=data.confirmation_code,
                ),
            )
            return response
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "CodeMismatchException":
                raise InvalidVerificationCodeException(
                    "he provided code does not match the expected value."
                )
            if error.response["Error"]["Code"] == "ExpiredCodeException":
                raise ExpiredVerificationCodeException(
                    "The provided code has expired."
                )
            if error.response["Error"]["Code"] == "UserNotFoundException":
                raise UserNotFoundException("User not found.")
            if error.response["Error"]["Code"] == "NotAuthorizedException":
                raise UnauthorizedException("Not authorized.")
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def resend_confirmation_code(self, email: EmailStr) -> Dict[str, Any]:
        try:
            response = cast(
                Dict[str, Any],
                self.client.resend_confirmation_code(
                    ClientId=self.cognito_user_pool_client_id, Username=email
                ),
            )
            return response
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "UserNotFoundException":
                raise UserNotFoundException("User not found.")
            if error.response["Error"]["Code"] == "LimitExceededException":
                raise LimitExceededException("Limit Exceeded.")
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def get_user(self, email: EmailStr) -> GetUserResponseDTO:
        try:
            response = cast(
                Dict[str, Any],
                self.client.admin_get_user(
                    UserPoolId=self.cognito_app_pool_id, Username=email
                ),
            )
            return GetUserResponseDTO(
                data=[
                    User(
                        username=response["Username"],
                        user_attributes=[
                            UserAttributeDTO(
                                name=attribute["Name"],
                                value=attribute["Value"],
                            )
                            for attribute in response["UserAttributes"]
                        ],
                        user_created_at=str(response["UserCreateDate"]),
                        user_last_modified_at=str(
                            response["UserLastModifiedDate"]
                        ),
                        user_status=response["UserStatus"],
                        user_enabled=response["Enabled"],
                    )
                ]
            )
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "UserNotFoundException":
                raise UserNotFoundException("User not found.")
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def user_signin(self, data: UserSigninDTO) -> AccessTokenResponseDTO:
        try:
            response = cast(
                Dict[str, Any],
                self.client.initiate_auth(
                    ClientId=self.cognito_user_pool_client_id,
                    AuthFlow="USER_PASSWORD_AUTH",
                    AuthParameters={
                        "USERNAME": data.email,
                        "PASSWORD": data.password,
                    },
                ),
            )
            return AccessTokenResponseDTO(
                data=[
                    dict(
                        access_token=response["AuthenticationResult"][
                            "AccessToken"
                        ],
                        expires_in=response["AuthenticationResult"][
                            "ExpiresIn"
                        ],
                        token_type=response["AuthenticationResult"][
                            "TokenType"
                        ],
                        refresh_token=response["AuthenticationResult"][
                            "RefreshToken"
                        ],
                        id_token=response["AuthenticationResult"]["IdToken"],
                    )
                ]
            )

        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "UserNotFoundException":
                raise UserNotFoundException("User not found.")
            if error.response["Error"]["Code"] == "UserNotConfirmedException":
                raise UserNotConfirmedException("Please verify your account.")
            if error.response["Error"]["Code"] == "NotAuthorizedException":
                raise InvalidCredentialsException(
                    "Incorrect username or password."
                )
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def forgot_password(self, email: EmailStr) -> ForgotPasswordResponseDTO:
        try:
            response = cast(
                Dict[str, Any],
                self.client.forgot_password(
                    ClientId=self.cognito_user_pool_client_id, Username=email
                ),
            )
            return ForgotPasswordResponseDTO(
                data=[
                    dict(
                        code_delivery_destination=response[
                            "CodeDeliveryDetails"
                        ]["Destination"],
                        code_delivery_type=response["CodeDeliveryDetails"][
                            "AttributeName"
                        ],
                    )
                ]
            )
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "UserNotFoundException":
                raise UserNotFoundException("User not found.")
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def confirm_forgot_password(
        self, data: ConfirmForgotPasswordDTO
    ) -> Dict[str, Any]:
        try:
            response = cast(
                Dict[str, Any],
                self.client.confirm_forgot_password(
                    ClientId=self.cognito_user_pool_client_id,
                    Username=data.email,
                    ConfirmationCode=data.confirmation_code,
                    Password=data.new_password,
                ),
            )
            return response
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "ExpiredCodeException":
                raise ExpiredVerificationCodeException("Code expired.")
            if error.response["Error"]["Code"] == "CodeMismatchException":
                raise InvalidVerificationCodeException("Code does not match.")
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def change_password(self, data: ChangePasswordDTO) -> Dict[str, Any]:
        try:
            response = cast(
                Dict[str, Any],
                self.client.change_password(
                    PreviousPassword=data.old_password,
                    ProposedPassword=data.new_password,
                    AccessToken=data.access_token,
                ),
            )
            return response
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "NotAuthorizedException":
                raise InvalidCredentialsException(
                    "Incorrect username or password."
                )
            if error.response["Error"]["Code"] == "LimitExceededException":
                raise LimitExceededException(
                    "Attempt limit exceeded, please try again later."
                )
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def new_access_token(self, refresh_token: str) -> AccessTokenResponseDTO:
        try:
            response = cast(
                Dict[str, Any],
                self.client.initiate_auth(
                    ClientId=self.cognito_user_pool_client_id,
                    AuthFlow="REFRESH_TOKEN_AUTH",
                    AuthParameters={
                        "REFRESH_TOKEN": refresh_token,
                    },
                ),
            )
            return AccessTokenResponseDTO(
                data=[
                    dict(
                        access_token=response["AuthenticationResult"][
                            "AccessToken"
                        ],
                        expires_in=response["AuthenticationResult"][
                            "ExpiresIn"
                        ],
                        token_type=response["AuthenticationResult"][
                            "TokenType"
                        ],
                        refresh_token=None,
                        id_token=response["AuthenticationResult"]["IdToken"],
                    )
                ]
            )
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "LimitExceededException":
                raise LimitExceededException(
                    "Attempt limit exceeded, please try again later."
                )
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise

    def logout(self, access_token: str) -> Dict[str, Any]:
        try:
            response = cast(
                Dict[str, Any],
                self.client.global_sign_out(AccessToken=access_token),
            )
            return response
        except botocore.exceptions.ClientError as error:
            logger.error(error.response)
            if error.response["Error"]["Code"] == "NotAuthorizedException":
                raise InvalidCredentialsException(
                    "Invalid access token provided."
                )
            if error.response["Error"]["Code"] == "TooManyRequestsException":
                raise TooManyRequestsException("Too many requests.")
            raise Exception("Internal server error.")
        except Exception as error:
            logger.error(f"SignUp error: {error}")
            raise
