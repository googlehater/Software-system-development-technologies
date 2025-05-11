from sqlalchemy.orm import Session
from typing import List, Optional
from models.order_cart import OrderCart
from .base_dao import BaseDAO


class OrderCartDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, OrderCart)

    def get_order_cart_by_id(self, id: int):
        # получение корзины по id
        return self.session.query(OrderCart).filter(OrderCart.id == id).all()
    
    def get_cart_items(self, order_id: int) -> List[OrderCart]:
        # получить все товары заказа
        return (
            self.session.query(OrderCart)
            .filter(OrderCart.order_id == order_id)
            .all()
                )
    
    def get_cart_item(self, order_id: int, product_id: int) -> Optional[OrderCart]:
        # получить конкретный товар в корзине
        return (
            self.session.query(OrderCart)
            .filter(
                OrderCart.order_id == order_id,
                OrderCart.product_id == product_id
            )
            .first()  # Вернёт одну запись или None
        )
    
    def add_to_cart(self, order_id: int, product_id: int, quantity: int) -> OrderCart:
        item = OrderCart(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity
        )
        self.session.add(item)
        self.session.commit()
        return item
    
    def update_quantity(self, order_id: int, product_id: int, new_quantity: int) -> bool:
        item = self.get_cart_item(order_id, product_id)
        if item:
            item.quantity = new_quantity
            self.session.commit()
            return True
        return False
    
    def remove_from_cart(self, order_id: int, product_id: int) -> bool:
        item = self.get_cart_item(order_id, product_id)
        if item:
            self.session.delete(item)
            self.session.commit()
            return True
        return False
