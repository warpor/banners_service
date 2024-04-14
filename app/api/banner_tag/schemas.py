from pydantic import BaseModel


class BannerTagCreate(BaseModel):
    banner_id: int
    tag_id: int
