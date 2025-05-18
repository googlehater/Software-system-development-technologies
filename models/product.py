from sqlalchemy import String, ForeignKey, Text, Numeric, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .category import Category
    from .brand import Brand
    from .order_cart import OrderCart


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id', ondelete='CASCADE')) 
    brand_id: Mapped[int] = mapped_column(ForeignKey('brands.brand_id', ondelete='CASCADE'))
    create_at: Mapped[date] = mapped_column(Date, default=date.today())

    category: Mapped['Category'] = relationship(back_populates='products', lazy='joined')
    brand: Mapped['Brand'] = relationship(back_populates='products', lazy='joined')
    order_cart: Mapped[list["OrderCart"]] = relationship(back_populates='product')

    def __repr__(self):  # вывод информации
        return f'''product(id={self.product_id})
        name={self.name!r}
        description: {self.description!r}\nprice: {self.price}]
        quantity: {self.quantity}\ncreate_at: {self.create_at}\n'''  
