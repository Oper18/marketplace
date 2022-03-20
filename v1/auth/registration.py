# coding: utf-8

from typing import Optional, List, Any, Union

from fastapi import APIRouter, Header, status, Response, Request
from fastapi_admin.utils import hash_password, check_password

from tortoise.exceptions import IntegrityError

from base_obj import etag_checker, replace_response, generate_tokens, login_required

from response_models import Error40xResponse

from .request_models import Register, UserChangeRequest
from .response_models import UserInfoResponse, UsersListResponse, RegResponse, \
    UserInfoResponse2

from models.models import Admin


router = APIRouter(
    prefix="/v1/register",
    tags=["register"]
)


@router.post(
    "/user",
    responses={
        200: {
            "model": RegResponse,
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong auth token",
        },
        406: {
            "model": Error40xResponse,
            "description": "method not accept for this user type",
        },
    }
)
async def register_user(
        reg: Register,
        request: Request,
        response: Response,
        status_code: Optional[Any] = status.HTTP_200_OK,
) -> dict:
    reg_dict = reg.dict()
    reg_dict["password"] = hash_password(password=reg_dict["password"])
    try:
        new_user = await Admin.create(**reg_dict)
    except IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return Error40xResponse.parse_obj(
            {"reason": "email allready registered"}
        )
    except:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Error40xResponse.parse_obj(
            {"reason": "registration failed"}
        )
    else:
        auth_tokens = await generate_tokens(
            pk=new_user.id,
            email=new_user.email,
            password=new_user.password,
        )
        res = {
            "auth": auth_tokens,
            "user_info": await new_user.as_dict(),
        }
        return RegResponse.parse_obj(res)


@router.get(
    "/list",
    responses={
        200: {
            "model": UsersListResponse,
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong auth token",
        },
    }
)
@login_required
@etag_checker
async def get_users(
        request: Request,
        response: Response,
        authorization: Optional[str] = Header(None),
        if_none_match: Optional[str] = Header(None),
        user_id: Optional[int] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        status_code: Optional[Any] = status.HTTP_200_OK,
        etag_request: Optional[str] = None,
) -> List[dict]:
    users = await Admin.all().limit(limit=limit).offset(offset=offset)
    users = [await i.as_dict() for i in users]
    return UsersListResponse.parse_obj(
        replace_response(
            response={"users": users},
            updated_at=users[-1]["updated_at"] if users else None,
            user_id=user_id,
        )
    )


@router.post(
    "/user/change",
    responses={
        200: {
            "model": UserInfoResponse2,
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong auth token",
        },
        406: {
            "model": Error40xResponse,
            "description": "method not accept for this user type",
        },
    }
)
@login_required
async def register_user(
        change: UserChangeRequest,
        request: Request,
        response: Response,
        status_code: Optional[Any] = status.HTTP_200_OK,
) -> Union[UserInfoResponse2, Error40xResponse]:
    change_dict = dict()
    for k, v in change.__dict__.items():
        if v is not None:
            change_dict[k] = v
    if change_dict.get("new_password") and \
        (
            not change_dict.get("old_password") or \
            not check_password(change_dict.get("old_password"), request.user.password)
        ):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Error40xResponse.parse_obj(
            {"reason": "need old and new passwords"}
        )
    elif change_dict.get("new_password") and \
        change_dict.get("old_password") and \
        check_password(change_dict.get("old_password"), request.user.password):
        change_dict.pop("old_password")
        change_dict["password"] = hash_password(change_dict.pop("new_password"))
    for k, v in change_dict.items():
        setattr(request.user, k, v)
    await request.user.save()
    return UserInfoResponse2.parse_obj(
        await request.user.as_dict()
    )
