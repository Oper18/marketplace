# coding: utf-8

import os
import re
import json

from functools import wraps

from typing import Optional, Union, List, Any

from fastapi import (
    APIRouter,
    status,
    Response,
    Request,
    Query,
    Form,
    File,
    UploadFile,
    Header,
)

from .response_models import (
    ProductResponse,
    ProductListResponse,
    ProductItemsListResponse,
    CategoryResponse,
    BrandNameResponse,
    ProductItemResponse,
)
from .request_models import (
    SerialNumberRequest,
    CategoryRequest,
    ProductRequest,
    ProductItemsListRequest,
)

from response_models import Error40xResponse

from .manager import (
    get_categories,
    get_brands,
    get_products,
    get_product_items,
    get_product,
    manage_category,
    manage_brand_name,
    manage_product,
    create_product_items,
    buy_rent_product_item,
    delete_product_item,
)

from base_obj import form_model_doc_generation, login_required


router = APIRouter(
    prefix="/v1/shop",
    tags=["shop"]
)


@router.get(
    "/brands",
    responses={
        200: {
            "model": List[CategoryResponse],
            "description": "products list with full count",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong",
        },
    },
    summary="Categories list",
)
async def get_brands_endpoint(
    request: Request,
    response: Response,
    limit: Optional[int] = Query(10, description="amount of returned brands"),
    offset: Optional[int] = Query(0, description="amount of scrolled brands"),
) -> List[CategoryResponse]:
    brand_names = await get_brands(
        limit=limit,
        offset=offset,
    )
    return [
        BrandNameResponse.parse_obj(brand)
        for brand in brand_names["items"]
    ]


@router.get(
    "/categories",
    responses={
        200: {
            "model": List[CategoryResponse],
            "description": "products list with full count",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong",
        },
    },
    summary="Categories list",
)
async def get_categories_endpoint(
    request: Request,
    response: Response,
    limit: Optional[int] = Query(10, description="amount of returned categories"),
    offset: Optional[int] = Query(0, description="amount of scrolled categories"),
) -> List[CategoryResponse]:
    categories = await get_categories(
        limit=limit,
        offset=offset,
    )
    return [
        CategoryResponse.parse_obj(cat)
        for cat in categories["items"]
    ]


@router.get(
    "/products",
    responses={
        200: {
            "model": ProductListResponse,
            "description": "products list with full count",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong",

        },
    },
    summary="Product list",
)
async def get_products_endpoint(
    request: Request,
    response: Response,
    limit: Optional[int] = Query(10, description="amount of returned products"),
    offset: Optional[int] = Query(0, description="amount of scrolled products"),
    brand_name: Optional[int] = Query(None, description="pk of products brand"),
    category: Optional[int] = Query(None, description="pk of product category"),
    sex: Optional[int] = Query(None, description="product sex"),
    age: Optional[int] = Query(None, description="product age"),
    name: Optional[str] = Query(None, description="product name or name part"),
    article_number: Optional[str] = Query(None, description="product article numaber or part of it"),
) -> ProductListResponse:

    res = await get_products(
        limit=limit,
        offset=offset,
        brand_name=brand_name,
        category=category,
        sex=sex,
        age=age,
        name=name,
        article_number=article_number,
    )

    res["products"] = res.pop("items", [])

    return ProductListResponse.parse_obj(res)


@router.get(
    "/product/items",
    responses={
        200: {
            "model": ProductItemsListResponse,
            "description": "products list with full count",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong",
        },
    },
    summary="Product items list",
)
async def get_product_items_endpoint(
    request: Request,
    response: Response,
    product_pk: int = Query(None, description="pk of product"),
    limit: Optional[int] = Query(10, description="amount of returned products"),
    offset: Optional[int] = Query(0, description="amount of scrolled products"),
    size: Optional[str] = Query(None, description="product items size"),
    serial_number: Optional[str] = Query(None, description="product serial_number"),
    sold: Optional[bool] = Query(False, description="is product sold"),
) -> ProductItemsListResponse:
    if not product_pk:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Error40xResponse.parse_obj(
            {"reason": "no product pk"}
        )
    product = await get_product(product_pk)
    items = await get_product_items(
        product=product_pk,
        limit=limit,
        offset=offset,
        size=size,
        serial_number=serial_number,
        sold=sold,
    )

    return ProductItemsListResponse.parse_obj(
        {
            "product": product,
            "count": items["count"],
            "items": items["items"],
        }
    )


@router.post(
    "/category/manage",
    responses={
        200: {
            "model": CategoryResponse,
            "description": "changed or created category",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong"
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong authentication"
        },
    },
    summary="create or change category",
)
@login_required
async def category_manage_endpoint(
    request: Request,
    response: Response,
    categories: CategoryRequest,
    authorization: Optional[str] = Header(None),
    status_code: Optional[Any] = Header(status.HTTP_200_OK, description="internal usage, not used by client"),
) -> CategoryResponse:
    category = await manage_category(**categories.dict())
    return CategoryResponse.parse_obj(category)


@router.post(
    "/brand/manage",
    responses={
        200: {
            "model": BrandNameResponse,
            "description": "changed or created brand",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong"
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong authentication"
        },
    },
    summary="create or change category",
)
@login_required
async def brand_manage_endpoint(
    request: Request,
    response: Response,
    pk: Optional[int] = Form(None, description="brand pk"),
    name: Optional[str] = Form(None, description="brand name"),
    logo: Optional[UploadFile] = File(None, description="brand logo"),
    authorization: Optional[str] = Header(None),
    status_code: Optional[Any] = Header(status.HTTP_200_OK, description="internal usage, not used by client"),
) -> BrandNameResponse:
    brand_name = await manage_brand_name(
        id=pk,
        name=name,
        logo=logo.file.read() if logo else None,
        ext=logo.filename.split(".")[-1] if logo and len(logo.filename.split(".")) > 1 else None,
    )
    return brand_name


@router.post(
    "/product/manage",
    responses={
        200: {
            "model": ProductResponse,
            "description": "changed or created product",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong"
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong authentication"
        },
    },
    summary="create or change category",
)
@login_required
async def product_manage_endpoint(
    request: Request,
    response: Response,
    product: str = Form(..., description=json.dumps(form_model_doc_generation(ProductRequest), indent=2).replace("\n", "\n\n")),
    authorization: Optional[str] = Header(None),
    status_code: Optional[Any] = Header(status.HTTP_200_OK, description="internal usage, not used by client"),
) -> ProductResponse:
    product = ProductRequest.parse_raw(product)
    form_data = await request.form()
    product_dict = product.dict()
    product_dict["gallery"] = []
    product_dict["exist_gallery"] = []
    for img in product_dict.pop("imgs", []):
        if img["id"]:
            product_dict["exist_gallery"].append(img["int"])
        elif img["key"]:
            product_dict["gallery"].append(
                {
                    "ext": form_data.get(img["key"]).filename.split(".")[-1] if len(form_data.get(img["key"]).filename.split(".")) > 1 else None,
                    "bytes": form_data.get(img["key"]).file.read(),
                }
            )
    res = await manage_product(**product_dict)
    return ProductResponse.parse_obj(res)


@router.post(
    "/product/items/manage",
    responses={
        200: {
            "model": List[ProductItemResponse],
            "description": "changed or created product items",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong"
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong authentication"
        },
    },
    summary="create or change category",
)
@login_required
async def product_items_manage_endpoint(
    request: Request,
    response: Response,
    items_list: ProductItemsListRequest,
    authorization: Optional[str] = Header(None),
    status_code: Optional[Any] = Header(status.HTTP_200_OK, description="internal usage, not used by client"),
) -> List[ProductItemResponse]:
    product_items = await create_product_items(**items_list.dict())
    return [
        ProductItemResponse.parse_obj(i)
        for i in product_items
    ]


@router.delete(
    "/product/item/remove",
    responses={
        200: {
            "model": Error40xResponse,
            "description": "delete success",
        },
        400: {
            "model": Error40xResponse,
            "description": "something wrong"
        },
        401: {
            "model": Error40xResponse,
            "description": "wrong authentication"
        },
    },
    summary="delete product item",
)
async def product_item_delete_endpoint(
    request: Request,
    response: Response,
    pk: int = Query(..., description="product item pk"),
    authorization: Optional[str] = Header(None),
    status_code: Optional[Any] = Header(status.HTTP_200_OK, description="internal usage, not used by client"),
):
    await delete_product_item(item_pk=pk)
    return Error40xResponse.parse_obj({"reason": "delete success"})
