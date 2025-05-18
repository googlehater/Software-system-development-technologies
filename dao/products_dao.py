from sqlalchemy.orm import Session
from models.product import Product
from .base_dao import BaseDAO
from .categories_dao import CategoryDAO
from datetime import date


class ProductDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Product)

    def create_product(
            self, 
            name: str,
            description: str,
            price: float,
            quantity: int,
            category_id: int,
            brand_id: int, 
            created_at = date.today()
    ):
        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
            brand_id=brand_id,
            created_at=created_at
        )
        
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        

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
    
    def get_all_products(self) -> list[Product]:
        '''возвращает все продукты'''
        return self.session.query(Product).all()
    