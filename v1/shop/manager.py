import os
import uuid
import dateutil.parser

from typing import List, Dict, Optional

from aiofile import async_open

from tortoise.expressions import Q

from models.models import (
    Category,
    BrandName,
    Product,
    ProductGallery,
    ProductItems,
)

from models.extensions import ExtendedModel, Sex, Age

from settings import IMG_PATH, IMG_DIR

from base_obj import segmented_path


async def get_categories(
    limit: int = 10,
    offset: int = 0,
):
    count = await Category.all().count()
    return {
        "count": count,
        "items": [
            await c.as_dict()
            for c in
            (await Category.all().limit(limit).offset(offset).order_by("-updated_at"))
        ],
    }


async def get_brands(
    limit: int = 10,
    offset: int = 0,
):
    count = await BrandName.all().count()
    res = []
    for bn in (await BrandName.all().limit(limit).offset(offset).order_by("-updated_at")):
        bn_dict = await bn.as_dict()
        bn_dict["logo"] = os.path.join(IMG_PATH, bn_dict["logo"]) if bn_dict.get("logo") else None
        res.append(bn_dict)

    return {"count": count, "items": res}


async def _serialize_product(product):
    product_dict = await product.as_dict()
    p_category = await product.category.all()
    product_dict["category"] = [await c.as_dict() for c in  p_category]
    p_brand = await product.brand_name.first()
    product_dict["brand_name"] = await p_brand.as_dict()
    product_dict["brand_name"]["logo"] = os.path.join(IMG_PATH, product_dict["brand_name"]["logo"]) if product_dict["brand_name"].get("logo") else None
    product_dict["gallery"] = []
    for img in (await product.imgs.all()):
        product_dict["gallery"].append(os.path.join(IMG_PATH, img.img))

    return product_dict


async def get_product(product_pk: int):
    product = await Product.\
        get(id=product_pk)

    product_dict = await _serialize_product(product)

    return product_dict


async def get_products(
    limit: int = 10,
    offset: int = 0,
    brand_name: int = None,
    category: int = None,
    sex: int = None,
    age: int = None,
    name: str = None,
    article_number: str = None,
    rent: bool = None,
    service: bool = None,
):
    products = Product

    if brand_name:
        products = products.filter(brand_name__id=brand_name)
    if category:
        products = products.filter(category__id=category)
    if sex:
        products = products.filter(sex=sex)
    if age:
        products = products.filter(age=age)
    if name:
        products = products.filter(name__icontains=name)
    if article_number:
        products = products.filter(article_number=article_number)
    if rent is not None:
        products = products.filter(rent=rent)
    if service is not None:
        products = products.filter(service=service)

    count = await products.all().count()

    products = await products.\
        all().\
        distinct().\
        limit(limit).\
        offset(offset).\
        order_by("-updated_at")

    res = []
    for p in products:
        p_dict = await p.as_dict()
        p_category = await p.category.all()
        p_dict["category"] = [await c.as_dict() for c in  p_category]
        p_brand = await p.brand_name.first()
        p_dict["brand_name"] = await p_brand.as_dict()
        p_dict["brand_name"]["logo"] = os.path.join(IMG_PATH, p_dict["brand_name"]["logo"]) if p_dict["brand_name"].get("logo") else None
        p_dict["gallery"] = []
        for img in (await p.imgs.all()):
            p_dict["gallery"].append(os.path.join(IMG_PATH, img.img))
        res.append(p_dict)

    return {"count": count, "items": res}


async def get_product_items(
    product: int,
    limit: int = 10,
    offset: int = 0,
    sold: bool = False,
    rent_date_start: str = None,
    rent_date_stop: str = None,
):
    count = await ProductItems.filter(product__pk=product, sold=False).all().count()
    items = ProductItems.filter(product__pk=product, sold=sold)
    if rent_date_start and not rent_date_stop:
        items = items.filter(
            rent_time_start__gte=rent_date_start,
            rent_time_start__lte=rent_date_stop,
        )
    elif rent_date_stop and not rent_date_start:
        items = items.filter(
            rent_time_stop__gte=rent_date_start,
            rent_time_stop__lte=rent_date_stop,
        )
    elif rent_date_start and rent_date_stop:
        items = items.filter(
            Q(
                Q(rent_time_start__gte=rent_date_start) &
                Q(rent_time_start__lte=rent_date_stop)
            ) |
            Q(
                Q(rent_time_stop__gte=rent_date_start) &
                Q(rent_time_stop__lte=rent_date_stop)
            )
        )

    items = await items.all().limit(limit).offset(offset).order_by('rent_time_start')

    return {
        "count": count,
        "items": [await i.as_dict() for i in items]
    }


async def manage_category(id: int = None, name: str = None):
    if not id and not name:
        return None
    if not id and name:
        category = await Category.create(name=name)
    elif id and name:
        await Category.get(id=id).update(name=name)
        category = await Category.get(id=id)
    return await category.as_dict()


async def manage_brand_name(
    id: int = None,
    name: str = None,
    logo: bytes = None,
    ext: str = None,
):
    if not name and not logo:
        return None
    logo_name = None
    if logo:
        logo_name = uuid.uuid4().hex
        if ext:
            logo_name +=  "." + ext
        async with async_open(segmented_path(IMG_DIR, logo_name), 'wb') as f:
            await f.write(logo)

    update_fields = {}
    if name:
        update_fields["name"] = name
    if logo_name:
        update_fields["logo"] = logo_name

    if id:
        await BrandName.get(id=id).update(**update_fields)
        brand = await BrandName.get(id=id)
    else:
        brand = await BrandName.create(**update_fields)

    brand_dict = await brand.as_dict()
    brand_dict["logo"] = os.path.join(IMG_PATH, brand_dict["logo"]) if brand_dict.get("logo") else None

    return brand_dict


async def manage_product(
    id: int = None,
    name: str = None,
    description: str = None,
    brand_name: int = None,
    category: List[int] = None,
    color: str = None,
    sex: int = None,
    age: int = None,
    article_number: str = None,
    price: float = None,
    currency: str = None,
    discount: float = None,
    rent: bool = False,
    service: bool = False,
    gallery: List[dict] = [],
    exist_gallery: List[int] = [],
    size: Optional[str] = None,
) -> dict:
    if not id and not brand_name:
        return {}

    update_fields = {}
    if brand_name:
        update_fields["brand_name"] = await BrandName.filter(pk=brand_name).first()
    if category:
        categories = await Category.filter(pk__in=category).all()
    if name:
        update_fields["name"] = name
    if description:
        update_fields["description"] = description
    if color:
        update_fields["color"] = color
    if sex:
        update_fields["sex"] = sex
    if age:
        update_fields["age"] = age
    if article_number:
        update_fields["article_number"] = article_number
    if price:
        update_fields["price"] = price
    if currency:
        update_fields["currency"] = currency
    if discount:
        update_fields["discount"] = discount
    if rent is not None:
        update_fields["rent"] = rent
    if service is not None:
        update_fields["service"] = service
    if size is not None:
        update_fields["size"] = size

    if id:
        await Product.get(id=id).update(**update_fields)
        product = await Product.get(id=id)
    else:
        if not update_fields.get("sex"):
            update_fields["sex"] = Sex.unisex
        if not update_fields.get("age"):
            update_fields["age"] = Age.common
        product = await Product.create(**update_fields)
    await product.category.clear()
    await product.category.add(*categories)
    await product.save()

    await ProductGallery.filter(~Q(img__in=exist_gallery)).delete()

    product_gallery = []
    for img in gallery:
        img_name = uuid.uuid4().hex
        if img["ext"]:
            img_name += "." + img["ext"]
        async with async_open(segmented_path(IMG_DIR, img_name), 'wb') as f:
            await f.write(img["bytes"])
        await ProductGallery.create(
            product=product,
            img=img_name,
        )

    product_dict = await _serialize_product(product)

    return product_dict


async def create_product_items(
    product: int,
    items: List[dict] = [],
):
    product = await Product.get(id=product)
    res_items = []
    for it in items:
        it["product"] = product
        if "id" in it.keys() and not it.get("id"):
            it.pop("id")
        it_obj = await ProductItems.create(**it)
        res_items.append(it_obj)

    return [
        await i.as_dict()
        for i in res_items
    ]


async def buy_rent_product_item(
    item_pk: Optional[int] = None,
    product_id: Optional[int] = None,
    article_number: Optional[str] = None,
    buyer: int = None,
    rent_time_start: str = None,
    rent_time_stop: str = None,
    salesman: int = None,
    payed_amount: float = None,
    payment_type: int = None,
):
    if not product_id and not item_pk and not article_number:
        return False
    
    if item_pk:
        product_item = await ProductItems.filter(id=item_pk, sold=False).first()
    elif product_id:
        product_item = await ProductItems.filter(product__id=product_id, sold=False).first()
    elif article_number:
        product_item = await ProductItems.filter(product__article_number=article_number, sold=False).first()

    if not product_item:
        return False
    product_item.sold = True
    if buyer:
        product_item.buyer = buyer
    if salesman:
        product_item.salesman = salesman
    if rent_time_start and rent_time_stop:
        product_item.rent_time_start = dateutil.parser.parse(rent_time_start)
        product_item.rent_time_stop = dateutil.parser.parse(rent_time_stop)

    if payed_amount is None:
        product = await product_item.product
        payed_amount = product.price

    product_item.payed_amount = payed_amount
    product_item.payment_type = payment_type

    await product_item.save()
    return True


async def delete_product_item(item_pk: int):
    await ProductItems.get(id=item_pk).delete()


async def delete_product(product_pk: int):
    await Product.get(id=product_pk).delete()


async def edit_product_item(product_item_pk: int, payed_amount: float):
    pi = await ProductItems.get(id=product_item_pk)
    pi.payed_amount = payed_amount
    await pi.save()
    return await pi.as_dict()
