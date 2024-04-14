from pydantic import BaseModel


class IdMixIn(BaseModel):
    id: int


class ReadFromAttributesMixIn(BaseModel):
    class Config:
        from_attributes = True
