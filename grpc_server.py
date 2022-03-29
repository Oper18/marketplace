# coding: utf-8

import asyncio
import json

import grpc
import market_pb2
import market_pb2_grpc

from tortoise import Tortoise

from v1.shop.manager import (
    get_categories,
    get_brands,
    get_product,
    get_products,
    get_product_items,
    manage_category,
    manage_brand_name,
    manage_product,
    create_product_items,
    buy_rent_product_item,
    delete_product_item,
)

from settings import DATABASE


class GetCategoriesServer(market_pb2_grpc.GetCategoriesServicer):
    async def GetCats(
            self,
            request: market_pb2.CategoriesRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.CategoriesResponse:
        res = await get_categories(
            limit=request.limit,
            offset=request.offset,
        )
        return market_pb2.CategoriesResponse(
            count=res["count"],
            items=res["items"],
        )


class ManageCategoryServer(market_pb2_grpc.ManageCategoryServicer):
    async def ManageCats(
            self,
            request: market_pb2.CategoryManageRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.CategoryItemResponse:
        res = await manage_category(
            id=request.id, name=request.name
        )
        return market_pb2.CategoryItemResponse(
            id=res["id"],
            name=res["name"],
            created_at=res["created_at"],
            updated_at=res["updated_at"],
        )


class GetBrandsServer(market_pb2_grpc.GetBrandsNamesServicer):
    async def GetBrands(
            self,
            request: market_pb2.BrandRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.BrandResponse:
        res = await get_brands(
            limit=request.limit,
            offset=request.offset,
        )
        return market_pb2.BrandResponse(
            count=res["count"],
            items=res["items"],
        )


class ManageBrandServer(market_pb2_grpc.ManageBrandsNamesServicer):
    async def ManageBrands(
            self,
            request: market_pb2.BrandManageRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.BrandItemResponse:
        res = await manage_brand_name(
            id=request.id,
            name=request.name,
            logo=request.logo,
            ext=request.ext,
        )
        return market_pb2.BrandItemResponse(
            id=res["id"],
            name=res["name"],
            logo=res["logo"],
            created_at=res["created_at"],
            updated_at=res["updated_at"],
        )


class GetProductsServer(market_pb2_grpc.GetProductsServicer):
    async def GetProds(
            self,
            request: market_pb2.ProductRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductListResponse:
        if request.id:
            res = await get_product(product_pk=request.id)
            res = {
                "count": 1,
                "items": [res]
            }
        else:
            if request.rent == -1:
                rent = None
            else:
                rent = bool(request.rent)
            if request.service == -1:
                service = None
            else:
                service = bool(request.service)
            res = await get_products(
                limit=request.limit,
                offset=request.offset,
                brand_name=request.brand_name,
                category=request.category,
                sex=request.sex,
                age=request.age,
                name=request.name,
                article_number=request.article_number,
                rent=rent,
                service=service,
            )
        return market_pb2.ProductListResponse(
            count=res["count"],
            items=res["items"],
        )


class ManageProductsServer(market_pb2_grpc.GetProductsServicer):
    async def ManageProds(
            self,
            request: market_pb2.ProductManageRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductResponse:
        res = await manage_product(
            id=request.id,
            name=request.name,
            description=request.description,
            brand_name=request.brand_name,
            category=request.category,
            color=request.color,
            sex=request.sex,
            age=request.age,
            article_number=request.article_number,
            price=request.price,
            currency=request.currency,
            discount=request.discount,
            rent=request.rent,
            service=request.service,
            gallery=[
                {"ext": g.ext, "bytes": g.bytes}
                for g in request.pgr
            ],
            exist_gallery=request.eg,
        )
        return market_pb2.ProductResponse(**res)


class GetProductItemsServer(market_pb2_grpc.GetProductsItemsServicer):
    async def GetProdItems(
            self,
            request: market_pb2.ProductItemsRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductItemsListResponse:
        res = await get_product_items(
            product=request.product,
            limit=request.limit,
            offset=request.offset,
            size=request.size,
            serial_number=request.serial_number,
            sold=request.sold,
        )
        return market_pb2.ProductItemsListResponse(
            count=res["count"],
            items=res["items"],
        )


class CreateProductItemsServer(market_pb2_grpc.CreateProductsItemsServicer):
    async def CreateProdItems(
            self,
            request: market_pb2.ProductItemCreateRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductItemsCreateResponse:
        res = await create_product_items(
            product=request.product,
            items=[
                {
                    "id": p.id if p.id else None,
                    "size": p.size,
                    "serial_number": p.serial_number,
                    "sold": p.sold,
                    "buyer": p.buyer,
                    "rent_time_start": p.rent_time_start if p.rent_time_start else None,
                    "rent_time_stop": p.rent_time_stop if p.rent_time_stop else None,
                }
                for p in request.items
            ]
        )
        return market_pb2.ProductItemsCreateResponse(arr=res)


class BuyProductItemServer(market_pb2_grpc.BuyProductItemServicer):
    async def BuyProdItem(
            self,
            request: market_pb2.ProductItemBuyRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductItemBuyResponse:
        res = await buy_rent_product_item(
            item_pk=request.item_pk,
            buyer=request.buyer,
            rent_time_start=request.rent_time_start,
            rent_time_stop=request.rent_time_stop,
            salesman=request.salesman,
        )
        return market_pb2.ProductItemBuyResponse(message=res)


class RemoveProductItemServer(market_pb2_grpc.RemoveProductItemServicer):
    async def RemoveProdItem(
            self,
            request: market_pb2.ProductItemRemoveRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductItemRemoveResponse:
        res = await delete_product_item(item_pk=request.item_pk)
        return market_pb2.ProductItemRemoveResponse(message=True)


async def serve() -> None:
    await Tortoise.init(
        db_url="postgres://{}:{}@{}:5432/{}".format(
            DATABASE["user"],
            DATABASE["password"],
            DATABASE["address"],
            DATABASE["name"],
        ),
        modules={"models": ["models.models", "aerich.models"]},
    )
    server = grpc.aio.server()

    market_pb2_grpc.add_GetCategoriesServicer_to_server(
        GetCategoriesServer(), server
    )
    market_pb2_grpc.add_ManageCategoryServicer_to_server(
        ManageCategoryServer(), server
    )
    market_pb2_grpc.add_GetBrandsNamesServicer_to_server(
        GetBrandsServer(), server
    )
    market_pb2_grpc.add_ManageBrandsNamesServicer_to_server(
        ManageBrandServer(), server
    )
    market_pb2_grpc.add_GetProductsServicer_to_server(
        GetProductsServer(), server
    )
    market_pb2_grpc.add_ManageProductsServicer_to_server(
        ManageProductsServer(), server
    )
    market_pb2_grpc.add_GetProductsItemsServicer_to_server(
        GetProductItemsServer(), server
    )
    market_pb2_grpc.add_CreateProductsItemsServicer_to_server(
        CreateProductItemsServer(), server
    )
    market_pb2_grpc.add_BuyProductItemServicer_to_server(
        BuyProductItemServer(), server
    )
    market_pb2_grpc.add_RemoveProductItemServicer_to_server(
        RemoveProductItemServer(), server
    )

    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print("Starting server on ", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
