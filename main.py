# coding: utf-8

import os
import uvicorn
from aioredis import Redis
import uuid

from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request, Depends

from fastapi_admin.app import FastAPIAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin import middlewares
from fastapi_admin.routes import router
from fastapi_admin.depends import get_resources, get_current_admin, get_redis
from fastapi_admin.template import templates
from fastapi_admin import constants
from fastapi_admin.utils import check_password
from fastapi_admin.i18n import _

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_401_UNAUTHORIZED

from tortoise.contrib.fastapi import register_tortoise

import aioredis

from settings import DATABASE, BASEDIR, REDIS

from v1.shop.shop import router as shop_router
from v1.auth.auth import router as auth_router

from models.resources import (
    AdminResource,
    CategoryResource,
    BrandNameResource,
    ProductResource,
    ProductGalleryResource,
    ProductItemsResource,
)
from models.extensions import AnonymousUser
from models.models import Admin

from base_obj import check_token

import grpc
import market_pb2
import market_pb2_grpc

from grpc_server import GetCategoriesServer


class ContractUsernamePasswordProvider(UsernamePasswordProvider):

    async def authenticate(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
    ):
        redis = request.app.redis  # type:Redis
        token = request.cookies.get(self.access_token)
        path = request.scope["path"]
        admin = None
        if token:
            token_key = constants.LOGIN_USER.format(token=token)
            admin_id = await redis.get(token_key)
            admin = await self.admin_model.get_or_none(pk=admin_id)
        request.state.admin = admin

        if path == self.login_path and admin:
            return RedirectResponse(url=request.app.admin_path + "/", status_code=HTTP_303_SEE_OTHER)

        response = await call_next(request)
        return response

    async def login(self, request: Request, redis: Redis = Depends(get_redis)):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        remember_me = form.get("remember_me")
        admin = await self.admin_model.get_or_none(username=username)
        if not admin or not check_password(password, admin.password):
            return templates.TemplateResponse(
                self.template,
                status_code=HTTP_401_UNAUTHORIZED,
                context={"request": request, "error": _("login_failed")},
            )
        response = RedirectResponse(url=request.app.admin_path + "/", status_code=HTTP_303_SEE_OTHER)
        if remember_me == "on":
            expire = 3600 * 24 * 30
            response.set_cookie("remember_me", "on")
        else:
            expire = 3600
            response.delete_cookie("remember_me")
        token = uuid.uuid4().hex
        response.set_cookie(
            self.access_token,
            token,
            expires=expire,
            path=request.app.admin_path,
            httponly=True,
        )
        await redis.set(constants.LOGIN_USER.format(token=token), admin.pk, ex=expire)
        return response


def create_app():
    login_provider = ContractUsernamePasswordProvider(
        admin_model=Admin,
        login_logo_url="https://preview.tabler.io/static/logo.svg"
    )

    _app = FastAPI(root_path="/api")

    admin_app = FastAPIAdmin(
        title="FastAdmin",
        description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
        root_path="/admin",
        admin_path="/admin/",
    )
    admin_app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
    admin_app.include_router(router)

    @admin_app.get("/")
    async def home(
            request: Request,
            resources=Depends(get_resources),
    ):
        if not request.state.admin:
            return RedirectResponse(
                url=request.app.admin_path + "/login", status_code=HTTP_303_SEE_OTHER
            )
        return templates.TemplateResponse(
            "dashboard.html",
            context={
                "request": request,
                "resources": resources,
                "resource_label": "Dashboard",
                "page_pre_title": "overview",
                "page_title": "Dashboard",
            },
        )

    _app.mount("/admin", admin_app)

    _app.include_router(auth_router)
    _app.include_router(shop_router)

    # _app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    #     expose_headers=[],
    # )

    register_tortoise(
        _app,
        db_url="postgres://{}:{}@{}:5432/{}".format(
            DATABASE["user"],
            DATABASE["password"],
            DATABASE["address"],
            DATABASE["name"],
        ),
        modules={"models": ["models.models", "aerich.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    @_app.on_event("startup")
    async def startup():
        redis = await aioredis.from_url("redis://{}:6379/0".format(REDIS), encoding="utf8")
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            template_folders=[os.path.join(BASEDIR, "templates")],
            providers=[login_provider],
            redis=redis,
        )
        admin_app.register(AdminResource)
        admin_app.register(CategoryResource)
        admin_app.register(BrandNameResource)
        admin_app.register(ProductResource)
        admin_app.register(ProductGalleryResource)
        admin_app.register(ProductItemsResource)

    return _app

app = create_app()

@app.middleware("http")
async def auth_middleware(request: Request, call_next, *args, **kwargs):
    request.scope["user"] = AnonymousUser()
    request.scope["auth"] = {"status": False, "reason": ""}
    if request.headers.get("authorization"):
        try:
            user_type, token = request.headers.get("authorization").split(' ')
            code, reason, user_info = await check_token(token=token)
        except:
            request.scope["auth"]["reason"] = "wrong token type"
        else:
            request.scope["user"] = user_info
            request.scope["auth"]["reason"] = reason
    else:
        request.scope["auth"]["reason"] = "no token"

    response = await call_next(request)

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)
