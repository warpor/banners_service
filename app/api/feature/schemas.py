from pydantic import BaseModel


class FeatureCreate(BaseModel):
    name: str
