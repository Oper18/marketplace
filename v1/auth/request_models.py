# coding: utf-8

from typing import Optional

from pydantic import BaseModel


class Auth(BaseModel):
    username: str
    password: str


class Refresh(BaseModel):
    refresh_token: str


class Register(BaseModel):
    username: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]


class UserChangeRequest(BaseModel):
    old_password: Optional[str]
    new_password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
