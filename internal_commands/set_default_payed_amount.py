import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from tortoise import Tortoise

from models.models import Product, ProductItems

from settings import DATABASE


async def main():
    await Tortoise.init(
        db_url="postgres://{}:{}@{}:5432/{}".format(
            DATABASE["user"],
            DATABASE["password"],
            DATABASE["address"],
            DATABASE["name"],
        ),
        modules={"models": ["models.models", "aerich.models"]},
    )

    product_items = await ProductItems.filter(payed_amount__isnull=True)
    for pit in product_items:
        product = await pit.product
        pit.payed_amount = product.price
        await pit.save()


if __name__ == "__main__":
    asyncio.run(main())

