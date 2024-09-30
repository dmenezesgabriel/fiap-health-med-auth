from unittest.mock import MagicMock, patch

import jwt
import pytest
import requests

from src.utils.jwks import JWKClient


class TestJWKClientInitialization:
    def test_initialization(self) -> None:
        # Arrange & Act
        client = JWKClient(
            uri="https://example.com/.well-known/jwks.json",
            headers={"Authorization": "Bearer token"},
        )

        # Assert
        assert client._uri == "https://example.com/.well-known/jwks.json"
        assert client._headers == {"Authorization": "Bearer token"}


class TestJWKClientGetSigningKeyFromJWT:
    @patch("src.utils.jwks.requests.get")
    def test_get_signing_key_success(self, mock_get: MagicMock) -> None:
        # Arrange
        token = "header.payload.signature"
        unverified_header = {"kid": "12345"}
        jwk = {
            "keys": [
                {
                    "kid": "12345",
                    "kty": "RSA",
                    "use": "sig",
                    "alg": "RS256",
                    "n": "0vx7agoebGcQSuuPiLJXZptNEX9PzNn74L...",
                    "e": "AQAB",
                    "x5c": ["MIIDBTCCAe2gAwIBAgIJA..."],
                    "x5t": "1VbL...",
                    "x5t#S256": "1VbL...",
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = jwk
        mock_get.return_value = mock_response

        with patch(
            "src.utils.jwks.jwt.get_unverified_header",
            return_value=unverified_header,
        ):
            with patch(
                "src.utils.jwks.RSAAlgorithm.from_jwk",
                return_value="public_key",
            ):
                client = JWKClient(
                    uri="https://example.com/.well-known/jwks.json"
                )

                # Act
                public_key = client.get_signing_key_from_jwt(token)

                # Assert
                assert public_key == "public_key"
                mock_get.assert_called_once_with(
                    url="https://example.com/.well-known/jwks.json",
                    headers=None,
                )

    @patch("src.utils.jwks.requests.get")
    def test_get_signing_key_no_kid_in_token(
        self, mock_get: MagicMock
    ) -> None:
        # Arrange
        token = "header.payload.signature"
        jwk = {"keys": []}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = jwk
        mock_get.return_value = mock_response

        with patch(
            "src.utils.jwks.jwt.get_unverified_header", return_value={}
        ):
            client = JWKClient(uri="https://example.com/.well-known/jwks.json")

            # Act & Assert
            with pytest.raises(
                ValueError, match="No 'kid' found in the JWT header."
            ):
                client.get_signing_key_from_jwt(token)

    @patch("src.utils.jwks.requests.get")
    def test_get_signing_key_kid_not_found(self, mock_get: MagicMock) -> None:
        # Arrange
        token = "header.payload.signature"
        unverified_header = {"kid": "12345"}
        jwk = {
            "keys": [
                {
                    "kid": "54321",
                    "kty": "RSA",
                    "use": "sig",
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = jwk
        mock_get.return_value = mock_response

        with patch(
            "src.utils.jwks.jwt.get_unverified_header",
            return_value=unverified_header,
        ):
            client = JWKClient(uri="https://example.com/.well-known/jwks.json")

            # Act & Assert
            with pytest.raises(
                ValueError,
                match="Unable to find a signing key that matches the 'kid': 12345",
            ):
                client.get_signing_key_from_jwt(token)

    @patch("src.utils.jwks.requests.get")
    def test_get_signing_key_jwks_request_exception(
        self, mock_get: MagicMock
    ) -> None:
        # Arrange
        token = "header.payload.signature"
        mock_get.side_effect = requests.RequestException("Request failed")

        client = JWKClient(uri="https://example.com/.well-known/jwks.json")

        # Act & Assert
        with patch("src.utils.jwks.logger.error") as mock_logger:
            with pytest.raises(
                requests.RequestException, match="Request failed"
            ):
                client.get_signing_key_from_jwt(token)
            mock_logger.assert_called_once_with(
                "Failed to fetch JWKs: Request failed"
            )

    @patch("src.utils.jwks.requests.get")
    def test_get_signing_key_jwt_decode_error(
        self, mock_get: MagicMock
    ) -> None:
        # Arrange
        token = "header.payload.signature"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"keys": []}
        mock_get.return_value = mock_response

        with patch(
            "src.utils.jwks.jwt.get_unverified_header",
            side_effect=jwt.DecodeError("Invalid token"),
        ):
            client = JWKClient(uri="https://example.com/.well-known/jwks.json")

            # Act & Assert
            with patch("src.utils.jwks.logger.error") as mock_logger:
                with pytest.raises(jwt.DecodeError, match="Invalid token"):
                    client.get_signing_key_from_jwt(token)
                mock_logger.assert_called_once_with(
                    "Failed to decode JWT: Invalid token"
                )


if __name__ == "__main__":
    pytest.main()
