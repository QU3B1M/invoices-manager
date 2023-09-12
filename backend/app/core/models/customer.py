from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db.session import Base


class Customer(Base):
    __tablename__ = 'Customer'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    website: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    invoices: Mapped[List['Invoices']] = relationship(
        back_populates='invoice_to')
