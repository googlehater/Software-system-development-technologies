from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from .order import Order


class Status(Base):
    __tablename__ = "status"

    status_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(50))

    orders: Mapped[List['Order']] = relationship(back_populates='status', lazy='joined')
