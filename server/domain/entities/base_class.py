from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


@as_declarative()
class Base:
    uuid: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                          index=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
