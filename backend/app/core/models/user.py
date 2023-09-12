from typing import List

from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db.session import Base


class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    website: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    invoices: Mapped[List['Invoices']] = relationship(
        back_populates='invoice_from')
