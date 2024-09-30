import logging
from enum import Enum
from typing import Any, Literal, Optional, cast

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.adapters.cloud.aws_client_adapter import AWSClientAdapter
from src.config import get_config
from src.utils.jwks import JWKClient

config = get_config()
logger = logging.getLogger(__name__)


class CognitoTokenUse(Enum):
    ID = "id"
    ACCESS = "access"


class CognitoJWTAuthorizer(HTTPBearer):

    def __init__(
        self,
        required_token_use: CognitoTokenUse,
        aws_default_region: str,
        cognito_user_pool_id: str,
        cognito_user_pool_client_id: str,
        issuer_uri: str,
        jwks_client: Any,
        auto_error: bool = True,
    ) -> None:
        super().__init__(auto_error=auto_error)
        self.required_token_use = required_token_use
        self.aws_default_region = aws_default_region
        self.cognito_user_pool_id = cognito_user_pool_id
        self.cognito_user_pool_client_id = cognito_user_pool_client_id
        self.jwks_client = jwks_client
        self.issuer_uri = issuer_uri

    async def __call__(self, request: Request) -> Any:
        credentials: Optional[HTTPAuthorizationCredentials] = (
            await super().__call__(request)
        )

        if not credentials:
            logger.error("Credentials not found.")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if not credentials.scheme == "Bearer":
            logger.error("Bearer not found.")
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Wrong authentication method",
            )
        token: str = credentials.credentials

        try:
            signing_key: str = self.jwks_client.get_signing_key_from_jwt(token)
        except jwt.exceptions.InvalidTokenError as e:
            logger.error(3)
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            ) from e

        try:
            claims = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                issuer=self.issuer_uri,
                options={
                    "verify_aud": False,
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iss": True,
                    "require": ["token_use", "exp", "iss", "sub"],
                },
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            logger.error("ExpiredSignatureError")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            ) from e
        except jwt.exceptions.InvalidTokenError as e:
            logger.error(e)
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            ) from e
        if self.required_token_use.value != claims["token_use"]:
            logger.error("No token_use claims")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if self.required_token_use == CognitoTokenUse.ID:
            if "aud" not in claims:
                logger.error("No aud in claims")
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
            if claims["aud"] != self.cognito_user_pool_client_id:
                logger.error("Wrong pool client id")
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
        elif self.required_token_use == CognitoTokenUse.ACCESS:
            if "client_id" not in claims:
                logger.error("client_id not in claims")
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
            if claims["client_id"] != self.cognito_user_pool_client_id:
                logger.error("Wrong pool client id")
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        return token


class CognitoAuthorizerFactory:
    def __init__(self) -> None:
        self.__aws_client = AWSClientAdapter(client_type="sts")
        self._issuer_uri = config.get_parameter("AWS_COGNITO_ISSUER_URI")
        self._aws_cognito_user_pool_id = config.get_parameter(
            "AWS_COGNITO_USER_POOL_ID"
        )
        self._aws_cognito_app_client_id = config.get_parameter(
            "AWS_COGNITO_APP_CLIENT_ID"
        )
        self.__jwks_client = self.__get_jwk_client()

    def __get_jwk_client(self) -> Any:
        headers = None
        if config.ENVIRONMENT == "local":
            headers = {
                "Authorization": (
                    "AWS4-HMAC-SHA256 Credential"
                    f"={self.__aws_client.aws_access_key_id}/20220524/"
                    f"{self.__aws_client.aws_region_name}/cognito-idp/"
                    "aws4_request, SignedHeaders=content-length;content-type;"
                    "host;x-amz-date, Signature=asdf"
                ),
                "x-amz-date": "20220524T000000Z",
                "Content-Type": "application/json",
                "Content-Length": "0",
            }
        return JWKClient(uri=self.__get_jwk_uri(), headers=headers)

    def __get_jwk_uri(self) -> str:
        jwk_uri = config.get_parameter("AWS_COGNITO_JWK_URI")
        if config.ENVIRONMENT == "local":
            jwk_uri = (
                cast(str, self.__aws_client.aws_endpoint_url)
                + "/"
                + cast(str, self._aws_cognito_user_pool_id)
                + "/.well-known/jwks.json"
            )
        return cast(str, jwk_uri)

    def __create_access_token_authorizer(self) -> CognitoJWTAuthorizer:
        return CognitoJWTAuthorizer(
            CognitoTokenUse.ACCESS,
            cast(str, self.__aws_client.aws_region_name),
            cast(str, self._aws_cognito_user_pool_id),
            cast(str, self._aws_cognito_app_client_id),
            cast(str, self._issuer_uri),
            self.__jwks_client,
        )

    def __create_access_id_authorizer(self) -> CognitoJWTAuthorizer:
        return CognitoJWTAuthorizer(
            CognitoTokenUse.ID,
            cast(str, self.__aws_client.aws_region_name),
            cast(str, self._aws_cognito_user_pool_id),
            cast(str, self._aws_cognito_app_client_id),
            cast(str, self._issuer_uri),
            self.__jwks_client,
        )

    def get(
        self, type: Literal["access_token", "access_id"]
    ) -> CognitoJWTAuthorizer:
        authorizers = {
            "access_token": self.__create_access_token_authorizer,
            "access_id": self.__create_access_id_authorizer,
        }
        return authorizers[type]()
