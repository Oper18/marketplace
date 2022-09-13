# coding: utf-8

from typing import Any, Type, Optional, Iterable

import datetime

from tortoise.models import Model, MODEL
from tortoise import fields
from tortoise.backends.base.client import BaseDBAsyncClient

from fastapi_admin.models import AbstractAdmin

from models.extensions import ExtendedModel, Sex, Age


class Admin(AbstractAdmin):
    _exclude = ("password")

    email = fields.CharField(max_length=256, unique=True)
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    external_id = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @classmethod
    async def create(cls: Type[MODEL], **kwargs: Any) -> MODEL:
        if not kwargs.get("email"):
            kwargs["email"] = kwargs.get("username")
        return await super(Admin, cls).create(**kwargs)

    @property
    def is_anonymous(self):
        return False


class Category(Model, ExtendedModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.name}"


class BrandName(Model, ExtendedModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)
    logo = fields.CharField(max_length=64, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.name}"


class Product(Model, ExtendedModel):
    _exclude = ("brand_name_id",)

    id = fields.IntField(pk=True)
    category = fields.ManyToManyField(
        'models.Category', related_name='products', through='product_category'
    )
    brand_name = fields.ForeignKeyField(
        'models.BrandName', related_name='products'
    )
    name = fields.CharField(max_length=256)
    description = fields.TextField()
    color = fields.CharField(max_length=64, null=True)
    sex = fields.IntEnumField(enum_type=Sex)
    age = fields.IntEnumField(enum_type=Age)
    article_number = fields.CharField(max_length=256, null=True, unique=True)
    size = fields.CharField(max_length=64, null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = fields.CharField(max_length=16, null=True)
    discount = fields.FloatField(default=0.0)
    rent = fields.BooleanField(default=False)
    service = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.name}"


class ProductGallery(Model, ExtendedModel):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField('models.Product', related_name='imgs')
    img = fields.CharField(max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"


class ProductItems(Model, ExtendedModel):
    _exclude = ("created_at", "updated_at", "product_id")

    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField('models.Product', related_name='items')
    sold = fields.BooleanField(default=False)
    buyer = fields.IntField(null=True)
    salesman = fields.IntField(null=True)
    rent_time_start = fields.DatetimeField(null=True)
    rent_time_stop = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    @classmethod
    async def create(cls: Type[MODEL], **kwargs: Any) -> MODEL:
        if int(kwargs.get("buyer", 0)) == 0:
            kwargs["buyer"] = None
        return await super(ProductItems, cls).create(**kwargs)
