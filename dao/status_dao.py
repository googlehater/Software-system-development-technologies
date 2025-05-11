from sqlalchemy.orm import Session
from models.order import Order
from models.status import Status
from .base_dao import BaseDAO


class StatusDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Status)

    def get_orders_by_status(self, status: str) -> list[Order]:
        # получить все заказы по статусу
        return (self.session.query(Order)
                .join(Status)
                .filter(Order.status.ilike(f'%{status}%'))
                .all()
                )

