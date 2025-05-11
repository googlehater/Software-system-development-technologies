from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, timedelta
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .order import Order


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    payment_method_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method_name: Mapped[str] = mapped_column(String(100))

    order: Mapped[Order] = relationship(back_populates='payment_method')
