# coding: utf-8

from typing import Optional, List

from pydantic import BaseModel, Field


class BrandNameResponse(BaseModel):
    id: int = Field(description="brand_name pk")
    name: str = Field(description="name of brand")
    logo: str = Field(description="path to logo brand")
    created_at: str = Field(description="date of record creation")
    updated_at: str = Field(description="date of record last update")


class CategoryResponse(BaseModel):
    id: int = Field(description="category pk")
    name: str = Field(description="category name")
    created_at: str = Field(description="date of record creation")
    updated_at: str = Field(description="date of record last update")


class ProductResponse(BaseModel):
    id: int = Field(description="product pk")
    category: List[CategoryResponse] = Field(description="list of categories")
    brand_name: BrandNameResponse = Field(description="product brand")
    name: Optional[str] = Field(description="product name")
    description: Optional[str] = Field(description="product description")
    color: Optional[str] = Field(description="product color")
    sex: str = Field(description="product sex")
    age: str = Field(description="product age")
    article_number: Optional[str] = Field(description="product article number")
    price: Optional[float] = Field(description="product price")
    currency: Optional[str] = Field(description="product price currency")
    discount: float = Field(description="product price discount")
    rent: bool = Field(description="is product rentable")
    gallery: Optional[List[str]] = Field([], description="list of product imgs")
    created_at: str = Field(description="date of record creation")
    updated_at: str = Field(description="date of record last update")


class ProductListResponse(BaseModel):
    count: int = Field(description="full amount of products records")
    products: List[ProductResponse] = Field(description="products list")


class ProductItemResponse(BaseModel):
    id: int = Field(description="pk of product item")
    size: Optional[str] = Field(description="size of item")
    serial_number: Optional[str] = Field(description="unique item serial number")
    sold: bool = Field(description="is this item sold")
    buyer: Optional[int] = Field(description="pk of buyer")
    rent_time_start: Optional[int] = Field(description="rent product start")
    rent_time_stop: Optional[int] = Field(description="rent product stop")


class ProductItemsListResponse(BaseModel):
    product: ProductResponse = Field(description="product info")
    count: int = Field(description="count of product items")
    items: List[ProductItemResponse] = Field(description="list of product items")
