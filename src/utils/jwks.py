import json
import logging
from typing import Dict, Optional, cast

import jwt
import requests
from jwt.algorithms import RSAAlgorithm

logger = logging.getLogger()


class JWKClient:
    def __init__(
        self,
        uri: str,
        headers: Optional[Dict[str, str]] = None,
    ):
        self._uri = uri
        self._headers = headers

    def get_signing_key_from_jwt(
        self,
        token: str,
    ) -> str:
        try:
            response = requests.get(url=self._uri, headers=self._headers)
            response.raise_for_status()
            jwks = response.json()

            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            if not kid:
                raise ValueError("No 'kid' found in the JWT header.")

            for jwk in jwks["keys"]:
                if jwk["kid"] == kid:
                    public_key = cast(
                        str,
                        RSAAlgorithm.from_jwk(json.dumps(jwk)),  # type: ignore
                    )
                    return public_key

            raise ValueError(
                f"Unable to find a signing key that matches the 'kid': {kid}"
            )

        except requests.RequestException as error:
            logger.error(f"Failed to fetch JWKs: {error}")
            raise
        except jwt.DecodeError as error:
            logger.error(f"Failed to decode JWT: {error}")
            raise
