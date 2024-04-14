from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class BannerTag(Base):
    __tablename__ = "banners_tags"

    id = Column(Integer, primary_key=True, index=True)
    banner_id = Column(Integer, ForeignKey("banners.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    tag = relationship("Tag",
                       back_populates="banner_tag",
                       lazy="selectin")

    banner = relationship("Banner",
                          back_populates="banner_tag",
                          lazy="selectin")
