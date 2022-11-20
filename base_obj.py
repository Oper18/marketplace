# coding: utf-8

import os
import jwt
import hashlib
import datetime
import json
import base64

from functools import wraps

from fastapi import status

from settings import LOCAL_SALT, SERVER_SECRET
from response_models import Error40xResponse

from models.models import Admin
from models.extensions import AnonymousUser

from settings import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SERVER_SECRET


async def check_token(token):
    try:
        token_info = jwt.decode(token, SERVER_SECRET, algorithms=['HS256'])
    except Exception as e:
        # logger.error('check_token, Decode auth token failed: {}'.format(e))
        return status.HTTP_401_UNAUTHORIZED, 'wrong token type', AnonymousUser
    else:
        try:
            user_info = await Admin.filter(id=token_info['user_id']).first()
        except:
            return status.HTTP_401_UNAUTHORIZED, 'no user', AnonymousUser
        else:
            if user_info:
                if user_info.password == token_info['password'] and \
                        token_info['expiration_time'] >= datetime.datetime.now().timestamp():
                    return status.HTTP_200_OK, 'user authenticated', user_info
                else:
                    return status.HTTP_401_UNAUTHORIZED, 'token expired', AnonymousUser
            else:
                return status.HTTP_401_UNAUTHORIZED, 'no user', AnonymousUser


def login_required(func):
    @wraps(func)
    async def wrapper(**kwargs):
        if kwargs.get('request').user and not kwargs['request'].user.is_anonymous:
            return await func(**kwargs)
        else:
            kwargs['response'].status_code = status.HTTP_401_UNAUTHORIZED
            return Error40xResponse.parse_obj({'reason': kwargs.get('request').auth.get("reason")})
    return wrapper


def etag_checker(func):
    @wraps(func)
    async def wrapper(**kwargs):
        etag = kwargs.get('if_none_match', None)
        if etag:
            etag = json.loads(base64.b64decode(etag.encode("utf-8")).decode("utf-8"))
        kwargs['etag_request'] = etag
        return await func(**kwargs)
    return wrapper


def replace_response(response, **kwargs):
    if kwargs:
        if kwargs.get("updated_at"):
            etag = base64.b64encode(json.dumps(kwargs).encode("utf-8"))
            etag = etag.decode("utf-8")
            response.update({"etag": etag})
    return response


async def generate_tokens(
    pk: int, email: str, password: str
) -> dict:
    access_token_exp_date = datetime.datetime.now().timestamp() + ACCESS_TOKEN_LIFETIME
    refresh_token_exp_date = datetime.datetime.now().timestamp() + REFRESH_TOKEN_LIFETIME
    access_token = jwt.encode(
        {
            'user_id': pk,
            'email': email,
            'password': password,
            'expiration_time': access_token_exp_date,
        },
        SERVER_SECRET,
        algorithm='HS256'
    )
    refresh_token = jwt.encode(
        {
            'user_id': pk,
            'email': email,
            'password': password,
            'expiration_time': refresh_token_exp_date,
        },
        SERVER_SECRET,
        algorithm='HS256'
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def segmented_path(root_path, file_name):
    os.makedirs(
        os.path.join(
            root_path,
            file_name[:2],
            file_name[2:4],
            file_name[4:6],
        ),
        exist_ok=True
    )
    return os.path.join(
        root_path,
        file_name[:2],
        file_name[2:4],
        file_name[4:6],
        file_name,
    )


def form_model_doc_generation(model):
    res = json.loads(model.schema_json())
    res = res["properties"]
    for i in res:
        res[i].pop("title", None)
        if res[i].get("$ref"):
            res[i] = form_model_doc_generation(model.__dict__["__fields__"][i].type_)
        elif res[i].get("type") and res[i].get("type") == "array":
            if res[i]["items"].get("$ref"):
                res[i]["items"] = form_model_doc_generation(model.__dict__["__fields__"][i].type_)

    return res


class BaseArrGenerator:
    def __init__(self, arr):
        self.arr = iter(arr)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.arr)
        except:
            raise StopAsyncIteration
