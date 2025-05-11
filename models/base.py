from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String
from typing_extensions import Annotated


str255 = Annotated[str, mapped_column(String(255))]
intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    pass
