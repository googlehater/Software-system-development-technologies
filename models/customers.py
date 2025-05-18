from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    

class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20))
    registration_date: Mapped[date] = mapped_column(Date, default=date.today)

    orders: Mapped[List['Order']] = relationship(back_populates='customer', lazy='selectin')
