from sqlalchemy.orm import Session
from models.product import Product
from .base_dao import BaseDAO
from .categories_dao import CategoryDAO


class ProductDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Product)

    def search_by_name(self, name: str) -> list[Product]:
        # поиск продуктов по названию
        # ilike - регистронезависимый
        # f'%{name}%' - поиск в любом месте строки
        return self.session.query(Product).filter(Product.name.ilike(f'%{name}%')).all()
    
    def create_product_category(self, product_name: str, category_name, price, **kwargs) -> Product:
        # создает продукт с категорией
        category_dao = CategoryDAO(self.session)
        category, _ = category_dao.get_create_category(category_name)

        return self.create(
            name=product_name,
            category_id=category.category_id,
            price=price,
            **kwargs
        )
    