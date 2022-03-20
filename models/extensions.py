# coding: utf-8

import datetime
import uuid
import enum


class ExtendedModel:

    _exclude = ()

    async def as_dict(self):
        res = {}
        for c in self.__dict__:
            if c[0] == "_" or c in self._exclude:
                continue
            if isinstance(getattr(self, c), datetime.datetime):
                res[c] = getattr(self, c).isoformat()
            else:
                res[c] = getattr(self, c)
        return res


class AnonymousUser(ExtendedModel):
    id = None
    email = "anonymous"

    @property
    def is_anonymous(self):
        return True


class Sex(enum.IntEnum):
    male = 1
    female = 2
    unisex = 3


class Age(enum.IntEnum):
    adult = 1
    child = 2
    common = 3
