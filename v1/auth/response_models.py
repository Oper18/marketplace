# coding: utf-8

from typing import Optional, List

from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]


class UserInfoResponse2(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    admin_id: Optional[int]
    last_login: Optional[str]
    created_at: str
    updated_at: str


class RegResponse(BaseModel):
    auth: AuthResponse
    user_info: UserInfoResponse2


class AccountInfo(BaseModel):
    user_info: UserInfoResponse2
    etag: str


class UsersListResponse(BaseModel):
    users: List[UserInfoResponse2]
    etag: Optional[str]
