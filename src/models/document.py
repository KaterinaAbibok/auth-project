from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True
    )

    type = Column(
        String,
        nullable=False
    )
