from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, timedelta
from patterns.observer.observer import Subject
from typing import TYPE_CHECKING

from models.base import Base

if TYPE_CHECKING:
    from .order import Order
    from .customers import Customer
    from .status import Status
    from .payment_methods import PaymentMethod
    from .order_cart import OrderCart
    


def default_expected_delivery():
    return date.today() + timedelta(days=10)


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.customer_id'))
    order_date: Mapped[date] = mapped_column(Date, default=date.today)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    address: Mapped[str] = mapped_column(String(100))
    expected_delivery: Mapped[date] = mapped_column(Date, default=default_expected_delivery)
    actual_delivery: Mapped[date] = mapped_column(Date, nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey('status.status_id'))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey('payment_methods.payment_method_id'))

    customer: Mapped["Customer"] = relationship(back_populates='orders')
    status: Mapped['Status'] = relationship(back_populates='orders')
    payment_method: Mapped['PaymentMethod'] = relationship(back_populates='orders')
    order_cart: Mapped[list["OrderCart"]] = relationship(back_populates='order')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subject = Subject()

    def attach(self, observer):
        self._subject.attach(observer)

    def detach(self, observer):
        self._subject.detach(observer)

    def notify(self, order_id, status):
        self._subject.notify(order_id, status)

    def set_status(self, new_status: str, session) -> None:
        from models.status import Status
        status_obj = session.query(Status).filter_by(status=new_status).first()
        
        if not status_obj:
            raise ValueError(f"Статус '{new_status}' не найден в базе данных")
        
        self.status_id = status_obj.status_id
        session.add(self)
        session.commit()
        self.notify(self.order_id, new_status)
