from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from datetime import date, timedelta
from patterns.observer.observer import Subject
from patterns.state.order_state import OrderState
from typing import TYPE_CHECKING, Optional
from patterns.strategy.payment import PaymentType
from patterns.strategy.strategy import PaymentStrategy


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

    from patterns.strategy.strategy import CardPayment
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_attr()
        # self._payment_strategy: Optional[PaymentStrategy] = None 
        self._state: None
        self._payment_strategy = None

    def _init_attr(self):
        if not hasattr(self, '_state'):
            self._state: Optional['OrderState'] = None
        if not hasattr(self, '_subject'):
            self._subject = Subject()

    def _init_state(self):
        """л инициализация состояния"""
        from patterns.state.state_factory import StateFactory
        self._state = StateFactory.create(self.status.status)
    
    @property
    def state(self) -> 'OrderState':
        # self._init_attr()
        if self._state is None:
            self._init_state()

        # if hasattr(self.state, 'next'):
        #     self.state.next(self, session)
        #     session.commit()
            
        #     # Уведомляем об изменении статуса
        #     if self.status:
        #         self.notify(self.order_id, self.status.status)
        # else:
        #     raise AttributeError("Метод next не найден в текущем состоянии")
        
        return self._state
    
    # @property
    # def state(self) -> 'OrderState':
    #     if self._state is None:
    #         self._init_state()
    #     return self._state

    def attach(self, observer):
        self._init_attr()
        self._subject.attach(observer)

    def detach(self, observer):
        self._init_attr()
        self._subject.detach(observer)

    def notify(self, order_id, status):
        self._init_attr()
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
    
    def next_status(self, session: Session):
        """Переход к следующему статусу"""
        self.state.next(self, session)
        session.commit()
        
        if self.status:
            self.notify(self.order_id, self.status.status)
    
    def prev_status(self, session: Session):
        """Переход к предыдущему статусу"""
        if self.state is None:
            self._init_state()
        try:
            self.state.prev(self, session)
            session.commit()
        except AttributeError as e:
            session.rollback()
            raise AttributeError(f'ошибка перехода статуса: {str(e)}')

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Устанавливает стратегию оплаты"""
        self._payment_strategy = strategy

    def process_payment(self, session: Session) -> bool:
        """Обработка платежа с использованием стратегии"""
        if not self._payment_strategy:
            raise ValueError("Способ оплаты не выбран")
            
        try:
            # Выполняем оплату через стратегию
            if self._payment_strategy.execute_payment(self.total_amount):
                self.next_status(session)  # Переводим в следующий статус
                return True
            return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Ошибка оплаты: {str(e)}")

    def pay_order(self, session: Session):
        '''Выполняет оплату заказа'''
        self.next_status(session)
        self._strategy.pay(self, session)
