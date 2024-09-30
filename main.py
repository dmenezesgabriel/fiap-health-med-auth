import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.adapters.auth.cognito_adapter import AWSCognitoAdapter
from src.adapters.http.api_adapter import HTTPApiAdapter
from src.config import get_config
from src.domain.services.auth_service import AuthService

config = get_config()
logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    cognito_adapter = AWSCognitoAdapter()
    auth_service = AuthService(auth_adapter=cognito_adapter)
    http_api = HTTPApiAdapter(auth_service=auth_service)
    app.include_router(http_api.router, prefix=config.APP_PATH)
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url=config.APP_PATH + "/docs",
    openapi_url=config.APP_PATH + "/openapi.json",
)
