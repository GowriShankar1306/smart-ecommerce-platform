from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String(20), nullable=False, default="pending")
    order_status = Column(String(20), nullable=False, default="pending")
    timestamp = Column(DateTime, nullable=False, server_default=func.now())

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )