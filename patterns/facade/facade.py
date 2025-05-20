from datetime import datetime
from dao.orders_dao import OrderDAO
from dao.products_dao import ProductDAO
from dao.customers_dao import CustomerDAO
from patterns.observer.observer import EmailNotification
from patterns.strategy.strategy import CardPayment
from patterns.strategy.strategy import CashByDelivery
from patterns.strategy.strategy import InstallmentPlanPayment


class OrderFacade:
    def __init__(self, session):
        self.session = session
        self.order_dao = OrderDAO(session)
        self.product_dao = ProductDAO(session)
        self.customer_dao = CustomerDAO(session)
        self.payment_dao = CardPayment()
        self.notifier = EmailNotification()
        # strategy
        self._payment_strategies = {
            'card': CardPayment(),
            'cash': CashByDelivery(),
            'installpayment': InstallmentPlanPayment()
        }
        self._current_strategy = self._payment_strategies['card']  # по умолчанию

    def place_order(self, customer_id: int, product_ids: list[int], address: str) -> bool:
        """Оформление заказа в один клик.
        
        Шаги:
        1. Проверить наличие товаров
        2. Создать заказ в БД
        3. Выполнить оплату
        4. Отправить уведомление"""
        try: 
            products = []
            total_amount = 0.0
            # 1
            for product_id in product_ids:
                product = self.product_dao.get_by_id(product_id)
                if product.quantity < 1:
                     raise ValueError(f"Товар {product_id} закончился")
                products.append(product)
                total_amount += float(product.price)

            # 2 создание заказа
            order_data = {
                'customer_id': customer_id,
                'order_date': datetime.today(),
                'total_amount': total_amount,
                'address': address,
                'status_id': 1,  # Статус "Новый"
                'payment_method_id': 1
            }

            order = self.order_dao.create(**order_data)
            
            # 3 Добавление товара в заказ
            for product in products:
                self.order_dao.add_product_to_order(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=1,
                    price=product.price
                )
               
            return True
        
        except Exception as e:
            self.session.rollback()
            print(f"[Ошибка] {str(e)}")
            return False
    

    def add_product_by_name(self, product_name: str, quantity: int):
        """Добавление товара по названию (для UI)"""
        product = self.product_dao.get_by_name(product_name)
        if not product:
            raise ValueError(f"Товар '{product_name}' не найден")
        
        return self.add_to_cart(product.product_id, quantity)  # Используем ID внутри
    
    def set_payment_method(self, method: str):
        self._current_strategy = self._payment_strategies.get(method)
        if not self._current_strategy:
            raise ValueError(f'Неизвестный метод оплаты: {method}')
        
