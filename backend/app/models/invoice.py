from sqlalchemy import Column, Unicode, BigInteger, Text, Float

from app.core.db.session import Base


class Invoice(Base):
    __tablename__ = "Invoice"

    id = Column(BigInteger, primary_key=True, index=True)
    date = Column(Unicode(100), nullable=False)
    due_date = Column(Unicode(100), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Unicode(100), nullable=False)
    description = Column(Unicode(100), nullable=False)
    invoice_html = Column(Text, nullable=False)
