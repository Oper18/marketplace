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
    delete_product,
    edit_product_item,
)

from v1.util import (
    export_stat_xls,
    get_debtors_ids,
    get_buyer_depts,
)

from statistic.handler import SailsStat

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
            size=request.size,
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
            sold=request.sold,
            rent_date_start=request.rent_date_start,
            rent_date_stop=request.rent_date_stop,
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
            product_id=request.product_id,
            article_number=request.article_number,
            buyer=request.buyer,
            rent_time_start=request.rent_time_start,
            rent_time_stop=request.rent_time_stop,
            salesman=request.salesman,
            payed_amount=request.payed_amount,
            payment_type=request.payment_type,
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


class RemoveProductServer(market_pb2_grpc.RemoveProductServicer):
    async def RemoveProduct(
            self,
            request: market_pb2.ProductRemoveRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductRemoveResponse:
        res = await delete_product(product_pk=request.product_pk)
        return market_pb2.ProductRemoveResponse(message=True)


class ProductItemsStatServer(
        market_pb2_grpc.RemoveProductServicer
):
    async def ProductItemsStat(
            self,
            request: market_pb2.ProductItemsStatRequest,
            context: grpc.aio.ServicerContext
    ) -> market_pb2.ProductItemsStatResponse:
        stat = await export_stat_xls(
            date_start=request.date_start,
            date_stop=request.date_stop,
        )
        return market_pb2.ProductItemsStatResponse(statistic=stat)


class SailsStatServer(market_pb2_grpc.SailsStatServicer):
    async def SailsStat(
        self,
        request: market_pb2.SailsStatRequest,
        context: grpc.aio.ServicerContext,
    ) -> market_pb2.SailsStatResponse:
        stat_obj = SailsStat(
            date_start=request.date_start,
            date_stop=request.date_stop,
        )
        stat = await stat_obj.get_sails_stat()
        return market_pb2.SailsStatResponse(statistic=stat)


class DetailSailsStatServer(market_pb2_grpc.SailsStatServicer):
    async def DetailSailsStat(
        self,
        request: market_pb2.SailsStatRequest,
        context: grpc.aio.ServicerContext,
    ) -> market_pb2.DetailSailsStatResponse:
        stat_obj = DetailSailsStat(
            date_start=request.date_start,
            date_stop=request.date_stop,
            detail=True,
        )
        stat = await stat_obj.get_sails_stat()

        return market_pb2.DetailSailsStatResponse(statistic=stat)


class DebtorsServer(market_pb2_grpc.DebtorsServicer):
    async def Debtors(
        self,
        request: market_pb2.DebtorsRequest,
        context: grpc.aio.ServicerContext,
    ) -> market_pb2.DebtorsResponse:
        debtors = await get_debtors_ids()
        return market_pb2.DebtorsResponse(debtors=debtors)


class BuyerDeptsServer(market_pb2_grpc.BuyerDeptsServicer):
    async def BuyerDepts(
        self,
        request: market_pb2.BuyerDeptsRequest,
        context: grpc.aio.ServicerContext,
    ) -> market_pb2.ProductItemsStatResponse:
        debts = await get_buyer_depts(buyer=request.buyer)
        return market_pb2.ProductItemsStatResponse(statistic=debts)


class ProductItemEditServer(market_pb2_grpc.ProductItemEditServicer):
    async def ProductItemEdit(
        self,
        request: market_pb2.ProductItemRequest,
        context: grpc.aio.ServicerContext,
    ) -> market_pb2.ProductItemRemoveResponse:
        product_item = await edit_product_item(
            product_item_pk=request.product_item_pk,
            payed_amount=request.payed_amount,
        )
        return market_pb2.ProductItemResponse(**product_item)


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
    market_pb2_grpc.add_RemoveProductServicer_to_server(
        RemoveProductServer(), server
    )
    market_pb2_grpc.add_ProductItemsStatServicer_to_server(
        ProductItemsStatServer(), server
    )
    market_pb2_grpc.add_SailsStatServicer_to_server(
        SailsStatServer(), server
    )
    market_pb2_grpc.add_DetailSailsStatServicer_to_server(
        DetailSailsStatServer(), server
    )
    market_pb2_grpc.add_DebtorsServicer_to_server(
        DebtorsServer(), server
    )
    market_pb2_grpc.add_BuyerDeptsServicer_to_server(
        BuyerDeptsServer(), server
    )
    market_pb2_grpc.add_ProductItemEditServicer_to_server(
        ProductItemEditServer(), server
    )

    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print("Starting server on ", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
