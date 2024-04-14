from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from database import Base


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey("features.id"))
    content = Column(JSONB)
    is_active = Column(Boolean)

    banner_tag = relationship("BannerTag",
                              back_populates="banner",
                              cascade="all, delete-orphan",
                              lazy="selectin")
