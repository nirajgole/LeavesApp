from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
    # # Generate __tablename__ automatically based on class name
    # @declared_attr
    # def __tablename__(cls) -> str:
    #     return cls.__name__.lower()