from sqlalchemy.orm import Session
from models.brand import Brand
from .base_dao import BaseDAO


class BrandDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Brand)

    def find_by_country(self, country: str):
        # поиск бредов по странам
        return self.session.query(Brand).filter_by(country=country).all()
