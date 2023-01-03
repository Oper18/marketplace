from typing import Union, Optional, Tuple

from dateutil.parser import parse
from datetime import datetime, date, timedelta

from tortoise.queryset import QuerySet

from base_obj import BaseArrGenerator

from models.models import ProductItems, Category


class SailsStat(object):
    def __init__(
        self,
        date_start: Union[str, datetime, date],
        date_stop: Union[str, datetime, date],
        salesman: Optional[int] = None,
    ):
        if isinstance(date_start, str):
            date_start = parse(date_start)
        if isinstance(date_stop, str):
            date_stop = parse(date_stop)

        self.date_start = date_start
        self.date_stop = date_stop
        self.salesman = salesman

        self.query = ProductItems.filter(
            sold=True,
            updated_at__gte=self.date_start,
            updated_at__lte=self.date_stop,
        )
        if self.salesman:
            self.query = product_items.filter(salesman=self.salesman)

        self._queryset = list()

    @property
    async def queryset(self):
        if not self._queryset:
            self._queryset = await self.query.\
                all().\
                order_by("-updated_at").\
                select_related("product").\
                distinct()
        return self._queryset

    def set_category_to_data(self, data: dict, category: str) -> dict:
        data["category"] = category
        return data

    async def serialize_data(
        self, product_item: ProductItems
    ) -> Tuple[dict, QuerySet]:
        product = await product_item.product
        categories = await product.category.all()
        data = await product_item.as_dict()
        data.pop("salesman", None)
        data["product"] = product.name
        data["price"] = (
            float(product.price) - float(product.price) * float(product.discount) / 100 
        ) / len(categories)
        return data, categories

    def _set_list_of_days(self):
        current_date = self.date_start
        res = list()
        
        while current_date <= self.date_stop:
            res.append(
                {
                    "date": current_date.date().isoformat(),
                    "data": list(),
                }
            )
            current_date += timedelta(days=1)

        return res

    async def _get_detail_stat(
        self, res: dict, pit: ProductItems, pit_dict: dict, category: Category
    ):
        category_iter = [
            i
            for i, d in enumerate(res) if d["category"] == category.id
        ]
        if not category_iter:
            res.append({"category": category.id, "data": list()})
            category_iter = -1
        else:
            category_iter = category_iter[-1]

        res[category_iter]["data"].append(
            self.set_category_to_data(pit_dict, category.name)
        )

        return res

    async def _get_common_stat(
        self, res: dict, pit: ProductItems, pit_dict: dict, category: Category
    ):
        category_iter = [
            i
            for i, d in enumerate(res) if d["category_id"] == category.id
        ]
        if not category_iter:
            res.append(
                {"category": category.name, "category_id": category.id, "amount": 0.0}
            )
            category_iter = -1
        else:
            category_iter = category_iter[-1]
        
        res[category_iter]["amount"] += pit_dict["price"]

        return res
    
    async def get_sails_stat(self, detail: Optional[bool] = False):
        res = self._set_list_of_days()
        product_items = await self.queryset
        async for pit in BaseArrGenerator(product_items):
            date_iter = [
                i
                for i, d in enumerate(res)
                if d["date"] == pit.updated_at.date().isoformat()
            ][0]
            data, categories = await self.serialize_data(pit)

            salesman_iter = [
                i
                for i, d in enumerate(res[date_iter]["data"])
                if d["salesman"] == pit.salesman
            ]
            if not salesman_iter:
                res[date_iter]["data"].append(
                    {
                        "salesman": pit.salesman,
                        "data": list(),
                    }
                )
                salesman_iter = -1
            else:
                salesman_iter = salesman_iter[0]

            async for c in BaseArrGenerator(categories):
                if detail:
                    res[date_iter]["data"][salesman_iter]["data"] = await self._get_detail_stat(
                        res=res[date_iter]["data"][salesman_iter]["data"],
                        pit=pit,
                        pit_dict=data,
                        category=c,
                    )
                else:
                    res[date_iter]["data"][salesman_iter]["data"] = await self._get_common_stat(
                        res=res[date_iter]["data"][salesman_iter]["data"],
                        pit=pit,
                        pit_dict=data,
                        category=c,
                    )
            last_date_iter = date_iter

        return res

