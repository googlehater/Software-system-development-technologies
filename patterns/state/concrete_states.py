from patterns.state.order_state import OrderState
from models.status import Status
from sqlalchemy.orm import Session
from models.order import Order

class ProvingState(OrderState):
    def next(self, order: Order, session: Session) -> None:
        status = session.query(Status).filter_by(status="paid").first()
        if not status:
            raise ValueError("Статус 'paid' не найден")
        
        order.status_id = status.status_id
        from .concrete_states import PaidState
        order._state = PaidState()
        session.commit()

    def prev(self, order: Order, session: Session) -> None:
        raise ValueError("Нельзя отменить заказ в статусе 'prooving'")

    def name(self) -> str:
        return "prooving"

class PaidState(OrderState):
    def next(self, order: Order, session: Session) -> None:
        status = session.query(Status).filter_by(status="shipped").first()
        if not status:
            raise ValueError("Статус 'shipped' не найден")
        
        order.status_id = status.status_id
        from .concrete_states import ShippedState
        order._state = ShippedState()
        session.commit()

    def prev(self, order: Order, session: Session) -> None:
        status = session.query(Status).filter_by(status="prooving").first()
        if not status:
            raise ValueError("Статус 'prooving' не найден")
        
        order.status_id = status.status_id
        from .concrete_states import ProvingState
        order._state = ProvingState()
        session.commit()

    def name(self) -> str:
        return "paid"

class ShippedState(OrderState):
    def next(self, order: Order, session: Session) -> None:
        raise ValueError("Заказ уже доставлен")

    def prev(self, order: Order, session: Session) -> None:
        status = session.query(Status).filter_by(status="paid").first()
        if not status:
            raise ValueError("Статус 'paid' не найден")
        
        order.status_id = status.status_id
        from .concrete_states import PaidState
        order._state = PaidState()
        session.commit()

    def name(self) -> str:
        return "shipped"