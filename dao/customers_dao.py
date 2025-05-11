from sqlalchemy.orm import Session
from models.customers import Customer
from .base_dao import BaseDAO


class CustomerDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Customer)

    def get_info_by_email(self, email) -> Customer | None:
        return self.session.query(Customer).filter(Customer.email.ilike(f'%{email}%')).first()
    