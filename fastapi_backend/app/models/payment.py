from sqlalchemy import Column, Integer, Numeric, String, ForeignKey

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_id = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="pending")