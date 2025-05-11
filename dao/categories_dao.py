from sqlalchemy.orm import Session
from models.category import Category
from .base_dao import BaseDAO


class CategoryDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Category)
    
    def find_by_category(self, category_name: str) -> Category | None:
        return self.session.query(Category).filter_by(name=category_name).first()
    
    def get_create_category(self, category_name: str) -> Category:
        category = self.find_by_category(category_name)
        if not category:
            category = self.create(name=category_name)
        return category
