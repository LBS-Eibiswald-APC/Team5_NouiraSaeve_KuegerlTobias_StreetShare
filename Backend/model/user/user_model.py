from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    hashed_pw = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(255), nullable=True)
    street = Column(String(255), nullable=True)
    house_nr = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    zip = Column(Integer, nullable=True)
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True
    )
    role = relationship("Role")
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

