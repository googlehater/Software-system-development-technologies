from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import Product


class Brand(Base):
    __tablename__ = "brands"

    brand_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))

    products: Mapped[list['Product']] = relationship(back_populates='brand', lazy='joined')
