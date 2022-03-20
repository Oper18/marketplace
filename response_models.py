# coding: utf-8

from typing import Optional

from pydantic import BaseModel, Field


class Error40xResponse(BaseModel):
    reason: Optional[str] = Field(
        description="information about error or response status"
    )
