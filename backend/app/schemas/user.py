from pydantic import BaseModel, ConfigDict, SecretStr, EmailStr


class User(BaseModel):
    """User model."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    firstname: str
    surname: str
    company_name: str | None = None
    address: str
    phone: str
    email: EmailStr
    website: str
    hashed_password: SecretStr
    is_active: bool = True
