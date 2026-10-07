from sqlalchemy import Column, BigInteger, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())