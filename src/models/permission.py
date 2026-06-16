from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.db import Base
from src.models.associations import role_permissions

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True
    )

    resource = Column(
        String,
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )
