import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dao.brand_dao import BrandDAO
from sqlalchemy import text
from models.status import Status
from patterns.factory.order_factory import OrderFactory
import sys


load_dotenv()

def main():
    from models.order import Order
    from patterns.observer.observer import EmailNotification, SMSNotification


    string_con = f"{os.getenv('DB_DRIVER')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine("postgresql://postgres:lasnessk@localhost:5433/elecronic_equipment_store1")
    session = Session(engine)
    





    # Создание заказа
    order = Order(
        customer_id=1,
        status_id=1,  # ID статуса "prooving"
        payment_method_id=1,
        total_amount=1.00,
        address='qq'
    )
    session.add(order)
    session.commit()

    # Работа со статусами
    order.next_status(session)  # prooving -> paid
    order.next_status(session)  # paid -> shipped
    order.prev_status(session)  # shipped -> paid
    
    session.close()

if __name__ == "__main__":
    main()




