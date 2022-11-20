# coding: utf-8

import os
import uuid
import aiofiles

from typing import Any

from starlette.requests import Request

from fastapi_admin.resources import Action, Field, Link, Model
from fastapi_admin.widgets import displays, filters, inputs
from fastapi_admin.file_upload import FileUpload

from models.models import (
    Admin,
    Category,
    BrandName,
    Product,
    ProductGallery,
    ProductItems,
)

from models.extensions import ExtendedModel, Sex, Age

from settings import IMG_DIR, IMG_PATH


def filename_generator(file):
    return uuid.uuid4().hex + '.' + file.filename.split('.')[-1]


class MarketPlaceAdminFileUpload(FileUpload):

    async def save_file(self, filename: str, content: bytes):
        file = os.path.join(self.uploads_dir, filename[:2], filename[2:4], filename[4:6], filename)
        os.makedirs(os.path.dirname(file), exist_ok=True)
        async with aiofiles.open(file, "wb") as f:
            await f.write(content)
        return os.path.join(self.prefix, filename)


img_upload = MarketPlaceAdminFileUpload(
    uploads_dir=IMG_DIR,
    prefix="",
    filename_generator=filename_generator,
)


class MarketImage(inputs.Image):

    async def render(self, request: Request, value: Any):
        if value:
            value = os.path.join(IMG_PATH, value)
        return await super(MarketImage, self).render(request, value)


class MarketEnum(inputs.Enum):

    async def parse_value(self, request: Request, value: Any):
        return self.enum(self.enum_type(value)).value


class AdminResource(Model):
    label = "Admin"
    model = Admin
    page_pre_title = "Admins"
    page_title = "Admins"
    filters = [
        filters.Search(
            name="username",
            label="Admin username",
            search_mode="icontains",
            placeholder="Search for admin username",
        ),
        filters.Search(
            name="email",
            label="Admin email",
            search_mode="icontains",
            placeholder="Search for admin email",
        ),
    ]
    fields = [
        "id",
        Field(
            name="username",
            label="",
            input_=inputs.Text(),
        ),
        Field(
            name="email",
            label="",
            input_=inputs.Email(),
        ),
        "last_login",
        Field(
            name="external_id",
            label="",
            input_=inputs.Number(),
        ),
        "created_at",
        "updated_at",
    ]


class CategoryResource(Model):
    label = "Category"
    model = Category
    page_pre_title = "Categories"
    page_title = "Categories"
    filters = [
        filters.Search(
            name="name",
            label="Category name",
            search_mode="icontains",
            placeholder="Search for category name",
        ),
    ]
    fields = [
        "id",
        Field(
            name="name",
            label="",
            input_=inputs.Text(),
        ),
        "created_at",
        "updated_at",
    ]


class BrandNameResource(Model):
    label = "Brand"
    model = BrandName
    page_pre_title = "Brands"
    page_title = "Brands"
    filters = [
        filters.Search(
            name="name",
            label="Brand name",
            search_mode="icontains",
            placeholder="Search for brandname",
        ),
    ]
    fields = [
        "id",
        Field(
            name="name",
            label="",
            input_=inputs.Text(),
        ),
        Field(
            name="logo",
            label="",
            input_=MarketImage(
                upload=img_upload, null=True
            ),
        ),
        "created_at",
        "updated_at",
    ]


class ProductResource(Model):
    label = "Products"
    model = Product
    page_pre_title = "Products"
    page_title = "Products"
    filters = [
        filters.Search(
            name="name",
            label="Product name",
            search_mode="icontains",
            placeholder="Search for product name",
        ),
        filters.Search(
            name="full_name",
            label="Product full name",
            search_mode="icontains",
            placeholder="Search for product full name",
        ),
    ]
    fields = [
        "id",
        # "category",
        Field(
            name="category",
            label="",
            input_=inputs.ManyToMany(model=Category),
        ),
        "brand_name",
        Field(
            name="name",
            label="",
            input_=inputs.Text(),
        ),
        Field(
            name="description",
            label="",
            input_=inputs.Text(),
        ),
        Field(
            name="color",
            label="",
            input_=inputs.Text(null=True),
        ),
        Field(
            name="sex",
            label="",
            input_=MarketEnum(enum=Sex),
        ),
        Field(
            name="age",
            label="",
            input_=MarketEnum(enum=Age),
        ),
        Field(
            name="article_number",
            label="",
            input_=inputs.Text(null=True),
        ),
        Field(
            name="price",
            label="",
            input_=inputs.Number(default=0.0),
        ),
        Field(
            name="currency",
            label="",
            input_=inputs.Text(null=True),
        ),
        Field(
            name="discount",
            label="",
            input_=inputs.Number(default=0.0),
        ),
        "rent",
        "created_at",
        "updated_at",
    ]


class ProductGalleryResource(Model):
    label = "Product's gallery"
    model = ProductGallery
    page_pre_title = "Product's gallery"
    page_title = "Product's gallery"
    filters = [
        filters.Search(
            name="product",
            label="Product pk",
            search_mode="equal",
            placeholder="Search for product imgs",
        ),
    ]
    fields = [
        "id",
        "product",
        Field(
            name="img",
            label="",
            input_=MarketImage(
                upload=img_upload, null=True
            ),
        ),
        "created_at",
        "updated_at",
    ]


class ProductItemsResource(Model):
    label = "ProductItems"
    model = ProductItems
    page_pre_title = "ProductItems"
    page_title = "ProductItems"
    filters = [
        filters.Search(
            name="product",
            label="Product pk",
            search_mode="equal",
            placeholder="Search for product items",
        ),
        filters.Search(
            name="buyer",
            label="Item buyer pk",
            search_mode="equal",
            placeholder="Search for product item buyer",
        ),
    ]
    fields = [
        "id",
        "product",
        "sold",
        Field(
            name="buyer",
            label="",
            input_=inputs.Number(null=True, default=None),
        ),
        "salesman",
        "rent_time_start",
        "rent_time_stop",
        "created_at",
        "updated_at",
    ]

