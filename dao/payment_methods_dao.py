from sqlalchemy.orm import Session
from models.payment_methods import PaymentMethod
from .base_dao import BaseDAO


class PaymentMethodDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, PaymentMethod)

    def show_payment(self) -> list[PaymentMethod]:
        return self.session.query(PaymentMethod).all()
