from sqlalchemy.orm import Session
from models.category import Category
from models.product import Product
from .base_dao import BaseDAO
from models.order import Order


class OrderDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Order)

    def get_products_by_category(self, category_name: str) -> list[Product]:
        # получение продуктов по категории
        return (self.session.query(Product)
                .join(Category)
                .filter(Category.name.ilike(f'%{category_name}%'))
                .all()
                )
    
    def get_all_orders(self) -> list[Order]:
        # получение всех заказов
        return self.session.query(Order).all()
    
    def add_product_to_order(self, order_id: int, product_id: int, quantity: int, price: float) -> None:
        # добавление продукта в заказ
        """
        Добавляет товар в заказ
        
        Args:
            order_id: ID заказа
            product_id: ID товара
            quantity: Количество
            price: Цена на момент заказа
        """
        from models.order_cart import OrderCart
        
        # Проверяем существование заказа и товара
        order = self.session.get(Order, order_id)
        if not order:
            raise ValueError(f"Заказ с ID {order_id} не найден")
            
        product = self.session.get(Product, product_id)
        if not product:
            raise ValueError(f"Товар с ID {product_id} не найден")
        
        # Проверяем доступное количество
        if product.quantity < quantity:
            raise ValueError(f"Недостаточно товара {product.name} на складе")
        
        # Создаем связь между заказом и товаром
        order_item = OrderCart(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price  # Сохраняем цену на момент заказа
        )
        
        self.session.add(order_item)
        self.session.commit()
        
        # Уменьшаем количество товара на складе
        product.quantity -= quantity
        self.session.add(product)
        self.session.commit()
