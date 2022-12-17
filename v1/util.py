from typing import List

from tortoise.expressions import Q, F
from tortoise.functions import Count
from tortoise.queryset import QuerySet

from models.models import ProductItems


async def product_items_response_arr(product_items: QuerySet) -> List[dict]:
    lost_product_items = dict()
    sold_product_items = list()
    
    for item in product_items:
        product = await item.product
        categories = await product.category.all()
        if not lost_product_items.get(product.id):
            lost_product_items[product.id] = await ProductItems.filter(
                product=product,
                sold=False,
            ).count()

        sold_product_items.append(
            {
                "id": item.id,
                "product_id": product.id,
                "product_name": product.name,
                "price": float(product.price) - float(product.price) * float(product.discount) / 100,
                "article_number": product.article_number,
                "size": product.size,
                "buyer": item.buyer,
                "salesman": item.salesman,
                "lost_items": lost_product_items[product.id],
                "rent_time_space": "{} - {}".format(
                    item.rent_time_start.isoformat(),
                    item.rent_time_stop.isoformat(),
                )
                if item.rent_time_start and item.rent_time_stop
                else "",
                "sold_date": item.updated_at.date().isoformat(),
                "payed_amount": item.payed_amount if item.payed_amount is not None else product.price,
                "payment_type": item.payment_type,
                "categories": [c.name for c in categories],
            }
        )

    return sold_product_items


async def export_stat_xls(date_start, date_stop) -> List[dict]:
    product_items = await ProductItems.filter(
        updated_at__gte=date_start,
        updated_at__lt=date_stop,
        sold=True,
    ).select_related("product")


    return await product_items_response_arr(product_items=product_items)


async def get_debtors_ids() -> List[int]:
    return [
        pi.buyer
        for pi in await ProductItems.filter(product__price__gt=F("payed_amount"))
        if pi.buyer
    ]


async def get_buyer_depts(buyer: int) -> List[dict]:
    product_items = await ProductItems.filter(
        buyer=buyer,
        product__price__gt=F("payed_amount"),
        sold=True,
    ).select_related("product")

    return await product_items_response_arr(product_items=product_items)

