from typing import Any

from pydantic import BaseModel

from core.schemas.mixins import IdMixIn, ReadFromAttributesMixIn


class BannerDataBaseModel(BaseModel):
    feature_id: int
    content: dict[str, Any]
    is_active: bool


class BannerCreate(BannerDataBaseModel):
    tag_ids: list[int]


class BannerPatchWithoutTagIds(ReadFromAttributesMixIn):
    feature_id: int | None = None
    content: dict[str, Any] | None = None
    is_active: bool | None = None


class BannerPatch(BannerPatchWithoutTagIds):
    tag_ids: list[int] | None = None


class BannerReturn(IdMixIn):
    pass


class BannerHistoryCreate(ReadFromAttributesMixIn):
    banner_id: int
    feature_id: int
    content: dict[str, Any]
    is_active: bool
    version: int
