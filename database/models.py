import datetime
from typing import Annotated

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from database.dtos import UserDTO

intpk = Annotated[int, mapped_column(Integer, primary_key=True)]
created = Annotated[int, mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=10.0)
    created_at: Mapped[created]

    images: Mapped[list['ImageUpload']] = relationship(back_populates='user')
    transactions: Mapped[list['Transaction']] = relationship(back_populates='user')

    def map_to_dto(self):
        return UserDTO(id=self.id, username=self.username,
                       name=self.name, balance=self.balance,
                       created_at=self.created_at)


class ImageUpload(Base):
    __tablename__ = 'image_uploads'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    uploaded_at: Mapped[created]

    user: Mapped[list['User']] = relationship(back_populates='images')


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[created]

    user: Mapped[list['User']] = relationship(back_populates='transactions')
