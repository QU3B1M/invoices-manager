from typing import List

from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db.session import Base


class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(nullable=True)
    company_name: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    website: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column()

    invoices: Mapped[List['Invoice']] = relationship(
        back_populates='invoice_from')
