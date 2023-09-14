from pydantic import BaseModel, ConfigDict, SecretStr, EmailStr


class UserBase(BaseModel):
    """User base model."""
    firstname: str
    surname: str
    nickname: str | None = None
    company_name: str | None = None
    address: str
    phone: str
    email: EmailStr
    website: str | None


class UserCreate(UserBase):
    """User create model."""
    password: SecretStr
    password_repeat: SecretStr


class UserDB(UserBase):
    """User model."""
    model_config = ConfigDict(from_attributes=True)

    # id: int
    hashed_password: SecretStr
    invoices: list['Invoice'] = []
