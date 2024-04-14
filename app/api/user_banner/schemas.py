from typing import Any

from pydantic import BaseModel


class UserBannerReturn(BaseModel):
    content: dict[str, Any]


class UserBannerReturnWithActive(UserBannerReturn):
    is_active: bool
