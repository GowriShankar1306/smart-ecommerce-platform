from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    image = Column(String(255), nullable=True)