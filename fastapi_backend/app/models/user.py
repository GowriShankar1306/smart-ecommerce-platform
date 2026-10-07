from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(254), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default="customer")

    first_name = Column(String(150), nullable=False, default="")
    last_name = Column(String(150), nullable=False, default="")

    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    date_joined = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )