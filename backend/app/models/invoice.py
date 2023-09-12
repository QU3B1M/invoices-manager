import enum

import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db.session import Base


class Currencies(enum.Enum):
    USD = 1
    ARS = 2


services_to_invoice = Table(
    "services_to_invoice",
    Base.metadata,
    Column("service_id", ForeignKey("Service.id"), primary_key=True),
    Column("invoice_id", ForeignKey("Invoice.id"), primary_key=True),
)


class Service(Base):
    __tablename__ = 'Service'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[Currencies] = mapped_column(nullable=False)

    invoices: Mapped[List['Invoice']] = relationship(
        secondary=services_to_invoice, back_populates="services"
    )


class Invoice(Base):
    __tablename__ = 'Invoice'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    number: Mapped[str] = mapped_column(index=True, nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    invoice_html: Mapped[str] = mapped_column(nullable=False)

    services: Mapped[List['Service']] = relationship(
        secondary=services_to_invoice, back_populates="invoices"
    )

    invoice_from_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    invoice_from: Mapped['User'] = relationship(back_populates='invoices')
    invoice_to_id: Mapped[int] = relationship(ForeignKey('Customer.id'))
    invoice_to: Mapped['Customer'] = relationship(back_populates='invoices')
