from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from . import Customer, User


class Invoice(BaseModel):
    """Model to force the user to send the correct data to generate the invoice."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    number: int
    date: datetime = Field(default_factory=datetime.utcnow)
    due_date: datetime = Field(default_factory=datetime.utcnow)
    quantity: int = Field(gt=0)
    total_amount: float
    currency: str
    unit_price: float
    description: str
    invoice_html: str = None

    invoice_from: User
    invoice_to: Customer
