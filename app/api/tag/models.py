from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True)

    banner_tag = relationship("BannerTag",
                               back_populates="tag",
                               lazy="selectin")
