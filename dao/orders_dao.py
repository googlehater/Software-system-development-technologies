from sqlalchemy.orm import Session
from models.category import Category
from models.product import Product
from .base_dao import BaseDAO


class CategoryDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Category)

    def get_products_by_category(self, category_name: str) -> list[Product]:
        # получение продуктов по категории
        return (self.session.query(Product)
                .join(Category)
                .filter(Category.name.ilike(f'%{category_name}%'))
                .all()
                )


