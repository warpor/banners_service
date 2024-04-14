from sqlalchemy import Column, String, Integer

from database import Base


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True)