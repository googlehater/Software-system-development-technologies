import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dao.brand_dao import BrandDAO
from sqlalchemy import text
from models.status import Status
import sys


load_dotenv()

def main():
    from models.order import Order
    from patterns.observer.observer import EmailNotification, SMSNotification


    string_con = f"{os.getenv('DB_DRIVER')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine("postgresql://postgres:lasnessk@localhost:5433/elecronic_equipment_store1")
    session = Session(engine)
    
    # Создание заказ
    order = Order(customer_id=1,
                  total_amount=363.00,
                  address="ул. 2-я Оранжерейная д.19",
                  status_id=1,
                  payment_method_id=1)
    session.add(order)
    session.commit()

    order1 = Order(customer_id=1,
                  total_amount=666.00,
                  address="ул. Тимирязева д.4",
                  status_id=1,
                  payment_method_id=3)
    session.add(order1)
    session.commit()
    
    # Создание наблюдателей
    email_notifier = EmailNotification()
    sms_notifier = SMSNotification()
    
    # Подписание на заказ
    order.attach(email_notifier)
    order.attach(sms_notifier)

    order1.attach(email_notifier)
    order1.attach(sms_notifier)

    

    order.set_status('prooving', session)
    order1.set_status('prooving', session)
    session.commit

    order.set_status('shipped', session)
    session.commit
    

    order.detach(sms_notifier)
    order1.detach(sms_notifier)

    order.set_status("shipped", session)
    
    session.close()

if __name__ == "__main__":
    main()



    # сервис лайер
