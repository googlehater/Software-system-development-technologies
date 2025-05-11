from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, timedelta
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .customers import Customer
    from .status import Status
    from .payment_methods import PaymentMethod


def default_expected_delivery():
    return date.today() + timedelta(days=10)

class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.customer_id'))
    order_date: Mapped[date] = mapped_column(Date, date.today)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    address: Mapped[str] = mapped_column(String(100))
    expected_delivery: Mapped[str] = mapped_column(Date, default=default_expected_delivery)
    actual_delivery: Mapped[date] = mapped_column(Date, nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey('status.status_id'))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey('payment_methods.payment_method_id'))

    customer: Mapped['Customer'] = relationship(back_populates='orders')
    status: Mapped['Status'] = relationship(back_populates='orders')
    payment_method: Mapped['PaymentMethod'] = relationship(back_populates='orders')

