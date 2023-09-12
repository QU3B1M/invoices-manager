
from pydantic import BaseModel, ConfigDict, EmailStr


class Customer(BaseModel):
    """Customer model."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    fullname: str
    address_first_line: str
    address_second_line: str | None = None
    phone: str
    email: EmailStr
    description: str | None = None
