"""
SQLAlchemy models for sneaker products
"""
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Sneakers(Base):
    """Sneaker product model"""
    __tablename__ = "sneakers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    drop_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )
    
    # Relationship
    sizes = relationship(
        "SneakerSizes",
        back_populates="sneaker",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Sneakers(id={self.id}, brand={self.brand}, name={self.name})>"


class SneakerSizes(Base):
    """Sneaker size and stock model"""
    __tablename__ = "sneaker_sizes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sneaker_id = Column(
        Integer,
        ForeignKey("sneakers.id", ondelete="CASCADE"),
        nullable=False
    )
    size = Column(String(10), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relationship
    sneaker = relationship("Sneakers", back_populates="sizes")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_sneaker_id', 'sneaker_id'),
        Index('idx_sneaker_id_size', 'sneaker_id', 'size'),
    )
    
    def __repr__(self):
        return f"<SneakerSizes(id={self.id}, sneaker_id={self.sneaker_id}, size={self.size}, stock={self.stock})>"