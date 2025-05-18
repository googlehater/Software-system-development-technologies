from models.order import Order
from models.status import Status
from sqlalchemy.orm import Session

class OrderFactory:
    """Фабрика для создания заказов с предустановленными статусами"""
    
    @staticmethod
    def create_proving_order(session: Session, customer_id: int, total: float, address: str) -> Order:
        """Создает заказ со статусом 'created'"""
        status = session.query(Status).filter_by(status="created").first()
        return Order(
            customer_id=customer_id,
            total_amount=total,
            address=address,
            status_id=status.status_id
        )

    @staticmethod
    def create_shipped_order(session: Session, customer_id: int, total: float, address: str) -> Order:
        """Создает заказ со статусом 'shipped' (оплачен)"""
        status = session.query(Status).filter_by(status="shipped").first()
        return Order(
            customer_id=customer_id,
            total_amount=total,
            address=address,
            status_id=status.status_id
        )
