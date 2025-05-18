from datetime import datetime
from dao.orders_dao import OrderDAO
from dao.products_dao import ProductDAO
from dao.customers_dao import CustomerDAO
from patterns.observer import NotificationService 
from patterns.strategy.strategy import PaymentStrategy
from patterns.strategy.strategy import CardPayment


class OrderFacade:
    
    def __init__(self, session):
        self.order_dao = OrderDAO(session)
        self.product_dao = ProductDAO(session)
        self.customer_dao = CustomerDAO(session)
        self.payment_dao = PaymentStrategy(CardPayment)
        self.notifier = NotificationService()

    def place_order(self, customer_id: int, product_ids: list[int]) -> bool:
        """Оформление заказа в один клик.
        
        Шаги:
        1. Проверить наличие товаров
        2. Создать заказ в БД
        3. Выполнить оплату
        4. Отправить уведомление"""
        try: 
            # 1
            for product_id in product_ids:
                product = self.product_dao.get_by_id(product_id)
                if product.quantity < 1:
                     raise ValueError(f"Товар {product_id} закончился")

            # 2
            order = self.order_dao.create(
                customer_id=customer_id,
                order_date=datetime.now(),
                product_ids=product_ids
            )

            # 3
            customer = self.customer_dao.get_by_id(customer_id)
            total = sum(self.product_dao.get_by_id(pid).price for pid in product_ids)
            payment_success = self.payment_strategy.pay(customer.email, total)

            # 4 
            if payment_success:
                self.notifier.notify(
                    recipient=customer.email,
                    message=f'Заказ №{order.order_id} успешно оформлен. Сумма: {total} руб.'
                )
                return True
            return False

        except Exception as e:
            print(f"Ошибка при оформлении заказа: {e}")
            return False
    

    def add_product_by_name(self, product_name: str, quantity: int):
        """Добавление товара по названию (для UI)"""
        product = self.product_dao.get_by_name(product_name)
        if not product:
            raise ValueError(f"Товар '{product_name}' не найден")
        
        return self.add_to_cart(product.product_id, quantity)  # Используем ID внутри
