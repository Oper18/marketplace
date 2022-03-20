# coding: utf-8

from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from models.extensions import Sex, Age


class SerialNumberRequest(BaseModel):
    serial_number: int = Field(description="Product serial number")


class CategoryRequest(BaseModel):
    id: Optional[int] = Field(None, description="category pk")
    name: Optional[str] = Field(None, description="category name")


class ProductGalleryImgRequest(BaseModel):
    id: Optional[int] = Field(None, description="product img pk")
    key: Optional[str] = Field(None, description="key in form data for upload image")


class ProductRequest(BaseModel):
    id: Optional[int] = Field(None, description="product pk")
    name: Optional[str] = Field(None, description="product name")
    description: Optional[str] = Field(None, description="product description")
    color: Optional[str] = Field(None, description="product color")
    sex: Optional[Sex] = Field(None, description="product sex")
    age: Optional[Age] = Field(None, description="product age")
    article_number: Optional[str] = Field(None, description="unique product article number")
    price: Optional[float] = Field(None, description="product price")
    currency: Optional[str] = Field(None, description="product price currency")
    discount: Optional[str] = Field(None, description="product price discount")
    rent: Optional[bool] = Field(None, description="is product rentable")
    category: List[int] = Field(None, description="list of product categories")
    brand_name: int = Field(None, description="product brand name")
    imgs: Optional[List[ProductGalleryImgRequest]] = Field(None, description="list of product imgs")


class ProductItemRequest(BaseModel):
    id: Optional[int] = Field(None, description="product item pk")
    size: Optional[str] = Field(None, description="size")
    serial_number: Optional[str] = Field(None, description="unique serial number")
    sold: Optional[bool] = Field(False, description="is item sold")
    buyer: Optional[int] = Field(0, description="buyer pk")
    rent_time_start: Optional[str] = Field(None, description="time start of item rent, only for rent")
    rent_time_stop: Optional[str] = Field(None, description="time stop of item rent, only for rent")


class ProductItemsListRequest(BaseModel):
    product: Optional[int] = Field(None, description="product pk")
    items: List[ProductItemRequest] = Field(description="list of product items")
