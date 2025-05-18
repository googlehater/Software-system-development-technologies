from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, timedelta
from .base import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderCart(Base):
    __tablename__ = "order_cart"

    order_cart_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    order: Mapped['Order'] = relationship(back_populates='order_cart')
    product: Mapped['Product'] = relationship(back_populates='order_cart')
