from sqlalchemy import Column, Integer, String, DECIMAL, Enum, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class OrderStatusEnum(enum.Enum):
    RESERVED = "RESERVED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    sneaker_id = Column(Integer, nullable=False, index=True)
    size = Column(DECIMAL(3, 1), nullable=False)
    status = Column(
        Enum(OrderStatusEnum),
        nullable=False,
        default=OrderStatusEnum.CONFIRMED,
        index=True
    )
    reserve_token = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now(), index=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )
    
    # Composite unique constraint
    __table_args__ = (
        Index('uk_user_product_size', 'user_id', 'sneaker_id', 'size', unique=True),
    )
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, sneaker_id={self.sneaker_id}, status={self.status})>"


class Sneaker(Base):
    __tablename__ = "sneakers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    release_date = Column(DateTime, index=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    def __repr__(self):
        return f"<Sneaker(id={self.id}, name={self.name}, brand={self.brand})>"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"