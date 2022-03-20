# coding: utf-8

import datetime
import jwt
import dateutil.parser

from typing import Optional, List, Any

from fastapi import APIRouter, status, Response, Header, Request
from fastapi_admin.utils import check_password

from tortoise.expressions import Q

from response_models import Error40xResponse

from .request_models import Auth, Refresh
from .response_models import AuthResponse, AccountInfo

from models.models import Admin

from base_obj import check_token, etag_checker, \
    replace_response, generate_tokens, login_required
from settings import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SERVER_SECRET


router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"]
)


@router.post(
    "",
    responses={
        200: {
            "model": AuthResponse,
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong auth token",
        },
    }
)
async def auth_method(
        auth: Auth,
        request: Request,
        response: Response,
        status_code: Optional[Any] = status.HTTP_200_OK,
) -> dict:
    user = await Admin.filter(Q(username=auth.username) | Q(email=auth.username)).first()
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return Error40xResponse.parse_obj({"reason": "wrong credentials"})
    if user and auth.password:
        try:
            check_password(auth.password, user.password)
        except:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return Error40xResponse.parse_obj({'reason': 'wrong username or password'})
        else:
            if check_password(auth.password, user.password):
                auth_tokens = await generate_tokens(
                    pk=user.id,
                    email=user.email,
                    password=user.password,
                )
                return AuthResponse.parse_obj(auth_tokens)

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return Error40xResponse.parse_obj({'reason': 'wrong username or password'})

@router.post(
    "/refresh",
    responses={
        200: {
            "model": AuthResponse,
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong auth token",
        },
    }
)
async def auth_refresh_method(
        refresh: Refresh,
        request: Request,
        response: Response,
        status_code: Optional[Any] = status.HTTP_200_OK,
) -> dict:
    code, response, user = await check_token(refresh.refresh_token)
    if code == status.HTTP_200_OK:
        access_token_exp_date = datetime.datetime.now().timestamp() + ACCESS_TOKEN_LIFETIME
        refresh_token_exp_date = datetime.datetime.now().timestamp() + REFRESH_TOKEN_LIFETIME
        access_token = jwt.encode(
            {
                'user_id': user.id,
                'username': user.username,
                'password': user.password,
                'expiration_time': access_token_exp_date,
            },
            SERVER_SECRET,
            algorithm='HS256'
        )
        refresh_token = jwt.encode(
            {
                'user_id': user.id,
                'username': user.username,
                'password': user.password,
                'expiration_time': refresh_token_exp_date,
            },
            SERVER_SECRET,
            algorithm='HS256'
        )
        return AuthResponse.parse_obj({'access_token': access_token, 'refresh_token': refresh_token})

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return Error40xResponse.parse_obj({'reason': 'wrong refresh token'})


@router.get(
    "/account/info",
    responses={
        200: {
            "model": AccountInfo,
            "decription": "full account information",
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong auth token",
        },
    }
)
@login_required
@etag_checker
async def get_account_info(
        request: Request,
        response: Response,
        authorization: Optional[str] = Header(None),
        if_none_match: Optional[str] = Header(None),
        status_code=status.HTTP_200_OK,
        etag_request: Optional[str] = None,
) -> List[dict]:
    if etag_request and \
            request.user.updated_at <= dateutil.parser.parse(etag_request.get("updated_at")) and \
            request.user.id == etag_request.get("user_id"):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    return AccountInfo.parse_obj(
        replace_response(
            response={"user_info": await request.user.as_dict()},
            updated_at=request.user.updated_at.isoformat(),
            user_id=request.user.id
        )
    )
