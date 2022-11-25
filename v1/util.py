from tortoise.expressions import Q
from tortoise.functions import Count

from models.models import ProductItems


async def export_stat_xls(date_start, date_stop):
    product_items = await ProductItems.filter(
        updated_at__gte=date_start,
        updated_at__lte=date_stop,
        sold=True,
    ).select_related("product")

    lost_product_items = dict()
    sold_product_items = list()
    
    for item in product_items:
        product = await item.product
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
                "price": product.price,
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
            }
        )

    return sold_product_items

