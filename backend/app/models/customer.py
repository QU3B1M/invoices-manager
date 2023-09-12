from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db.session import Base


class Customer(Base):
    __tablename__ = 'Customer'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    address_first_line: Mapped[str] = mapped_column(nullable=False)
    address_second_line: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    invoices: Mapped[List['Invoices']] = relationship(
        back_populates='invoice_to')
