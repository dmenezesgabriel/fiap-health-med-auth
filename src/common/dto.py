from typing import Annotated, List, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import TypedDict


class UserSignupDTO(BaseModel):
    full_name: str = Field(max_length=50)
    cpf: str
    email: EmailStr
    password: Annotated[str, MinLen(8)]
    role: str
    crm: Optional[str] = None


class UserVerifyDTO(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]


class UserSigninDTO(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]


class ConfirmForgotPasswordDTO(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]
    new_password: Annotated[str, MinLen(8)]


class ChangePasswordDTO(BaseModel):
    old_password: Annotated[str, MinLen(8)]
    new_password: Annotated[str, MinLen(8)]
    access_token: str


class ChangePasswordRequestDTO(BaseModel):
    old_password: Annotated[str, MinLen(8)]
    new_password: Annotated[str, MinLen(8)]


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class SignUpDict(TypedDict):
    user_id: str
    user_confirmed: bool
    code_delivery_destination: str
    code_delivery_type: str


class SignUpResponseDTO(BaseModel):
    data: List[SignUpDict]


class AccessTokenDict(TypedDict):
    access_token: str
    expires_in: int
    token_type: str
    id_token: str
    refresh_token: Optional[str]


class AccessTokenResponseDTO(BaseModel):
    data: List[AccessTokenDict]


class ForgotPasswordDict(TypedDict):
    code_delivery_destination: str
    code_delivery_type: str


class ForgotPasswordResponseDTO(BaseModel):
    data: List[ForgotPasswordDict]


class UserAttributeDTO(TypedDict):
    name: str
    value: Optional[str]


class User(BaseModel):
    username: str
    user_attributes: List[UserAttributeDTO]
    user_created_at: str
    user_last_modified_at: str
    user_status: str
    user_enabled: bool


class GetUserResponseDTO(BaseModel):
    data: List[User]
